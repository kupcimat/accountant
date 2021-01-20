import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class Message:
    s3_object_name: str
    receipt_handle: str
    attributes: Dict[str, Any]
    message_attributes: Dict[str, Any]


def get_queue_url(queue_name: str) -> str:
    sqs = boto3.client("sqs")
    response = sqs.get_queue_url(QueueName=queue_name)
    return response["QueueUrl"]


def receive_message(queue_url: str, wait_time: int = 10) -> Optional[Message]:
    sqs = boto3.client("sqs")
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        AttributeNames=["SentTimestamp"],
        MessageAttributeNames=["All"],
        WaitTimeSeconds=wait_time,
    )
    if "Messages" in response:
        message = response["Messages"][0]
        receipt_handle = message["ReceiptHandle"]
        if "ObjectCreated:Put" in message["Body"]:
            return _parse_message(message)
        else:
            delete_message(queue_url, receipt_handle)
            logging.warn("action=process_message unknown message")
    return None


def delete_message(queue_url: str, receipt_handle: str):
    sqs = boto3.client("sqs")
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle,
    )


def _parse_message(message: Dict[str, Any]) -> Message:
    message_body = json.loads(message["Body"])
    s3_object_name = message_body["Records"][0]["s3"]["object"]["key"]
    receipt_handle = message["ReceiptHandle"]
    attributes = message["Attributes"] if "Attributes" in message else {}
    message_attributes = (
        message["MessageAttributes"] if "MessageAttributes" in message else {}
    )
    return Message(s3_object_name, receipt_handle, attributes, message_attributes)
