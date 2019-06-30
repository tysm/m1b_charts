from flask import Flask, url_for
from flask_restful import Api, Resource

from m1b.api.call.app import (
    NewCall,
    AddEmotions,
    CallBarChart,
    CallTimeChart,
    CallTimeChartEmotion,
)


class Index(Resource):
    def get(self):
        return {
            "call:new_call": url_for("newcall"),
            "call:add_emotions": url_for("addemotions", call_id=0),
            "chart:call_bar_chart": url_for("callbarchart", call_id=0),
            "chart:call_time_chart": url_for("calltimechart", call_id=0),
            "chart:call_time_chart_emotion": url_for(
                "calltimechart", call_id=0, emotion="<string:emotion>"
            ),
        }


def add_cors_to_response(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers[
        "Access-Control-Allow-Methods"
    ] = "OPTIONS, GET, POST, PUT, PATCH, DELETE"
    return response


app = Flask(__name__)
api = Api(app)
api.add_resource(Index, "/")
api.add_resource(NewCall, "/calls")
api.add_resource(AddEmotions, "/calls/<int:call_id>")
api.add_resource(CallBarChart, "/calls/<int:call_id>/bar_chart")
api.add_resource(CallTimeChart, "/calls/<int:call_id>/time_chart")
api.add_resource(
    CallTimeChartEmotion, "/calls/<int:call_id>/time_chart/<string:emotion>"
)
app.after_request(add_cors_to_response)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
