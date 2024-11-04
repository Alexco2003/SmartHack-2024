# SmartHack-2024

<<<<<<< Updated upstream
=======
You can read more about the task [here](/docs/problem.md)

## Approaches

### Linear Optimization

#### Definition

**Linear programming (LP)**, also called **linear optimization**, is a method to achieve the best outcome (such as maximum profit or lowest cost) in a **mathematical model** whose requirements and objective are represented by **linear relationships**.

#### Decision Variables

In a transportation problem, we aim to determine the optimal flow of units from supply nodes to demand nodes. Here, the **decision variables** are the **arcs** connecting these nodes. Specifically, we need to decide the amount of fuel to transport from each refinery to tank storage and from tank storage to customers.

We define separate arcs for the `refinery → tank` and `tank → customer` flows, as they incur different costs per unit distance.

Let:

```math
X_{ij} = \text{the amount of fuel transported from refinery } i \text{ to tank } j
```

```math
X_{jk} = \text{the amount of fuel transported from tank } j \text{ to customer } k
```

These variables represent the quantity of fuel pushed from one node to another in the network.

#### Objective Function

```math
f = \sum{} distance_{ij} * 0.05 + \sum{} distance_{jk} * 0.42 
```

Where:

```math
distance_{ij} \text{ is the distance between refinery } i \text{ and tank storage } j
```

```math
0.05 \text{ is the cost per unit distance for pipeline connections}
```

```math
distance_{jk} \text{ is the distance between tank storage } j \text{ and customer } k
```

```math
0.42 \text{ is the cost per unit distance for truck connections}
```

#### Constraints

```math
\text{demanded quantity} - tolerance <= \sum{} X_{jk} <= \text{demanded quantity} + tolerance
```

Where `tolerance` is empirically set to adjust needs

```math
\sum{} X_{ij} <= \text{maximum } refinery_{i} \text{ output}
```

```math
\sum{} X_{jk} <= \text{maximum } tank_{j} \text{ output}
```

Meaning you can not push more than your current stock or max output

```math
\sum{} X_{ij} + \sum{} X_{jk} > 0
```

And at least one move should be made

### A*

TODO

>>>>>>> Stashed changes
## PIP Dependency Solver

This project requires several Python packages to function correctly. Follow the instructions below to set up your environment and install the necessary dependencies.

### Installing Dependencies

To install all the required Python packages listed in `requirements.txt`, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

### Updating Dependencies

If you add any new packages or make changes to your environment, you can update your `requirements.txt` file with the following command:

> [!WARNING]
> BUT only after running the above command

```bash
pip freeze > requirements.txt
```

Or you can enter them by hand 