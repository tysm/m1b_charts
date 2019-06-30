from peewee import DateTimeField
from peewee import IntegerField
from peewee import FloatField
from peewee import ForeignKeyField

from m1b.db.models.base import _BaseModel


class Call(_BaseModel):
    class Meta:
        table_name = "call"

    user_id = IntegerField()
    timestamp = DateTimeField()


class Emotions(_BaseModel):
    class Meta:
        table_name = "emotions"

    call = ForeignKeyField(Call)

    anger = FloatField()
    contempt = FloatField()
    disgust = FloatField()
    fear = FloatField()
    happiness = FloatField()
    neutral = FloatField()
    sadness = FloatField()
    surprise = FloatField()
    timestamp = DateTimeField()


_CALLS_TABLES = (Call, Emotions)
