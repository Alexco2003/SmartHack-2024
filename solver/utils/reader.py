import csv
from typing import List

from solver.utils.types import Connection, Customer, Demand, Refinery, Tank


def read_connections(file_path: str) -> List[Connection]:
    connections = []
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            connection = Connection(
                id=row['id'],
                from_id=row['from_id'],
                to_id=row['to_id'],
                distance=int(row['distance']),
                lead_time_days=int(row['lead_time_days']),
                connection_type=row['connection_type'],
                max_capacity=int(row['max_capacity']),
                current_capacity=0
            )
            connections.append(connection)
    return connections


def read_customers(file_path: str) -> List[Customer]:
    customers = []
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            customer = Customer(
                id=row["id"],
                name=row["name"],
                max_input=int(row["max_input"]),
                over_input_penalty=float(row["over_input_penalty"]),
                late_delivery_penalty=float(row["late_delivery_penalty"]),
                early_delivery_penalty=float(row["early_delivery_penalty"]),
                node_type=row["node_type"],
            )
            customers.append(customer)
    return customers


def read_demands(file_path: str) -> List[Demand]:
    demands = []
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            demand = Demand(
                id=row["id"],
                customer_id=row["customer_id"],
                quantity=int(row["quantity"]),
                post_day=int(row["post_day"]),
                start_delivery_day=int(row["start_delivery_day"]),
                end_delivery_day=int(row["end_delivery_day"]),
            )
            demands.append(demand)
    return demands


def read_refineries(file_path: str) -> List[Refinery]:
    refineries = []
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            refinery = Refinery(
                id=row['id'],
                name=row['name'],
                capacity=int(row['capacity']),
                max_output=int(row['max_output']),
                production=int(row['production']),
                overflow_penalty=float(row['overflow_penalty']),
                underflow_penalty=float(row['underflow_penalty']),
                over_output_penalty=float(row['over_output_penalty']),
                production_cost=float(row['production_cost']),
                production_co2=float(row['production_co2']),
                initial_stock=int(row['initial_stock']),
                node_type=row['node_type'],
                current_stock=int(row['initial_stock'])
            )
            refineries.append(refinery)
    return refineries


def read_tanks(file_path: str) -> List[Tank]:
    tanks = []
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tank = Tank(
                id=row['id'],
                name=row['name'],
                capacity=int(row['capacity']),
                max_input=int(row['max_input']),
                max_output=int(row['max_output']),
                overflow_penalty=float(row['overflow_penalty']),
                underflow_penalty=float(row['underflow_penalty']),
                over_input_penalty=float(row['over_input_penalty']),
                over_output_penalty=float(row['over_output_penalty']),
                initial_stock=int(row['initial_stock']),
                node_type=row['node_type'],
                current_stock=int(row['init
            )
            tanks.append(tank)
    return tanks
