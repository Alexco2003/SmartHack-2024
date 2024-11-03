from typing import List, Union

from solver.api_interface import MovementType, ResponseType, Rest
from solver.linalg.problem_definition import ProblemModel
from solver.utils.mapper import map_demand_type_to_demand
from solver.utils.types import Demand


class LingalgPlayer:
    """A class to manage a session and play multiple rounds in tester environment.

    Attributes:
        SESSION_ID (Union[str, None]): The session identifier, initialized as None and assigned
            when a session is started.
        NUMBER_OF_ROUNDS (int): The total number of rounds to play, defaulted to 42.
        moves (List[MovementType]): A list of moves made by the player during each round.
    """

    SESSION_ID = None
    NUMBER_OF_ROUNDS = 42
    moves: List[MovementType] = []

    @staticmethod
    def start_session() -> None:
        LingalgPlayer.SESSION_ID = Rest.start_session()

    @staticmethod
    def set_api_key(api_key: str) -> None:
        Rest.set_api_key(api_key)

    @staticmethod
    def play() -> ResponseType:
        """Manages the entire play session, including starting the session, processing each round,
        handling demands, and ending the session.

        Returns:
            ResponseType: The final response from the last round played.
        """
        LingalgPlayer.start_session()

        ProblemModel.load_data()

        response: Union[ResponseType, None] = None
        for round_number in range(LingalgPlayer.NUMBER_OF_ROUNDS):
            response = Rest.play_round(
                LingalgPlayer.SESSION_ID,
                {
                    "day": round_number,
                    "movements": LingalgPlayer.moves,
                },
            )

            demands: List[Demand] = map_demand_type_to_demand(response["demand"])

            ProblemModel.load_demands(demands)
            ProblemModel.process_data()

            for index in range(len(ProblemModel.demands)):
                ProblemModel.process_demand(ProblemModel.demands[index])

            LingalgPlayer.moves = ProblemModel.moves

        Rest.end_session()
        return response
