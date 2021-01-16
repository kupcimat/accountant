import logging
from dataclasses import dataclass, field
from typing import Dict

import boto3
from botocore.exceptions import ClientError


@dataclass
class PresignedUrl:
    url: str
    params: Dict[str, str] = field(default_factory=dict)


def generate_upload_url(
    bucket_name: str, object_name: str, expiration: int = 300
) -> PresignedUrl:
    s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_post(
            bucket_name, object_name, ExpiresIn=expiration
        )
        return PresignedUrl(url=response["url"], params=response["fields"])
    except ClientError as e:
        logging.error("action=generate_upload_url status=error", e)
        raise RuntimeError("Cannot generate upload url")


def generate_download_url(
    bucket_name: str, object_name: str, expiration: int = 300
) -> PresignedUrl:
    s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
        return PresignedUrl(url=response)
    except ClientError as e:
        logging.error("action=generate_download_url status=error", e)
        raise RuntimeError("Cannot generate download url")


def exists_object(bucket_name: str, object_name: str) -> bool:
    s3_client = boto3.client("s3")
    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            logging.error("action=exists_object status=error", e)
            raise RuntimeError("Cannot check object")
    return True


def create_curl(presigned_url: PresignedUrl) -> str:
    form_data = [f"-F '{key}={value}'" for key, value in presigned_url.params.items()]
    form_data.append(f"-F 'file=@filename'")
    return f"curl -L {' '.join(form_data)} {presigned_url.url}"
