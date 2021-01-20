from dataclasses import dataclass


class WorkerException(Exception):
    def __init__(self, message: str):
        self.message = message


@dataclass
class Error:
    id: str
    message: str


@dataclass
class Transaction:
    date: str
    amount: str
    account: str
    description: str
    variable_symbol: str
