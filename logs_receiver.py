"""
    使用扇形交换机
    使用临时队列
"""

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 声明队列与交换机
channel.exchange_declare(exchange='logs',exchange_type='fanout')
result = channel.queue_declare(queue='',exclusive=True)
queue_name = result.method.queue

# 绑定临时队列到交换机
channel.queue_bind(exchange='logs',queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch,method,properities,body):
    print('[x] %r'%body)

channel.basic_consume(queue=queue_name,on_message_callback=callback)
channel.start_consuming()