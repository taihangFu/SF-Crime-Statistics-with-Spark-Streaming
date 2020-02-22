import asyncio
import logging

from confluent_kafka import Consumer

BROKER_URL = "localhost:9092"

async def consume(topic_name):
    """Consumes data from the Kafka Topic"""
    c = Consumer({"bootstrap.servers": BROKER_URL, "group.id": "0"}) # Consumer groups consist of one or more consumers
    c.subscribe([topic_name])

    logging.basicConfig(level=logging.DEBUG)

    while True:
        messages = c.consume(5, timeout=1.0)

        # To indicate how many messages have consumed.
        logging.info(f"consumed {len(messages)} messages")
        for message in messages:
            if message is None:
                logging.warning("no message received by consumer")
            elif message.error() is not None:
                logging.error(f"error from consumer {message.error()}")
            else:
                logging.info(f"consumed message {message.key()}: {message.value()}")
        
        # Do not delete this!
        await asyncio.sleep(0.01)


def main():
    
    try:
        asyncio.run(consume("com.udacity.crime.police-event")) 
    except KeyboardInterrupt as e:
        print("shutting down")

        
if __name__ == "__main__":
    main()