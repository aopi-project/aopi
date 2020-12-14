from typing import List, Optional, Union

from aiohttp.web_request import FileField
from multidict import MultiDictProxy
from pydantic import Field
from pydantic.fields import SHAPE_LIST
from pydantic.main import BaseConfig, BaseModel


class PackageUploadModel(BaseModel):
    action: str = Field(..., alias=":action")
    author: str
    author_email: str
    blake2_256_digest: str
    classifiers: List[str]
    comment: str
    content: FileField
    description: str
    description_content_type: str
    download_url: str
    project_urls: str
    filetype: str
    home_page: str
    keywords: str
    license: str
    maintainer: str
    maintainer_email: str
    md5_digest: str
    metadata_version: str
    name: str
    protocol_version: str
    pyversion: str
    requires_dist: Optional[List[str]]
    requires_python: str
    sha256_digest: str
    summary: str
    version: str

    @classmethod
    def from_multidict(
        cls, values: MultiDictProxy[Union[str, bytes, FileField]]
    ) -> "PackageUploadModel":
        formatted_dict = dict()
        for key in set(values.keys()):
            field = cls.__fields__.get(key)
            if field and field.shape == SHAPE_LIST:
                formatted_dict[key] = values.getall(key)
            else:
                formatted_dict[key] = values.getone(key)

        return PackageUploadModel(**formatted_dict)

    class Config(BaseConfig):
        arbitrary_types_allowed = True


class PackageVersion(BaseModel):
    requires_python: Optional[str]
    sha256_digest: str
    version: str
    filename: str
    filetype: str
