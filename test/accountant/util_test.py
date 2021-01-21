import pytest
import re
from dataclasses import dataclass

from accountant.util import generate_id, serialize, serialize_list


@dataclass
class Question:
    name: str
    priority: int


@dataclass
class Answer:
    name: str
    priority: int


def test_generate_id():
    assert re.match(r"^[a-f0-9]+$", generate_id())


@pytest.mark.parametrize(
    "model,expected",
    [
        (
            Question(name="what", priority=1),
            {"question": {"name": "what", "priority": 1}},
        ),
        (
            Answer(name="42", priority=2),
            {"answer": {"name": "42", "priority": 2}},
        ),
    ],
)
def test_serialize(model, expected):
    assert serialize(model) == expected


@pytest.mark.parametrize(
    "models,expected",
    [
        ([], []),
        (
            [Question(name="what", priority=1)],
            [{"question": {"name": "what", "priority": 1}}],
        ),
        (
            [Question(name="what", priority=1), Answer(name="42", priority=2)],
            [
                {"question": {"name": "what", "priority": 1}},
                {"answer": {"name": "42", "priority": 2}},
            ],
        ),
    ],
)
def test_serialize_list(models, expected):
    assert serialize_list(models) == expected
