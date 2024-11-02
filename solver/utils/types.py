from typing import TypedDict
from dataclasses import dataclass

class Connection(TypedDict):
    id: str
    from_id: str
    to_id: str
    distance: int
    lead_time_days: int
    connection_type: str
    max_capacity: int

@dataclass
class Customer:
    id: str
    name: str
    max_input: int
    over_input_penalty: float
    late_delivery_penalty: float
    early_delivery_penalty: float
    node_type: str

@dataclass
class Demand:
    id: str
    customer_id: str
    quantity: int
    post_day: int
    start_delivery_day: int
    end_delivery_day: int

@dataclass
class Refinery:
    id: str
    name: str
    capacity: int
    max_output: int
    production: int
    overflow_penalty: float
    underflow_penalty: float
    over_output_penalty: float
    production_cost: float
    production_co2: float
    initial_stock: int
    node_type: str

@dataclass
class Tank:
    id: str
    name: str
    capacity: int
    max_input: int
    max_output: int
    overflow_penalty: float
    underflow_penalty: float
    over_input_penalty: float
    over_output_penalty: float
    initial_stock: int
    node_type: str