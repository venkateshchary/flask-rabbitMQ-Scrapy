from kombu import Connection, Exchange, Producer, Queue


def producer(msg=None):
    print("------- in producer")
    rabbit_url = "amqp://localhost:5672/"
    conn = Connection(rabbit_url)
    channel = conn.channel()
    exchange = Exchange("scrapy", type="direct")
    producer = Producer(exchange=exchange, channel=channel, routing_key="quotes")
    queue = Queue(name="quotation", exchange=exchange, routing_key="quotes")
    queue.maybe_bind(conn)
    queue.declare()
    producer.publish(msg)
    print("published ->")
