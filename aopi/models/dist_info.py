from enum import Enum, unique
from typing import List, Optional

from fastapi import File, UploadFile
from pydantic import Field
from pydantic.main import BaseConfig, BaseModel

from aopi.utils.pydantic_form import as_form


@unique
class ReadmeContentType(str, Enum):
    MD = "text/markdown"
    RST = "text/x-rst"
    PLAIN = "text/plain"


class DistInfoModel(BaseModel):
    name: str
    version: str
    filetype: str
    metadata_version: float
    md5_digest: Optional[str]
    sha256_digest: Optional[str]
    requires_python: Optional[str]
    protocol_version: Optional[str]
    author: Optional[str]
    summary: Optional[str]
    blake2_256_digest: Optional[str]
    comment: Optional[str]
    license: Optional[str]
    keywords: Optional[str]
    provides: Optional[str]
    requires: Optional[str]
    obsoletes: Optional[str]
    home_page: Optional[str]
    maintainer: Optional[str]
    description: Optional[str]
    author_email: Optional[str]
    download_url: Optional[str]
    provides_dist: Optional[str]
    platform: Optional[List[str]]
    obsoletes_dist: Optional[str]
    maintainer_email: Optional[str]
    classifiers: Optional[List[str]]
    requires_external: Optional[str]
    project_urls: Optional[List[str]]
    requires_dist: Optional[List[str]]
    supported_platform: Optional[List[str]]
    description_content_type: Optional[ReadmeContentType]
    python_version: Optional[str] = Field(None, alias="pyversion")


@as_form
class PackageUploadModel(DistInfoModel):
    action: str = Field(..., alias=":action")
    content: UploadFile = File(...)

    class Config(BaseConfig):
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
