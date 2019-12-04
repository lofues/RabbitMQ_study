import sys

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

# 声明队列
channel.queue_declare('task_queue',durable=True)


for i in range(10):
    # 通过默认交换机生产消息
    channel.basic_publish(exchange='',
                    routing_key='task_queue',
                    body='hello world...%d'%i)
    time.sleep(1)

# 关闭连接
connection.close()