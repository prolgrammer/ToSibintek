import pika

# Настройки для подключения к RabbitMQ
rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_user = 'rabbitmq'
rabbitmq_password = '1234'

# Параметры очереди
queue_name = 'neural_queue'
message = 'Network connection problem'  # Пример сообщения

# Создаем учетные данные для подключения
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)

def send_message_to_queue(message):
    """Отправляет сообщение в очередь RabbitMQ."""
    # Устанавливаем соединение с RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
    )
    channel = connection.channel()

    # Объявляем очередь, если её нет
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

if __name__ == "__main__":
    send_message_to_queue(message)  # Отправляем тестовое сообщение
