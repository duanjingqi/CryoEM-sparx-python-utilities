#!/usr/bin/env python
# Usage: dctf_apply.py img1.hdf img2.hdf ... imgN.hdf
# To apply ctf values generated from relion to HDF images.
# The script will look for the star file of same root name as the hdf file has in the current folder. So be sure to check there are correct star files. 
# A single star file only enlisted the ctf value for the single image it indexed to . It generated from parallel run of relion on PMACS. 
# created by Jingqi at Thanksgiving 2016

import sys
from EMAN2 import *
from sparx import *

def ctf_object(star_name): 
    """Retrieve the ctf values from a star file."""

    star_list = open(star_name).read().strip().split('\n').pop().split()
    # defocus = (defocusU + defocusV)/2, unit in A.
    defocus = (float(star_list[2]) + float(star_list[3]))/2
    # unit in mm.
    cs = float(star_list[6])
    # same as EMAN & sparx.
    voltage = float(star_list[5])

    ### BE SURE TO CORRECT THE FOLLOWING PARAMETERS ACCORDINGLY! ###
    # unit in A.
    apix = float(3.4)
    # default = 0 for negative stain.
    bfactor = float(0)
    # in percentage, 60 for negative stain.
    amp_contrast = int(60)
    # default = 0.
    ampas = float(0)
    # default = 0
    angas = float(0)

    # Although EMAN or sparx take the defocus value in um, generate_ctf function can convert A into um. So no math need for the defocus value. 
    ctf_list = [defocus, cs, voltage, apix, bfactor, amp_contrast, ampas, angas]
    img_ctf = generate_ctf(ctf_list)

    return img_ctf


micrograph_path = sys.argv[1:]

for name in micrograph_path: 
    star_name = name.split(".")[0] + "_ctf.star"
    ctf_name = name.split(".")[0] + "_ctf.hdf"
    
    # check if the star file exists. 
    if os.path.isfile(star_name) == False: 
        print "ERRO: no star file exists for %s!!!" %name
        sys.exit(1)

    # get the ctf value from the star file
    img_ctf = ctf_object(star_name)

    # apply the ctf value to the micrograph
    micrograph = get_image(name)
    micrograph_ctf = filt_ctf(micrograph, img_ctf, True, 1, 1)
    micrograph_ctf.write_image(ctf_name)

    
    print "CTF had been applied to %s and %s had been generated!" %(name, ctf_name)

