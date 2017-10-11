#!/usr/bin/env python
# Usage: dpartres_apply.py partres/partres
# To apply ctf values generated from sxcter.py to HDF images.
# created by Jingqi 1/20/2017

import sys
from EMAN2 import *
from sparx import *

ctf_list = open(sys.argv[1]).read().strip().split('\n')

for line in ctf_list: 
    # read in the micrograph
    micrograph = get_image(line.split()[-1])
    # extract ctf list
    ctf_list = [float(each) for each in line.split()[:8]]
    ctf = generate_ctf(ctf_list)
    # apply the ctf value to the micrograph and make a new micrograph
    micrograph_ctf = filt_ctf(micrograph, ctf, True, 1, 1)
    ctf_name = line.split()[-1].split('.')[0] + "_ctf.hdf"
    micrograph_ctf.write_image(ctf_name)

