import orm

from aopi.models.meta import database, metadata


class User(orm.Model):
    __tablename__ = "users"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    name = orm.String(max_length=100, index=True)
    email = orm.String(max_length=100, allow_null=True)
