import uuid
from typing import List

from solver.api_interface import DemandType
from solver.utils.types import Demand


def map_demand_type_to_demand(demands_type: List[DemandType]) -> List[Demand]:
    new_demands: List[Demand] = [
        Demand(
            str(uuid.uuid4()),
            demand_type["customerId"],
            demand_type["amount"],
            demand_type["postDay"],
            demand_type["startDay"],
            demand_type["endDay"],
        )
        for demand_type in demands_type
    ]

    return new_demands
