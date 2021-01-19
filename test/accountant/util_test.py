import re

from accountant.util import generate_id


def test_generate_id():
    assert re.match(r"^[a-f0-9]+$", generate_id())
