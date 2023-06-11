from pprint import pprint
from requests import request, Response
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("ASSISTANT_API")


class Requests:
    def __init__(self, **default_params: dict) -> None:
        self.default_params = default_params

    def request(self, path: list = [], **params: dict) -> Response:
        params = {
            **self.default_params,
            **params
        }

        if 'url' not in params:
            raise "Url must be contain!"

        if 'json' not in params:
            params['json'] = {}

        params['url'] = params['url'] + "/".join(path)

        return request(**params)


interface = Requests(
    url=url,
    headers={
        "Content-Type": "application/json"
    }
)


class OpenAi:
    def __init__(self, chat) -> None:
        self.chat = chat
        self.createChat()

    def addMessage(self, message) -> Response:
        return interface.request(
            path=['chat', 'message'],
            method='POST',
            json={
                "name": self.chat,
                "message": {
                    "content": message,
                    "role": "user"
                }
            }).json()

    def getHistory(self):
        return interface.request(["chat"], method="GET", json={
            "name": self.chat
        }).json()

    def getAiResponse(self):
        return interface.request(
            ["chat", "send-history"],
            method="POST",
            json={
                "name": self.chat
            }
        ).json()["response"]

    def createChat(self):
        return interface.request(["chat"], method="POST", json={
            "name": self.chat
        }).json()
