import { getFileExtension } from '@/utils.common';

export function uploadBinFiles(uploadState, opts, commit) {
  return new Promise((resolve, reject) => {
    const form = new FormData();
    const xhr = new XMLHttpRequest();

    xhr.withCredentials = true;

    form.append('dataset', uploadState.datasetName);
    form.append('project', uploadState.projectName);
    form.append('xml_file', uploadState.xmlFile);

    uploadState.binFiles.forEach((elem) => {
      form.append('bin_list', elem);
    });

    xhr.upload.addEventListener('progress',
      (e) => {
        commit('updateProgress', e);
      }, false);

    xhr.onreadystatechange = () => {
      if (xhr.readyState === 4) {
        console.log(xhr.responseText);
        resolve('OK');
      }
    };

    xhr.onerror = () => {
      console.log(xhr.responseText);
      const err = 'err';
      reject(err);
    };

    xhr.open('POST', opts.action, true);
    xhr.send(form);
    console.log('uploadBinFiles');
  });
}

export default {
  addFilesToUpload: ({ commit }, fileList) => {
    for (let index = 0; index < fileList.length; index += 1) {
      const file = fileList[index];
      if (getFileExtension(file) === 'bin') {
        commit('addBinFile', file);
      } else if (getFileExtension(file) === 'xml') {
        commit('setXmlFile', file);
      }
    }
  },
  clearFilesToUpload: ({ commit }) => {
    commit('clearFilesToUpload');
  },
  storeBinUploadFormData: ({ commit }, formData) => {
    commit('storeBinUploadFormData', formData);
  },
  uploadFiles: ({ commit, state }) => {
    console.log('before Upload');

    uploadBinFiles(
      state.binUpload,
      {
        action: 'http://localhost:3000/upload/',
      },
      commit,
    ).then(commit('uploadComplete')).catch();
    console.log('after Upload');
  },
};
