import joblib
import pika
import pickle
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Настройки для подключения к RabbitMQ
rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_user = 'rabbitmq'
rabbitmq_password = '1234'

# Параметры для очередей
request_queue_name = 'request-stage-2-events-topic-queue'  # Очередь для входящих запросов второй нейронки
response_queue_name = 'response-stage-2-events-topic-queue'  # Очередь для исходящих ответов второй нейронки

# Создаем учетные данные для подключения
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)

# Загрузка модели FAQ и данных
class FAQModel:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.data = None

    def load_data(self, filepath, encoding='ISO-8859-1', sep=';'):
        self.data = pd.read_csv(filepath, encoding=encoding, sep=sep)
        self.data['embedding'] = self.model.encode(self.data['Topic'].tolist(), convert_to_tensor=False).tolist()
        self.data['embedding'] = self.data['embedding'].apply(lambda x: np.squeeze(x))

    def find_similar_request(self, query, service_label, top_n=5, threshold=0.5):
        if self.data is None:
            return None, "Данные не загружены. Пожалуйста, загрузите данные с помощью load_data()."
        query_embedding = np.squeeze(self.model.encode([query], convert_to_tensor=False))
        service_data = self.data[self.data['label'] == service_label]
        if service_data.empty:
            return None, "К сожалению, мы не нашли подходящих вопросов для данного сервиса."
        embeddings = np.vstack(service_data['embedding'].values)
        similarities = cosine_similarity([query_embedding], embeddings).flatten()
        top_indices = np.argsort(similarities)[-top_n:][::-1]
        similar_requests = service_data.iloc[top_indices]
        similarity_scores = similarities[top_indices]
        if max(similarity_scores) < threshold:
            return None, "К сожалению, мы не можем найти ответ на ваш вопрос."
        results = []
        for req, answer, score in zip(similar_requests['Topic'], similar_requests['Solution'], similarity_scores):
            results.append({'Похожий запрос': req, 'Ответ': answer, 'Сходство': score})
        return results

# Инициализация модели и загрузка данных
faq_model = joblib.load("../../data/model/answer_model/faq_model.pkl")
faq_model.load_data("../../data/data_training/dataset_.csv")
# Функция для отправки сообщения в RabbitMQ
def send_message_to_queue(message, queue_name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),  # Кодируем сообщение в JSON
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"Отправлено сообщение: {message}")
    connection.close()

# Callback-функция для обработки входящих сообщений
def callback(ch, method, properties, body):
    message = json.loads(body.decode('utf-8'))  # Декодируем и преобразуем JSON
    print(f"Получено сообщение: {message}")

    user=message.get("user")
    query = message.get("query")
    service_label = message.get("service_label")

    # Проверка на корректность данных
    if query and service_label:
        # Поиск похожего запроса
        similar_requests = faq_model.find_similar_request(query, service_label)
        if similar_requests:
            response = {
                "user": user,
                "query": query,
                "service_label": service_label,
                "results": similar_requests
            }
        else:
            response = {
                "user": user,
                "query": query,
                "service_label": service_label,
                "message": "К сожалению, мы не можем найти ответ на ваш вопрос."
            }
    else:
        response = {
            "message": "Неверный формат запроса. Убедитесь, что в запросе присутствуют поля 'query' и 'service_label'."
        }

    # Отправка результата в очередь для ответов
    send_message_to_queue(response, response_queue_name)

def main():
    # Устанавливаем соединение с RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=request_queue_name, durable=True)
    channel.basic_consume(queue=request_queue_name, on_message_callback=callback, auto_ack=True)
    print('Ожидание сообщений. Нажмите CTRL+C для выхода.')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Выход...')
    finally:
        connection.close()

if __name__ == "__main__":
    main()
