#!/usr/bin/env python

import sys
import os

def df(list1,list2):
    """ Generate the difference between two lists and put them in third list. list1 is longer than list2, list3 is empty."""
    alist = []
    for line in list1: 
        if line not in list2:
            alist.append(line)

    return alist

# Prepare input files
filelist = sys.argv[1:]
list1 = []
list2 = []
if os.path.getsize(filelist[0]) > os.path.getsize(filelist[1]): 
    list1 = open(filelist[0]).read().split('\n')
    list2 = open(filelist[1]).read().split('\n')
else:
    list1 = open(filelist[1]).read().split('\n')
    list2 = open(filelist[0]).read().split('\n')

list_diff = df(list1,list2)

with open(filelist[2],'w') as f: 
    f.write("\n".join(list_diff))



