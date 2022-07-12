####
# Author: Kartik Gokhale
# Date: 09.07.2022
####

## How to Run the Code
# 1. python script_video.py --path /path_to_folder

## Current Situation
# 1. Able to differentiate between bacteria and background fluid
# 2. Can differentiate between clumps of pointsets and label different bacteria(identify correct number of bacteria) - Accuracy NOT measured
# 3. Differentiate between bacteria using prior frame results(proximity) and grouping(maybe k-means)

## Plan Ahead
# 1. Make it robust against collisions 
#   - Stuff to Try : https://learnopencv.com/simple-background-estimation-in-videos-using-opencv-c-python/

# (csv file headings)
# (x,y,frame_num, bacteria_num)

# Time_Gap = 0.14s
# 1 Pixel = 0.667 microns

# Its dimensions(E. Coli.) are those of a cylinder 1.0-2.0 micrometers long, with radius about 0.5 micrometers.
# Thus, have chosen a sphere of radius 4 microns



import argparse
from inspect import trace
from posixpath import sep
from re import L
from tkinter import Frame
import numpy as np
from PIL import Image
import os
import glob
from matplotlib import pyplot as plt
import math
from utils import *
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, required=True, help="Enter the path to the directory containing the .tif files")
parser.add_argument("--output", type=str, required=False, help="Enter the path to the output csv")
args = parser.parse_args()

thres = 25 # Confidence interval for detecting Bacteria = (16, 40)
# dist_thres = 4.8 # Confidence interval for distance - Hard-Coded (Tested Against 6)
dist_thres = 4.8
frame_num = 1
prev_num_bact = 0

with open(args.output, 'w') as f:
    for images in os.listdir(args.path):
        print(frame_num)
        im = Image.open(args.path + images)
        # im.show()
        imarray = np.array(im)

        ls = locations(imarray, thres)
        for l in ls:
            # print(l)
            a,b = l
            imarray[b][a] = [255,0,0]

        bacteria_centres = differentiate_bacteria(ls, dist_thres)
        num_bacteria = len(bacteria_centres)

        if prev_num_bact > num_bacteria:
            bacteria_centres = differentiate_bacteria(ls, dist_thres - 1)
        # print(bacteria_centres)

        num_bacteria = len(bacteria_centres)

        if bacteria_centres:
            for t in bacteria_centres:
                f.write(str(t[0]) + "," + str(t[1]) + "," + str(frame_num))
                f.write("\n")

        # trace_bacteria() # Will Develop function to trace bacteria through the frames
        frame_num += 1

        prev_num_bact = num_bacteria

        # plt.imshow(imarray, interpolation='nearest')
        # plt.show()