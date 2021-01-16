import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3

from accountant.config import QUEUE_NAME


@dataclass
class Message:
    data: str
    receipt_handle: str
    attributes: Dict[str, Any]
    message_attributes: Dict[str, Any]


def process_message():
    sqs = boto3.client("sqs")
    queue_url = _get_queue_url(sqs, QUEUE_NAME)

    message = _receive_message(sqs, queue_url)
    if message:
        _delete_message(sqs, queue_url, message)
        logging.info(f"action=process_message status=success message={message.data}")
    else:
        logging.info("action=process_message status=success message=no_message")


def _get_queue_url(sqs, queue_name: str) -> str:
    response = sqs.get_queue_url(QueueName=queue_name)
    return response["QueueUrl"]


def _receive_message(sqs, queue_url: str) -> Optional[Message]:
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        AttributeNames=["SentTimestamp"],
        MessageAttributeNames=["All"],
        WaitTimeSeconds=5,
    )
    if "Messages" in response:
        message = response["Messages"][0]
        attributes = message["Attributes"] if "Attributes" in message else {}
        message_attributes = (
            message["MessageAttributes"] if "MessageAttributes" in message else {}
        )
        return Message(
            data=message["Body"],
            receipt_handle=message["ReceiptHandle"],
            attributes=attributes,
            message_attributes=message_attributes,
        )
    return None


def _delete_message(sqs, queue_url: str, message: Message):
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=message.receipt_handle,
    )
