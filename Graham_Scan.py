import random
import sys
import time
from collections import defaultdict
from math import atan2
from operator import itemgetter
import pickle
import numpy as np


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

#Calculate the Polar angle
def polar_angle(origin,o_point):
    angle_list = {}#defaultdict(list)
    for i in range (0,len(o_point)):
        if origin == o_point[i]:
            pass
        else:
            x_diff = origin[0] - o_point[i][0]
            y_diff = origin[1] - o_point[i][1]
            polar_angle = atan2(y_diff,x_diff)
            angle_list.update({i:polar_angle})
    return angle_list

#Sort the points according to polar angles
def sort_coords_angle(angle_list,coord):
    sort_angle = sorted(((value,key) for (key,value) in angle_list.items()),reverse=False)
    sorted_coords = []
    for i in range (0,len(sort_angle)):
        sorted_coords.append(coord[int(sort_angle[i][1])])
    return sorted_coords,sort_angle

#caluclate the orientation by caluclating the cross product of 3 points
def orientation(p1,p2,p3):
    ornt = (p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0])
    return ornt    


from matplotlib import pyplot as plt

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
    plt.title('Convex Hull using Graham Scan')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show() 

    return xs,ys

def GrahamScan(coord,x_cord,y_cord):
	y_val, id_y = min((y_val, id_y) for (id_y, y_val) in enumerate(y_cord))
	angle_list = polar_angle(coord[id_y],coord)
	sort_coords,sort_angle = sort_coords_angle(angle_list,coord)
	convex_hull =[coord[id_y], sort_coords[0]]

	for i in sort_coords[1:]:
		len_convexhull = len(convex_hull)
		while orientation(convex_hull[-2],convex_hull[-1],i) <= 0:
			del convex_hull[-1]
		convex_hull.append(i)

	return convex_hull

coord,x_cord,y_cord = file_to_x_y('inputfile.txt')
start = time.time()
convex_hull = GrahamScan(coord,x_cord,y_cord)
end = time.time()
time = end - start
print('Time:',time)
xs,ys = plot(x_cord,y_cord,convex_hull)
y_min = min(y_cord)
