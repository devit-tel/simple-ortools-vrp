import random

import geopy.distance as calDiff
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import numpy as np
import pandas


# Load drivers data from file csv
def loadDrivers():
    drivers = pandas.read_csv('sample_data/drivers.csv')
    locationNames = []
    latList = []
    lngList = []

    # for index in range(len(drivers)):
    #     latList.append(float(drivers["lat"][index]))
    #     lngList.append(float(drivers["lng"][index]))

    return latList, lngList, locationNames


def loadRandomDrivers():
    drivers = pandas.read_csv('sample_data/drivers.csv')
    locationNames = []
    latList = []
    lngList = []

    # Number of driver
    driverCount = 4
    driverList = []

    while len(driverList) != driverCount:
        index = random.randint(1, len(drivers)-1)
        if index in driverList:
            continue

        latList.append(float(drivers["lat"][index]))
        lngList.append(float(drivers["lng"][index]))
        locationNames.append(drivers["name"][index])

        driverList.append(index)

    return latList, lngList, locationNames


# Load locations data from file csv
def loadDestinationLocations():
    destinations = pandas.read_csv('sample_data/destinations.csv')
    locationNames = []
    latList = []
    lngList = []

    for index in range(len(destinations)):
        latList.append(float(destinations["lat"][index]))
        lngList.append(float(destinations["lng"][index]))
        locationNames.append(destinations["name"][index])

    return latList, lngList, locationNames


# Create distance matrix from lat,lng list
def getDistanceMatrix(latList, lngList):
    # validate input
    lenLocations = len(latList)
    if lenLocations != len(lngList):
        return

    # Create empty array dimension
    matrix = np.zeros(shape=(lenLocations, lenLocations))

    for i in range(lenLocations):
        for j in range(lenLocations):
            if j == i:
                # Ignore calculate distance when same location
                continue

            if matrix[i, j] > 0:
                # Ignore calculate dupplicate
                continue

            # Calculate distance
            origin = (latList[i], lngList[i])
            destination = (latList[j], lngList[j])

            distance = calDiff.distance(origin, destination).km
            matrix[i, j] = distance
            matrix[j, i] = distance

    return matrix


# Get driver routes from result solution
def getDriverRouteListFromSolution(data, manager, routing, solution):
    driverRoutes = []
    driverRouteDistances = []
    for vehicle_id in range(data['num_vehicles']):
        routes = []
        route_distance = 0

        index = routing.Start(vehicle_id)

        while not routing.IsEnd(index):
            routes.append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)

        driverRouteDistances.append(route_distance)
        driverRoutes.append(routes)
    return driverRoutes, driverRouteDistances
