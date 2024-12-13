import numpy as np
import pandas as pd

# Define a function to read the transportation problem parameters from an external file
def read_transportation_problem(file_path):
    """Reads the transportation problem from a CSV file."""
    data = pd.read_csv(file_path)
    
    # Extract supply and demand
    supply = data.iloc[1:, 0].astype(float).to_numpy()  # First column: supply (skip header)
    demand = data.iloc[0, 1:].astype(float).to_numpy()  # First row: demand (skip header)
    
    # Extract cost matrix
    cost_matrix = data.iloc[1:, 1:].astype(float).to_numpy()  # Remaining rows and columns: cost matrix
    
    return supply, demand, cost_matrix

# Northwest corner rule implementation
def northwest_corner_rule(supply, demand):
    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))
    i, j = 0, 0

    while i < m and j < n:
        allocation[i, j] = min(supply[i], demand[j])
        supply[i] -= allocation[i, j]
        demand[j] -= allocation[i, j]

        if supply[i] == 0:
            i += 1
        elif demand[j] == 0:
            j += 1

    return allocation

# Minimum cost method implementation
def minimum_cost_method(supply, demand, cost_matrix):
    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))
    cost_flattened = [(cost_matrix[i, j], i, j) for i in range(m) for j in range(n)]
    cost_flattened.sort()  # Sort by cost

    for cost, i, j in cost_flattened:
        if supply[i] > 0 and demand[j] > 0:
            allocation[i, j] = min(supply[i], demand[j])
            supply[i] -= allocation[i, j]
            demand[j] -= allocation[i, j]

    return allocation

# Minimum Row Cost method implementation
def minimum_row_cost_method(supply, demand, cost_matrix):
    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))

    for i in range(m):
        while supply[i] > 0:
            valid_costs = [(cost_matrix[i, j], j) for j in range(n) if demand[j] > 0]
            if not valid_costs:
                break
            _, j = min(valid_costs)
            allocation[i, j] = min(supply[i], demand[j])
            supply[i] -= allocation[i, j]
            demand[j] -= allocation[i, j]

    return allocation

# Vogel's approximation method implementation
def vogels_approximation_method(supply, demand, cost_matrix):
    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))

    while np.sum(supply) > 0 and np.sum(demand) > 0:
        row_penalties = []
        col_penalties = []

        for i in range(m):
            if supply[i] > 0:
                valid_costs = [cost_matrix[i, j] for j in range(n) if demand[j] > 0]
                if len(valid_costs) > 1:
                    sorted_costs = sorted(valid_costs)
                    row_penalties.append((sorted_costs[1] - sorted_costs[0], i))
                else:
                    row_penalties.append((float('inf'), i))
            else:
                row_penalties.append((float('inf'), i))

        for j in range(n):
            if demand[j] > 0:
                valid_costs = [cost_matrix[i, j] for i in range(m) if supply[i] > 0]
                if len(valid_costs) > 1:
                    sorted_costs = sorted(valid_costs)
                    col_penalties.append((sorted_costs[1] - sorted_costs[0], j))
                else:
                    col_penalties.append((float('inf'), j))
            else:
                col_penalties.append((float('inf'), j))

        max_row_penalty = max(row_penalties, key=lambda x: x[0])
        max_col_penalty = max(col_penalties, key=lambda x: x[0])

        if max_row_penalty[0] >= max_col_penalty[0]:
            i = max_row_penalty[1]
            valid_costs = [(cost_matrix[i, j], j) for j in range(n) if demand[j] > 0]
            _, j = min(valid_costs)
        else:
            j = max_col_penalty[1]
            valid_costs = [(cost_matrix[i, j], i) for i in range(m) if supply[i] > 0]
            _, i = min(valid_costs)

        allocation[i, j] = min(supply[i], demand[j])
        supply[i] -= allocation[i, j]
        demand[j] -= allocation[i, j]

    return allocation

# Main function to test with the given file path
if __name__ == "__main__":
    file_path = "C:\\Users\\nicol\\Downloads\\Optimi4.csv"
    supply, demand, cost_matrix = read_transportation_problem(file_path)

    print("Supply:", supply)
    print("Demand:", demand)
    print("Cost Matrix:")
    print(cost_matrix)

    while True:
        print("\nChoose a method to solve the transportation problem:")
        print("1. Northwest Corner Rule")
        print("2. Minimum Cost Method")
        print("3. Minimum Row Cost Method")
        print("4. Vogel's Approximation Method")
        print("5. Exit")

        choice = int(input("Enter your choice (1-5): "))

        if choice == 1:
            allocation = northwest_corner_rule(supply.copy(), demand.copy())
            method = "Northwest Corner Rule"
        elif choice == 2:
            allocation = minimum_cost_method(supply.copy(), demand.copy(), cost_matrix.copy())
            method = "Minimum Cost Method"
        elif choice == 3:
            allocation = minimum_row_cost_method(supply.copy(), demand.copy(), cost_matrix.copy())
            method = "Minimum Row Cost Method"
        elif choice == 4:
            allocation = vogels_approximation_method(supply.copy(), demand.copy(), cost_matrix.copy())
            method = "Vogel's Approximation Method"
        elif choice == 5:
            print("Exiting the program.")
            break
        else:
            print("Invalid choice! Please try again.")
            continue

        print(f"\nAllocation ({method}):")
        print(allocation)

        another = input("\nWould you like to try another method? (yes/no): ").strip().lower()
        if another != 'yes':
            print("Goodbye!")
            break
