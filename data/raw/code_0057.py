#!/usr/bin/env python3

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as np


def create_data_model():
    data = {}

    # Distance matrix (km)
    base_distances = [
        [0, 4, 8, 5, 7],
        [4, 0, 10, 7, 3],
        [8, 10, 0, 6, 9],
        [5, 7, 6, 0, 4],
        [7, 3, 9, 4, 0],
    ]

    # Simulated traffic multiplier (1.0 = normal, >1 = heavy traffic)
    traffic = [
        [1, 1.2, 1.1, 1.3, 1.0],
        [1.2, 1, 1.4, 1.1, 1.3],
        [1.1, 1.4, 1, 1.2, 1.5],
        [1.3, 1.1, 1.2, 1, 1.1],
        [1.0, 1.3, 1.5, 1.1, 1],
    ]

    size = len(base_distances)
    time_matrix = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            time_matrix[i][j] = base_distances[i][j] * traffic[i][j]

    # Delivery priorities (higher = more important)
    priorities = [0, 3, 2, 5, 1]

    data["time_matrix"] = time_matrix.astype(int).tolist()
    data["num_vehicles"] = 2
    data["depot"] = 0
    data["priorities"] = priorities

    return data


def print_solution(data, manager, routing, solution):
    total_time = 0

    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        route_time = 0
        route = []

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_time += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

        route.append(manager.IndexToNode(index))

        print(f"Route for vehicle {vehicle_id}: {route}")
        print(f"Time: {route_time}\n")

        total_time += route_time

    print(f"Total time: {total_time}")


def main():
    data = create_data_model()

    manager = pywrapcp.RoutingIndexManager(
        len(data["time_matrix"]), data["num_vehicles"], data["depot"]
    )

    routing = pywrapcp.RoutingModel(manager)

    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        base_time = data["time_matrix"][from_node][to_node]

        priority_factor = 1 - (data["priorities"][to_node] * 0.05)

        return int(base_time * priority_factor)

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print("No solution found")


if __name__ == "__main__":
    main()