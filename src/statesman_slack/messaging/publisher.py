__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Messaging
"""

import pika, pika.exceptions
import os, logging, time, json, socket
from statesman_slack import constants
from threading import Thread
from statesman_slack.utils.commands import construct_command


def send_amqp_message(msg: dict):
    """_summary_

    Args:
        msg (_type_): _description_
    """
    logging.debug("msg: %s", msg)

    command = construct_command(msg)
    logging.debug("command: %s", command)

    body_data = {
        "sender": os.environ.get(constants.POD, socket.gethostname()),
        "timestamp": time.time(),
        "response_data": {
            "queue": os.environ[constants.RABBITMQ_QUEUE],
            "application_id": msg["application_id"],
            "token": msg["token"],
            "raw_data": msg["data"],
        },
        "user": {
            "service": "slack",
            "org_id": f"slack|{msg['guild_id']}",
            "canonical_id": f"slack|{msg['member']['user']['id']}",
            "data": msg["member"]["user"],
        },
        "data": {"command": command},
    }
    body = json.dumps(body_data)
    logging.debug("body: %s", body)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    try:
        channel.basic_publish(exchange=os.environ[constants.RABBITMQ_EXCHANGE], routing_key=os.environ[constants.RABBITMQ_API_QUEUE], body=body)
    except pika.exceptions.UnroutableError as e:
        logging.exception("Health check message was returned:", e)
    except Exception as e:
        logging.exception("Exception while attempting to publish message:", e)
    finally:
        channel.close()
