
# Show frames 190, 350-360

import argparse
from re import L
import numpy
from PIL import Image
import os
import glob
from matplotlib import pyplot as plt
import math
from utils import *

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, required=True, help="Enter the path to the directory containing the .tif files")
parser.add_argument("--output", type=str, required=False, help="Enter the path to the output csv")
args = parser.parse_args()

thres = 25 # Confidence interval for detecting Bacteria = (16, 40)
dist_thres = 4.8 # Confidence interval for distance - Hard-Coded (Tested against 6)

try:
    im = Image.open(args.path)
except:
    print("No image found")
    exit(0)

im.show()
imarray = numpy.array(im)

ls = locations(imarray, thres)

# Un-comment following block to display all bacterial points
# for l in ls:  
#     # print(l)
#     a,b = l
#     imarray[b][a] = [255,0,0]

bacteria_centres = differentiate_bacteria(ls, dist_thres)
print(bacteria_centres)

for l in bacteria_centres:
    # print(l)
    a,b = l
    imarray[int(b)][int(a)] = [255,0,0]

print("Number of bacteria detected:", len(bacteria_centres))

plt.imshow(imarray, interpolation='nearest')
plt.show()