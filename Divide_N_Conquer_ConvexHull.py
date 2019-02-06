import matplotlib.pyplot as plt
import statistics as stat
import time
import operator
import copy
import sys

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

def file_to_list(filename):
	""" Returns a list of all points"""
	points_list = []
	try:
		file = open(filename, 'r')
		no_of_points = int(file.readline())
		for i in file:
			i = i.split()
			i[0] = int(i[0])
			i[1] = int(i[1])
			i[2] = int(i[2])
			i = tuple(i)
			points_list.append(i)
		file.close()
	except:
		print("Invalid file name")

	return points_list, no_of_points

def plot(points_list, convex_hull = None, skyline = None):
	x=[]
	y=[]
	for point in points_list:
		x.append(point[1])
		y.append(point[2])
	plt.scatter(x,y)

	if convex_hull != None:
		for i in  convex_hull:
			for p1 in convex_hull[i]:
				p0 = i
				plt.plot((p0[1], p1[1]), (p0[2], p1[2]), 'r')
	x1 = []
	y1 = []
	if skyline != None:
		for point in skyline:
			x1.append(point[1])
			y1.append(point[2])
	plt.scatter(x1,y1,marker="X")
	plt.title('Convex Hull using Divide N Conquer')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.show()

def median_of_medians(points_list,x_or_y_no):
	median_list = []
	for i in range(0,len(points_list),5):
		temp = points_list[i:i+5]
		temp.sort(key = operator.itemgetter(x_or_y_no))
		if len(temp) == 5:
			median = temp[2]
		else:
			median = temp[(len(temp)-1)//2]
		median_list.append(median)
	median_list.sort(key = operator.itemgetter(1))
	mom = median_list[(len(median_list)-1)//2]
	return mom

def max_of_hull(hull,axis_no):
	x_or_y_of_hull = []
	for point in hull:
		x_or_y_of_hull.append(point[axis_no])
	x_or_y_max = max(x_or_y_of_hull)
	for point in hull:
		if x_or_y_max == point[axis_no]:
			return point

def min_of_hull(hull,axis_no):
	x_or_y_of_hull = []
	for point in hull:
		x_or_y_of_hull.append(point[axis_no])
	x_or_y_max = min(x_or_y_of_hull)
	for point in hull:
		if x_or_y_max == point[axis_no]:
			return point

def is_on_segment(p1, p2, p3):
	"""Needed only for the co-linear condition"""
	if (p2[1] <= max(p1[1],p3[1])) and (p2[1] >= min(p1[1],p3[1])) and (p2[2] <= max(p1[2],p3[2])) and (p2[2] >= min(p1[2],p3[2])):
		return True
	else: return False

def orientation(point1, point2, point3):
	"""Return 0 or 1 or 2 Depending on the orientation of points 1 to 3"""
	result = (point2[2] - point1[2]) * (point3[1] - point2[1]) - (point3[2] - point2[2]) * (point2[1] - point1[1])
	if result == 0:
		return 0
	elif result > 0:
		return 1					#	Clockwise Orientation
	else: return 2					#	CounterClockwise Orientation

def is_intersecting(p1, p2, p3, p4):
	"""
	:param p1: point of line 1
	:param p2: point of line 1
	:param p3: point of line 2
	:param p4: point of line 2
	:return:
	"""
	o1 = orientation(p1, p2, p3)
	o2 = orientation(p1, p2, p4)
	o3 = orientation(p3, p4, p1)
	o4 = orientation(p3, p4, p2)

	#	general case
	if o1 != o2 and o3 != o4:
		return True
	#	Special Case
	elif (o1 == 0 and is_on_segment(p1,p3,p2)) or (o2 == 0 and is_on_segment(p1,p3,p2)) or (o3 == 0 and is_on_segment(p3,p1,p4)) or (o4 == 0 and is_on_segment(p3,p2,p4)):
		return True
	else: return False

def upper_tangent(left_hull, right_hull, point1, point2):
	"""
	:param left_hull: left_hull
	:param right_hull: right_hull
	:param point1: max point of left hull, later changes to form tangents
	:param point2: min point of right hull, later changes to form tangents
	:return: point1, point2
	"""

	flag = False
	counter = 0
	while not flag:
		flag = True
		o1 = False
		while(not o1):
			o1 = True
			for point in left_hull[point1]:
				if orientation(point, point1, point2) != 1:
					o1 = False
					break
			if o1 is False:
				point1 = point

		o2 = False
		while(not o2):
			o2 = True
			for point in right_hull[point2]:
				if orientation(point1, point2, point) != 1:
					o2 = False
					break
			if o2 is False:
				flag = False
				point2 = point

	return point1, point2

def lower_tangent(left_hull, right_hull, point1, point2):
	"""
		:param left_hull: left_hull
		:param right_hull: right_hull
		:param point1: max point of left hull, later changes to form tangents
		:param point2: min point of right hull, later changes to form tangents
		:return: point1, point2
		"""
	flag = False
	counter = 0
	while not flag:
		flag = True
		o1 = False
		while (not o1):
			o1 = True
			for point in left_hull[point1]:
				if orientation(point, point1, point2) != 2:
					o1 = False
					break
			if o1 is False:
				point1 = point

		o2 = False
		while (not o2):
			o2 = True
			for point in right_hull[point2]:
				if orientation(point1, point2, point) != 2:
					o2 = False
					break
			if o2 is False:
				flag = False
				point2 = point

	return point1, point2

def delete_hull_points(hull,p1,p2,o_value):
	"""Removing all the clockwise and counterclockwise points between upper and lower tangent points from left and right hull respectievely"""
	temp = []
	for point in hull:
		if point != p1 and point != p2:
			if orientation(p1, point, p2) != o_value:		#	if uppertangentpoint, anypoint, lowertangentpoint != ccw
				temp.append(point)
	for point in temp:
		hull.pop(point)

	temp = []
	for point in hull[p1]:
		if point != p2:
			if orientation(p1, point, p2) != o_value:
				temp.append(point)
	for point in temp:
		hull[p1].remove(point)

	temp = []
	for point in hull[p1]:
		if point == p2 and len(hull[p1]) == 2:
			temp.append(point)
	for point in temp:
		hull[p1].remove(point)

	temp = []
	for point in hull[p2]:
		if point != p1:
			if orientation(p1, point, p2) != o_value:
				temp.append(point)
	for point in temp:
		hull[p2].remove(point)

	temp = []
	for point in hull[p2]:
		if point == p1 and len(hull[p2]) == 2:
			temp.append(point)
	for point in temp:
		hull[p2].remove(point)

	return hull

def convex_hull_divide_conquer(points_list):
	if len(points_list) <= 3:
		convex_dict = {}
		for i in points_list:
			a = []
			for j in points_list:
				if i!=j:
					a.append(j)
			convex_dict[i] = a
		return convex_dict

	x = []
	y = []
	l = []
	r = []

	for point in points_list:
		x.append(point[1])
		y.append(point[2])
	x_median = stat.median_low(x)
	# mom = median_of_medians(points_list,1)
	# x_median = mom[1]
	for i in points_list:
		if i[1] > x_median:
			r.append(i)
		else:
			l.append(i)

	left_hull = convex_hull_divide_conquer(l)
	right_hull = convex_hull_divide_conquer(r)

	if left_hull != None:
		max_point = max_of_hull(left_hull,1)
	if right_hull != None:
		min_point = min_of_hull(right_hull,1)

	if left_hull != None and right_hull != None:
		upper_p1, upper_p2 = upper_tangent(left_hull, right_hull, max_point, min_point)
		lower_p1, lower_p2 = lower_tangent(left_hull, right_hull, max_point, min_point)
		left_hull = delete_hull_points(left_hull,upper_p1,lower_p1,2)
		right_hull = delete_hull_points(right_hull, upper_p2, lower_p2, 1)
		left_hull[upper_p1].append(upper_p2)
		right_hull[upper_p2].append(upper_p1)
		left_hull[lower_p1].append(lower_p2)
		right_hull[lower_p2].append(lower_p1)
		left_hull.update(right_hull)
		convex_hull = left_hull
	return convex_hull

def naive_skyline(points_list):
	neglect = []
	for p1 in points_list:
		for p2 in points_list:
			if p2 != p1:
				if (p2[1] >= p1[1] and p2[2] >= p1[2]):
					neglect.append(p1)
					break
	neglect = set(neglect)
	for point in neglect:
		points_list.remove(point)
	return points_list

def DnQskyline(points_list):
	convex_hull = convex_hull_divide_conquer(points_list)
	point_with_x_max = max_of_hull(convex_hull,1)
	point_with_y_max = max_of_hull(convex_hull,2)
	skyline_points = []
	for point in convex_hull:
		if point[2] >= point_with_x_max[2] and point[1] >= point_with_y_max[1]:
			skyline_points.append(point)

	return skyline_points

def main(argv):
	while(True):
		ip = input("\nEnter :"
							 "\n\t1: Divide and Conquer (Tangent Approach)\n\t2: Naive Skyline using Divide and Conquer\n\t3: Skyline using Convex Hull\nOr Enter any other number to exit\n")
		points_list, no_of_points = file_to_list('inputfile.txt')
		if int(ip) == 1:
			start = time.time()
			convex_hull = convex_hull_divide_conquer(points_list)
			end = time.time()
			finaltime = end - start
			print('D n Q convex Hull Time:', finaltime)
			plot(points_list,convex_hull)
		elif int(ip) == 2:
			start = time.time()
			skyline1 = naive_skyline(copy.deepcopy(points_list))
			end = time.time()
			finaltime = end - start
			plot(points_list, None, skyline1)
			print('\nNaive_skyline Time:', finaltime)
		elif int(ip) == 3:
			start = time.time()
			skyline = DnQskyline(points_list)
			end = time.time()
			finaltime = end - start
			plot(points_list, None, skyline)
			print('\nDQ skyline Skyline Time:', finaltime)
		else:
			break

if __name__ == '__main__':
    main(sys.argv)