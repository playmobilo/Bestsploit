import glob

path = '/home/akos/bme/Bestsploit/Code'

files = [f for f in glob.glob(path + "**/*.*", recursive=True)]

for f in files:
    print(f)