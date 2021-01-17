import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3

from accountant.config import QUEUE_NAME


@dataclass
class Message:
    s3_object_name: str
    receipt_handle: str
    attributes: Dict[str, Any]
    message_attributes: Dict[str, Any]


def process_message():
    sqs = boto3.client("sqs")
    queue_url = _get_queue_url(sqs, QUEUE_NAME)

    message = _receive_message(sqs, queue_url)
    if message:
        _delete_message(sqs, queue_url, message.receipt_handle)
        logging.info(f"action=process_message status=success message={message}")
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
        receipt_handle = message["ReceiptHandle"]
        if "ObjectCreated:Post" in message["Body"]:
            return _parse_message(message)
        else:
            _delete_message(sqs, queue_url, receipt_handle)
            logging.warn("action=process_message unknown message")
    return None


def _parse_message(message: Dict[str, Any]) -> Message:
    message_body = json.loads(message["Body"])
    s3_object_name = message_body["Records"][0]["s3"]["object"]["key"]
    receipt_handle = message["ReceiptHandle"]
    attributes = message["Attributes"] if "Attributes" in message else {}
    message_attributes = (
        message["MessageAttributes"] if "MessageAttributes" in message else {}
    )
    return Message(s3_object_name, receipt_handle, attributes, message_attributes)


def _delete_message(sqs, queue_url: str, receipt_handle: str):
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle,
    )
