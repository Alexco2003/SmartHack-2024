import json
from typing import Dict, List, TypedDict, Union

import requests


class ErrorType(TypedDict):
    type: str
    title: str
    status: int
    detail: str
    instance: str
    properties: Dict[str, dict]


class DemandType(TypedDict):
    customerId: str
    amount: int
    postDay: int
    startDay: int
    endDay: int


class PenaltyType(TypedDict):
    day: int
    type: str
    message: str
    cost: float
    co2: float


class MetricsType(TypedDict):
    day: int
    cost: float
    co2: float


class ResponseType(TypedDict):
    round: int
    demand: List[DemandType]
    penalties: List[PenaltyType]
    deltaKpis: MetricsType
    totalKpis: MetricsType


class MovementType(TypedDict):
    connectionId: str
    amount: int


class RequestBodyType(TypedDict):
    day: int
    movements: List[MovementType]


class Rest:
    """A utility class for managing TESTER API sessions and requests.

    Attributes:
        PORT (int): The port number for the REST API, default is 8080.
        API_KEY (str | None): The API key used for authentication, default is None.
        USER_AGENT (str): The User-Agent header string for HTTP requests.
    """

    PORT: int = 8080
    API_KEY: Union[str, None] = None
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    )
    TIMEOUT: int = 30.0

    @staticmethod
    def set_api_key(api_key: str) -> None:
        Rest.API_KEY = api_key

    @staticmethod
    def set_port(port: int) -> None:
        Rest.PORT = port

    @staticmethod
    def set_timeout(timeout: float) -> None:
        Rest.TIMEOUT = timeout

    @staticmethod
    def is_api_key_none() -> None:
        if Rest.API_KEY is None:
            raise ValueError("API KEY can not be None")

    @staticmethod
    def start_session() -> Union[str, ErrorType]:
        """Initiates a session with the REST API.

        Returns:
            str | ErrorType: The SESSION-ID response as a string or an error type if the request fails.
        """

        Rest.is_api_key_none()

        response = None

        try:
            response = requests.post(
                f"http://localhost:{Rest.PORT}/api/v1/session/start",
                headers={"accept": "*/*", "User-Agent": Rest.USER_AGENT, "API-KEY": Rest.API_KEY},
                timeout=Rest.TIMEOUT,
            )

            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if response is not None:
                return json.loads(response.text)

            return ""

        return response.text

    @staticmethod
    def end_session() -> Union[ResponseType, ErrorType]:
        """Ends the current session with the REST API.

        Returns:
            ResponseType | ErrorType: The server response as a response type or an error type if the request fails.
        """
        Rest.is_api_key_none()

        response = requests.post(
            f"http://localhost:{Rest.PORT}/api/v1/session/end",
            headers={"accept": "*/*", "User-Agent": Rest.USER_AGENT, "API-KEY": Rest.API_KEY},
            timeout=Rest.TIMEOUT,
        )

        return json.loads(response.text)

    @staticmethod
    def play_round(session_id: str, body: RequestBodyType) -> Union[ResponseType, ErrorType]:
        """Sends a request to play a round in the current session.

        Args:
            session_id (str): The ID of the current session.
            body (RequestBodyType): The request body containing round details.

        Returns:
            ResponseType | ErrorType: The server response as a response type or an error type if the request fails.
        """

        Rest.is_api_key_none()

        response = requests.post(
            f"http://localhost:{Rest.PORT}/api/v1/play/round",
            headers={
                "accept": "*/*",
                "User-Agent": Rest.USER_AGENT,
                "API-KEY": Rest.API_KEY,
                "SESSION-ID": session_id,
            },
            json=body,
            timeout=Rest.TIMEOUT,
        )

        return json.loads(response.text)
