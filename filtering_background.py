from PIL import Image
import glob
import numpy as np
import os

images_path = r'E:\wall_segmentation\Images\test\segmented'
out_path = r'E:\wall_segmentation\Images\test\segmented_filtered'

if not os.path.exists(out_path):
    os.makedirs(out_path)

image_files_list = glob.glob(images_path + '/*tif')

for image_file in image_files_list:
    filename = image_file.split('\\')[-1]
    filename = filename.replace('.', '', 1)
    img = Image.open(image_file)

    img = np.array(img)
    if img.mean() > 201:
        continue
    else:
        img = Image.fromarray(img)
        img.save(out_path + '/' + filename)

