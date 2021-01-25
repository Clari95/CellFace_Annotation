export default {
  getTotalFilesToUpload: (state) => {
    let total = state.binUpload.binFiles.length;
    if (state.binUpload.xmlFile) {
      total += 1;
    }
    return total;
  },
};
