#!/usr/bin/env python
# Usage: dsplit_average.py stack1 stack2 
# stack1 --- parental image stack
# stack2 --- classified image stack usually generated from sxisac
# For the stacks in different folders, their full pathes must be provided. 
# created by Jingqi Duan

import sys
from EMAN2 import *
from sparx import *

def get_id(aclass): 
    """Fetch the raw image ID from the classified image stack."""
    img_ID = aclass.get_attr('members')
    img_ID_int = [int(each) for each in img_ID]

    return img_ID_int

def dsplit_average(): 
    """Unstack the class average and make image stack for each class."""
    # load the pathes for the parental, classified and new stacks
    image_path = sys.argv[1:]

    # check argument size
    if len(image_path) != 2: 
        print "Usage: dsplit_average.py stack1 stack2"
        print "error! only 2 files can be taken"
        sys.exit(1)

    # load image stacks
    parental_stack = EMData.read_images(image_path[0])
    classified_stack = EMData.read_images(image_path[1])

    # loop through the class average, split, and make particle stack for each class
    for aclass in classified_stack: 

        # get the image ID list for the "aclass"
        raw_ID = get_id(aclass)

        # get the name for the "aclass"
        name = "class_{:03d}.hdf".format(classified_stack.index(aclass)) 

        # write the selected images to a new image stack
        i = 0
        for id in raw_ID: 
	    parental_stack[id].write_image(name, i)
	    i += 1

if __name__ == "__main__":
    dsplit_average()
