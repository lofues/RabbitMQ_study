"""
    模拟 rabbitmq 的生产者
"""
import pika

# 跟本地机器代理建立连接  将参数修改为其他ip即可连接其他机器
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 将消息发送给一个队列  队列不存在就丢弃
channel.queue_declare(queue='hello',durable=True)

# 通过默认交换机将消息转发给队列,exchange为空字符串表示默认  routing_key 参数填写队列名称
# properties 属性设置：delivery_mode = 2可以将队列中的消息设置为持久消息，重启rabbit仍然存在
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='hello world',
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                      ))


# 发送之后断开连接
connection.close()