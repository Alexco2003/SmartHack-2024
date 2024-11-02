# How to read CSV

```python
from utils.reader import read_connections, read_customers, read_demands, read_refineries, read_tanks 

connections = read_connections('data/connections.csv')
print(connections) 

customers = read_customers('data/customers.csv')
print(customers) 

demands = read_demands('data/demands.csv')
print(demands) 

refineries = read_refineries('data/refineries.csv')
print(refineries) 

tanks = read_tanks('data/tanks.csv')
print(tanks)
```