import getopt
import os
import sys

from PIL import Image


def crop(infile_crop, height_crop, width_crop):
    im = Image.open(infile_crop)
    img_width, img_height = im.size
    for i in range(img_height // height_crop):
        for j in range(img_width // width_crop):
            box = (j * width_crop, i * height_crop, (j + 1) * width_crop, (i + 1) * height_crop)
            yield im.crop(box)


def arg_getter(argv):
    height_arg = ''
    width_arg = ''
    try:
        opts, args = getopt.getopt(argv, "hi:w:", ["height=", "width="])
    except getopt.GetoptError:
        print(os.path.basename(__file__) + ' -i <height_arg> -o <width_arg>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(os.path.basename(__file__) + ' -i <height_arg> -o <width_arg>')
            sys.exit()
        elif opt in ("-i", "--height"):
            height_arg = arg
        elif opt in ("-w", "--width"):
            width_arg = arg
    return int(height_arg), int(width_arg)


if __name__ == '__main__':

    height, width = arg_getter(sys.argv[1:])
    filenames = next(os.walk(os.getcwd()))[2]
    filenames.remove(os.path.basename(__file__))

    start_num = 0
    for f in filenames:
        infile = f
        filename = infile.split('.')
        dir_name = filename[0]
        extension = filename[1]
        if not os.path.isdir(dir_name):
            os.system('mkdir ' + dir_name)
        for k, piece in enumerate(crop(infile, height, width), start_num):
            img = Image.new('RGB', (height, width), 255)
            img.paste(piece)
            path = os.path.join('' + dir_name, filename[0] + "-{}.".format(k) + extension)
            img.save(path)
