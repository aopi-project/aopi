import re
from typing import Any, Tuple, Type, Union

import databases
import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm.attributes import InstrumentedAttribute

from aopi.settings import settings

database = databases.Database(settings.aopi_db_url)
metadata = sqlalchemy.MetaData()


@as_declarative(metadata=metadata)
class Base(object):
    __name__: str
    __table__: sa.Table
    __table_args__: Tuple[Any, ...]

    @declared_attr
    def __tablename__(self) -> str:
        """
        Converts CamelCase class name to snake_case table name.

        :return table name in snake_case.
        """
        name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", self.__name__)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    @declared_attr
    def id(self) -> Any:
        return sa.Column(
            sa.Integer,
            primary_key=True,
        )

    @classmethod
    def select_query(
        cls,
        *columns: Union[InstrumentedAttribute, Type["Base"]],
        use_labels: bool = False,
    ) -> sa.sql.Select:
        return sa.select(columns or [cls], use_labels=use_labels)

    @classmethod
    def insert_query(cls, **values: Any) -> sa.sql.Insert:
        return cls.__table__.insert().values(**values)

    @classmethod
    def update_query(cls) -> sa.sql.Update:
        return cls.__table__.update()

    @classmethod
    def delete_query(cls) -> sa.sql.Delete:
        return cls.__table__.delete()
