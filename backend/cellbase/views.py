from django.http import HttpResponse, JsonResponse
from os import path
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import Http404

from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .models import Dataset, Tag, Project, DatasetTag, PhaseDataset
from .utils_upload import handle_upload_bin_folder, TemporaryFileUploadHandler, upload_folder_process_upload
from .utils_preview import h5group_to_nested_dict
from django.core.exceptions import ObjectDoesNotExist

import magic as magic_unix
import h5py
import json
import numpy as np
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from background_task import background
from background_task.models import Task, CompletedTask

from os import path, remove
from pathlib import Path
import tempfile
import os
import fnmatch
import time

import xmltodict
import numpy as np
import ctypes
import h5py
import json
import re

# Error Logging
import logging
logging.basicConfig(filename='views_error.log',level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# EXPLORER #############################################################################################################

@require_GET
# @login_required
def explore(request, f_path=''):
    '''
    View that returns the information of the current directory in the filesystem.
    :param request: request information.
    :param f_path: relative filepath from the URL.
    :return: an array of JSON objects that represent the characteristics of the files/directories in the current path.
    '''
    f_path = f_path.split('/')  # splitting just in case the OS doesn't use unix
    current_folder_path = path.join(settings.MEDIA_ROOT, *f_path)

    # open the current folder using Django specific classes.
    current_folder = FileSystemStorage(
        location=current_folder_path,
        file_permissions_mode=0o644,
        directory_permissions_mode=0o644
    )

    # current_folder_info: [[folder1, folder2, ...], [file1, file2, ...]]
    current_folder_info = [[], []]
    try:
        current_folder_info = current_folder.listdir(path='.')
    except NotADirectoryError:
        raise Http404('Not a Directory')

    # store data of present folder
    folder_data = []
    for f_name in current_folder_info[0]:   # reading folders
        folder_data.append({
            'name': f_name,
            'is_folder': True,
            'created': current_folder.get_created_time(name=f_name),
            'modified': current_folder.get_modified_time(name=f_name),
            'accessed': current_folder.get_accessed_time(name=f_name),
        })

    # update file's information
    for f_name in current_folder_info[1]:  # reading files
        file_path = path.join(current_folder_path, f_name)

        ## Fetch tags
        try:
            obj = Dataset.objects.get(path=file_path)
            obj_tags = DatasetTag.objects.filter(dataset_id=obj.id)
            tags = [Tag.objects.get(id=el.tag_id).tag_name for el in obj_tags]
        except ObjectDoesNotExist:
            tags = []

        # get file type using specific library
        type_file = magic_unix.from_file(filename=file_path)
        type_file_mime = magic_unix.from_file(filename=file_path, mime=True)
        folder_data.append({
            'name': f_name,
            'is_folder': False,
            'created': current_folder.get_created_time(name=f_name),
            'modified': current_folder.get_modified_time(name=f_name),
            'accessed': current_folder.get_accessed_time(name=f_name),
            'size': current_folder.size(name=f_name),
            'type': type_file,
            'type/mime': type_file_mime,
            'tags': tags
        })

    return JsonResponse({'response': folder_data}, safe=True)


# UPLOAD ###############################################################################################################
@require_POST
@login_required
def upload_bin(request):
    '''
    View responsible for receiving the request to upload a raw data folder.
    :param request: request information.
    :return: Form to fill if GET, HTTP response if POST.
    '''
    # use special upload handler (which does not delete temporary files)
    request.upload_handlers = [TemporaryFileUploadHandler(request)]

    if 'dataset' not in request.POST.keys() or \
            'xml_file' not in request.FILES.keys() or \
            'bin_list' not in request.FILES.keys():
        return HttpResponse('Bad Request.', status=400)  # Bad Request

    # read http request
    title = request.POST['dataset']
    xml_f = request.FILES['xml_file']
    bin_fs = request.FILES.getlist('bin_list')
    project = request.POST['project'] if 'project' in request.POST.keys() else "unresolved_project"
    tags = request.POST.getlist('tags') if 'tags' in request.POST.keys() else []
    fs_path = path.join(settings.MEDIA_ROOT, project)

    # extract file names and paths of bin files
    bin_fs_paths=[]
    bin_fs_names=[]
    for bin_f in bin_fs:
        print(bin_f.name)
        bin_fs_names.append(bin_f.name)
        bin_fs_paths.append(bin_f.temporary_file_path())

    # save all to json file
    temporary_file_path = path.join(path.dirname(bin_fs_paths[0]),'temp_data_for_uploading.json')
    #temporary_file_path = 'temp_data_for_uploading.json'
    with open(temporary_file_path, 'w') as outfile:
        json.dump([title,project,tags,fs_path,xmltodict.parse(xml_f),bin_fs_names,bin_fs_paths], outfile)

    # delete uploaded temporary xml file (since its already parsed and saved to json file)
    xml_f.close()
    remove(xml_f.temporary_file_path())

    # start handle_upload_bin_folder as background_task (with path to json file as argument)
    handle_upload_bin_folder(request.user.username, title, temporary_file_path)

    return HttpResponse("Upload done. Processing in background...", status=201)


@require_POST
@login_required
def upload_folder(request):
    '''
    View responsible for receiving the request to upload a raw data folder.
    :param request: request information.
    :return: Form to fill if GET, HTTP response if POST.
    '''
    if 'Content-Type' not in request.POST.keys() or \
            'dataset' not in request.POST.keys() or \
            'project' not in request.POST.keys() or \
            'totalFiles' not in request.POST.keys():
        return HttpResponse('Bad Request.', status=400)  # Bad Request

    # read http request info
    file = request.FILES.get('file')
    type = request.POST['Content-Type']
    dataset = request.POST['dataset']
    project = request.POST['project']
    totalFiles = int(request.POST['totalFiles'])
    tags = request.POST.get('tags', [])

    # set directory where to save file to, if needed create directory
    dirpath = path.join(settings.FILE_UPLOAD_TEMP_DIR, f'{project}_{dataset}')
    Path(dirpath).mkdir(parents=False, exist_ok=True)        #create directory

    # check if upload complete
    if request.POST.get('command') == 'upload_complete':
        if len(fnmatch.filter(os.listdir(dirpath), '*.bin')) >= totalFiles:
            upload_folder_process_upload(request.user.username, dataset, project, tags, dirpath)
            return HttpResponse("Upload Complete, all files received.", status=201)
        else:
            return HttpResponse('Files missing.', status=400)

    # save file
    filepath = path.join(dirpath, file.name)
    with open(filepath, 'wb+') as dest_file:
        for chunk in file.chunks():
            dest_file.write(chunk)

    #print(f'upload done! Type: {type}, dataset: {dataset}, project: {project}, total number of bin files: {totalFiles}, saved to {filepath}')

    return HttpResponse("Request Received", status=201)


# PREVIEW ##############################################################################################################
@require_GET
@login_required
def preview(request, f_path=''):
    '''
    View that returns the information of the .raw file in the filesystem.
    :param request: request information.
    :param f_path: relative filepath of the .raw file.
    :return: a dictionary that mimics the structure of the .raw files.
    '''
    f_path = f_path + '.raw'     # because ".raw" is not being caught by the URL
    f_path = f_path.split('/')
    raw_file_path = path.join(settings.MEDIA_ROOT, *f_path)

    # open the .raw file
    raw_file = h5py.File(raw_file_path, mode='r')
    raw_preview_data = {
        'file_path': raw_file_path,
        'groups': list(raw_file.keys()),
    }
    is_valid = True
    # only have to do this because the structure of the .raw allows it
    for group in list(raw_file.keys()):
        if group not in ['image', 'meta', 'label']:
            is_valid = False
            break
        raw_preview_data[group] = list(raw_file[group].keys())

    if not is_valid:
        return HttpResponse('Invalid H5.', status=418)

    return JsonResponse({'response': raw_preview_data}, safe=True)


def fetch_raw_image(raw_file, image_name, background_sub=True):
    img_arr_data = raw_file['image'][image_name][()]
    if background_sub:
        img_arr_data -= raw_file['meta']['background']
    return img_arr_data


@require_GET
# @login_required
def preview_details(request, f_path='', group='', ds_name=''):
    '''
    View that returns the information of the .raw file in the filesystem.
    :param request: request information.
    :param f_path: relative filepath of the .raw file.
    :param group: name of the group inside the .raw file from the f_path.
    :param ds_name: name of the dataset inside the group.
    :return: the value requested to complete the preview of the .raw file.
    '''
    f_path = f_path + '.raw'
    f_path = f_path.split('/')
    raw_file_path = path.join(settings.MEDIA_ROOT, *f_path)
    raw_file = h5py.File(raw_file_path, mode='r')

    # if all else fails, value is None
    value = None
    if group == 'meta':
        value = h5group_to_nested_dict(raw_file[group][ds_name])
        if ds_name == 'xml':  # need to load the JSON information of the XML
            value = json.loads(value)
        elif not isinstance(value, dict):
            value = str(value) ## needed for sending as json response
    elif group == 'image':
        background_sub = json.loads(request.GET.get('backgroundSubtraction', 'false'))
        value = fetch_raw_image(raw_file, ds_name, background_sub).tolist()
    elif group == 'label':
        value = raw_file[group][ds_name][()].tolist()   # else its label, not well-defined behaviour for now...

    return JsonResponse({'response': value}, safe=True)


@login_required
def metadata(request, f_path='', ds_name=''):
    if request.method == 'GET':
        return preview_details(request, f_path, 'meta', ds_name)
    elif request.method == 'DELETE':
        pass  # Do something ?
    elif request.method == 'POST':
        return meta_edit(request, f_path, ds_name)
    else:
        return HttpResponse('Method not allowed', status=405)


# EDIT META ############################################################################################################
@require_POST
@login_required
def meta_edit(request, f_path='', ds_name=''):
    raw_file_path = path.join(settings.MEDIA_ROOT, *f_path.split('/'))
    raw_file = h5py.File(raw_file_path + '.raw', 'r+')
    raw_file_meta_group = raw_file['meta']

    for k in (raw_file_meta_group.keys() & request.POST.keys() & {ds_name}):
        print('updating key: {}'.format(k))
        del raw_file_meta_group[k]
        raw_file_meta_group.create_dataset(k, data=request.POST[k])

    raw_file.close()
    # created new h5 successfully
    return HttpResponse("Updated successfully", status=201)


# STATUS ###############################################################################################################
@require_GET
#@login_required
def status(request):
    '''
    View that returns the status of background_tasks
    '''

    # Running tasks
    running_tasks = list(Task.objects.values('task_name', 'task_params', 'last_error','locked_by'))

    # Completed tasks (just for testing)
    #completed_tasks = list(CompletedTask.objects.values('task_name', 'task_params'))

    # TODO: add support for running or not ('locked_by' probably) and errors
    task_names = []
    for task in running_tasks:
        user_name = json.loads(task['task_params'])[0][0]
        if user_name == request.user.username:
            if task['task_name'] == 'cellbase.utils_upload.handle_upload_bin_folder': task_names.append({'task_name': f'Processing Upload ({json.loads(task["task_params"])[0][1]})'})
            if task['task_name'] == 'cellbase.utils_upload.upload_folder_process_upload': task_names.append({'task_name': f'Processing Upload ({json.loads(task["task_params"])[0][1]})'})
            if task['task_name'] == 'cellbase.views.preprocess_dataset_blocking': task_names.append({'task_name': f'Preprocessing Dataset ({json.loads(task["task_params"])[0][1]})'})

    # just for testing
    #logging.info(pending_tasks_qs, running_tasks_qs, completed_tasks_qs)
    #logging.info(running_tasks_qs)

    #return HttpResponse("ok")
    return JsonResponse({'response': list(task_names)}, safe=False)
    #return JsonResponse({'response': list(completed_tasks_qs)}, safe=True)

# UTILITY ##############################################################################################################
def available_tags(request):
    data = list(set(list(Tag.objects.all().values_list('tag_name', flat=True))))
    return JsonResponse({'response': data}, safe=True)


def available_projects(request):
    data = list(set(list(Project.objects.all().values_list('project_name', flat=True))))
    return JsonResponse({'response': data}, safe=True)


@require_POST
@login_required
def preprocess_dataset(request, f_path=''):
    data = json.loads(request.body)
    print(data)

    # launch asynchronous call, no need to wait for it to end
    if path.exists(path.join(settings.MEDIA_ROOT, *((f_path + '.phase').split('/')))):
        return HttpResponse('File already exists.', status=400)

    # Update DB
    raw_path, phase_path = f_path + '.raw', f_path + '.phase'
    raw_file_path = path.join(settings.MEDIA_ROOT, *(raw_path.split('/')))
    phase_path = path.join(settings.MEDIA_ROOT, *(phase_path.split('/')))
    raw_dataset = Dataset.objects.get(path=raw_file_path)
    phase_ds = PhaseDataset()
    phase_ds.name = raw_dataset.name
    phase_ds.path = phase_path
    phase_ds.raw = raw_dataset
    phase_ds.background_subtraction = data['backgroundSubtraction']
    phase_ds.crop_min = data['cropMin']
    phase_ds.crop_max = data['cropMax']
    phase_ds.save()

    preprocess_dataset_blocking(request.user.username, raw_file_path, phase_path, data)
    return HttpResponse('Request is being handled in the background', status=200)


@background
def preprocess_dataset_blocking(user, raw_file_path, phase_path, preprocess_args):
    raw_file = h5py.File(raw_file_path, mode='r')

    ## Spawn workers for converting each image
    pool = ThreadPoolExecutor()
    futures = [
        (key, pool.submit(
            convert_float_image,
            fetch_raw_image(raw_file, key, preprocess_args['backgroundSubtraction']),
            preprocess_args)) \
        for key in raw_file['image'].keys()
    ]

    ## Write to new .phase dataset
    phase_h5 = h5py.File(phase_path, mode='w-') ## will fail if file exists

    raw_file.copy('meta', phase_h5)
    raw_file.copy('label', phase_h5)
    phase_h5.create_group('image')

    ## Gather results
    pool.shutdown(wait=True)
    for key, fut in futures:
        phase_h5['image'][key] = fut.result()

    raw_file.close()
    phase_h5.close()
    print('done with phase data; path: {}'.format(phase_path))


def convert_float_image(img: np.ndarray, preprocess_args: dict):
    new_img = np.ndarray(img.shape, dtype=np.uint8)
    crop_range = preprocess_args['cropMax'] - preprocess_args['cropMin']

    for row in range(len(img)):
        for col in range(len(img[row])):
            new_img[row][col] = min(
                255,
                round(
                    max(img[row][col] - preprocess_args['cropMin'], 0) * 255 / crop_range
                )
            )
    return new_img

