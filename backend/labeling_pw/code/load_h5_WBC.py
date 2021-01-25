import numpy as np
import cv2
import h5py
import os, os.path
#from backend import settings


def read_bin(file_path, data_type=np.float32):
    """

    :param file_path:
    :param data_type:
    :return:
    """
    raw = np.fromfile(str(file_path), dtype=data_type)
    width = binary_float_to_int(raw[0])
    height = binary_float_to_int(raw[1])

    image = np.reshape(raw[2:], [height, width])
    return image


def binary_float_to_int(float_number):
    """

    :param float_number:
    :return:
    """
    return ctypes.c_uint.from_buffer(ctypes.c_float(float_number)).value


def unpack_image_from_h5(file_handle, shape, indices, path_template=None):
    if path_template is None:
        path_template = '%d'
    images = []
    for i in indices:
        images.append(np.reshape(data[path_template % i][...], shape))

    return images


def scale_image(image, factor=1.):
    return cv2.resize(image, (0, 0), fx=factor, fy=factor, interpolation=cv2.INTER_AREA)


def meanImage(image_series):
    image_mean = np.median(image_series, axis=2)
    cv2.imwrite('../dataset/mean_Mono_Capture1.png', image_mean)

    return image_series, image_mean


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
        image_raw = image_raw[np.newaxis, ...]
        image_series = np.append(image_series, image_raw, axis=0)
        i = i + 1
    mean_Image = meanImage(image_series)

    return image_series, mean_Image, celltyp


if __name__ == '__main__':
    prepareData()
