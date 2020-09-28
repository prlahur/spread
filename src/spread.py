#!/usr/bin/env python                                                           
# -*- coding: utf-8 -*-

'''
Put description of contents here
'''

import sys
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

# Note that class name starts with capital letter

class Space():
    '''
    The space in which everything takes place.
    '''
    def __init__(self):
        self.min = [0.0, 0.0]
        self.max = [0.0, 0.0]

    def setMinLocation(self, location=list):
        if isinstance(location, list):
            if len(location) == 2:
                self.min = location
            else:
                raise ValueError("Illegal list size")
        else:
            raise TypeError("Not a list")

    def getMinLocation(self):
        return self.min

    def setMaxLocation(self, location=list):
        if isinstance(location, list):
            if len(location) == 2:
                self.max = location
            else:
                raise ValueError("Illegal list size")
        else:
            raise TypeError("Not a list")

    def getMaxLocation(self):
        return self.max

    def getRandomLocation(self):
        location = [random.uniform(self.min[i], self.max[i]) for i in range(2)]
        return location

    def print(self):
        print(self.min, self.max)


class Member():
    '''
    Describe this class
    '''
    def __init__(self):
        self.id = 0
        self.location = [0.0, 0.0]
        self.pace = 10.0

    def setId(self, id=int):
        self.id = id

    def getId(self):
        return self.id

    def setLocation(self, location=list):
        if isinstance(location, list):
            if len(location) == 2:
                self.location = location
            else:
                raise ValueError("Illegal list size")
        else:
            raise TypeError("Not a list")

    def getLocation(self):
        return self.location

    def moveInRandom(self, space=Space):
        for i in range(2):
            self.location[i] = self.location[i] + random.uniform(-self.pace, self.pace)
            self.location[i] = min(self.location[i], space.max[i])
            self.location[i] = max(self.location[i], space.min[i])
        return self.location

    def setPace(self, pace=float):
        self.pace = pace

    def getPace(self):
        return self.pace

    def inSquare(self, distance=float, location=list):
        return inSquare(self.location, distance, location)

    def print(self):
        print(self.id, ":", "%.1f" % self.location[0], "%.1f" % self.location[1])

    def printLocation(self):
        print(self.id, ":", "%.1f" % self.location[0], "%.1f" % self.location[1])



class Population():
    '''
    Population contains members.
    '''
    def __init__(self, size=int):
        '''
        Initialize the population.
        '''
        self.size = size
        self.members = []
        for i in range(size):
            member = Member()
            member.setId(i)
            self.members.append(member)

    def setRandomLocation(self, space=Space):
        [member.setLocation(space.getRandomLocation()) for member in self.members]

    def setRandomPace(self):
        [member.setPace(random.uniform(0.0, 20.0)) for member in self.members]

    def moveInRandom(self, space=Space):
        [member.moveInRandom(space) for member in self.members]

    def print(self):
        '''
        Print out members data: ID and location
        '''
        [member.print() for member in self.members]

    def printLocation(self):
        '''
        Print out location of members
        '''
        [member.printLocation() for member in self.members]

    def printNearbyMembers(self, nearDistance=float):
        nearList = []
        for member in self.members:
            nearList.clear()
            for otherMember in self.members:
                if member != otherMember:
                    otherLocation = otherMember.getLocation()
                    if member.inSquare(nearDistance, otherLocation):
                        nearList.append(otherMember.getId())
            print("Near", member.getId(), ":", nearList)


    
def inSquare(centre=list, distance=float, point=list):
    '''
    Return true if another point is within a given square centred around a point
    '''
    for i in range(2):
        if (point[i] < centre[i] - distance):
            return False
        elif (point[i] > centre[i] + distance):
            return False
    return True



def main():
    '''
    This is the main routine.
    Describe what this does
    '''
    print("Setting up space")
    xmin = 0.0
    xmax = 1000.0
    space = Space()
    space.setMinLocation([xmin, xmin])
    space.setMaxLocation([xmax, xmax])
    space.print()

    populationSize = 30
    print("Setting up population of", populationSize)
    population = Population(populationSize)
    population.setRandomLocation(space)
    population.setRandomPace()
    # population.printLocation()

    # nearDistance = 100.0
    # population.printNearbyMembers(nearDistance)

    # population.moveInRandom()
    # population.printLocation()

    # print("Each member finds other members near it")
    # nearList = []
    # for member in population.members:
    #     nearList.clear()
    #     for otherMember in population.members:
    #         if member != otherMember:
    #             otherLocation = otherMember.getLocation()
    #             if member.inSquare(nearDistance, otherLocation):
    #                 nearList.append(otherMember.getId())
    #     print("Near", member.getId(), ":", nearList)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, aspect=1)
    majorTicks = np.arange(xmin, xmax, 100.0)

    def makeChart(i=int):
        ax.clear()
        ax.set_xlim([0, 1000])
        ax.set_ylim([0, 1000])
        ax.set_aspect('equal')
        # ax.set_autoscale_on(False)

        ax.set_xticks(majorTicks)
        ax.set_yticks(majorTicks)

        ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

        ax.set_title("Location of all members", fontsize=20, verticalalignment='bottom')
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        # scatter.set_data([member.location[0] for member in population.members], 
        #     [member.location[1] for member in population.members])
        ax.scatter([member.location[0] for member in population.members], 
            [member.location[1] for member in population.members],
            c=[member.id for member in population.members], cmap='rainbow')
        population.moveInRandom(space)

    # makeChart()
    animator = ani.FuncAnimation(fig, makeChart, interval=100)

    plt.show()


if (__name__ == "__main__"):
    if sys.version_info[0] == 3:
        main()
    else:
        raise ValueError("Must use Python 3")
