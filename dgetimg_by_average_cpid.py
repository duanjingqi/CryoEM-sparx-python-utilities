#!/usr/bin/env python
# Usage: dgetimg_by_average.py stack1 stack2 stack3
# stack1 --- parental image stack
# stack2 --- classified image stack usually generated from sxisac
# stack3 --- the image stack to be generated
# For the stacks in different folders, their full pathes must be provided. 
# created by Jingqi Duan

import sys
from EMAN2 import *
from sparx import *

def get_id(classified_stack): 
    """Fetch the raw image ID from the classified image stack."""
    ID_list = []
    for image in classified_stack: 
        ID_list.extend(image.get_attr('members'))

    member_ID = list(set([int(each) for each in ID_list]))

    return member_ID

def dgetimg_by_average(): 
    """Get the images from the parental stack and make a new image stack."""
    # load the pathes for the parental, classified and new stacks
    image_path = sys.argv[1:]

    # check argument size
    if len(image_path) != 3: 
        print "Usage: dgetimg_by_average.py stack1 stack2 stack3"
        print "error! only 3 files can be taken"
        sys.exit(1)

    # load image stacks
    parental_stack = EMData.read_images(image_path[0])
    classified_stack = EMData.read_images(image_path[1])

    # get the raw image ID for the classified_stack
    raw_ID = get_id(classified_stack)

    # write the selected images to a new image stack
    i = 0
    for id in raw_ID: 
        parental_stack[id].set_attr('pid',id)
	parental_stack[id].write_image(image_path[2], i)
        i += 1

if __name__ == "__main__":
    dgetimg_by_average()
