import os
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from docx import Document
import numpy as np


class InstructionModel:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.file_names = None
        self.filename_embeddings = None
        self.folder_path = None

    def load_instructions(self, folder_path):
        # Проверка на существование папки
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Папка {folder_path} не найдена.")

        # Сохранение пути к папке и списка .docx файлов
        self.folder_path = folder_path
        self.file_names = [file_name for file_name in os.listdir(folder_path) if file_name.endswith('.docx')]

        if not self.file_names:
            raise FileNotFoundError("Нет .docx файлов в папке с инструкциями.")

        # Генерация эмбеддингов для названий файлов
        self.filename_embeddings = self.model.encode(self.file_names, convert_to_tensor=False)

    def load_instruction_text(self, doc_path):
        try:
            doc = Document(doc_path)
            full_text = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
            return full_text
        except Exception as e:
            print(f"Ошибка при загрузке файла {doc_path}: {e}")
            return None

    def keyword_match(self, filename, keywords):
        return any(keyword in filename.lower() for keyword in keywords)

    def find_best_instruction(self, query, threshold_filename=0.3, threshold_instruction=0.3):
        if not self.file_names or self.filename_embeddings is None:
            raise ValueError("Инструкции не загружены. Пожалуйста, вызовите метод load_instructions().")

        # Создание эмбеддинга для запроса
        query_embedding = np.squeeze(self.model.encode([query], convert_to_tensor=False))
        keywords = query.lower().split()  # ключевые слова из запроса

        # Этап 1: Точное совпадение ключевых слов
        candidate_indices = [i for i, file_name in enumerate(self.file_names) if
                             self.keyword_match(file_name, keywords)]

        # Если нет совпадений по ключевым словам, переходим к embedding-сравнению
        if not candidate_indices:
            similarities = cosine_similarity([query_embedding], self.filename_embeddings).flatten()
            candidate_indices = [i for i, score in enumerate(similarities) if score >= threshold_filename]

        if not candidate_indices:
            return None, "К сожалению, подходящей инструкции не найдено на основе названия файлов."

        # Этап 2: Поиск по текстам отобранных инструкций
        best_instruction = None
        best_similarity = 0

        for i in candidate_indices:
            file_name = self.file_names[i]
            doc_path = os.path.join(self.folder_path, file_name)

            # Загрузка текста инструкции
            instruction_text = self.load_instruction_text(doc_path)
            if not instruction_text:
                continue

            # Сходство с текстом инструкции
            instruction_embedding = np.squeeze(self.model.encode([instruction_text], convert_to_tensor=False))
            instruction_similarity = cosine_similarity([query_embedding], [instruction_embedding]).flatten()[0]

            # Проверка на лучшее совпадение
            if instruction_similarity > best_similarity and instruction_similarity >= threshold_instruction:
                best_instruction = instruction_text
                best_similarity = instruction_similarity

        if best_instruction is None:
            return None, "К сожалению, подходящей инструкции не найдено."

        return best_instruction, best_similarity

    def save_model(self, filepath="model/docs_model/instruction_model.pkl"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_model(filepath="model/docs_model/instruction_model.pkl"):
        with open(filepath, 'rb') as f:
            return pickle.load(f)


# Пример использования модели

if __name__ == "__main__":
    # Инициализация и загрузка инструкций
    instruction_model = InstructionModel()
    instruction_model.load_instructions("documentation")

    # Пример запроса пользователя
    query = "How can I troubleshoot issues with freezing on my lapto    p?"

    # Поиск подходящей инструкции
    best_instruction, similarity_score = instruction_model.find_best_instruction(query)

    # Вывод результата
    if best_instruction:
        print("Наиболее подходящая инструкция:")
        print(best_instruction)
        print(f"\nСходство: {similarity_score}")
    else:
        print(similarity_score)

    # Сохранение модели
    instruction_model.save_model("model/docs_model/instruction_model.pkl")
