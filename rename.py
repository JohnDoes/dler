import os
import glob

folder = "ja-en"
start = 1

i = start
path ="./pia/"
files = sorted(glob.glob(path + folder + '/*'))
for f in files:
    l = f.split("_")
    os.rename(f, l[0] + "_ep" + '{0:04d}'.format(i) + '_' + l[2])
    i = i + 1
