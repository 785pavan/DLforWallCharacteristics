import os
import cv2

i = 0
filenames = next(os.walk(os.getcwd()))[2]
filenames.remove(os.path.basename(__file__))
for filename in filenames:
    dst = "image." + str(i) + ".tif"
    src = os.getcwd() + '\\' + filename
    dst = os.getcwd() + '\\' + dst
    # rename() function will
    # rename all the files
    os.rename(src, dst)
    i += 1
print('done')
