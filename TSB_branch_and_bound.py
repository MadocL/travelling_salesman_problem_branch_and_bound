from ortools.linear_solver import pywraplp
import random
from copy import deepcopy
from time import time

MAX_ = 999999


def compute(costs):
    # !------------- GOOGLE'S CODE -------------

    # Data
    num_workers = len(costs)
    num_tasks = len(costs[0])

    # Solver
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SCIP")

    if not solver:
        return

    # Variables
    # x[i, j] is an array of 0-1 variables, which will be 1
    # if worker i is assigned to task j.
    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i, j] = solver.IntVar(0, 1, "")

    # Constraints
    # Each worker is assigned to at most 1 task.
    for i in range(num_workers):
        solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1)

    # Each task is assigned to exactly one worker.
    for j in range(num_tasks):
        solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1)

    # Objective
    objective_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            objective_terms.append(costs[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # Solve
    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    solution_tuples = []

    # print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f"Total cost = {solver.Objective().Value()}\n")
        for i in range(num_workers):
            for j in range(num_tasks):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if x[i, j].solution_value() > 0.5:
                    solution_tuples.append((i, j))
                    print(f"Worker {i} assigned to task {j}." + f" Cost: {costs[i][j]}")
    else:
        print("No solution found.")

    # !------------- END OF GOOGLE'S CODE (except 'solution_tuples' list few lines above) -------------

    chains = merge_solutions_tuple_into_chains(solution_tuples)

    # "suppression" d'un arc de la chaine la plus courte dans le cas où il y a plusieurs chaînes
    # et appel récursif de la fonction "compute"
    if len(chains) > 1:
        print("Multiple chains found:")
        print(chains)
        min_chain = chains[0]
        for c in chains:
            if len(c) < len(min_chain):
                min_chain = c

        costs[min_chain[0][0]][min_chain[0][1]] = MAX_
        print(f"Costs updated: {costs}")
        compute(costs)
    else:
        print("Final chain found:")
        print([(element[0]+1, element[1]+1) for element in chains[0]])


def merge_solutions_tuple_into_chains(solution_tuples: list[tuple]) -> list[list[tuple]]:

    # create chains from solution tuples
    chains: list[list[tuple]] = []
    for s in solution_tuples:
        if not chains:
            chains.append([s])
        else:
            for c in chains:
                if c[0][0] == s[1]:
                    c.insert(0, s)
                    break

                if c[-1][1] == s[0]:
                    c.append(s)
                    break
            else:
                chains.append([s])

    # merge chains
    k = 0
    new_chains = deepcopy(chains)

    while k == 0 or new_chains != chains:
        if k != 0:
            chains = deepcopy(new_chains)

        for i in range(len(chains)):
            for j in range(i+1, len(chains)):
                if chains[i][0][0] == chains[j][-1][1]:
                    new_chains[j].extend(new_chains[i])
                    new_chains.pop(i)
                    break
                if chains[i][-1][1] == chains[j][0][0]:
                    new_chains[i].extend(new_chains[j])
                    new_chains.pop(j)
                    break
            if chains != new_chains:
                break
        k += 1

    return chains


def generate_costs(n: int):
    costs = []
    for _ in range(n):
        costs.append([random.randint(1, 10) for _ in range(n)])

    for i in range(n):
        costs[i][i] = MAX_

    print(f"Generated costs: {costs}")
    return costs


# calculate the average time based in 100 runs with a different costs matrix for each run
def calc_time(n: int):
    sum_ = 0
    for _ in range(100):
        start_time = time()
        compute(generate_costs(n=n))
        sum_ += time() - start_time
    print(sum_/100)


if __name__ == "__main__":
    # calc_time(n=20)

    costs = generate_costs(n=20)
    compute(deepcopy(costs))
    print(f"\nOriginal costs: {costs}")
