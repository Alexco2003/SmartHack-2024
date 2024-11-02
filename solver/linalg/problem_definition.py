import pulp
from solver.utils.reader import *

PIPELINE_COST_PER_UNIT_DISTANCE = 0.05
TRUCK_COST_PER_UNIT_DISTANCE = 0.42

connections: List[Connection] = read_connections("../../data/connections.csv")
customers: List[Customer] = read_customers("../../data/customers.csv")
tanks: List[Tank] = read_tanks("../../data/tanks.csv")
refineries: List[Refinery] = read_refineries("../../data/refineries.csv")
demands: List[Demand] = read_demands("../../data/demands.csv")
demands = demands[:246]

refineries_ids = [refinery.id for refinery in refineries]
tanks_ids = [tank.id for tank in tanks]
customers_ids = [customer.id for customer in customers]

production_cost = {refinery.id: refinery.production_cost for refinery in refineries}
production_co2 = {refinery.id: refinery.production_co2 for refinery in refineries}

# max output tanks can send
tank_max_outputs = {tank.id: min(tank.max_output, tank.initial_stock) for tank in tanks}
refinery_max_outputs = {refinery.id: min(refinery.max_output, refinery.initial_stock) for refinery in refineries}

transport_cost = {}

# Create a dictionary to hold valid connections
valid_connections = {}

for connection in connections:
    from_id = connection["from_id"]
    to_id = connection["to_id"]
    distance = connection["distance"]
    connection_type = connection["connection_type"]

    if connection_type == "PIPELINE":
        transport_cost[(from_id, to_id)] = distance * PIPELINE_COST_PER_UNIT_DISTANCE
    elif connection_type == "TRUCK":
        transport_cost[(from_id, to_id)] = distance * TRUCK_COST_PER_UNIT_DISTANCE

    valid_connections[(from_id, to_id)] = connection["max_capacity"]

# model
model = pulp.LpProblem("Fuel_Delivery_Optimization", pulp.LpMinimize)

# decision variables
# Stage 1: Transport from refinery to tank
x_refinery_to_tank = pulp.LpVariable.dicts(
    "x_refinery_to_tank",
    [
        (refinery.id, tank.id)
        for refinery in refineries
        for tank in tanks
        if (refinery.id, tank.id) in valid_connections
    ],
    lowBound=0,
    cat="Integer",
)

# Stage 2: Transport from tank to customer
x_tank_to_customer = pulp.LpVariable.dicts(
    "x_tank_to_customer",
    [
        (tank.id, demand.customer_id)
        for tank in tanks
        for demand in demands
        if (tank.id, demand.customer_id) in valid_connections
    ],
    lowBound=0,
    cat="Integer",
)

threshold = 100
for demand in demands:
    customer_id = demand.customer_id
    demand_id = demand.id
    quantity_needed = demand.quantity

    # Ensure that total delivery from all tanks meets demand within a threshold range
    model += (
        pulp.lpSum(
            [x_tank_to_customer[tank.id, customer_id] for tank in tanks if (tank.id, customer_id) in valid_connections]
        )
        >= quantity_needed - threshold,
        f"Demand_Fulfillment_{customer_id}_{demand_id}_Min",
    )

    model += (
        pulp.lpSum(
            [x_tank_to_customer[tank.id, customer_id] for tank in tanks if (tank.id, customer_id) in valid_connections]
        )
        <= quantity_needed + threshold,
        f"Demand_Fulfillment_{customer_id}_{demand_id}_Max",
    )

for tank in tanks:
    model += (
        pulp.lpSum(
            [
                x_tank_to_customer[tank.id, demand.customer_id]
                for demand in demands
                if (tank.id, demand.customer_id) in valid_connections
            ]
        )
        <= tank_max_outputs[tank.id],
        f"Tank_Max_Outputs_{tank.id}",
    )

for refinery in refineries:
    model += (
        pulp.lpSum(
            [x_refinery_to_tank[refinery.id, tank.id] for tank in tanks if (refinery.id, tank.id) in valid_connections]
        )
        <= refinery_max_outputs[refinery.id],
        f"Refinery_Max_Outputs_{refinery.id}",
    )

model += (
    # Transport cost for Stage 1: refinery to tank
    pulp.lpSum(
        [
            transport_cost[refinery.id, tank.id] * x_refinery_to_tank[refinery.id, tank.id]
            for refinery in refineries
            for tank in tanks
            if (refinery.id, tank.id) in transport_cost
        ]
    )
    # Transport cost for Stage 2: tank to customer
    + pulp.lpSum(
        [
            transport_cost[tank.id, demand.customer_id] * x_tank_to_customer[tank.id, demand.customer_id]
            for tank in tanks
            for demand in demands
            if (tank.id, demand.customer_id) in transport_cost
        ]
    ),  # Example objective term for production cost
    "Total_Cost",
)

model.solve()

print("Status:", pulp.LpStatus[model.status])
for v in model.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)

print("Total Cost = ", pulp.value(model.objective))
