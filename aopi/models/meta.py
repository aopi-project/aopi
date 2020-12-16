import databases
import sqlalchemy

from aopi.settings import settings

database = databases.Database(settings.aopi_db_url)
metadata = sqlalchemy.MetaData()
