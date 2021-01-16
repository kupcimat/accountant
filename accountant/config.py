import os


def get_env_str(variable: str, default: str) -> str:
    return os.getenv(variable, default)


def get_env_int(variable: str, default: int) -> int:
    return int(os.getenv(variable, default))


PORT = get_env_int("PORT", 80)
QUEUE_NAME = get_env_str("QUEUE_NAME", "accountant-worker-queue")
UPLOAD_BUCKET_NAME = "accountant-document-uploads"
RESULT_BUCKET_NAME = "accountant-document-results"
