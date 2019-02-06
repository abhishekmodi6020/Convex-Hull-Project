#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 15:04:07 2018

@author: harish
"""

import numpy as np

import random
from collections import defaultdict
from math import atan2
from operator import itemgetter
from matplotlib import pyplot as plt
import numpy as np
import time
from collections import defaultdict

def file_to_x_y(filename):
	x_y = []
	x_cord = []
	y_cord = []
	try:
		file = open(filename, 'r')
		no_of_points = int(file.readline())
		for i in file:
			i = i.split()
			i[1] = int(i[1])
			i[2] = int(i[2])
			x_cord.append(i[1])
			y_cord.append(i[2])
			x_y.append((i[1],i[2]))
		file.close()
	except:
		print("Invalid file name")

	return x_y,x_cord,y_cord

def input_generator(no_of_input,x_range_min, x_range_max, y_range_min, y_range_max):
    x_y = []
    x_cord = []
    y_cord = []
    for i in range(0,no_of_input):
        x= random.randint(x_range_min,x_range_max)
        y= random.randint(y_range_min,y_range_max)
        x_y.append((x,y))
        x_cord.append(x)
        y_cord.append(y)

    return x_y,x_cord,y_cord

def orientation(p1,p2,p3):
    ornt = (p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0])
    return ornt    

def convexHull(cords):
    min_cord = min(cords)
    start = min_cord
    convexHull = [start]
    p = start    
    while(True) :
        q = cords[0]
        for r in cords:
            if r == p:
                continue
            if orientation(p,q,r) >= 0:
                q = r
        if q != start:
            convexHull.append(q)
            p = q
        else:
            break

    return convexHull

#plot thehull
def plot(x_cord,y_cord,convex_hull=None):
    
    xs = np.asarray(x_cord)
    ys = np.asarray(y_cord)
    plt.scatter(xs,ys)
    
    if convex_hull != None:
        for i in range(0,len(convex_hull)):
            p1 = convex_hull[i]
            p0 = convex_hull[i-1]
            plt.plot((p0[0],p1[0]),(p0[1],p1[1]),'r')
    plt.title('Convex Hull using Jarvis Scan')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show() 

    return xs,ys   

def onionConvexHull(convex_hull,coord):
    onion_convex = defaultdict(list)
    #convex_hull_update = convex_hull
    onion_convex[0].append(convex_hull)
    i=1
    while(len(coord)>0):
        remain_points =  set(coord) - set(convex_hull)
        #print('coord',remain_points)
        if(len(remain_points) > 0):
            hull_points = convexHull(list(remain_points))
            onion_convex[i].append(hull_points)
            convex_hull = hull_points
            coord = remain_points
            i = i + 1
        else:
            break
    return onion_convex

def plotOnion(onion_convex,x_cord,y_cord):
    xs = np.asarray(x_cord)
    ys = np.asarray(y_cord)
    plt.scatter(xs,ys)
    if convex_hull != None:
        for key, value in onion_convex.items():
            for i in range(0,len(value[0])):
                p1 = onion_convex[key][0][i]
                p0 = onion_convex[key][0][i-1]
                plt.plot((p0[0],p1[0]),(p0[1],p1[1]),'r')
    plt.title('Onion Convex Hull')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show() 

coord,x_cord,y_cord = file_to_x_y('inputfile.txt')
start = time.time()
convex_hull = convexHull(coord)
end = time.time()
time = end - start
onion_convex = onionConvexHull(convex_hull,coord)
print('Execution Time:', time)
xs,ys = plot(x_cord,y_cord,convex_hull)    

plotOnion(onion_convex,x_cord,y_cord)