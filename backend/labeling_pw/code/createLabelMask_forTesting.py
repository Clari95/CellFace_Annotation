import cv2
import matplotlib
from matplotlib import pyplot as plt
from skimage.morphology import closing, disk,erosion,dilation,opening
import numpy as np
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
import load_h5_WBC
import os, re, os.path
import xlwt
from xlwt import Workbook
import h5py
from skimage import measure
from PIL import Image as im

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def showImage(name,img,save,folder):
    #cv2.imshow(name, img)
    #img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    #im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    if save ==True:
        status=cv2.imwrite(folder+ '/'+str(name)+'.png', img)
        print(str(name)+'.png written to file-system : ', status)
    #cv2.waitKey(0)

def plot (image, name, k, what, folder):

    plt.pcolor(image)  # , cmap = 'hsv' )
    ax = plt.gca()  # get the axis
    ax.set_ylim(ax.get_ylim()[::-1])  # invert the axis
    ax.xaxis.tick_top()  # and move the X-Axis
    # ax.yaxis.set_ticks(np.arange(0, 16, 1)) # set y-ticks
    ax.yaxis.tick_left()
    plt.title(name + ' ' + str(k) +'th image')

    levels = [0, 1, 2, 3, 4, 5]
    colors = ['antiquewhite', 'navy', 'blue', 'mediumpurple', 'darkorchid']
    cmap, norm = matplotlib.colors.from_levels_and_colors(levels, colors)
    matplotlib.image.imsave(folder + '/' + str(k) + '_image_' + what + '.png', image, cmap='viridis')#cmaps.viridis)
    matplotlib.image.imsave(folder + '/' + str(k) + '_image_' + what + 'classic.png', image, cmap='YlGnBu')  # cmaps.viridis)
    print('saved in: ' +folder +'/' + str(k) +'_image_plot_' + what)
    #plt.savefig(folder +'/' + str(k) +'_image_plot_' + what)
    #plt.show()

def clean_image(image, min_intensity=20, min_size=10, min_max_opt_height=80, min_mean_opt_height=80):
    # remove "almost black" pixels
    # image = self.gs_image
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
    #filtered = cv2.GaussianBlur(image, (filterSize,filterSize),0)
    showImage('1_1', image)
    filtered = cv2.medianBlur(image, filterSize)
    showImage('2_1', filtered)
    adaptive_thresh = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize,
                                            C)
    showImage('3_1', adaptive_thresh)
    ret, thresh_mask = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    showImage('4_1', thresh_mask)
    combi_thresh = cv2.add(thresh_mask, adaptive_thresh)
    return adaptive_thresh

def thresh2(image, filterSize=5, blockSize=21, C=0):
    # Adaptive Thresholding (room for parameter tuning)
    #filtered = cv2.GaussianBlur(image, (filterSize,filterSize),0)
    showImage('1_2', image)
    filtered = cv2.medianBlur(image, filterSize)
    showImage('2_2', filtered)
    adaptive_thresh = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize,
                                            C)
    showImage('3_2', adaptive_thresh)

    return adaptive_thresh


def HoleFill(im_th):  # Method to fill holes potentially resulting from applying adaptive thresholding.
    # Copy the thresholded image.
    im_floodfill = im_th.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255);

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv
    return im_out


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
        path = os.path.join(folder, 'mask/' + str(k) + '_labelregions_Mon.npy')
        labels[labels != 0] = 3
        np.save(path, labels)
        # image = plot(labels, 'seperated objects - watershed', k, 'watershed',folder)

    return image_clean,  labels

def prepareData(dataset_typ):
    # print(settings.MEDIA_ROOT)
    if (dataset_typ == 'Monocytes'):
        path_to_h5 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'RAW/20190522_Dominik_Heim_190522_DH_WB_Mon_0001_Capture_1.phase')
    elif (dataset_typ == 'Neutrophils'):
        path_to_h5 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'RAW/20190516_Dominik_Heim_190516_DH_WB_Neu_0001_Capture_2.phase')
    elif (dataset_typ == 'Eosinophils'):
        path_to_h5 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'RAW/20190516_Dominik_Heim_190516_DH_WB_Eos_0001_Capture_1.phase')
    elif (dataset_typ == 'Lymphocytes'):
        path_to_h5 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'RAW/20190516_Dominik_Heim_190516_DH_WB_Lym_0001_Capture_1.phase')
    else:
        print('wrong dataset_typ')
    string_sep = path_to_h5.split('_')
    celltyp = string_sep[7]
    print('celltyp: ', celltyp)
    print(path_to_h5)
    data = h5py.File(path_to_h5, 'r')
    i = 2
    #image_series = np.empty((0, 384, 512), int)
    image_series = np.array(data['image']['00001'])
    image_series = image_series[np.newaxis, ...]
    while i < 200:
        number_str = '%05d' % i
        image_raw = np.array(data['image'][number_str])
        #print(image_raw.shape)
        image_raw = image_raw[np.newaxis, ...]
        image_series = np.append(image_series, image_raw, axis=0)
        i = i + 1
    #mean_Image = meanImage(image_series)
    mean_Image = 0

    return image_series, mean_Image, celltyp

