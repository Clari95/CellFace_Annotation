export default {
  setXmlFile: (state, xmlFile) => {
    state.binUpload.xmlFile = xmlFile;
  },
  addBinFile: (state, binFile) => {
    state.binUpload.binFiles.push(binFile);
  },
  clearFilesToUpload: (state) => {
    state.binUpload.xmlFile = null;
    state.binUpload.binFiles = [];
  },
  updateProgress: (state, progressEvent) => {
    const p = (progressEvent.loaded / progressEvent.total) * 100;
    console.log(`Progress: ${p}`);
    state.binUpload.uploadProgress = p;
  },
  uploadComplete: () => {
    console.log('upload complete');
  },
  storeBinUploadFormData: (state, formData) => {
    state.binUpload.datasetName = formData.datasetName;
    state.binUpload.projectName = formData.projectName;
    state.binUpload.tags = formData.tags;
  },
};
