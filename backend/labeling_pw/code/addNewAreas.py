#import load_h5_WBC
import cv2
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import os, os.path

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def plot (image, name, k, folder):

    plt.pcolor(image)  # , cmap = 'hsv' )
    ax = plt.gca()  # get the axis
    ax.set_ylim(ax.get_ylim()[::-1])  # invert the axis
    ax.xaxis.tick_top()  # and move the X-Axis
    ax.yaxis.tick_left()
    plt.title(name + ' ' + str(k) +'th image')
    levels = [0, 1, 2, 3, 4, 5]
    colors = ['antiquewhite', 'navy', 'blue', 'mediumpurple', 'darkorchid']
    cmap, norm = matplotlib.colors.from_levels_and_colors(levels, colors)
    matplotlib.image.imsave(folder + '/' + str(k) + '_image_' + name + '.png', image, cmap=cmap)#cmaps.viridis)
    print('saved in: ' +folder +'/' + str(k) +'_image_plot_' )

def start(im, number, data, folder):
    # 257, 328, 242, 58, 37, 233
    im_thresh = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize=21,C=0)

    #cv2.imwrite(folder + '/' + str(number) + 'test.png', adaptive_thresh)
    print('add new areas for image ' + str(number) + ' with ' + data)
    k = 0
    label = 3
    list_labels = data.split(",")
    all_pixel_values = []
    wrong_area = False

    while k < len(list_labels):
        x_value = int(float(list_labels[k]))
        y_value = int(float(list_labels[k + 1]))
        pixel_value = im[y_value, x_value]
        #appening all pixel_values?
        print('pixelvalues: ', x_value, y_value, pixel_value)

        if pixel_value > 25:
            print('pixel value not zero')
            retval, im_thresh, mask1, rect = cv2.floodFill(im_thresh, None, (x_value, y_value), label)
            wrong_area = False
        else:
            print('pixel value zero means background')
            wrong_area = True
        all_pixel_values.append(pixel_value)
        k = k + 2
        #label = label + 1

    #if folder != 'none':
     #   path = os.path.join(folder, str(number) + '_labelregions.npy')
        #path2 = os.path.join(folder, 'labelregions.npy')
        #print('Info Labelregions min max : ', labels.min(), labels.max())
        #np.save(path, im_thresh)
    #status = cv2.imwrite('/home/clari/PycharmProjects/cellphaser/backend/labeling_pw/code/test/newareas_' + str(number) + '.png', im_thresh)
    #print('.png written to file-system : ', status)
    im_thresh[im_thresh == 255] = 0 #0 is background
    number_newareas = len(list_labels) / 2
    im_thresh[im_thresh != 3] = 0
    #folder = '/home/clari/PycharmProjects/cellphaser/backend/labeling_pw/code/label_masks_addedregions'
    #name = 'LabelMask_newareas'
    #plot(im_thresh, name, number, folder)

    return im_thresh, wrong_area

if __name__ == '__main__':
    # image_series, mean_image = load_h5_WBC.prepareData()
    image = cv2.imread('/home/clari/PycharmProjects/cellphaser/frontend/src/assets/example_images/Mono_00002.png')
    cv2.imshow('image2', image)
    start(image, 2, [257, 328, 242, 58, 37, 233])
