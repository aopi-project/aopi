from datetime import datetime

import orm

from aopi.models import Package
from aopi.models.meta import database, metadata


class PackageVersion(orm.Model):
    __tablename__ = "packages_versions"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    package = orm.ForeignKey(Package)

    url = orm.Text()
    size = orm.Float()
    version = orm.Text()
    yanked = orm.Boolean()
    comment_text = orm.Text()
    yanked_reason = orm.Text()
    downloads = orm.Integer(default=0)
    filename = orm.Text(allow_null=False)
    md5_digest = orm.Text(allow_null=False)
    sha256_digest = orm.Text(allow_null=False)
    upload_time = orm.DateTime(default=datetime.now)
    package_type = orm.String(max_length=30, allow_null=False)
    python_version = orm.String(max_length=30, allow_null=False)
    metadata_version = orm.Float()
