#!/usr/bin/env python
# Usage: dgetimg_by_id.py stack_1 stack_2 micrograph_number_file
# stack1 --- parental image stack
# stack2 --- the image stack to be generated
# micrograph_number_file --- contains the micrograph number to be selected.
# For the stacks in different folders, their full pathes must be provided. 
# Make sure the input files be in correct order
# created by Jingqi Duan

import sys
from EMAN2 import *
from EMAN2db import db_open_dict, db_list_dicts, db_remove_dict, e2gethome
from sparx import *

# file path
file_path = sys.argv[1:]

# check if the input files are correct.
if len(file_path) != 3: 
    print """Input file Error!
             dgetimg_by_id.py only take three inputs."""
    sys.exit(1)

# Parental particle stack
stack_raw = EMData.read_images(file_path[0])
micrograph_number_list = open(file_path[2]).read().strip().split('\n')

# Output 
stack_output = file_path[1]

# write the selected images to stack_output
i = 0
for id in micrograph_number_list: 
    stack_raw[int(id)].write_image(stack_output, i)
    i += 1
