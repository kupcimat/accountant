import logging
from typing import Dict, IO

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError


# TODO make S3 calls non-blocking
def generate_upload_url(
    bucket_name: str, object_name: str, metadata: Dict[str, str]
) -> str:
    return _generate_presigned_url(bucket_name, object_name, "put_object", metadata)


def generate_download_url(bucket_name: str, object_name: str) -> str:
    return _generate_presigned_url(bucket_name, object_name, "get_object")


def _generate_presigned_url(
    bucket_name: str,
    object_name: str,
    client_method: str,
    metadata: Dict[str, str] = None,
    expiration: int = 300,
) -> str:
    params = {"Bucket": bucket_name, "Key": object_name}
    if metadata:
        params["Metadata"] = metadata
    # Invalid signature without configuring addressing_style
    s3 = boto3.client("s3", config=Config(s3={"addressing_style": "path"}))
    try:
        url = s3.generate_presigned_url(
            client_method, Params=params, ExpiresIn=expiration
        )
        return url
    except ClientError as e:
        logging.error("action=generate_presigned_url status=error", e)
        raise RuntimeError("Cannot generate presigned url")


def exists_object(bucket_name: str, object_name: str) -> bool:
    s3 = boto3.client("s3")
    try:
        s3.head_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            logging.error("action=exists_object status=error", e)
            raise RuntimeError("Cannot check object")
    return True


def download_object(bucket_name: str, object_name: str, file: IO):
    s3 = boto3.client("s3")
    try:
        s3.download_fileobj(bucket_name, object_name, file)
    except ClientError as e:
        logging.error("action=download_object status=error", e)
        raise RuntimeError("Cannot download object")


def upload_object(bucket_name: str, object_name: str, file: IO):
    s3 = boto3.client("s3")
    try:
        s3.upload_fileobj(file, bucket_name, object_name)
    except ClientError as e:
        logging.error("action=upload_object status=error", e)
        raise RuntimeError("Cannot upload object")


def create_upload_curl(url: str, metadata: Dict[str, str]) -> str:
    headers = " ".join(
        [f"-H 'x-amz-meta-{key}: {value}'" for key, value in metadata.items()]
    )
    return f"curl -X PUT {headers} --upload-file filename '{url}'"


def create_download_curl(url: str) -> str:
    return f"curl '{url}'"
