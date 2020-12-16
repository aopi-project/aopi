from typing import Any, Dict

import orm

from aopi.api.simple.models import PackageUploadModel
from aopi.models.meta import database, metadata


class Package(orm.Model):
    __tablename__ = "packages"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    name = orm.Text(allow_null=False, index=True)

    author = orm.Text(allow_null=True)
    summary = orm.Text(allow_null=True)
    license = orm.Text(allow_null=True)
    keywords = orm.Text(allow_null=True)
    home_page = orm.Text(allow_null=True)
    maintainer = orm.Text(allow_null=True)
    project_urls = orm.Text(allow_null=True)
    author_email = orm.Text(allow_null=True)
    maintainer_email = orm.Text(allow_null=True)

    @staticmethod
    def cast_upload_to_data(upload: PackageUploadModel) -> Dict[str, Any]:
        return dict(
            name=upload.name,
            summary=upload.summary,
            license=upload.license,
            keywords=upload.keywords,
            home_page=upload.home_page,
            author=upload.author,
            author_email=upload.author_email,
            project_urls=";".join(upload.project_urls) if upload.project_urls else None,
            maintainer=upload.maintainer,
            maintainer_email=upload.maintainer_email,
        )

    @classmethod
    async def create_by_upload(cls, upload: PackageUploadModel) -> "Package":
        upload_dict = cls.cast_upload_to_data(upload)
        return await cls.objects.create(**upload_dict)

    async def update_by_upload(self, upload: PackageUploadModel) -> None:
        upload_dict = self.cast_upload_to_data(upload)
        await self.update(**upload_dict)