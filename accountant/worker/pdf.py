import re
from typing import Dict, List

import pdfplumber

from accountant.worker.models import Transaction, WorkerException


STATEMENT_REGEX = (
    r"(\d{2}\.\d{2}\.\d{4})"  # date
    r"([\w\s]+?)"  # description
    r"(\d+-?\d+/\d{4})\s+"  # account
    r"(\d+)\s+"  # variable_symbol
    r"(-?[\d ]+,\d+)"  # amount
)


def parse_document(file_name: str, metadata: Dict[str, str]) -> List[Transaction]:
    try:
        pdf = pdfplumber.open(file_name)
        transactions = []
        for page in pdf.pages:
            page_text = page.extract_text()
            transactions.extend(_parse_page(page_text))
        return transactions
    except Exception as e:
        raise WorkerException("Cannot parse pdf") from e


def _parse_page(page_text: str) -> List[Transaction]:
    transactions = re.findall(STATEMENT_REGEX, page_text)
    return [
        Transaction(date, amount, account, description.strip(), variable_symbol)
        for date, description, account, variable_symbol, amount in transactions
    ]
