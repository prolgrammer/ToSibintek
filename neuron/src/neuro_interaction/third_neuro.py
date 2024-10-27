import os
import pickle
import json
import pika
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from docx import Document

# Настройки RabbitMQ
rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_user = 'rabbitmq'
rabbitmq_password = '1234'

# Названия очередей
request_queue_name = 'request-stage-3-events-topic-queue'  # Очередь для входящих запросов третьей нейронки
response_queue_name = 'response-stage-3-events-topic-queue'  # Очередь для исходящих ответов третьей нейронки

# Настройка учетных данных для подключения
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)


# Класс для загрузки и поиска инструкций
class InstructionModel:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.file_names = None
        self.filename_embeddings = None
        self.folder_path = None

    def load_instructions(self, folder_path):
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Папка {folder_path} не найдена.")
        self.folder_path = folder_path
        self.file_names = [file_name for file_name in os.listdir(folder_path) if file_name.endswith('.docx')]

        if not self.file_names:
            raise FileNotFoundError("Нет .docx файлов в папке с инструкциями.")

        self.filename_embeddings = self.model.encode(self.file_names, convert_to_tensor=False)

    def load_instruction_text(self, doc_path):
        try:
            doc = Document(doc_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
        except Exception as e:
            print(f"Ошибка при загрузке файла {doc_path}: {e}")
            return None

    def keyword_match(self, filename, keywords):
        return any(keyword in filename.lower() for keyword in keywords)

    def find_best_instruction(self, query, threshold_filename=0.3, threshold_instruction=0.3):
        if not self.file_names or self.filename_embeddings is None:
            raise ValueError("Инструкции не загружены. Пожалуйста, вызовите метод load_instructions().")

        query_embedding = np.squeeze(self.model.encode([query], convert_to_tensor=False))
        keywords = query.lower().split()

        candidate_indices = [i for i, file_name in enumerate(self.file_names) if self.keyword_match(file_name, keywords)]
        if not candidate_indices:
            similarities = cosine_similarity([query_embedding], self.filename_embeddings).flatten()
            candidate_indices = [i for i, score in enumerate(similarities) if score >= threshold_filename]

        if not candidate_indices:
            return None, "К сожалению, подходящей инструкции не найдено на основе названия файлов."

        best_instruction = None
        best_similarity = 0
        for i in candidate_indices:
            file_name = self.file_names[i]
            doc_path = os.path.join(self.folder_path, file_name)
            instruction_text = self.load_instruction_text(doc_path)
            if not instruction_text:
                continue

            instruction_embedding = np.squeeze(self.model.encode([instruction_text], convert_to_tensor=False))
            instruction_similarity = cosine_similarity([query_embedding], [instruction_embedding]).flatten()[0]

            if instruction_similarity > best_similarity and instruction_similarity >= threshold_instruction:
                best_instruction = instruction_text
                best_similarity = instruction_similarity

        if best_instruction is None:
            return None, "К сожалению, подходящей инструкции не найдено."
        return best_instruction, best_similarity


# Инициализация модели и загрузка инструкций
instruction_model = InstructionModel()
instruction_model.load_instructions("documentation")


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
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"Отправлено сообщение: {message}")
    connection.close()


# Callback-функция для обработки входящих сообщений
def callback(ch, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    print(f"Получено сообщение: {message}")

    user = message.get("user")
    query = message.get("query")
    service_label = message.get("service_label")

    if query:
        best_instruction, similarity_score = instruction_model.find_best_instruction(query)
        if best_instruction:
            response = {
                "user": user,
                "query": query,
                "result": best_instruction,
                "similarity_score": similarity_score
            }
        else:
            response = {
                "user": user,
                "query": query,
                "message": "К сожалению, подходящей инструкции не найдено."
            }
    else:
        response = {
            "message": "Неверный формат запроса. Убедитесь, что в запросе присутствует поле 'query'."
        }

    send_message_to_queue(response, response_queue_name)


def main():
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
