import json
import logging
import os
import tempfile

from accountant.config import QUEUE_NAME, RESULT_BUCKET_NAME, UPLOAD_BUCKET_NAME
from accountant.queue import Message, delete_message, get_queue_url, receive_message
from accountant.storage import download_object, get_object_metadata, upload_object
from accountant.util import serialize, serialize_list
from accountant.worker.models import Error, WorkerException
from accountant.worker.pdf import parse_document

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s",
)
logging.getLogger("pdfminer").setLevel(logging.ERROR)


def process_message(message: Message):
    with tempfile.TemporaryDirectory() as tmp_dir:
        document_file = os.path.join(tmp_dir, "document")
        result_file = os.path.join(tmp_dir, "result")

        # Download document and metadata
        download_object(UPLOAD_BUCKET_NAME, message.s3_object_name, document_file)
        metadata = get_object_metadata(UPLOAD_BUCKET_NAME, message.s3_object_name)

        # Parse document and write result
        transactions = parse_document(document_file, metadata)
        with open(result_file, "w") as file:
            json.dump(serialize_list(transactions), file, sort_keys=True)

        # Upload result
        upload_object(RESULT_BUCKET_NAME, message.s3_object_name, result_file)


def process_error(message: Message, error_message: str):
    with tempfile.TemporaryDirectory() as tmp_dir:
        error_file = os.path.join(tmp_dir, "error")

        # Create and write error
        error = Error(id="error.worker", message=error_message)
        with open(error_file, "w") as file:
            json.dump(serialize(error), file, sort_keys=True)

        # Upload error
        upload_object(RESULT_BUCKET_NAME, message.s3_object_name, error_file)


def process_task():
    queue_url = get_queue_url(QUEUE_NAME)
    message = receive_message(queue_url)
    if message:
        try:
            process_message(message)
            delete_message(queue_url, message)
            logging.info(f"action=process_task status=success message={message}")
        except WorkerException as e:
            process_error(message, e.message)
            delete_message(queue_url, message)
            logging.exception(f"action=process_task status=error message={e.message}")
    else:
        logging.info("action=process_task status=success message=no_message")


if __name__ == "__main__":
    try:
        process_task()
    except Exception as e:
        logging.exception("action=process_task status=error")
