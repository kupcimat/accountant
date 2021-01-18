import logging
import tempfile

from accountant.config import QUEUE_NAME, RESULT_BUCKET_NAME, UPLOAD_BUCKET_NAME
from accountant.queue import delete_message, get_queue_url, receive_message
from accountant.storage import download_object, upload_object

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s",
)


def process_message():
    queue_url = get_queue_url(QUEUE_NAME)

    message = receive_message(queue_url)
    if message:
        # TODO process PDF
        with tempfile.NamedTemporaryFile(delete=True) as file:
            download_object(UPLOAD_BUCKET_NAME, message.s3_object_name, file)
            file.seek(0)
            document = file.read()
            logging.info(f"action=download_file file={document}")
        with tempfile.NamedTemporaryFile(delete=True) as file:
            result = b"tmp result\n"
            file.write(result)
            file.seek(0)
            upload_object(RESULT_BUCKET_NAME, message.s3_object_name, file)
        delete_message(queue_url, message.receipt_handle)
        logging.info(f"action=process_message status=success message={message}")
    else:
        logging.info("action=process_message status=success message=no_message")


if __name__ == "__main__":
    try:
        process_message()
    except Exception as e:
        logging.error("action=process_message status=error", e)
