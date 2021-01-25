import numpy as np
import cv2
import os, re, os.path
from skimage import measure
import sklearn
from sklearn.metrics import hamming_loss
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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

def getAccuracy_final(solutions, references, numberImages, level_num):
    print('in getAccuracy final')
    #SOL_PATH =os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Tutorial/solution/' + str(level_num) + '_Level')
    #solution = np.load(SOL_PATH +'/' + str(number) + '_SegMask.npy')
    accuracy = []
    accuracy_numlabels_all = []
    accuracy_pixel_all = []
    accuracy_correctlabel_all = []
    if level_num == 5:
        solutions = solutions[10:20, :, :]
    print('shape of referernce vs number Images vs. size solution: ', references.shape[0], numberImages, solutions.shape[0])
    for x in range(references.shape[0]):
        solution = solutions[x, :, :]
        reference = references[x, :, :]
    # how many labels compared to solution
        num_labels_sol = measure.label(solution)
        num_labels_sol = num_labels_sol.max()
        if num_labels_sol == 0:
            print('no info in image')
            accuracy_numlabels = 0
        else:
            #print('number of labeld areas Solution: ', num_labels_sol)
            num_labels = measure.label(reference)
            num_labels = num_labels.max()
            #print('number of labeld areas by user: ', num_labels)

            accuracy_numlabels = num_labels / num_labels_sol

            #print(bcolors.WARNING + 'accuracies for image ' + str(x) + bcolors.ENDC)
            #print(bcolors.WARNING + 'accuracy num of labels of all possible num of labels: ', accuracy_numlabels)

            solution_copy = np.copy(solution)
            reference_copy = np.copy(reference)
            # how many areas are not labeld or labeld wrong
            solution[solution != 0] = 1  #alle zu labelde pixel
            reference[reference != 0] = 1 # alle gelabelde pixel
            # all not labeled areas undependend of label
            diff_pixel = solution - reference
            # fehlende pixel
            pixel_nonzero = np.count_nonzero(diff_pixel)
            accuracy_pixel = ((384 * 512) - pixel_nonzero) / (384 * 512)
            #print('accuracy labeled pixel of all possible to lebel pixel: ', accuracy_pixel)

            #how many worng labels
            mask = np.where(diff_pixel != 0, 0, solution_copy)
            diff_label = mask - reference_copy
            nonzero = np.count_nonzero(diff_label)
            #diff[diff !=0] = 1;
            wrong_labels = measure.label(diff_label)
            wrong_labels = wrong_labels.max()
            #nothing labeled
            if num_labels == 0:
                accuracy_correctlabels = 0
                #print('set accuracy correct labels to zero because nothing labels in image by user')
            else:
                #print('data correct', num_labels, wrong_labels)
                accuracy_correctlabels = (num_labels - wrong_labels) / num_labels
                #print(accuracy_correctlabels)
            #print( 'accuracy correct labeled cells out of alle labeld cells: ' + str(accuracy_correctlabels) + bcolors.ENDC)
            average = (accuracy_numlabels + accuracy_correctlabels) / 2
            accuracy.append(average)
            accuracy_numlabels_all.append(accuracy_numlabels)
            accuracy_pixel_all.append(accuracy_pixel)
            accuracy_correctlabel_all.append(accuracy_correctlabels)
            #print('correct labeled: ', accuracy_correctlabel_all)

    #average over all labled images in this sesssion for all different accuracys in list
    if (numberImages != 0):
        accuracy_all = buildAverage(accuracy, accuracy_numlabels_all, accuracy_pixel_all, accuracy_correctlabel_all, numberImages)
    else:
        accuracy_all = [0, 0, 0, 0]
    print(bcolors.OKGREEN + 'accuracy average for all images: ' + str(accuracy_all) + bcolors.ENDC)

    return accuracy_all

def buildAverage(accuracy, accuracy_numlabels, accuracy_pixel, accuracy_correctlabels, numberImages):
    accuracy_overall = 0
    print('number images in building average: ', numberImages)
    # i = 0
    #print(accuracy)
    for x in accuracy:
        accuracy_overall = accuracy_overall + x
    accuracy = accuracy_overall / numberImages
    #print('accuracy over all images: ', accuracy)

    accuracy_numlabels_overall = 0
    for x in accuracy_numlabels:
        accuracy_numlabels_overall = accuracy_numlabels_overall + x
        # i += 1
    accuracy_numlabels = accuracy_numlabels_overall / numberImages
    print('accuracy number of labels over all images: ', accuracy_numlabels)

    accuracy_pixel_overall = 0
    for x in accuracy_pixel:
        #print(x)
        accuracy_pixel_overall = accuracy_pixel_overall + x
        # i += 1
    accuracy_pixel = accuracy_pixel_overall / numberImages
    print('accuracy pixel over all images: ', accuracy_pixel)

    accuracy_correctlabels_overall = 0
    #print('correct labels list:', accuracy_correctlabels)
    for x in accuracy_correctlabels:
        print(x)
        accuracy_correctlabels_overall = accuracy_correctlabels_overall + x
        # i += 1
    accuracy_correctlabels = accuracy_correctlabels_overall / numberImages
    print('accuracy correct labels over all images: ', accuracy_correctlabels)

    accuracy_all = [accuracy_numlabels, accuracy_pixel, accuracy_correctlabels, accuracy]

    return accuracy_all

def dice_metric(inputs, target):
    intersection = 2.0 * (target * inputs).sum()
    union = target.sum() + inputs.sum()
    if target.sum() == 0 and inputs.sum() == 0:
        return 1.0

    return intersection / union

def dice_loss(inputs, target):
    num = target.size(0)
    inputs = inputs.reshape(num, -1)
    target = target.reshape(num, -1)
    smooth = 1.0
    intersection = (inputs * target)
    dice = (2. * intersection.sum(1) + smooth) / (inputs.sum(1) + target.sum(1) + smooth)
    dice = 1 - dice.sum() / num
    return dice

def bce_dice_loss(inputs, target):
    dicescore = dice_loss(inputs, target)
    bcescore = nn.BCELoss()
    bceloss = bcescore(inputs, target)

    return bceloss + dicescore

if __name__ == '__main__':
    label_regions = cv2.imread('../dataset/createSegMask/labelregions.png')
    SegmentationMask = labelAreas(label_regions) #, 'dataset/csv/110520_MONO_000'+str(k)+'.csv')
    plot(SegmentationMask, 'Segmentation Mask labeled by User', k, 'SegMask')


