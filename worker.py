import logging

from accountant.queue import process_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s",
)


if __name__ == "__main__":
    try:
        process_message()
    except Exception as e:
        logging.error("action=process_message status=error", e)
