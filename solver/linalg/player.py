from typing import List, Union

from solver.api_interface import MovementType, ResponseType, Rest
from solver.linalg.problem_definition import ProblemModel
from solver.utils.mapper import map_demand_type_to_demand
from solver.utils.types import Demand


class LingalgPlayer:
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
