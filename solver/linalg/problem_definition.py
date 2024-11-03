import os

import pulp
from solver.api_interface import MovementType
from solver.utils.reader import *
from solver.utils.regex import extract_ids


class ProblemModel:
    PIPELINE_COST_PER_UNIT_DISTANCE = 0.05
    TRUCK_COST_PER_UNIT_DISTANCE = 0.42
    DISTANCE_FROM_QUANTITY_NEEDED = 100

    connections: List[Connection] = []
    customers: List[Customer] = []
    tanks: List[Tank] = []
    refineries: List[Refinery] = []
    demands: List[Demand] = []
    current_demand: List[Demand] = []

    valid_connections = {}

    model = None
    x_tank_to_customer = {}
    x_refinery_to_tank = {}

    tank_max_outputs = {}
    refinery_max_outputs = {}

    transport_cost = {}
    sent_units = {}

    TOTAL_COST = 0

    mapped_connection = {}
    moves: List[MovementType] = []

    @staticmethod
    def get_path(name: str) -> str:
        return os.path.join(os.getcwd(), "../", "data", name)

    @staticmethod
    def load_data() -> None:
        ProblemModel.connections = read_connections(ProblemModel.get_path("connections.csv"))
        ProblemModel.customers = read_customers(ProblemModel.get_path("customers.csv"))
        ProblemModel.tanks = read_tanks(ProblemModel.get_path("tanks.csv"))
        ProblemModel.refineries = read_refineries(ProblemModel.get_path("refineries.csv"))
        # ProblemModel.demands = read_demands("../../data/demands.csv")

    @staticmethod
    def load_demands(demands: List[Demand]) -> None:
        ProblemModel.demands = demands

    @staticmethod
    def process_data() -> None:
        ProblemModel.refineries_ids = [refinery.id for refinery in ProblemModel.refineries]
        ProblemModel.tanks_ids = [tank.id for tank in ProblemModel.tanks]
        ProblemModel.customers_ids = [customer.id for customer in ProblemModel.customers]

        # max output tanks can send
        ProblemModel.tank_max_outputs = {
            tank.id: min(tank.max_output, tank.initial_stock) for tank in ProblemModel.tanks
        }
        ProblemModel.refinery_max_outputs = {
            refinery.id: min(refinery.max_output, refinery.initial_stock) for refinery in ProblemModel.refineries
        }

        for tank in ProblemModel.tanks:
            ProblemModel.sent_units[tank.id] = 0

        for refinery in ProblemModel.refineries:
            ProblemModel.sent_units[refinery.id] = 0

        ProblemModel.transport_cost = {}

        # Create a dictionary to hold valid connections
        ProblemModel.valid_connections = {}

        for connection in ProblemModel.connections:
            from_id = connection["from_id"]
            to_id = connection["to_id"]
            distance = connection["distance"]
            connection_type = connection["connection_type"]

            if connection_type == "PIPELINE":
                ProblemModel.transport_cost[(from_id, to_id)] = distance * ProblemModel.PIPELINE_COST_PER_UNIT_DISTANCE
            elif connection_type == "TRUCK":
                ProblemModel.transport_cost[(from_id, to_id)] = distance * ProblemModel.TRUCK_COST_PER_UNIT_DISTANCE

            ProblemModel.valid_connections[(from_id, to_id)] = connection["max_capacity"]
            ProblemModel.mapped_connection[(from_id, to_id)] = connection["id"]

    @staticmethod
    def build_model() -> None:
        # model
        ProblemModel.model = pulp.LpProblem("Fuel_Delivery_Optimization", pulp.LpMinimize)

    @staticmethod
    def add_decision_variables() -> None:
        # decision variables
        # Stage 1: Transport from refinery to tank
        ProblemModel.x_refinery_to_tank = pulp.LpVariable.dicts(
            "x_refinery_to_tank",
            [
                (refinery.id, tank.id)
                for refinery in ProblemModel.refineries
                for tank in ProblemModel.tanks
                if (refinery.id, tank.id) in ProblemModel.valid_connections
            ],
            lowBound=0,
            cat="Integer",
        )

        # Stage 2: Transport from tank to customer
        ProblemModel.x_tank_to_customer = pulp.LpVariable.dicts(
            "x_tank_to_customer",
            [
                (tank.id, demand.customer_id)
                for tank in ProblemModel.tanks
                for demand in ProblemModel.current_demand
                if (tank.id, demand.customer_id) in ProblemModel.valid_connections
            ],
            lowBound=0,
            cat="Integer",
        )

    @staticmethod
    def add_constraints() -> None:
        for demand in ProblemModel.current_demand:
            customer_id = demand.customer_id
            demand_id = demand.id
            quantity_needed = demand.quantity

            # Ensure that total delivery from all tanks meets demand within a threshold range
            ProblemModel.model += (
                pulp.lpSum(
                    [
                        ProblemModel.x_tank_to_customer[tank.id, customer_id]
                        for tank in ProblemModel.tanks
                        if (tank.id, customer_id) in ProblemModel.valid_connections
                    ]
                )
                >= quantity_needed - ProblemModel.DISTANCE_FROM_QUANTITY_NEEDED,
                f"Demand_Fulfillment_{customer_id}_{demand_id}_Min",
            )

            ProblemModel.model += (
                pulp.lpSum(
                    [
                        ProblemModel.x_tank_to_customer[tank.id, customer_id]
                        for tank in ProblemModel.tanks
                        if (tank.id, customer_id) in ProblemModel.valid_connections
                    ]
                )
                <= quantity_needed + ProblemModel.DISTANCE_FROM_QUANTITY_NEEDED,
                f"Demand_Fulfillment_{customer_id}_{demand_id}_Max",
            )

        for tank in ProblemModel.tanks:
            ProblemModel.model += (
                pulp.lpSum(
                    [
                        ProblemModel.x_tank_to_customer[tank.id, demand.customer_id]
                        for demand in ProblemModel.current_demand
                        if (tank.id, demand.customer_id) in ProblemModel.valid_connections
                    ]
                )
                <= ProblemModel.tank_max_outputs[tank.id] - ProblemModel.sent_units[tank.id],
                f"Tank_Max_Outputs_{tank.id}",
            )

        for refinery in ProblemModel.refineries:
            ProblemModel.model += (
                pulp.lpSum(
                    [
                        ProblemModel.x_refinery_to_tank[refinery.id, tank.id]
                        for tank in ProblemModel.tanks
                        if (refinery.id, tank.id) in ProblemModel.valid_connections
                    ]
                )
                <= ProblemModel.refinery_max_outputs[refinery.id] - ProblemModel.sent_units[refinery.id],
                f"Refinery_Max_Outputs_{refinery.id}",
            )

        # at least one move
        ProblemModel.model += (
            pulp.lpSum(ProblemModel.x_refinery_to_tank.values()) + pulp.lpSum(ProblemModel.x_tank_to_customer.values())
            >= 1,
            "At_Least_One_Move",
        )

    @staticmethod
    def add_function_objective() -> None:
        ProblemModel.model += (
            # Transport cost for Stage 1: refinery to tank
            pulp.lpSum(
                [
                    ProblemModel.transport_cost[refinery.id, tank.id]
                    * ProblemModel.x_refinery_to_tank[refinery.id, tank.id]
                    for refinery in ProblemModel.refineries
                    for tank in ProblemModel.tanks
                    if (refinery.id, tank.id) in ProblemModel.transport_cost
                ]
            )
            # Transport cost for Stage 2: tank to customer
            + pulp.lpSum(
                [
                    ProblemModel.transport_cost[tank.id, demand.customer_id]
                    * ProblemModel.x_tank_to_customer[tank.id, demand.customer_id]
                    for tank in ProblemModel.tanks
                    for demand in ProblemModel.current_demand
                    if (tank.id, demand.customer_id) in ProblemModel.transport_cost
                ]
            ),  # Example objective term for production cost
            "Total_Cost",
        )

    @staticmethod
    def solve() -> None:
        ProblemModel.model.solve()

    @staticmethod
    def display() -> None:
        print("Status:", pulp.LpStatus[ProblemModel.model.status])
        for v in ProblemModel.model.variables():
            if v.varValue > 0:
                print(v.name, "=", v.varValue)

        print("Total Cost = ", pulp.value(ProblemModel.model.objective))

    @staticmethod
    def produce_refinery() -> None:
        ProblemModel.refinery_max_outputs = {
            refinery.id: min(refinery.max_output, refinery.initial_stock) for refinery in ProblemModel.refineries
        }

        refinery_max_outputs_copy = {
            refinery.id: min(refinery.max_output, ProblemModel.refinery_max_outputs[refinery.id] + refinery.production)
            for refinery in ProblemModel.refineries
        }

        ProblemModel.refinery_max_outputs = refinery_max_outputs_copy

    @staticmethod
    def process_demand(demand: Demand) -> None:
        ProblemModel.current_demand = [demand]

        ProblemModel.update_model()
        ProblemModel.solve()

        for v in ProblemModel.model.variables():
            ids = extract_ids(v.name)
            value = v.varValue if v.varValue >= 0 else 0  # TODO: try abs

            if value == 0:
                continue

            # replace _ to -
            for i in range(len(ids)):
                ids[i] = ids[i].replace("_", "-")

            if v.name[:18] == "x_tank_to_customer":
                ProblemModel.sent_units[ids[0]] += value
            elif v.name[:18] == "x_refinery_to_tank":
                ProblemModel.sent_units[ids[0]] += value

                diff = ProblemModel.sent_units[ids[1]] - value
                if diff < 0:
                    diff = 0
                ProblemModel.sent_units[ids[1]] = diff

            ProblemModel.moves.append(
                {"connectionId": ProblemModel.mapped_connection[(ids[0], ids[1])], "amount": value}
            )

        ProblemModel.TOTAL_COST += pulp.value(ProblemModel.model.objective)
        ProblemModel.produce_refinery()
        # ProblemModel.display()

    @staticmethod
    def update_model() -> None:
        ProblemModel.build_model()
        ProblemModel.add_decision_variables()
        ProblemModel.add_constraints()
        ProblemModel.add_function_objective()
