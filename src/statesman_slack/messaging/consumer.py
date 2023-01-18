__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Messaging
"""

import pika, pika.exceptions
import os, logging, time, json, socket
from statesman_slack import constants
from threading import Thread

# from statesman_slack.utils.slack import handle_interaction_response
from statesman_slack.messaging import params


class MessageConsumer(Thread):
    """_summary_

    Args:
        Thread (_type_): _description_
    """

    def message_callback(self, ch, method, properties, body):
        """_summary_

        Args:
            ch (_type_): _description_
            method (_type_): _description_
            properties (_type_): _description_
            body (_type_): _description_
        """
        logging.info("ch: %s, method: %s, properties: %s, body: %s", ch, method, properties, body)

        try:
            msg = json.loads(body)
            logging.debug("msg: %s", msg)

            # TODO: check response type, handle appropriately

            # handle_interaction_response(msg)
        except Exception as e:
            logging.exception("Exception while processing message from consumer:", e)

    def run(self):
        logging.info("Consumer thread started.")
        while True:
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            try:
                channel.basic_consume(queue=os.environ[constants.RABBITMQ_QUEUE], on_message_callback=self.message_callback, auto_ack=True)
                channel.start_consuming()
            except Exception as e:
                logging.exception("Exception while attempting to consume message:", e)
            finally:
                channel.stop_consuming()
                channel.close()
                connection.close()


consumer_thread = MessageConsumer()
consumer_thread.setDaemon(True)
consumer_thread.start()
