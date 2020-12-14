import databases
import sqlalchemy

from aopi.settings import settings

database = databases.Database(rf"sqlite:///{settings.aopi_db_file}")
metadata = sqlalchemy.MetaData()