def deleteFiles(mypath):
    #mypath = "my_folder"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))

def getData():
    SAVE_IMAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'label_mask')
    createLabelMask.deleteFiles(SAVE_IMAGES)

    #just works separate not embedded in the system, incomment import load...

    image_series, mean_image = load_h5_WBC.prepareData()  # mean_image at the moment not used anymore
    deleteFiles(SAVE_IMAGES)
    #image_series, mean_image = load_h5_WBC.prepareData()
    k = 27
    while k < 200:
        img = image_series[:, :, k - 1]
        mask, labels = createMask(img, k, SAVE_IMAGES)
        k = k+1
    return labels

def updateScores(user='', points='', numberCells='', numberRegions=''):


    # Workbook is created
    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1')

    sheet1.write(1, 0, 'name')
    sheet1.write(2, 0, 'points')
    sheet1.write(3, 0, 'CLEMEN TOWN')
    sheet1.write(4, 0, 'RAJPUR ROAD')
    sheet1.write(5, 0, 'CLOCK TOWER')
    sheet1.write(1, 1, user)
    sheet1.write(2, 1, points)
    sheet1.write(0, 3, 'CLEMEN TOWN')
    sheet1.write(0, 4, 'RAJPUR ROAD')
    sheet1.write(0, 5, 'CLOCK TOWER')

    wb.save('xlwt example.xls')

def getAccuracy(SegMask, number, level_num, dataset_typ):
    print('in getAccuracy')
    if level_num != 4 and level_num != 5:
        SOL_PATH =os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Tutorial/solution/' + str(level_num) + '_Level')
        solution = np.load(SOL_PATH +'/' + str(number) + '_SegMask.npy')
    elif level_num == 4 or level_num == 5:
        print('in calc accuracy for level with image number ', level_num, number)
        SOL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'solution/Seg_masks_solution_' + dataset_typ + '/level0_' + str(number) + '_SegMask.npy')
        solution = np.load(SOL_PATH)
        print('solition size: ', solution.shape[0])
    #IoU
    target = solution
    prediction = SegMask
    intersection = np.logical_and(target, prediction)
    union = np.logical_or(target, prediction)
    iou_score = np.sum(intersection) / np.sum(union)
    print(bcolors.OKGREEN + 'iou_score ' + str(iou_score) + bcolors.ENDC)

    """not usfull just binary"""
    #hamming_loss = sklearn.metrics.hamming_loss(solution, SegMask)
    #print(bcolors.OKGREEN + 'hamming_loss ' + str(hamming_loss) + bcolors.ENDC)

    #accuracy_score = sklearn.metrics.accuracy_score(solution, SegMask, normalize=False)
    #print(bcolors.OKGREEN + 'accuracyScore ' + str(accuracy_score) + bcolors.ENDC)


    # how many labels compared to solution
    num_labels_sol = measure.label(solution)
    num_labels_sol = num_labels_sol.max()
    print('number of labeld areas Solution: ', num_labels_sol)
    num_labels = measure.label(SegMask)
    num_labels = num_labels.max()
    print('number of labeld areas by user: ', num_labels)

    if num_labels_sol != 0:
        accuracy_numlabels = num_labels / num_labels_sol
    else:
        accuracy_numlabels = 0

    print(bcolors.WARNING + 'accuracys for image ' + str(number))
    print('accuracy num of labels of all possibel num of labels: ', accuracy_numlabels)

    solution_ref = np.copy(solution)
    SegMask_ref = np.copy(SegMask)
    # how many areas are not labeld or labeld wrong
    solution[solution != 0] = 1  #alle possible labeled pixel
    SegMask[SegMask != 0] = 1 # alle tatsächlich gelabelden pixel
    # all not labeled areas undependend of label
    diff_pixel = solution - SegMask
    # fehlende pixel
    pixel_nonzero = np.count_nonzero(diff_pixel)
    accuracy_pixel = ((384 * 512) - pixel_nonzero) / (384 * 512)
    print('accuracy labeled pixel of all possible to labeled pixel: ', accuracy_pixel)

    #how many worng labels
    mask = np.where(diff_pixel != 0, 0, solution_ref)
    diff_label = mask - SegMask_ref
    nonzero = np.count_nonzero(diff_label)
    #diff[diff !=0] = 1;
    wrong_labels = measure.label(diff_label)
    wrong_labels = wrong_labels.max()
    print('wronglabels in acciúracy: ', wrong_labels)
    accuracy_correctlabels = (num_labels - wrong_labels) / num_labels
    print('accuracy correct labeld cells out of alle labeld cells: ' + str(accuracy_correctlabels) + bcolors.ENDC)

    return accuracy_numlabels, accuracy_pixel, accuracy_correctlabels

