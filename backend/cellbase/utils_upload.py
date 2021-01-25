from os import path
from pathlib import Path

import numpy as np
import ctypes
import h5py
import json
import re
import os
import fnmatch
import xmltodict
import shutil

from django.core.files.uploadhandler import FileUploadHandler
from django.core.files.uploadedfile import UploadedFile
from django.core.files import temp as tempfile
from django.conf import settings

# Error Logging
import logging
logging.basicConfig(filename='views_error.log',level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

from background_task import background
from .models import Dataset, Tag, Project, DatasetTag, PhaseDataset

N_median = 50  # later we can make it an argument

# UTILS ################################################################################################################
# from Stefan's h5 repository
def binary_float_to_int(b_number):
    """
    :param b_number: a floating point number encoded as binary.
    :return: the corresponding float value.
    """
    return ctypes.c_uint.from_buffer(ctypes.c_float(b_number)).value


# from Stefan's h5 repository (adapted)
def read_bin(file_bytes):
    """
    :param file_bytes: bytes of a .bin file.
    :return: the matrix of numbers that represent an image
    """
    raw = np.frombuffer(file_bytes, dtype=np.float32)
    width = binary_float_to_int(raw[0])
    height = binary_float_to_int(raw[1])
    image = np.reshape(raw[2:], [height, width])
    return image

def generate_aggregate_statistics(raw_file):
    """
    Generates aggregate statistics on the dataset
    and saves it on the metadata/statistics group.
     min, max, quartiles,
     average, std_deviation,
     histogram
    """
    meta_group = raw_file['meta']
    images = [img[()] for img in raw_file['image'].values()]
    stats_group = meta_group.create_group('statistics')

    frequencies, boundaries = np.histogram(images)
    stats_group.create_dataset('hist_frequencies', data=frequencies)
    stats_group.create_dataset('hist_boundaries', data=boundaries)

    stats_group.create_dataset('min', data=np.min(images))
    stats_group.create_dataset('max', data=np.max(images))
    stats_group.create_dataset('average_val', data=np.average(images))
    stats_group.create_dataset('average', data=np.average(images, axis=0))
    stats_group.create_dataset('std', data=np.std(images))

# handle_upload_bin_folder #############################################################################################
@background #(schedule=10)
def handle_upload_bin_folder(user, title, temporary_file_path): #(name, xml_file, bin_files, project, tags, fs_path=""):
    """
    :param user: user, who created task (not used in function, important for status of tasks)
    :param title: title of new dataset (not used in function, important for status of tasks)
    :param temporary_file_path: file path of temporary json file containing all parameter (name,project,tags,fs_path,xml_data,bin_fs_names,bin_fs_paths)
    """
    logging.info(f'Temporary file path: {temporary_file_path}')
    try:
        # load from temporary file
        with open(temporary_file_path) as json_file:
            name,project,tags,fs_path,xml_data,bin_fs_names,bin_fs_paths = json.load(json_file)
        # delete temporary file
        os.remove(temporary_file_path)

        logging.info(f'bin_fs_names: {bin_fs_names}, bin_fs_paths: {bin_fs_paths}')

        # DB: Dataset
        dataset = Dataset()
        dataset.name = name
        dataset.path = path.join(fs_path, name + ".raw")
        dataset.save()
        # DB: Project
        project_ds = Project()
        project_ds.dataset = dataset
        project_ds.project_name = project
        project_ds.save()
        # DB: Tag and DatasetTag
        for tag_text in tags:
            tag_ds, created = Tag.objects.get_or_create(tag_name=tag_text)
            dataset_tag = DatasetTag(dataset=dataset, tag=tag_ds)
            dataset_tag.save()

        # XML
        xml_retrieved_info = {
            'capture': {},
            'microscope': {},
            'camera': {},
            'laser': {},
            'objective': {},
            'reconstruction': {}
        }
        for sub_group in xml_retrieved_info:
            sub_group_data = xml_data['meta_data_conf']['dhm_ovizio_data'][sub_group]
            xml_retrieved_info[sub_group] = dict(sub_group_data)

        # ensure directory exists (if it doesn't, creates it)
        Path(fs_path).mkdir(parents=True, exist_ok=True)
        # create RAW file
        raw_file_path = path.join(fs_path, name)
        try:
            raw_file = h5py.File(raw_file_path + ".raw", 'w-')
        except OSError:
            return False
        # create all the groups
        h5_image_group = raw_file.create_group("image")
        h5_meta_group = raw_file.create_group("meta")
        raw_file.create_group("label")  # not doing anything here, just creating

        # fill the images
        median_images = []
        n_files, f_shape = 0, (0, 0)
        for up_file_name, up_file_path in zip(bin_fs_names, bin_fs_paths):
            up_file = open(up_file_path, 'rb')
            up_name = str(int(re.findall('t((\d)+)_', up_file_name)[0][0])).zfill(5)
            bin_data = up_file.read()
            bin_data_handled = read_bin(bin_data)
            # create dataset with all information and image data
            try:
                h5_image_group.create_dataset(name=up_name,
                                              data=bin_data_handled,
                                              compression="gzip",
                                              compression_opts=2)
                n_files += 1
                f_shape = bin_data_handled.shape if n_files == 1 else f_shape  # update only at the first image
                if n_files <= N_median:
                    median_images.append(bin_data_handled)
            except RuntimeError:
                pass
            # remove temporary bin file
            os.remove(up_file_path)

        # fill "meta" group
        median = np.median(np.asarray(median_images), axis=0)
        h5_meta_group.create_dataset("n_files", data=n_files)
        h5_meta_group.create_dataset("img_size", data=f_shape)
        h5_meta_group.create_dataset("type", data="none")
        h5_meta_group.create_dataset("version", data="none")
        h5_meta_group.create_dataset("xml", data=json.dumps(xml_retrieved_info))
        h5_meta_group.create_dataset("background", data=median)

        ## Gather aggregate statistics
        generate_aggregate_statistics(raw_file)

        # close container file
        raw_file.close()

    except Exception as e:
        logging.exception("message")

    return True

# handle folder upload
@background #(schedule=10)
def upload_folder_process_upload(user, name, project, tags, dirpath):
    """
    :param user: user, who created task (not used in function, important for status of tasks)
    :param title: title of new dataset (also important for status of tasks)
    :param project: ...
    :param tags: ...
    :param dirpath: ...
    """
    #TODO: check if working correctly

    # extract file names and paths of bin files (and xml file)
    all_fs = os.listdir(dirpath)
    xml_f_path = os.path.join(dirpath, fnmatch.filter(all_fs, '*.xml')[0])
    bin_fs_paths = [os.path.join(dirpath, f) for f in fnmatch.filter(all_fs, '*.bin')]

    # read xml file
    xml_f = open(xml_f_path,'rb')
    xml_data = xmltodict.parse(xml_f)
    xml_f.close()

    # set path for h5
    fs_path = path.join(settings.MEDIA_ROOT, project)

    # XML
    xml_retrieved_info = {
        'capture': {},
        'microscope': {},
        'camera': {},
        'laser': {},
        'objective': {},
        'reconstruction': {}
    }
    for sub_group in xml_retrieved_info:
        sub_group_data = xml_data['meta_data_conf']['dhm_ovizio_data'][sub_group]
        xml_retrieved_info[sub_group] = dict(sub_group_data)

    # ensure directory exists (if it doesn't, creates it)
    Path(fs_path).mkdir(parents=True, exist_ok=True)
    # create RAW file
    raw_file_path = path.join(fs_path, name)
    try:
        raw_file = h5py.File(raw_file_path + ".raw", 'w-')
    except OSError:
        return False
    # create all the groups
    h5_image_group = raw_file.create_group("image")
    h5_meta_group = raw_file.create_group("meta")
    raw_file.create_group("label")  # not doing anything here, just creating

    # fill the images
    median_images = []
    n_files, f_shape = 0, (0, 0)
    for up_file_path in bin_fs_paths:
        up_file = open(up_file_path, 'rb')
        up_name = str(int(re.findall('t((\d)+)_', up_file.name)[0][0])).zfill(5)
        bin_data = up_file.read()
        bin_data_handled = read_bin(bin_data)
        # create dataset with all information and image data
        try:
            h5_image_group.create_dataset(name=up_name,
                                          data=bin_data_handled,
                                          compression="gzip",
                                          compression_opts=2)
            n_files += 1
            f_shape = bin_data_handled.shape if n_files == 1 else f_shape  # update only at the first image
            if n_files <= N_median:
                median_images.append(bin_data_handled)
        except RuntimeError:
            pass
        up_file.close()

    # fill "meta" group
    median = np.median(np.asarray(median_images), axis=0)
    h5_meta_group.create_dataset("n_files", data=n_files)
    h5_meta_group.create_dataset("img_size", data=f_shape)
    h5_meta_group.create_dataset("type", data="none")
    h5_meta_group.create_dataset("version", data="none")
    h5_meta_group.create_dataset("xml", data=json.dumps(xml_retrieved_info))
    h5_meta_group.create_dataset("background", data=median)

    ## Gather aggregate statistics
    generate_aggregate_statistics(raw_file)

    # close container file
    raw_file.close()

    # DB: Dataset
    dataset = Dataset()
    dataset.name = name
    dataset.path = path.join(fs_path, name + ".raw")
    dataset.save()
    # DB: Project
    project_ds = Project()
    project_ds.dataset = dataset
    project_ds.project_name = project
    project_ds.save()
    # DB: Tag and DatasetTag
    for tag_text in tags:
        tag_ds, created = Tag.objects.get_or_create(tag_name=tag_text)
        dataset_tag = DatasetTag(dataset=dataset, tag=tag_ds)
        dataset_tag.save()

    # delete temp folder (including bin files and xml file)
    shutil.rmtree(dirpath)

    return True


# TEMPORARY FILE HANDLER ###############################################################################################
class TemporaryFileUploadHandler(FileUploadHandler):
    """
    Upload handler that streams data into a temporary file.
    """
    def new_file(self, *args, **kwargs):
        """
        Create the file object to append to as data is coming in.
        """
        super().new_file(*args, **kwargs)
        self.file = TemporaryUploadedFile(self.file_name, self.content_type, 0, self.charset, self.content_type_extra)

    def receive_data_chunk(self, raw_data, start):
        self.file.write(raw_data)

    def file_complete(self, file_size):
        self.file.seek(0)
        self.file.size = file_size
        return self.file

class TemporaryUploadedFile(UploadedFile):
    """
    A file uploaded to a temporary location (i.e. stream-to-disk).
    """
    def __init__(self, name, content_type, size, charset, content_type_extra=None):
        _, ext = os.path.splitext(name)
        file = tempfile.NamedTemporaryFile(suffix='.upload' + ext, dir=settings.FILE_UPLOAD_TEMP_DIR, delete=False)     #delete=False to deactivate automatic deleting of temp files
        super().__init__(file, name, content_type, size, charset, content_type_extra)

    def temporary_file_path(self):
        """Return the full path of this file."""
        return self.file.name


    def close(self):
        try:
            return self.file.close()
        except FileNotFoundError:
            # The file was moved or deleted before the tempfile could unlink
            # it. Still sets self.file.close_called and calls
            # self.file.file.close() before the exception.
            pass