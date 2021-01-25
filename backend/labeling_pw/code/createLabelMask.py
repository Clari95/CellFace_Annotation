import cv2
import matplotlib
from matplotlib import pyplot as plt
from skimage.morphology import closing, disk,erosion,dilation,opening
import numpy as np
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
#import load_h5_WBC
import os, re, os.path
from skimage import measure

def showImage(name,img,save = False):
    #cv2.imshow(name, img)
    if save ==True:
        status=cv2.imwrite('../dataset/createSegMask/'+str(name)+'.png', img)
        print(str(name)+'.png written to file-system : ', status)
    #cv2.waitKey(0)

def plot (image, name, k, what, folder):

    plt.pcolor(image)  # , cmap = 'hsv' )
    ax = plt.gca()  # get the axis
    ax.set_ylim(ax.get_ylim()[::-1])  # invert the axis
    ax.xaxis.tick_top()  # and move the X-Axis
    ax.yaxis.tick_left()
    plt.title(name + ' ' + str(k) +'th image')
    levels = [0, 1, 2, 3, 4, 5]
    colors = ['antiquewhite', 'navy', 'blue', 'mediumpurple', 'darkorchid']
    cmap, norm = matplotlib.colors.from_levels_and_colors(levels, colors)
    # matplotlib.image.imsave(folder + '/' + str(k) + '_image_' + what + '.png', image, cmap=cmap)#cmaps.viridis)
    # print('saved in: ' +folder +'/' + str(k) +'_image_plot_' + what)

    return image

def clean_image(image, min_intensity=20, min_size=10, min_max_opt_height=80, min_mean_opt_height=80):
    image[image <= 20] = 0
    # Remove small objects not connected to anything
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
    # connectedComponentswithStats yields every seperated component with information on each of them, such as size
    sizes = stats[1:, -1];
    nb_components = nb_components - 1

    image_cleaned = np.zeros((output.shape))
    # for every component in the image, you keep it only if corresponds to the defined criteria
    for i in range(0, nb_components):
        if sizes[i] >= min_size and (np.mean(image[output == i + 1]) >= min_mean_opt_height or np.max(
                image[output == i + 1]) >= min_max_opt_height):
            image_cleaned[output == i + 1] = image[output == i + 1]
    image = image_cleaned.astype(np.uint8)

    return image


def thresh(image, filterSize=5, blockSize=21, C=0):
    # Adaptive Thresholding (room for parameter tuning)
    # filtered = cv2.GaussianBlur(image, (filterSize,filterSize),0)
    filtered = cv2.medianBlur(image, filterSize)

    adaptive_thresh = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize,
                                            C)
    return adaptive_thresh


def watershed_func(mask, min_distance=2, blur=True):
    # watershade: separates different objects in an image
    distance = ndi.distance_transform_edt(mask)
    if (blur == True):
        distance = cv2.GaussianBlur(distance, (3, 3), 0)
    local_maxi = peak_local_max(distance, indices=False,
                                labels=mask, footprint=np.ones((3, 3)))
    markers = ndi.label(local_maxi, structure=np.ones((3, 3)))[0]
    labels = watershed(-distance, markers, mask=mask)
    return labels


def createMask(img, k, folder):
    image_clean = clean_image(img, min_intensity=20, min_size=140, min_max_opt_height=100, min_mean_opt_height=100)
    image = thresh(image_clean, filterSize=3, blockSize=25, C=0)  # kernelSize max 3!!
    mask = dilation(image, disk(1))
    #watershed transform
    labels = watershed_func(mask, blur=True)
    if folder != 'none':
        path = os.path.join(folder, str(k) + '_labelregions.npy')
        labels[labels != 0] = 3
        np.save(path, labels)
        # image = plot(labels, 'seperated objects - watershed', k, 'watershed',folder)

    #labels_num = measure.label(labels)

    return image_clean,  labels

def deleteFiles(mypath):
    #mypath = "my_folder"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            #print("all files deleted")
            os.remove(os.path.join(root, file))

def getData():
    SAVE_IMAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'label_masks')
    # createLabelMask.deleteFiles(SAVE_IMAGES)

if __name__ == '__main__':

    getData()
