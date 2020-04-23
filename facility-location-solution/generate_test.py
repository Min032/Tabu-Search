import random
import math

'''
    Script asks for input of number of storages, number of customers, map size
    (map is of square shape) and the problem index. Problem index indicates
    the index that will be appended to corresponding generated files.

    For problem index = 1, program generates 2 files:
    loc1.txt:
        First line contains two integers, number of storages (S) and
        number of customers (C).
        Following S lines contain coordinates of the storages.
        After that, following C lines contain coordinates of customers.

        num_of_storages num_of_customers
        sx1 sy1
        sx2 sy2
        ...
        sxS syS
        cx1 cy1
        cx2 cy2
        ...
        cxC cyC

    costs1.txt:
        First line contains two integers, number of storages (S) and
        number of customers (C).
        Following S lines contain two integers, storage capacity and cost of
        establishing a storage. These values are hardcoded.
        After that, following 2*C lines are:
        demand_of_storage
        list of costs to each storage

        num_of_storages num_of_customers
        cap1 cost1
        cap2 cost2
        ...
        capS costS
        demand1
        cost_c1_to_s1 cost_c1_to_s2 ... cost_c1_to_sS
        demand2
        cost_c2_to_s1 cost_c2_to_s2 ... cost_c2_to_sS
        ...
        demandC
        cost_cC_to_s1 cost_cC_to_s2 ... cost_cC_to_sS

    Currently, capacity is hardcoded to 1000.
    Storage costs (cost of setting up a storage) is either 2000, for storages
    in the center of the city (the inner square of size map_size/2), or 1000 otherwise.
    Storage location is (x,y), and both coordinates are random on (0, map_size)

    Customer demands can vary anywhere from 50 to 100.
    Customer location is (x,y), and both coordinates are random on (0, map_size)
    Customer costs for each storage will be evaluated as Euclidean distance from
    customer location to storage location.
'''

def in_city_center(map_size, location):
    center_boundary = map_size / 4
    if (location[0] > center_boundary and \
            location[0] < map_size - center_boundary and \
            location[1] > center_boundary and \
            location[1] < map_size - center_boundary):
        return True
    else:
        return False

def generate_locations(num_facilities, map_size):
    locations = []
    for i in range(num_facilities):
        location = (random.randint(1, map_size), random.randint(1, map_size))
        locations.append(location)
    return locations

def euclidean_distance(loc1, loc2):
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

def main():
    num_storages = int(input("Number of storages: "))
    num_customers = int(input("Number of customers: "))
    map_size = int(input("Map size: "))
    problem_index = int(input("Problem index: "))
    storage_size = int(input("Storage size:"))
    storage_cost_center = int(input("Cost of storage in city center: "))
    storage_cost_normal = int(input("Cost of storage otherwise: "))

    storage_locations = generate_locations(num_storages, map_size)
    customers_locations = generate_locations(num_customers, map_size)

    with open("input/loc{}.txt".format(problem_index), "w") as locations_file:
        locations_file.write("{} {}\n".format(num_storages, num_customers))
        locations_file.write("{}\n".format(map_size))
        
        for i in range(num_storages):
            locations_file.write("{} {}\n".format(storage_locations[i][0], \
                storage_locations[i][1]))

        for i in range(num_customers):
            locations_file.write("{} {}\n".format(customers_locations[i][0], \
                customers_locations[i][1]))

    customer_costs = []
    for i in range(num_customers):
        costs_of_current = [euclidean_distance(customers_locations[i], j) \
                for j in storage_locations]
        customer_costs.append(costs_of_current)

    with open("input/test{}.txt".format(problem_index), "w") as output:
        output.write("{} {}\n".format(num_storages, num_customers))

        for i in range(num_storages):
            if(in_city_center(map_size, storage_locations[i])):
                output.write("{} {}\n".format(storage_size, storage_cost_center))
            else:
                output.write("{} {}\n".format(storage_size, storage_cost_normal))

        for i in range(num_customers):
            output.write("{}\n".format(random.randint(50, 100)))
            output.write(' '.join(map(str, customer_costs[i])))
            output.write('\n')

if __name__ == '__main__':
    main()
