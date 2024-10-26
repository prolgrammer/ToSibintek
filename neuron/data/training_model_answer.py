import os
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np


class FAQModel:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.data = None

    def load_data(self, filepath, encoding='ISO-8859-1', sep=';'):
        self.data = pd.read_csv(filepath, encoding=encoding, sep=sep)
        # Создаем эмбеддинги для всех запросов в датасете и корректируем размерность
        self.data['embedding'] = self.model.encode(self.data['Topic'].tolist(), convert_to_tensor=False).tolist()
        self.data['embedding'] = self.data['embedding'].apply(lambda x: np.squeeze(x))  # Убираем лишнее измерение

    def find_similar_request(self, query, service_label, top_n=5, threshold=0.5):
        if self.data is None:
            return None, "Данные не загружены. Пожалуйста, загрузите данные с помощью load_data()."

        # Преобразуем запрос пользователя в эмбеддинг и корректируем его размерность
        query_embedding = np.squeeze(self.model.encode([query], convert_to_tensor=False))

        # Фильтруем запросы по метке сервиса
        service_data = self.data[self.data['label'] == service_label]
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

        # Формируем и возвращаем результат
        results = []
        for i, (req, answer, score) in enumerate(
                zip(similar_requests['Topic'], similar_requests['Solution'], similarity_scores)):
            results.append({
                'Похожий запрос': req,
                'Ответ': answer,
                'Сходство': score
            })

        return results

    def save_model(self, filepath="model/answer_model/faq_model.pkl"):
        # Создаем папки, если они не существуют
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # Сохраняем модель
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_model(filepath="model/answer_model/faq_model.pkl"):
        with open(filepath, 'rb') as f:
            return pickle.load(f)


# Пример использования

# Инициализация модели и загрузка данных
faq_model = FAQModel()
faq_model.load_data("data_training/dataset_.csv")

# Пример запроса пользователя
query = "Network connection problem"
service_label = "Network"

# Поиск похожего запроса и вывод ответа
similar_requests = faq_model.find_similar_request(query, service_label)
if similar_requests:
    for i, result in enumerate(similar_requests):
        print(f"Похожий запрос {i + 1}: {result['Похожий запрос']} (Сходство: {result['Сходство']})")
        print(f"Ответ: {result['Ответ']}")
else:
    print("К сожалению, мы не можем найти ответ на ваш вопрос.")

# Сохранение модели в папке model/answer_model
faq_model.save_model()

# Загрузка модели из папки model/answer_model
loaded_model = FAQModel.load_model()
