import glob
import os
import threading

from PIL import Image


def create_image(infile):
    path, suffix = os.path.splitext(infile)
    print("infile %s, %s" % (path, suffix))
    filename = os.path.basename(infile).replace(suffix, '')
    png_path = path.replace(filename, '') + '/d_png/'
    if not os.path.exists(png_path):
        try:
            os.mkdir(png_path)
        except FileExistsError:
            print('%s exists.' % png_path)
    im = Image.open(infile)
    im.save(png_path + filename + ".png", "PNG")


def start():
    for infile in glob.glob(r'C:\Users\LH\Desktop\222\*.webp'):
        t = threading.Thread(target=create_image, args=(infile,))
        t.start()


if __name__ == '__main__':
    start()
