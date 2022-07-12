####
# Author: Kartik Gokhale
# Date: 10.07.2022
####


## Evaluations
# 1. Frame Accuracy: Measures how many frames were correctly identified to have bacteria
# 2. Location Accuracy: Measures how many bacteria were correctly placed within 3 microns of annotated location
# 3. Measurement Accuracy: Measures how many bacteria units were correctly considered
# 4. Labelling Accuracy: Will add a labelling accuracy to measure how many bacteria were correctly labelled
##

import csv
import argparse
from utils import dist
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, required=True, help="Enter the path to the directory containing the .tif files")
parser.add_argument("--output", type=str, required=False, help="Enter the path to the output csv")
args = parser.parse_args()

thres_dist = 5

true_data = []
true_frames = []
measured_data = []
measured_frames = []

with open(args.path, "r") as f:
    reader = csv.reader(f, delimiter=",")
    for i, row in enumerate(reader):
        true_data.append([float(row[0]), float(row[1]), int(row[2])])
        if int(row[2]) not in true_frames:
            true_frames.append(int(row[2]))


with open(args.output, 'r') as f:
    lines = f.readlines()
    for line in lines:
        contents = line.split(',')
        measured_data.append([float(contents[0]), float(contents[1]), int(contents[2])])
        if int(contents[2]) not in measured_frames:
            measured_frames.append(int(contents[2]))

incorrect_frames = 0
total_frames = 966

bacteria_detected = len(measured_data)
true_bacteria = len(true_data)
correctly_detected_bacteria = 0

for x in measured_frames:
    if x not in true_frames:
        incorrect_frames += 1

for x in true_frames:
    if x not in measured_frames:
        incorrect_frames += 1

print("Frame Accuracy: {:.2f}%" .format(100 - incorrect_frames*100.0 /total_frames))


for x in measured_data:
    frame_num = x[2]
    true_indices = [i for i, x in enumerate(true_data) if x[2] == frame_num]
    if true_indices:
        loc1 = [x[0], x[1]]
        d = 1000
        for index in true_indices:
            loc2 = [true_data[index][0], true_data[index][1]]
            d = min(d, dist(loc1, loc2))
        if d <= thres_dist:
            correctly_detected_bacteria += 1
        # else:
        #     print(x[2])
        
print("Location Accuracy: {:.2f}%" .format(correctly_detected_bacteria*100.0/true_bacteria))
print("Measurement Accuracy: {:.2f}%" .format(bacteria_detected*100.0/true_bacteria))
