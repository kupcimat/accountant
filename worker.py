import logging

import boto3

from accountant.config import QUEUE_NAME
from accountant.queue import delete_message, get_queue_url, receive_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s",
)


def process_message():
    sqs = boto3.client("sqs")
    queue_url = get_queue_url(sqs, QUEUE_NAME)

    message = receive_message(sqs, queue_url)
    if message:
        delete_message(sqs, queue_url, message.receipt_handle)
        logging.info(f"action=process_message status=success message={message}")
    else:
        logging.info("action=process_message status=success message=no_message")


if __name__ == "__main__":
    try:
        process_message()
    except Exception as e:
        logging.error("action=process_message status=error", e)
