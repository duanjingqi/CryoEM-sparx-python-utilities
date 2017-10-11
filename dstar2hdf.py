#!/usr/bin/env python
# Usage: dstar2hdf.py star_file stackout
# created by Jingqi 
# 6/11/2017

import sys
from subprocess import Popen,PIPE
from EMAN2 import *
from sparx import *

# global variant
apix = float(1.63)
bfactor = float(0)
ampas = float(0)
angas = float(0)

def get_image(wheresptcl): 
    """ Get the particle from the relion mrcs (take a single string as input). """
    ptcl_path = wheresptcl.split('@')[1][:-4]+"hdf"
    ptcl_index = int(wheresptcl.split('@')[0])-1
    image = EMData().read_image(ptcl_path,ptcl_index)
    return image

def ctf_gen(dfxu,dfxv,cs,voltage,amp_contrast): 
    """Retrieve the ctf values from a star file."""

    # defocus = (defocusU + defocusV)/2, unit in A.
    defocus = (dfxu+dfxv)/2
    # Although EMAN or sparx take the defocus value in um, generate_ctf function can convert A into um. So no math need for the defocus value. 
    ctf_list = [defocus, cs, voltage, apix, bfactor, amp_contrast, ampas, angas]
    img_ctf = generate_ctf(ctf_list)
    return img_ctf


star_file = sys.argv[1]
stackout = sys.argv[2]

# Get line index
## _rlnImageName (particle image)
ptcl_line = Popen(['grep','_rlnImageName',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnDefocusU
dfxu_line = Popen(['grep','_rlnDefocusU',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnDefocusV
dfxv_line = Popen(['grep','_rlnDefocusV',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnSphericalAberration
cs_line = Popen(['grep','_rlnSphericalAberration',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnVoltage
kev_line = Popen(['grep','_rlnVoltage',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnAmplitudeContrast
ampc_line = Popen(['grep','_rlnAmplitudeContrast',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnCoordinateX
crdx_line = Popen(['grep','_rlnCoordinateX',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnCoordinateY
crdy_line = Popen(['grep','_rlnCoordinateY',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnMicrographName
mic_line = Popen(['grep','_rlnMicrographName',star_file], stdout=PIPE).stdout.read().split()[1][1:]

i = 0
for row in open(star_file).read().split('\n'):
    if len(row.split()) > 4: 
        star_row = row.split()
# Particle image        
        wheresptcl = star_row[int(ptcl_line)-1]
        image = get_image(wheresptcl)
# CTF object
        dfxu = float(star_row[int(dfxu_line)-1])
        dfxv = float(star_row[int(dfxv_line)-1])
        cs = float(star_row[int(cs_line)-1])
        voltage = float(star_row[int(kev_line)-1])
        amp_contrast = float(star_row[int(ampc_line)-1])
        image_ctf = ctf_gen(dfxu,dfxv,cs,voltage,amp_contrast)
        image.set_attr("ctf", image_ctf)
# Set other attributes
        crdx = float(star_row[int(crdx_line)-1])
        crdy = float(star_row[int(crdy_line)-1])
        image.set_attr("ptcl_source_coord",[crdx,crdy])
        mic_source = star_row[int(mic_line)-1]
        image.set_attr("ptcl_source_image",mic_source)
# write stack 
        image.write_image(stackout, i)
        i += 1

#---END---
