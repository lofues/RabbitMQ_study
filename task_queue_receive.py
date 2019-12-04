import time

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明队列
channel.queue_declare('task_queue',durable=True)

# 定义回调函数
def callback(channel,method,properties,body):
    # body为二进制
    body = body.decode()
    print('received %s'%body)
    time.sleep(body.count('.'))
    print('done')
    # 启动确认后，如果程序断开 下次启动时会从上次断开的地方执行(执行未ack的部分)
    channel.basic_ack(delivery_tag=method.delivery_tag)

# prefetch_count = 1 表示每次每个worker都只从队列从取出一个并执行，避免一个忙碌其余空闲的情况
channel.basic_qos(prefetch_count=1)
channel.basic_consume('task_queue',callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()