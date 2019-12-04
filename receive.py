"""
    模拟RabbitMQ的消费者,将消息接受并打印
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明队列，以免队列不存在
# 设置持久化：durable = True 这样rabbitMq重启队列不会丢失
channel.queue_declare(queue='hello',durable=True)

# 设置回调函数，当收到消息时执行
def callback(ch,method,properties,body):
    print("received %s"%body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 设置回调函数被队列消费
channel.basic_consume('hello',callback)

# 无限循环等待执行
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


