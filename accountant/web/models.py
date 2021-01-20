from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class Root:
    links: Dict[str, str]


@dataclass
class DocumentRequest:
    documentType: str


@dataclass
class DocumentUpload:
    uploadUrl: str
    uploadCurl: str
    links: Dict[str, str]


@dataclass
class DocumentResult:
    resultUrl: str
    resultCurl: str
    links: Dict[str, str]


def serialize(model: Any) -> Dict[str, Any]:
    model_name = type(model).__name__
    wrapper_name = model_name[0].lower() + model_name[1:]
    return {wrapper_name: asdict(model)}
