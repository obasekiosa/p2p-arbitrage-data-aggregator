import os
import shutil
from os import listdir
from os.path import isfile, join
import datetime

x = datetime.datetime.now()

y = f"{x.year}_{x.month}_{x.day}_{x.hour}_{x.minute}_{x.second}"


mypath = os.path.dirname(os.path.abspath(__file__))
# print(mypath)
onlyfiles = [f for f in listdir(mypath) if isfile(
    join(mypath, f)) and f.endswith(".json")]

d = join(mypath, 'output', y)
os.mkdir(d)

for f in onlyfiles:
    shutil.move(join(mypath, f), join(d, f))

# print(onlyfiles)

# import datetime

# x = datetime.datetime.now()

# y = f"{x.year}_{x.month}_{x.day}_{x.hour}_{x.minute}_{x.second}"

# print(y)
