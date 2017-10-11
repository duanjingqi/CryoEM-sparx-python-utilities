#!/usr/bin/env python
# Usage: dgetimg_by_starid.py stack_1 stack_2 star_file
# stack1 --- parental image stack
# stack2 --- the image stack to be generated
# star_file --- contains the micrograph number to be selected.
# For the stacks in different folders, their full pathes must be provided. 
# Make sure the input files be in correct order
# created by Jingqi Duan

import sys
from EMAN2 import *
from EMAN2db import db_open_dict, db_list_dicts, db_remove_dict, e2gethome
from sparx import *

def starid(line):
    """get id from each line in star_file"""
    return int(line.split('@')[0])

#def myimage(parental_stack, micrograph_id): 
#    """Extract micrograph by its ID"""
#    micrograph = EMData() 
#    i = micrograph_id - 1
#    micrograph.read_image(parental_stack, i)
#    return micrograph

# file path
file_path = sys.argv[1:]

if len(file_path) != 3: 
    print """Input file Error!
             dgetimg_by_id.py only take three inputs."""
    sys.exit(1)

parental_stack = EMData.read_images(file_path[0])
selected_stack = file_path[1]
star_file = file_path[2]

i = 0
for line in open(star_file): 
    if len(line.split()) > 5: 
        # Extract micrograph ID 
        micrograph_id = starid(line) - 1

        # Get micrograph
        # micrograph = myimage(parental_stack, micrograph_id)

        # Build a new stack
        parental_stack[micrograph_id].write_image(selected_stack, i)
        i += 1

print "%d images has been dropped to %s!" % (i, selected_stack)

# Done!!!
