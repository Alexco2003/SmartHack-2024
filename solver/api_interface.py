import json
from typing import Dict, TypedDict

import requests


class ErrorType(TypedDict):
    type: str
    title: str
    status: int
    detail: str
    instance: str
    properties: Dict[str, dict]


class Rest:
    PORT: int = 8080
    API_KEY: str | None = None
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    )

    @staticmethod
    def set_api_key(api_key: str) -> None:
        Rest.API_KEY = api_key

    @staticmethod
    def set_port(port: int) -> None:
        Rest.PORT = port

    @staticmethod
    def start_session() -> str | ErrorType:
        if Rest.API_KEY is None:
            raise ValueError("API KEY can not be None")

        response = None

        try:
            response = requests.post(
                f"http://localhost:{Rest.PORT}/api/v1/session/start",
                headers={"accept": "*/*", "User-Agent": Rest.USER_AGENT, "API-KEY": Rest.API_KEY},
            )

            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if response is not None:
                return json.loads(response.text)

            return ""

        return response.text

    @staticmethod
    def end_session() -> None:
        pass

    @staticmethod
    def play_round() -> None:
        pass
