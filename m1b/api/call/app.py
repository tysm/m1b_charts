import datetime

import numpy as np
from flask import request, make_response
from flask_restful import Resource
from peewee import fn as peewee_fn
from werkzeug.exceptions import BadRequest

from m1b.db.models.calls import Call, Emotions
from m1b.utils.chart import bar_chart, linear_char
from m1b.utils.face import request_emotion


class NewCall(Resource):
    def post(self):
        post_body = request.get_json()

        user_id = post_body.get("user_id")
        if not isinstance(user_id, int):
            raise BadRequest("invalid user_id")

        timestamp = request.args.get("timestamp")
        if not isinstance(timestamp, str):
            raise BadRequest("invalid timestamp")
        timestamp = datetime.datetime.fromisoformat(timestamp)

        new_call = Call.create(user_id=user_id, timestamp=timestamp)
        return {"id": new_call.id}


class AddEmotions(Resource):
    def post(self, call_id: int):
        image = request.data
        if not image:
            raise BadRequest("invalid image data")
        post_body = request_emotion(image)

        if not isinstance(post_body, list):
            raise BadRequest("invalid image data")

        try:
            call = Call.get_by_id(call_id)
        except Call.DoesNotExist:
            raise BadRequest("invalid call_id")

        timestamp = request.args.get("timestamp")
        if not isinstance(timestamp, str):
            raise BadRequest("invalid timestamp")
        timestamp = datetime.datetime.fromisoformat(timestamp)

        emotions = post_body[0]["faceAttributes"].get("emotion")
        if not isinstance(emotions, dict):
            raise BadRequest("invalid emotions")

        new_emotions = Emotions.create(call=call, timestamp=timestamp, **emotions)
        emotions["id"] = new_emotions.id
        return {"id": call_id, "emotions": emotions}


class CallBarChart(Resource):
    def get(self, call_id: int):
        try:
            call = Call.get_by_id(call_id)
        except Call.DoesNotExist:
            raise BadRequest("invalid call_id")

        call_emotions_total = list(
            Emotions.select(
                peewee_fn.SUM(Emotions.anger).alias("anger_total"),
                peewee_fn.SUM(Emotions.contempt).alias("contempt_total"),
                peewee_fn.SUM(Emotions.disgust).alias("disgust_total"),
                peewee_fn.SUM(Emotions.fear).alias("fear_total"),
                peewee_fn.SUM(Emotions.happiness).alias("happiness_total"),
                peewee_fn.SUM(Emotions.neutral).alias("neutral_total"),
                peewee_fn.SUM(Emotions.sadness).alias("sadness_total"),
                peewee_fn.SUM(Emotions.surprise).alias("surprise_total"),
            )
            .where(Emotions.call == call)
            .execute()
        )[0]
        emotions = {
            "raiva": call_emotions_total.anger_total or 0.0,
            "desprezo": call_emotions_total.contempt_total or 0.0,
            "desgosto": call_emotions_total.disgust_total or 0.0,
            "medo": call_emotions_total.fear_total or 0.0,
            "felicidade": call_emotions_total.happiness_total or 0.0,
            "neutro": call_emotions_total.neutral_total or 0.0,
            "tristeza": call_emotions_total.sadness_total or 0.0,
            "surpresa": call_emotions_total.surprise_total or 0.0,
        }

        emotions_keys = list(emotions.keys())
        emotions_values = np.asarray(list(emotions.values()), dtype=np.float32)
        emotions_values /= emotions_values.max()

        response = make_response(bar_chart(emotions_keys, emotions_values))
        response.headers.set("Content-Type", "image/png")
        return response


class CallTimeChart(Resource):
    def get(self, call_id: int):
        try:
            call = Call.get_by_id(call_id)
        except Call.DoesNotExist:
            raise BadRequest("invalid call_id")

        call_emotions_list = list(
            Emotions.select().where(Emotions.call == call).execute()
        )
        if len(call_emotions_list) == 0:
            response = make_response(b"")
            response.headers.set("Content-Type", "image/png")
            return response

        times = []
        emotions = {
            "raiva": [],
            "desprezo": [],
            "desgosto": [],
            "medo": [],
            "felicidade": [],
            "neutro": [],
            "tristeza": [],
            "surpresa": [],
        }
        for item in call_emotions_list:
            times.append((item.timestamp - call.timestamp).total_seconds() / 60)
            emotions["raiva"].append(item.anger)
            emotions["desprezo"].append(item.contempt)
            emotions["desgosto"].append(item.disgust)
            emotions["medo"].append(item.fear)
            emotions["felicidade"].append(item.happiness)
            emotions["neutro"].append(item.neutral)
            emotions["tristeza"].append(item.sadness)
            emotions["surpresa"].append(item.surprise)

        response = make_response(
            linear_char(list(emotions.keys()), list(emotions.values()), times)
        )
        response.headers.set("Content-Type", "image/png")
        return response


class CallTimeChartEmotion(Resource):
    def get(self, call_id: int, emotion: str):
        try:
            call = Call.get_by_id(call_id)
        except Call.DoesNotExist:
            raise BadRequest("invalid call_id")

        valid_emotions = {
            "anger": "raiva",
            "contempt": "desprezo",
            "disgust": "disgust",
            "fear": "medo",
            "happiness": "felicidade",
            "neutral": "neutro",
            "sadness": "tristeza",
            "surprise": "surpresa",
        }
        if emotion not in valid_emotions:
            raise BadRequest("invalid emotion")

        call_emotions_list = list(
            Emotions.select().where(Emotions.call == call).execute()
        )
        if len(call_emotions_list) == 0:
            response = make_response(b"")
            response.headers.set("Content-Type", "image/png")
            return response

        times = []
        emotions = {valid_emotions[emotion]: []}
        for item in call_emotions_list:
            times.append((item.timestamp - call.timestamp).total_seconds() / 60)
            emotions[valid_emotions[emotion]].append(getattr(item, emotion))

        response = make_response(
            linear_char(list(emotions.keys()), list(emotions.values()), times)
        )
        response.headers.set("Content-Type", "image/png")
        return response
