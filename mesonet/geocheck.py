import matplotlib.delaunay as md  
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import math
import time

def find_angles(tri_x_points, tri_y_points):
    #Find distances/lengths of the edges of the triangles
    a = math.hypot(tri_x_points[0] - tri_x_points[1], tri_y_points[0] - tri_y_points[1])
    b = math.hypot(tri_x_points[1] - tri_x_points[2], tri_y_points[1] - tri_y_points[2])
    c = math.hypot(tri_x_points[0] - tri_x_points[2], tri_y_points[0] - tri_y_points[2])
    #Use the Law of Cosines to determine the angles of each triangle (corresponds to labeled edges)
    angle_C = np.arccos((np.square(a)+np.square(b)-np.square(c))/(2*a*b))
    angle_A = np.arccos((np.square(b)+np.square(c)-np.square(a))/(2*b*c))
    angle_B = np.arccos((np.square(c)+np.square(a)-np.square(b))/(2*a*c))
    #angle_X is in radians
        
    return (a, angle_A, b, angle_B, c, angle_C)
        
#This is used to find out which triangles are closest to being ideal for performing the line integral calculation
def weight_triangle(angle_edges):
    angles = np.asarray([angle_edges[1], angle_edges[3], angle_edges[5]]) #Angles A,B,C
    edges = np.asarray([angle_edges[0], angle_edges[2], angle_edges[4]]) #Length of Edges a, b, c
    perimeter = np.sum(edges)
            
    #determine area of the triangle using Heron's formula
    p = perimeter/2
    area = np.sqrt(p * ((p - edges[0])*(p - edges[1])*(p-edges[2])))
            
    #Find the minimum angle:
    min_angle = np.min(angles)
    tan_min_angle = np.power(np.tan(min_angle),2)
    
    return tan_min_angle/area

#This function performs the geometric check to determine whether or not the triangle input should be discarded
#because it has an angle less than 15 degrees.
def geometric_check(angle_edges, min_angle):
    angles = np.asarray([angle_edges[1], angle_edges[3], angle_edges[5]])
    degrees_angles = np.degrees(angles)
    print "Degrees: ", degrees_angles
    if len(np.where(degrees_angles <= min_angle)[0]) >= 1:
        return True
    if np.isnan(angles):
        return True
    return False
    
def distance(x1, x2, y1, y2):
    return np.sqrt(np.power((x1 - x2),2) + np.power((y1 - y2),2))

#obs_point is a tuple (x,y)
#obs_x_pts is a list of all of the x coordinates of the other observations
#obs_y_pts is a list of all of the y coordinates of the other observations
#min_obs is the minimum number of observations that must be in the circles
#max_obs is the maximum number of observations that must be in the circles 
def circle_scanning(obs_point, obs_x_pts, obs_y_pts, min_obs, max_obs):
    #dist is a list of the distances between the center of the circle and the other obs
    dist = distance(obs_point[0], obs_x_pts, obs_point[1], obs_y_pts)
    #print dist
    #dist = np.delete(dist, [0])
    inside_circle_xs = []
    inside_circle_ys = []
    looking_for_obs = min_obs
    for radius in np.arange(0,10000000, 100):
        #print "Radius of circle: ", radius
        #Which obs are within the circle?
        validIdx = np.where(dist <= radius)
        #How many obs are within the circle?
        obs_in_circle = len(validIdx[0])
        #Are there enough obs in the circle?
        if obs_in_circle == looking_for_obs:
            xtemp = np.insert(obs_x_pts[validIdx[0]],0,obs_point[0])
            ytemp = np.insert(obs_y_pts[validIdx[0]],0,obs_point[1])
            inside_circle_xs.append(xtemp)
            inside_circle_ys.append(ytemp)
            looking_for_obs = looking_for_obs + 1
        if obs_in_circle > max_obs-1:
            break

    #inside_circle_xs = np.asarray(inside_circle_xs)
    #inside_circle_ys = np.asarray(inside_circle_ys)
    return inside_circle_xs, inside_circle_ys

if __name__ == '__main__':
  

