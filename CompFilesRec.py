#!/usr/bin/python3
# vim: set cc=80 tw=79:

"""
Print to file the differences in two directory structures.

Looking recursively in pairs of directories (which are defined below),
find differences in file contents, and list those files with their paths
(and size in bytes), alphabetically sorted.
If Run in Terminal is chosen, see an indication of progress printed.
"""
import datetime
import os
import socket
import sys
import time

# get two timestamps:
start = time.time()
startd = datetime.datetime.now().isoformat(' ')

# specify the hard drive folders that I want to look in:
mpt = '/media/jo/'
hd0 = 'WD1001FALS'
# Setup a list of folder pairs:
fldrs = [
    # 'WD1001FALS/Vs Conflict',
    '/mnt/WD1001FALS/Vs Unseen', '/run/media/jo/SAMSUNG/SamsungM3/Vs Unseen',
    '/mnt/WD1001FALS/Vs Technos/', '/run/media/jo/Expansion Drive/Vs Technos/',
    ]
fldrn = len(fldrs)
hd1 = 'Expansion Drive'
fldr = '/Vs Technos'


# function to create file lists with relative paths included:
def filelister(listdir):
#   initialise a list just with the base folder path:
    flc = 0
    fileList = [listdir]
    for root, folders, files in os.walk(listdir):
        for file in files:
            # indication of progress:
            flc += 1
            # print(flc, end='\r', flush=True)
            # - works, but Flake8 reports as invalid syntax E901, so:
            sys.stdout.write('\r' + str(flc))
            sys.stdout.flush()
            abspath = os.path.join(root, file)
            # take listdir out of the printout:
            fileList.append(abspath.replace(listdir + "/", "") +
                            # add file's bytesize:
                            "  ("+str(os.path.getsize(abspath))+" bytes)")
    return fileList

for ifldrs in range(fldrn):
    print(fldrs[ifldrs])
    # Create the lists for each folder-pair
    list = [[], []]
# appending to the first (root folder name) items the count:
fldr0 = mpt+hd0+fldr
print('Looking at contents of', fldr0)
list0 = filelister(fldr0)
ll0 = len(list0)
list0[0] += ' - contains '+str(ll0-1)+' files, these ones unmatched:'
print(' - file records loaded in.')

fldr1 = mpt+hd1+fldr
print('Looking at contents of', fldr1)
list1 = filelister(fldr1)
ll1 = len(list1)
list1[0] += ' - contains '+str(ll1-1)+' files, these ones unmatched:'
print(' - file records loaded in.')

# working through first list, eliminate items duplicated in the second,
# leaving two lists of unmatched items:
print('Looking for differences in the records now...')
list2 = []
for ircomp in range(ll0):
    item = list0.pop(0)
    # indication of progress:
    sys.stdout.write('\r' + str(ircomp))
    sys.stdout.flush()
    try:
        list1.remove(item)
    except ValueError:
        list2.append(item)
list1.sort()
list2.sort()
# using a filename taken from this script's own name:
flnm = sys.argv[0].replace('./', '').replace('.py', '.')+'txt'
print(' - all done, results are in \'' + flnm + '\'.')

# create a file object for output:
fo = open(flnm, 'w')
# create a nice header:
wrt1 = socket.gethostname()+' folder changes at '+startd+'\n\n'
# the resulting unmatched items:
wrt2 = '\n'.join(list1)+'\n\n'+'\n'.join(list2)
# and the time taken:
wrt3 = '\n\ntook '+str(time.time()-start)+' seconds to find the differences'
# write and close the file object:
fo.write(wrt1+wrt2+wrt3)
fo.close()