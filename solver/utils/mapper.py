import uuid
from typing import List

from solver.api_interface import DemandType
from solver.utils.types import Demand


def map_demand_type_to_demand(demands_type: List[DemandType]) -> List[Demand]:
    """Maps a list of `DemandType` objects to a list of `Demand` objects.

    Each `DemandType` object in the input list is used to create a new `Demand` object, with
    a unique ID generated for each `Demand` instance.

    Args:
        demands_type (List[DemandType]): A list of `DemandType` objects

    Returns:
        List[Demand]: A list of `Demand` objects, each corresponding to a `DemandType` object in the input.
    """
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
