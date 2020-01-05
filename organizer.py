# Let's create 3 categories:
# For reference => (100000000 byte = 100MB)
# File size <= 100MB
# 100MB < File size <= 500MB
# 1GB <= File size

# Usage #
# python organizer.py -d [dirname]

from os import walk, makedirs, path
from shutil import move
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument("-d", "--dirname", required=True,
                help="name of the directory")
args = vars(ap.parse_args())
pathName = args["dirname"].replace("\\", "/")
pathName = pathName+"/" if pathName[-1] != "/" else pathName
smallDir = pathName+"small/"
medDir = pathName+"medium/"
largeDir = pathName+"large/"
smallLimit = 100000000
medLimit = 500000000


def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in walk(start_path):
        for f in filenames:
            fp = path.join(dirpath, f)
            if not path.islink(fp):
                total_size += path.getsize(fp)
    return total_size

fnames = []
dnames = []
for (dirpath, dirnames, filenames) in walk(pathName):
    fnames.extend(filenames)
    dnames.extend(dirnames)

removeDirs = list(set(dnames).difference(["small", "medium", "large"]))

for f in fnames:
    fSize = path.getsize(pathName+f)
    fPath = pathName+f
    ext = f.split(".")[-1]+"/"
    if fSize <= smallLimit:
        makedirs(smallDir+ext, exist_ok=True)
        move(fPath, smallDir+ext+f)
    elif fSize <= medLimit:
        makedirs(medDir+ext, exist_ok=True)
        move(fPath, medDir+ext+f)
    else:
        makedirs(largeDir+ext, exist_ok=True)
        move(fPath, largeDir+ext+f)

for d in removeDirs:
    dirSize = get_size(pathName+d)
    dPath = pathName+d
    if dirSize <= smallLimit:
        makedirs(smallDir, exist_ok=True)
        move(dPath, smallDir+d)
    elif dirSize <= medLimit:
        makedirs(medDir, exist_ok=True)
        move(dPath, medDir+d)
    else:
        makedirs(largeDir, exist_ok=True)
        move(dPath, largeDir+d)

print("Congratulations, you should now be free from clutter in this directory")
