####
# Author: Kartik Gokhale
# Date: 12.07.2022
####

import csv
import argparse
from utils import dist
import numpy as np
from PIL import Image
import cv2
import os
import math

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, required=True, help="Enter the path to the directory containing the .tif files")
parser.add_argument("--annotations", type=str, required=True, help="Enter the path to the csv containing annotations")
parser.add_argument("--output", type=str, required=False, help="Enter the path to the output csv")
args = parser.parse_args()

data = []
frames = []

with open(args.annotations, "r") as f:
    reader = csv.reader(f, delimiter=",")
    for i, row in enumerate(reader):
        data.append([float(row[0]), float(row[1]), int(row[2])])
        if int(row[2]) not in frames:
            frames.append(int(row[2]))

for images in os.listdir(args.path):
    im = Image.open(args.path + images)
    imarray = np.array(im)
    dims = imarray.shape
    break

fps = 10
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
output = cv2.VideoWriter(args.output, fourcc, fps, (dims[1], dims[0]))

frame_num = 1
for images in os.listdir(args.path):
    im = Image.open(args.path + images)
    imarray = np.array(im)

    if frame_num in frames:
        for x in data:
            if x[2] == frame_num:
                cv2.circle(imarray, (int(x[0]), int(x[1])), 5, (0,0,255))
        output.write(imarray)
    else:
        output.write(imarray)
    frame_num += 1
