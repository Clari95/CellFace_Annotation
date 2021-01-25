from os import path
import os
from django.conf import settings

import numpy as np
import png
import threading
import hashlib
import h5py
import datetime


def to_json_compatible(obj):
    """
    Converts a given object to json compatible format.
    """
    if isinstance(obj, np.ndarray):
        obj = obj.tolist()
    elif isinstance(obj, np.integer):
        obj = int(obj)
    elif isinstance(obj, np.floating):
        obj = float(obj)
    elif isinstance(obj, datetime.datetime):
        return obj.__str__()
    return obj


def h5group_to_nested_dict(raw_file):
    """
    Recursively construct a nested dictionary corresponding
     to the given .raw file.
    """
    # base case
    if isinstance(raw_file, h5py.Dataset):
        return to_json_compatible(raw_file[()])

    # recursive case
    elif isinstance(raw_file, h5py.Group):
        result = dict()
        for key, val in raw_file.items():
            result[key] = h5group_to_nested_dict(val)

        return result


def hash_string_value(name):
    return hashlib.sha1(name.encode()).hexdigest()


def construct_image_helper(array_data):
    max_arr_data = 4.0  # array_data.max()
    min_arr_data = 0.0  # array_data.min()
    new_arr = np.zeros(shape=array_data.shape, dtype=np.int8)
    for i in range(len(array_data)):
        for j in range(len(array_data[i])):
            clipped_value = min(max_arr_data, max(min_arr_data, array_data[i][j]))
            new_arr[i][j] = 255 - int(255 * clipped_value / 4.0)
            # new_arr[i][j] = int(255 * ((array_data[i][j] - min_arr_data) / (max_arr_data - min_arr_data)))
    return new_arr


def construct_image(image_path, array_data):
    """
    Construct the PNG image from the 2d array of floats and store it.
    :param image_path: the path to the image in the filesystem.
    :param array_data: a 2D array of floats
    :return:
    """
    n_arr_data = construct_image_helper(array_data)
    png_file = png.from_array(n_arr_data, 'L;8')
    png_file.save(image_path)
    return


def get_or_create_image_path(raw_name, raw_file, image_name):
    """
    Returns the path of the preview image to be displayed, in case the image isn't cached, creates a thread to do it.
    :param raw_name: name of the .raw file
    :param raw_file: the .raw file reference
    :param image_name: name of the dataset to search in raw_file['image']
    :return: the path where the image is stored.
    """

    # search in cache folder for the image
    cache_folder = settings.CACHES['default']['LOCATION']
    folder_to_search = hash_string_value(raw_name)
    path_of_images = path.join(cache_folder, folder_to_search)
    # create directory if not exists
    os.makedirs(path_of_images, exist_ok=True)

    preview_img_name = hash_string_value(image_name) + ".png"
    preview_img_path = path.join(path_of_images, preview_img_name)

    if os.path.isfile(preview_img_path):    # image already exists
        return preview_img_path
    else:   # need to create image
        n_arr_data = raw_file['image'][image_name][()]
        threading.Thread(target=construct_image, args=(preview_img_path, n_arr_data,)).start()

    return preview_img_path
