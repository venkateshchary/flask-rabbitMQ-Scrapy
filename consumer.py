from kombu import Connection, Exchange, Queue, Consumer
from mongoclient import mongoconnection

def process_message(body, message):
    print('The body is {}'.format(body))
    conn = mongoconnection()
    insert = conn.insert(body)
    print("doc is :",insert)
    message.ack()

def consumer():
    rabbit_url = "amqp://localhost:5672/"
    conn = Connection(rabbit_url)
    exchange = Exchange("scrapy", type="direct")
    queue = Queue(name="quotation", exchange=exchange, routing_key="quotes")
    with Consumer(conn, queues=queue, callbacks=[process_message], accept=["json"]): 
        conn.drain_events(timeout=2)
    return "consumed successfully"
