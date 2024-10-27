import pika
import pandas as pd
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from nltk.corpus import stopwords, wordnet
from transformers import BertTokenizer, BertModel
import torch
from collections import Counter
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import joblib
import random
import nltk

# Настройки для подключения к RabbitMQ
rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_user = 'rabbitmq'
rabbitmq_password = '1234'
queue_name = 'neural_queue'

# Создаем учетные данные для подключения
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)

# Загрузка модели и токенизатора
classifier = joblib.load("../../data/model/service_model/logistic_regression_model.pkl")
le = joblib.load("../../data/model/service_model/label_encoder.pkl")
tokenizer = joblib.load("../../data/model/service_model/tokenizer.pkl")
model = BertModel.from_pretrained("bert-base-uncased")

# Предобработка текста
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# Функция для генерации BERT-эмбеддингов
def bert_text_to_vector(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# Функция для получения топ-N сервисов для нового текста
def get_top_predictions(text, model, classifier, top_n=3):
    text_vector = bert_text_to_vector(text, tokenizer, model)
    probas = classifier.predict_proba([text_vector])[0]
    top_indices = probas.argsort()[-top_n:][::-1]
    top_classes = le.inverse_transform(top_indices)
    return [(top_classes[i], probas[i]) for i in range(top_n)]

def callback(ch, method, properties, body):
    message = body.decode('utf-8')  # Декодируем сообщение
    print(f"Получено сообщение: {message}")

    # Предобработка и получение предсказаний
    preprocessed_message = preprocess_text(message)
    top_services = get_top_predictions(preprocessed_message, model, classifier)

    print("Топ предполагаемых сервисов для обращения:", top_services)

def main():
    # Устанавливаем соединение с RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
    )
    channel = connection.channel()

    # Объявляем очередь, если её нет
    channel.queue_declare(queue=queue_name, durable=True)

    # Устанавливаем обработчик для сообщений
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print('Ожидание сообщений. Нажмите CTRL+C для выхода.')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Выход...')
    finally:
        connection.close()

if __name__ == "__main__":
    main()
