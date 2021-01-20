import uuid
from dataclasses import asdict
from typing import Any, Dict, List


def generate_id() -> str:
    return uuid.uuid4().hex


def serialize(model: Any) -> Dict[str, Any]:
    model_name = type(model).__name__
    wrapper_name = model_name[0].lower() + model_name[1:]
    return {wrapper_name: asdict(model)}


def serialize_list(models: List[Any]) -> List[Dict[str, Any]]:
    return [serialize(m) for m in models]
