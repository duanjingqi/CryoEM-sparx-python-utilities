#!/usr/bin/env python
# Usage: dctf_split.py star_file
# created by Jingqi 
# 6/11/2017

import sys
from subprocess import Popen,PIPE

# global variant
apix = float(1.63)
bfactor = float(0)
ampas = float(0)
angas = float(0)

star_file = sys.argv[1]

# Get column index
## _rlnImageName (particle image)
#ptcl_col = Popen(['grep','_rlnImageName',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnDefocusU
dfxu_col = Popen(['grep','_rlnDefocusU',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnDefocusV
dfxv_col = Popen(['grep','_rlnDefocusV',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnSphericalAberration
cs_col = Popen(['grep','_rlnSphericalAberration',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnVoltage
kev_col = Popen(['grep','_rlnVoltage',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnAmplitudeContrast
ampc_col = Popen(['grep','_rlnAmplitudeContrast',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnCoordinateX
#crdx_col = Popen(['grep','_rlnCoordinateX',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnCoordinateY
#crdy_col = Popen(['grep','_rlnCoordinateY',star_file], stdout=PIPE).stdout.read().split()[1][1:]
## _rlnMicrographName
mic_col = Popen(['grep','_rlnMicrographName',star_file], stdout=PIPE).stdout.read().split()[1][1:]

for row in open(star_file).read().split('\n'):
    if len(row.split()) > 4: 
        star_row = row.split()

# CTF object: [defocus,cs,voltage,apix,bfactor,ampcont]

        dfxu = float(star_row[int(dfxu_col)-1])
        dfxv = float(star_row[int(dfxv_col)-1])
        defocus = (dfxu + dfxv) / 20000
        cs = float(star_row[int(cs_col)-1])
        voltage = float(star_row[int(kev_col)-1])
        ampcont = float(star_row[int(ampc_col)-1]) * 100

        ctf_list = "{} {} {} {} {} {} {} {}".format(defocus,cs,voltage,apix,bfactor,ampcont,ampas,angas)

# Write to local file
        mrc_prefix = star_row[int(mic_col)-1].split("/")[-1][:-4]
        ctf_file_path = "micrographs" + "/" + mrc_prefix + "_ctf.dat"
        open(ctf_file_path,"w").write(ctf_list)

#---END---