def recalculationAcc():
    names = ['Katharina', 'Konstantin', 'Annkatrin La',
             'simon',
             'Jakob',
             'Fabian',
             'Damian',
             'Maria Arnas',
             'Sophia',
             'johanna_erber',
             'Alina',
             'palmermax',
             'marty', 'Jonny']
    all = []
    for name in names:
        folder = '/home/clari/Schreibtisch/Master/Thesis/UserResults/Basic/Seg_masks_' + name + '_Neutrophils_basic'
        i = 11
        accuracy = []
        accuracy_correct = []
        sum = 0
        sum_corr = 0
        while i < 21:
            file = folder + '/level0_' + str(i) + '_SegMask.npy'
            if os.path.isfile(file):
                SegMask = np.load(file)
                accuracy_numlabels, accuracy_pixel, accuracy_correctlabels = getAccuracy(SegMask, i, 5, 'Neutrophils')
                print(accuracy_numlabels, accuracy_pixel, accuracy_correctlabels)
                accuracy.append(accuracy_numlabels)
                accuracy_correct.append(accuracy_correctlabels)
                sum = sum + accuracy_numlabels
                sum_corr = sum_corr + accuracy_correctlabels
            i = i + 1
        accuracy.append(1.0)
        sum = sum + 1.0
        sum_corr = sum_corr + 1.0
        print(accuracy)

        # sum = sum(int(i) for i in accuracy)
        # print(int(i) for i in accuracy)
        print(sum)
        print('accuracy: ' + str(sum / 10))
        print('accuracy_corr: ' + str(sum_corr / 10))
        all.append([sum / 10, sum_corr / 10])
    print(all)

    return all

def generatePlots(folder):
    i = 21
    """
    while i < 11:
        #/home/clari/Schreibtisch/Master/Thesis/UserResults/Basic/Seg_masks_Alina_Neutrophils_basic
        file = folder + '/level4_'+str(i)+'_SegMask.npy'
        if os.path.isfile(file):
            img =np.load(file)
        #cv2.imwrite(folder + '/testlevel4.png', img)
            plot(img, 'result', i, 'result', folder)
        i = i +1
    """
    while i < 22:
        #/home/clari/Schreibtisch/Master/Thesis/UserResults/Basic/Seg_masks_Alina_Neutrophils_basic
        file = folder + '/level0_' +str(i) +'_SegMask.npy'  #modified'+str(i)+'.png'
        if True: #os.path.isfile(file):
            #img =np.load(file)
            img= np.zeros((384,512))
            print(img.shape)
            img[:,0:102] = 0
            img[:,103:204] = 1
            img[:,205:306] = 2
            img[:,307:408] = 3
            img[:,409:512] = 5
            plot(img, 'test', i, 'test', folder)
        i = i + 1

if __name__ == '__main__':

    """
    image_series, mean_image = load_h5_WBC.prepareData()
    img = image_series[:, :, 1]
    print(img.shape)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    """
    # folder = '/home/clari/PycharmProjects/cellphaser/backend/labeling_pw/code/solution/Seg_masks_solution_Neutrophils'
    folder = '/home/clari/Schreibtisch/Master/Thesis/UserResults/orginal'#Basic/Seg_masks_Sophia_Neutrophils_basic'

    #recalculationAcc()
    generatePlots(folder)

    k = 22
    while k < 21:
        image_series, mean_Image, celltyp = prepareData('Neutrophils')
        img = image_series[k - 1, :, :]
        cv2.imwrite(folder +'/image_' + str(k)+'.png', img)
        k = k +1
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #createMask(img, k, folder)
    #print(folder + '/img/image_' + str(k))
    #np.save(folder + '/img/Mon_image_' + str(k) + '.npy', img)



    """
    k=1
    while k<4:
        path = '/home/clari/PycharmProjects/cellphaser/backend/labeling_pw/code/Seg_masks_clarissa_Neutrophils/'+ str(k)+'_SegMask.npy'
        #path = '/home/clari/Schreibtisch/Master/Forschungspraxis/Seg_masks_user/Seg_masks_AMRI/'+ str(k)+'_SegMask.png'

        path2 = '/home/clari/PycharmProjects/cellphaser/backend/labeling_pw/code/Seg_masks_clarissa_Neutrophils'
        im = cv2.imread(path)
        #print(im)
        im = np.load(path)
        #im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('test',im)
       #print(im.shape)
        plot(im,'test',k,'test',path2)
        
        print(im.max())
        print(im.min())
        colors, counts = np.unique(im.reshape(-1, 3),
                                   return_counts=True,
                                   axis=0)
        print(colors)
        print(counts)
        print(np.count_nonzero((im == [0]).all))
        print(np.count_nonzero((im == [1]).all))
        print(np.count_nonzero((im == [2]).all))
        
        k = k + 1
    """

      # .meanImage('dataset/RAW/20190522_Dominik Heim_190522_DH_WB_Mon_0001_Capture 1-LAPTOP-LLI8UF8G.phase')
    #img = image_series[:, :, k - 1]
    #createMask(img, k, SAVE_IMAGES)

