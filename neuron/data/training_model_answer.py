# Импорты необходимых библиотек
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

# Загрузка данных
data = pd.read_csv("data_training/dataset_.csv", encoding='ISO-8859-1', sep=';')

# Инициализируем модель SentenceTransformer для эмбеддингов
model_bert = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Создаем эмбеддинги для всех запросов в датасете и корректируем размерность
data['embedding'] = model_bert.encode(data['Topic'].tolist(), convert_to_tensor=False).tolist()
data['embedding'] = data['embedding'].apply(lambda x: np.squeeze(x))  # Убираем лишнее измерение

# Функция для поиска похожих запросов с учетом фильтрации по метке `label`
def find_similar_request(query, service_label, data, top_n=5, threshold=0.5):
    # Преобразуем запрос пользователя в эмбеддинг и корректируем его размерность
    query_embedding = np.squeeze(model_bert.encode([query], convert_to_tensor=False))

    # Фильтруем запросы по метке сервиса
    service_data = data[data['label'] == service_label]
    if service_data.empty:
        return None, "К сожалению, мы не нашли подходящих вопросов для данного сервиса."

    # Вычисляем косинусное сходство между запросом и отфильтрованными эмбеддингами
    embeddings = np.vstack(service_data['embedding'].values)
    similarities = cosine_similarity([query_embedding], embeddings).flatten()

    # Находим наиболее похожие запросы
    top_indices = np.argsort(similarities)[-top_n:][::-1]
    similar_requests = service_data.iloc[top_indices]
    similarity_scores = similarities[top_indices]

    # Если лучший результат ниже порога, возвращаем стандартный ответ
    if max(similarity_scores) < threshold:
        return None, "К сожалению, мы не можем найти ответ на ваш вопрос."

    return similar_requests, similarity_scores


# Пример запроса пользователя
query = "Network connection problem"
service_label = "Network"  # Здесь указываем метку сервиса, к которому относится вопрос

# Находим ответ
similar_requests, similarity_scores = find_similar_request(query, service_label, data)

# Выводим результаты
if similar_requests is not None:
    for i, (req, answer, score) in enumerate(
            zip(similar_requests['Topic'], similar_requests['Solution'], similarity_scores)):
        print(f"Похожий запрос {i + 1}: {req} (Сходство: {score})")
        print(f"Ответ: {answer}")
else:
    print(similarity_scores)  # Если похожий запрос не найден, выводим стандартное сообщение
