import pika
import time

# Настройки для подключения к RabbitMQ
rabbitmq_host = 'localhost'  # или IP-адрес контейнера Docker
rabbitmq_port = 5672
rabbitmq_user = 'rabbitmq'   # замените на нового пользователя
rabbitmq_password = '1234'   # замените на пароль нового пользователя

# Параметры очереди и сообщение
queue_name = 'test_queue'
message = 'Hello, RabbitMQ!'

# Создаем учетные данные для подключения
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)

# Функция для отправки сообщения
def send_message():
    # Создаем подключение и канал
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
    )
    channel = connection.channel()

    # Убеждаемся, что очередь существует, иначе создаем её
    channel.queue_declare(queue=queue_name, durable=True)

    # Отправляем сообщение
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Сохранение сообщения при перезагрузке RabbitMQ
        )
    )

    print(f"Отправлено сообщение: {message}")

    # Закрываем соединение
    connection.close()

# Функция для получения сообщения
def receive_message():
    # Создаем подключение и канал
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
    )
    channel = connection.channel()

    # Забираем сообщение из очереди
    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
    if method_frame:
        print(f"Получено сообщение: {body.decode()}")
    else:
        print("Нет сообщений в очереди")

    # Закрываем соединение
    connection.close()

# Основной блок: отправка и получение сообщения с задержкой
if __name__ == "__main__":
    send_message()          # Отправляем сообщение
    time.sleep(5)           # Задержка в 5 секунд
    receive_message()       # Получаем сообщение
