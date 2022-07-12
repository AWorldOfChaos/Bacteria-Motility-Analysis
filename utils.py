####
# Author: Kartik Gokhale
# Date: 09.07.2022
####

import math

def locs(im: list, thres: float) -> tuple:
    x=-1
    y=-1
    for i in range(len(im)):
        for j in range(len(im[0])):
            if im[i][j][2]>thres:
                x = j
                y = i
    return (x,y)

def mox(im: list, thres: float) -> tuple:
    m = 0
    x = -1
    y = -1
    for i in range(len(im)):
        for j in range(len(im[0])):
            if im[i][j][2]>m and im[i][j][2]>thres:
                m = im[i][j][2]
                x = j
                y = i
    return (x,y)

def locations(im: list, thres: float) -> list:
    m = 0
    l = []
    for i in range(len(im)):
        for j in range(len(im[0])):
            if im[i][j][2]>thres:
                m = im[i][j][2]
                l.append([j,i])
    return l

def dist(one: tuple, two: tuple) -> float:
    return math.sqrt((one[0]-two[0])*(one[0]-two[0]) + (one[1]-two[1])*(one[1]-two[1]))

def differentiate_bacteria(points: list, dist_thres: float) -> list:
    bacteria_centres = []
    on = False
    num = 0
    curr_centre = [0, 0]
    while points:
        removed_points = []
        for point in points:
            if not on:
                curr_centre = point
                num = 1
                on = True
                removed_points.append(point)
            else:
                if dist(point, [curr_centre[0]/num, curr_centre[1]/num]) < dist_thres:
                    curr_centre = [curr_centre[0]+point[0], curr_centre[1]+point[1]]
                    num += 1
                    removed_points.append(point)
            
        for point in removed_points:
            points.remove(point)
        
        on = False
        if num>8:
            bacteria_centres.append([curr_centre[0]/num, curr_centre[1]/num]) # Consider putting bounds on number of points

    return bacteria_centres

def trace_bacteria():
    pass
