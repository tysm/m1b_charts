import datetime

from peewee import DateTimeField
from peewee import Model
from peewee import MySQLDatabase

import m1b.utils as utils


db = MySQLDatabase(
    database=utils.env.get("database", "database"),
    user=utils.env.get("database", "user"),
    password=utils.env.get("database", "password"),
)


class _BaseModel(Model):
    class Meta:
        database = db

    created_at = DateTimeField(default=datetime.datetime.utcnow)
