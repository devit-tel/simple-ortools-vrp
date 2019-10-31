"""Vehicles Routing Problem (VRP)."""
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

import model
import plot


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}km\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}km'.format(max_route_distance))


def create_data_model():
    """Stores the data for the problem."""

    # Prepare data load from files
    destinationLatList, destinationLngList, destinationLocationNames = model.loadDestinationLocations()
    driverLatList, driverLngList, driverLocationNames = model.loadRandomDrivers()
    driverCount = len(driverLatList)

    # Initial model
    data = {}
    data['distance_matrix'] = model.getDistanceMatrix(
        driverLatList+destinationLatList, driverLngList+destinationLngList)
    data['num_vehicles'] = driverCount
    data['depot'] = 0

    # Set config multiple depot
    data['starts'] = []
    data['ends'] = []
    for i in range(driverCount):
        data['starts'].append(i)
        data['ends'].append(i)

    # Variable for plot
    allLatitudes = driverLatList+destinationLatList
    allLongitudes = driverLngList+destinationLngList
    allLocationNames = driverLocationNames+destinationLocationNames

    return data, allLatitudes, allLongitudes, allLocationNames


def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data, allLats, allLngs, AllLocationNames = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['starts'], data['ends'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)

        # Plot solution to graph
        driverRoutes, driverDistances = model.getDriverRouteListFromSolution(
            data, manager, routing, solution)
        plot.plotRouteResult(
            allLats, allLngs, AllLocationNames, driverRoutes, driverDistances)


if __name__ == '__main__':
    main()
