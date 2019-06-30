import requests

from m1b.utils._env import env


API_URL = env.get("face-api", "url")


def request_emotion(image_bin):
    params = {"returnFaceAttributes": "emotion"}
    headers = {
        "ocp-apim-subscription-key": env.get("face-api", "key"),
        "content-type": "application/octet-stream",
    }
    r = requests.post(
        API_URL + "/detect", params=params, data=image_bin, headers=headers
    )
    return r.json()
