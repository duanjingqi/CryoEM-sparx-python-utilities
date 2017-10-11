#!/usr/bin/env python
# Usage: dgetimg_by_average.py stack1 stack2 path_to_target_directory
# stack1 --- parental image stack
# stack2 --- classified image stack usually generated from sxisac
# path_to_target_directory --- the place where the substacks will go to, must be the aboslute path
# created by Jingqi Duan

import sys
import os
from EMAN2 import *
from sparx import *

def stackgen(avgmemberID,astackname): 
    """ Generate a stack by using image ID out of the original stack (used to be the input stack for sxisac). """
    i = 0
    for xyz in avgmemberID: 
	orgstack[xyz].write_image(astackname, i)
        i += 1

# Check input
infile = sys.argv[1:]
# check argument size
if len(infile) != 3: 
    print "Usage: dgetimg_by_average.py stack1 stack2 path_to_target_dicrectory"
    print "error! only 3 files can be taken"
    sys.exit(1)

# Image stack
orgstack = EMData.read_images(infile[0])    # the input stack for sxisac
classavg = EMData.read_images(infile[1])    # the class averages generated in sxisac
# Directory path
path2target = infile[2]                    # string

##############################################################################################
# Loop through classavg to:                                                                  # 
# 1) get micrograph member IDs for each class;                                               # 
# 2) put micrograph members to a substack;                                                   # 
# 3) write the class average and the substack to subdirectory;                               #  
# 4) perform 2D alignment with average as template.                                          #
##############################################################################################

# Loop start...
for aavg in classavg:

    # Get micrograph member ID
    avgmemberID = [int(x) for x in aavg.get_attr('members')]
    # the name of substack
    astackname = 'class_{:0>3}.hdf'.format(classavg.index(aavg))
    # make a subdirectory and change path to it
    subdir = path2target + '/' + 'class_{:0>3}'.format(classavg.index(aavg))
    os.mkdir(subdir)
    os.chdir(subdir)
    # substack output
    stackgen(avgmemberID,astackname)
    # write aavg
    aavg.write_image("average.hdf")
    # set xform.align2d to zero
    header(astackname,'xform.align2d',zero=True)
    # sxali2d
    ali2d(astackname,'al2d',ou=80,xr='4 2',ts='2 1',maxit=10,template="average.hdf",CTF=True)
    # change directory
    os.chdir(path2target)
### END ###
