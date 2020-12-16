import orm

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
    description = orm.Text(allow_null=True)
    project_urls = orm.Text(allow_null=True)
    author_email = orm.Text(allow_null=True)
    maintainer_email = orm.Text(allow_null=True)
    description_content_type = orm.Text(allow_null=True)
