import os
import subprocess
import sys

try:
    import image_slicer
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'image-slicer'])
finally:
    import image_slicer
if __name__ == '__main__':
    num_splits = int(sys.argv[1])
    filenames = next(os.walk(os.getcwd()))[2]
    filenames.remove(os.path.basename(__file__))
    i = 0
    for f in filenames:
        tiles = image_slicer.slice(f, num_splits, save=False)
        dir_name = f.split('.')[0]
        if not os.path.isdir(dir_name):
            os.system('mkdir ' + dir_name)
        image_slicer.save_tiles(tiles, directory=(os.getcwd() + '\\' + dir_name), prefix=dir_name)
        i = i + 1
    print('{} files successful split into {} each'.format(i, num_splits))
    # final = image_slicer.join(tiles)
    # if not os.path.isdir('frame_final'):
    #     os.system('mkdir ' + 'frame_final')
    # image = image_slicer.join(tiles)
    # image.save('modified_frame.tif')
