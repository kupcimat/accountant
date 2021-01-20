from dataclasses import dataclass
from typing import Dict


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
