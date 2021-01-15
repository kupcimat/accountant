import os


def get_env_int(variable: str, default: int) -> int:
    return int(os.getenv(variable, default))


PORT = get_env_int("PORT", 80)
UPLOAD_BUCKET_NAME = "accountant-document-uploads"
RESULT_BUCKET_NAME = "accountant-document-results"
