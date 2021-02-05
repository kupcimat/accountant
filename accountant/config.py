import os

import boto3
import botocore.client


def get_env_str(variable: str, default: str) -> str:
    return os.getenv(variable, default)


def get_env_int(variable: str, default: int) -> int:
    return int(os.getenv(variable, default))


def boto3_client(
    service_name: str, config: botocore.client.Config = None, endpoint_url: str = None
):
    return boto3.client(
        service_name,
        config=config,
        endpoint_url=endpoint_url or os.getenv("AWS_ENDPOINT_URL"),
    )


def boto3_client_localhost(service_name: str, config: botocore.client.Config = None):
    return boto3_client(
        service_name, config, endpoint_url=os.getenv("AWS_ENDPOINT_URL_LOCALHOST")
    )


PORT = get_env_int("PORT", 80)
QUEUE_NAME = get_env_str("QUEUE_NAME", "accountant-worker-queue")
UPLOAD_BUCKET_NAME = "accountant-document-uploads"
RESULT_BUCKET_NAME = "accountant-document-results"
