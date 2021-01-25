import numpy as np
import cv2
import matplotlib
from matplotlib import pyplot as plt

import os, re, os.path
import time


def showImage(folder, name,img,save = False):
    #cv2.imshow(name, img)
    if save ==True:
        status=cv2.imwrite(folder + str(name)+'.png', img)
        print(str(name)+'.png written to file-system : ', status)
    #cv2.waitKey(0)

def plot (image, name, k, folder, file):
    plt.pcolor(image)  # , cmap = 'hsv' )
    ax = plt.gca()  # get the axis
    ax.set_ylim(ax.get_ylim()[::-1])  # invert the axis
    ax.xaxis.tick_top()  # and move the X-Axis
    ax.yaxis.tick_left()
    plt.title(name + ' ' + str(k) +'th image')
    levels = [0, 1, 2, 3, 4, 5]
    colors = ['antiquewhite', 'navy', 'blue', 'mediumpurple', 'darkorchid']
    cmap, norm = matplotlib.colors.from_levels_and_colors(levels, colors)
    matplotlib.image.imsave(folder + '/' + k + '_' + file + '_vis.png', image, cmap=cmap)#cmaps.viridis)
    print('saved in : '+ folder + '/' + k + '_' + file + '.png')
    plt.show()

#isnt used because from phase data background is already subtracted
def backgroundSubstraction(img, mean_image):
    mean_image = mean_image[..., np.newaxis]
    img = img - mean_image
    #img[img < 0] = 0
    return img

def deleteFiles(mypath):
    #mypath = "my_folder"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))

def labelAreas(list_labels, list_regions, lastEle, image_number, user, dataset_typ, GET_REGIONS, level_num, tooltype):
    print('labelAreas')
    print(GET_REGIONS)
    k = 0
    j = 0
    wrong_label = False
    first_image = False


    SAVE_IMAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Seg_masks_' + user + '_' + dataset_typ + '_' + tooltype)
    #GET_REGIONS= os.path.join(os.path.dirname(os.path.abspath(__file__)), 'label_masks_temp')
    #GET_REGIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Tutorial/mask/first_SingelCells')
    print('level number: ', level_num)
    if (level_num == 4 or level_num == 5 or level_num == 0):
        file = os.path.join(GET_REGIONS, str(image_number) + '_labelregions.npy')
    else:
        file = os.path.join(GET_REGIONS, str(level_num) + 'level_' + str(image_number) + '_labelregions.npy')

    print('File: ', file)
    while not os.path.exists(file):
        time.sleep(1)
    if os.path.isfile(file):
        image_label = np.load(file)   #load LabelMask
    else:
        raise ValueError("%s isn't a file!" % file)

    # because 0-5 reserved for cell labels, imagelabel has value from 0-#numberofareas, can get in conflice with labels for cells
    image_label = image_label * 100

    """for areas labeled whole region, more cells in one box but same label"""
    if list_regions != 'none':
        list_regions = list_regions.split(",")
        if len(list_regions) == 3:
            first_image = True

        while (j < len(list_regions)):
            x_value = round(float(list_regions[j]))
            y_value = round(float(list_regions[j + 1]))
            width = round(float(list_regions[j + 2]))
            height = round(float(list_regions[j + 3]))
            label_str = list_regions[j + 4]
            label_str = label_str.strip()
            print ('data of regions: ', x_value, y_value, width, height, label_str)
            if (label_str == 'Single Cell'):
                label = 1
            elif (label_str == 'Aggregate'):
                label = 2
            elif (label_str == 'Platelet'):
                label = 3
            elif (label_str == 'Background'):
                label = 0
            elif (label_str == 'Other'):
                label = 5
            else:
                print('no label: default label = 0')
                label = 0
            image_label[y_value : y_value + height, x_value : x_value + width][image_label[y_value : y_value + height, x_value : x_value + width] != 0] = label

            box = image_label[y_value : y_value + height, x_value : x_value + width]
            print('max value:', np.argmax(box))
            #image_label_new = image_label
            if lastEle == 'region':
                if np.argmax(box) != 0:
                #if [image_label[y_value : y_value + height, x_value : x_value + width].any() == label]:
                    wrong_label = False
                else:
                    wrong_label = True

            j = j + 5

    """for areas labeled with onyl one cell, crosses labeled"""
    if list_labels != 'none':
        list_labels = list_labels.split(",")
        if len(list_labels) == 3:
            first_image = True

        #print('image label min max after *100: ', image_label.min(), image_label.max())
        while (k < len(list_labels)):
            x_value = list_labels[k]
            y_value = list_labels[k + 1]

            label_str = list_labels[k + 2]
            x_value = round(float(x_value))
            y_value = round(float(y_value))
            pixel_value = image_label[y_value, x_value]
            print(x_value, y_value, label_str)
            label_str = label_str.strip()
            #print(label_str)
            # Singel Cell, Aggregate, Parasite, Background, Other
            if (label_str == 'Single Cell'):
                label = 1
            elif (label_str == 'Aggregate'):
                label = 2
            elif (label_str == 'Platelet'):
                label = 3
            elif (label_str == 'Background'):
                label = 0
            elif (label_str == 'Other'):
                label = 5
            else:
                print('no label: default label = 0')
                label = 0
                    #if pixel_value != 0:
            # appening all pixel_values?
            print('pixelvalues: ', x_value, y_value, pixel_value)

            #only no background label to class
            if lastEle == 'cell':
                print('pixel value: ', pixel_value)
                if pixel_value != 0:
                    print('label area with: ', label)
                    retval, image_label, mask1, rect = cv2.floodFill(image_label, None, (x_value, y_value), label)
                    wrong_label = False
                else:
                    wrong_label = True
            k = k + 3
        #deletes not labeled Areas
    image_label[image_label > 5] = 0 #set all to background
    #SegmentationMask = image_label
    print(image_label.shape)
    SAVE_MASK = os.path.join(SAVE_IMAGES, 'level' + str(level_num) + '_' + str(image_number) + '_SegMask.npy')
    print(SAVE_MASK)
    np.save(SAVE_MASK, image_label)
    #status = cv2.imwrite(os.path.join(SAVE_IMAGES, str(image_number)+'_SegMask.png'), SegmentationMask)
    print('SegMask saved in: ', SAVE_IMAGES)
    print('WRONG LABEL: ', wrong_label)
    #plot(SegmentationMask, 'Segmentation Mask labeled by User', image_number, SAVE_IMAGES, 'SegMask')

    return image_label, wrong_label, first_image



if __name__ == '__main__':
    label_regions = cv2.imread('../dataset/createSegMask/labelregions.png')
    SegmentationMask = labelAreas(label_regions) #, 'dataset/csv/110520_MONO_000'+str(k)+'.csv')
    plot(SegmentationMask, 'Segmentation Mask labeled by User', k, 'SegMask')


