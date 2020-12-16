from enum import Enum, unique
from typing import List, Optional, Union

from aiohttp.web_request import FileField
from multidict import MultiDictProxy
from pydantic import Field
from pydantic.fields import SHAPE_LIST
from pydantic.main import BaseConfig, BaseModel


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


class PackageUploadModel(DistInfoModel):
    action: str = Field(..., alias=":action")
    content: FileField

    @classmethod
    def from_multidict(
        cls, values: MultiDictProxy[Union[str, bytes, FileField]]
    ) -> "PackageUploadModel":
        formatted_dict = dict()
        for key in set(values.keys()):
            field = cls.__fields__.get(key)
            if field and field.shape == SHAPE_LIST:
                formatted_dict[key] = values.getall(key) or None
            else:
                formatted_dict[key] = values.getone(key) or None

        return PackageUploadModel(**formatted_dict)

    class Config(BaseConfig):
        arbitrary_types_allowed = True
