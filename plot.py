import sys

import matplotlib as matplotlib
import matplotlib.pyplot as plt


def plotRouteResult(xlist, ylist, locationNames, driverRoutes, driverDistances):
    # config font
    plt.rcParams['font.sans-serif'] = 'Silom'

    # config size figure
    my_dpi = 96
    plt.figure(figsize=(1500/my_dpi, 900/my_dpi), dpi=my_dpi)

    # plot locations
    plt.plot(xlist, ylist, 'ro')

    # for loop driver list
    for index in range(len(driverRoutes)):
        tempXList = []
        tempYList = []
        totalRouteLoad = 0

        for j in range(len(driverRoutes[index])):
            tempIndex = driverRoutes[index][j]
            plt.annotate("step: %d: %s" % (j, locationNames[tempIndex]), (xlist[tempIndex], ylist[tempIndex]),
                         (xlist[tempIndex]-0.002, ylist[tempIndex]-0.005))

            tempXList.append(xlist[tempIndex])
            tempYList.append(ylist[tempIndex])

        tempXList.append(tempXList[0])
        tempYList.append(tempYList[0])
        plt.plot(tempXList, tempYList, label="%s %d (distance: %d km)" % (locationNames[index],
                                                                          index, driverDistances[index]))

    # display
    plt.legend(title="VRP with Multiple Depot (total distance : %d)" %
               (sum(driverDistances)))
    plt.ylabel('VRP with Multiple Depot')
    plt.show()
