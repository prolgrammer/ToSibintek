# Импорт необходимых библиотек
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from docx import Document
import numpy as np
import os

# Инициализация модели SentenceTransformer
model_bert = SentenceTransformer('paraphrase-MiniLM-L6-v2')


# Функция для загрузки текста из .docx файла
def load_instruction_text(doc_path):
    try:
        doc = Document(doc_path)
        full_text = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
        return full_text
    except Exception as e:
        print(f"Ошибка при загрузке файла {doc_path}: {e}")
        return None


# Создание эмбеддингов для названий файлов
def create_filename_embeddings(file_names):
    return model_bert.encode(file_names, convert_to_tensor=False)


# Функция для двухэтапного поиска
def find_best_instruction(query, folder_path, filename_embeddings, file_names, threshold_filename=0.5,
                          threshold_instruction=0.3):
    # Этап 1: Сравнение с эмбеддингами названий файлов
    query_embedding = model_bert.encode([query], convert_to_tensor=False)
    query_embedding = np.squeeze(query_embedding)  # Убираем лишние измерения, если они есть

    # Проверяем, что filename_embeddings двумерный массив
    filename_embeddings = np.array(filename_embeddings)
    if filename_embeddings.ndim != 2:
        filename_embeddings = np.squeeze(filename_embeddings)

    # Теперь выполняем вычисление сходства
    similarities = cosine_similarity([query_embedding], filename_embeddings).flatten()

    # Фильтруем файлы по названию, учитывая только те, у которых сходство выше порога
    candidate_indices = [i for i, score in enumerate(similarities) if score >= threshold_filename]
    if not candidate_indices:
        return None, "К сожалению, подходящей инструкции не найдено на основе названия файлов."

    # Этап 2: Поиск по текстам отобранных инструкций
    best_instruction = None
    best_similarity = 0

    for i in candidate_indices:
        file_name = file_names[i]
        doc_path = os.path.join(folder_path, file_name)

        # Загрузка и проверка текста инструкции
        instruction_text = load_instruction_text(doc_path)
        if not instruction_text:
            continue

        # Вычисляем сходство с текстом инструкции
        instruction_embedding = model_bert.encode([instruction_text], convert_to_tensor=False)
        instruction_embedding = np.squeeze(instruction_embedding)  # Убираем лишние измерения, если они есть
        instruction_similarity = cosine_similarity([query_embedding], [instruction_embedding]).flatten()[0]

        # Проверяем, лучше ли это совпадение
        if instruction_similarity > best_similarity and instruction_similarity >= threshold_instruction:
            best_instruction = instruction_text
            best_similarity = instruction_similarity

    if best_instruction is None:
        return None, "К сожалению, подходящей инструкции не найдено."

    return best_instruction, best_similarity


# Основная часть кода
def main(query, folder_path, threshold_filename=0.5, threshold_instruction=0.3):
    # Проверка существования папки с инструкциями
    if not os.path.exists(folder_path):
        print(f"Папка {folder_path} не найдена.")
        return None, "Папка с инструкциями не найдена."

    # Получение списка .docx файлов
    file_names = [file_name for file_name in os.listdir(folder_path) if file_name.endswith('.docx')]
    if not file_names:
        print("Нет .docx файлов в папке с инструкциями.")
        return None, "Инструкции не найдены."

    # Генерация эмбеддингов для названий файлов
    filename_embeddings = create_filename_embeddings(file_names)

    # Выполнение двухэтапного поиска
    best_instruction, similarity_score = find_best_instruction(query, folder_path, filename_embeddings, file_names,
                                                               threshold_filename, threshold_instruction)

    # Вывод результата
    if best_instruction:
        print("Наиболее подходящая инструкция:")
        print(best_instruction)
        print(f"\nСходство: {similarity_score}")
    else:
        print(similarity_score)


# Пример запроса пользователя
if __name__ == "__main__":
    query = "Network connection problem"
    folder_path = "documentation"
    main(query, folder_path)
