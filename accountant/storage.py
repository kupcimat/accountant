import logging
from dataclasses import dataclass, field
from typing import Dict, IO

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError


@dataclass
class PresignedUrl:
    url: str
    params: Dict[str, str] = field(default_factory=dict)


# TODO make S3 calls non-blocking
def generate_upload_url(
    bucket_name: str, object_name: str, expiration: int = 300
) -> PresignedUrl:
    s3 = boto3.client("s3")
    try:
        response = s3.generate_presigned_post(
            bucket_name, object_name, ExpiresIn=expiration
        )
        return PresignedUrl(url=response["url"], params=response["fields"])
    except ClientError as e:
        logging.error("action=generate_upload_url status=error", e)
        raise RuntimeError("Cannot generate upload url")


def generate_download_url(
    bucket_name: str, object_name: str, expiration: int = 300
) -> PresignedUrl:
    # Invalid signature without addressing_style config
    s3 = boto3.client("s3", config=Config(s3={"addressing_style": "path"}))
    try:
        response = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
        return PresignedUrl(url=response)
    except ClientError as e:
        logging.error("action=generate_download_url status=error", e)
        raise RuntimeError("Cannot generate download url")


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


def create_upload_curl(presigned_url: PresignedUrl) -> str:
    form_data = [f"-F '{key}={value}'" for key, value in presigned_url.params.items()]
    form_data.append(f"-F 'file=@filename'")
    return f"curl -L {' '.join(form_data)} {presigned_url.url}"


def create_download_curl(presigned_url: PresignedUrl) -> str:
    return f"curl -L '{presigned_url.url}'"
