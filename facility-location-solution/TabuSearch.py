import random
import math

class TabuSearch:
    def __init__(self):
        self.max_iters = 100
        self.tabu_list_length = 50

        self.num_storages = 0
        self.num_customers = 0
        # Capacities of the storages
        self.capacities = []
        # Costs of opening storages
        self.storage_costs = []
        # Customer demands
        self.demands = []
        # Transportation costs from each storage for each customer
        self.customer_costs = []

    def parse_input(self, filename):
        input = open(filename, "r")
        first_line = input.readline().split()
        self.num_storages = int(first_line[0])
        self.num_customers = int(first_line[1])

        for i in range(self.num_storages):
            line = input.readline().split()
            x = int(line[0])
            y = int(line[1])
            self.capacities.append(x)
            self.storage_costs.append(y)

        for i in range(self.num_customers):
            x = int(input.readline())
            self.demands.append(x)
            costs_line = input.readline().split()
            self.customer_costs.append(list(map(float, costs_line)))

    def generate_initial_solution(self):
        # TODO: Note 1: it should have more True values, otherwise it has difficulties finding
        # a starting point
        # solution = random.choices([True, False], k=num_storages)

        # Note 2: if all are initially True, results are worse.
        # solution = [True for i in range(num_storages)]

        solution = [random.random() for i in range(self.num_storages)]
        solution = [i < 0.75 for i in solution]

        return solution

    def calculate_cost(self, solution, customer_allocation):
        total_cost = 0
        # Cost of opening storages
        for i in range(self.num_storages):
            if solution[i]:
                total_cost += self.storage_costs[i]
        # Cost of transport
        for i in range(self.num_customers):
            total_cost += self.customer_costs[i][customer_allocation[i]]

        return total_cost

    # Inner loop - optimizes store allocation
    def find_best_allocation(self, solution):
        min_total_cost = float('inf')
        current_total_cost = 0
        # Customers are keys, their respective storages are values
        customer_allocation = {}

        for i in range(self.max_iters):
            current_capacities = self.capacities.copy()

            # Finding the min transportation distance to a valid storage.
            for i in range(self.num_customers):
                min_transport_cost = float('inf')
                allocated_to = -1

                for j in range(self.num_storages):
                    if solution[j] and self.demands[i] <= current_capacities[j] \
                            and self.customer_costs[i][j] < min_transport_cost:
                        allocated_to = j
                        min_transport_cost = self.customer_costs[i][j]

                # Impossible to find valid storage.
                if allocated_to == -1:
                    return False

                customer_allocation[i] = allocated_to
                current_capacities[allocated_to] -= self.demands[i]

            total_cost = self.calculate_cost(solution, customer_allocation)

            if total_cost < min_total_cost:
                min_total_cost = total_cost

        return min_total_cost

    def is_in_tabu(self, tabu_list, solution):
        for t in tabu_list:
            if solution == t:
                return True
        return False

    def get_random_neighbour(self, solution):
        new_solution = solution.copy()
        invert_index = random.randrange(self.num_storages)
        new_solution[invert_index] = not new_solution[invert_index]
        return new_solution, invert_index

    # Outer loop - optimizes which storages are open
    def find_best_solution(self, solution):
        current_cost = self.find_best_allocation(solution)
        while current_cost == False:
            current_cost = self.find_best_allocation(solution)
        min_cost = current_cost
        best_solution = solution
        tabu_list = []
        tabu_list.append(solution)

        for i in range(self.max_iters):
            solution, invert_index = self.get_random_neighbour(solution)

            if self.is_in_tabu(tabu_list, solution):
                continue

            current_cost = self.find_best_allocation(solution)

            if current_cost and current_cost < min_cost:
                min_cost = current_cost
                best_solution = solution
            else:
                solution[invert_index] = not solution[invert_index]

            if len(tabu_list) >= self.tabu_list_length:
                tabu_list = tabu_list[1:]

            tabu_list.append(solution)

        return best_solution, min_cost


def main():
    problem_index = int(input("Index of the problem you are solving: "))

    tabu = TabuSearch()
    tabu.parse_input('input/test{}.txt'.format(problem_index))

    global_min_cost = float('inf')
    global_best_solution = []

    with open('logs/log{}.txt'.format(problem_index), 'w') as log_file:
        for i in range(100):
            solution = tabu.generate_initial_solution()
            best_solution, min_cost = tabu.find_best_solution(solution)

            if min_cost < global_min_cost:
                log_file.write("{}\n{}\n".format(min_cost, best_solution))
                print(min_cost, '\n', best_solution)
                global_min_cost = min_cost
                global_best_solution = best_solution

    print('-------------------------------------------------------')
    print('Best value:', global_min_cost)
    print('Best solution: ', global_best_solution)

    with open('solutions/sol{}.txt'.format(problem_index), 'w') as output:
        output.write(','.join(map(str, global_best_solution)))

if __name__ == '__main__':
    main()
