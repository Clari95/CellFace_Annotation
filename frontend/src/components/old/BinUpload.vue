<template>
  <div class="bin-upload-container">
    <v-form id="upload-form" ref="form">
      <v-text-field
        v-model="datasetName"
        label="Dataset Name"
        prepend-icon="fa-file-archive-o"
        required
      ></v-text-field>
      <v-text-field
        v-model="projectName"
        label="Project Name"
        prepend-icon="fa-user"
        required
      ></v-text-field>
      <TagInput
        ref="tagInput"
      />
      <v-row class="mx-auto mt-4">
        <p v-if="getTotalFilesToUpload">{{ getTotalFilesToUpload }} Files Selected for Upload</p>
      </v-row>
      <v-row>
        <v-progress-linear
          v-model="uploadProgress"
          height="25"
          reactive
          v-if="getTotalFilesToUpload"
        >
          <strong>{{ uploadProgress }}%</strong>
        </v-progress-linear>
      </v-row>
      <v-row class="mx-auto mt-4">
        <v-menu open-on-hover top offset-y close-on-click class="mr-4">
          <template v-slot:activator="{ on }">
            <v-btn color="secondary" v-on="on">
              Select <v-icon right>fa-plus</v-icon>
            </v-btn>
          </template>
          <HiddenInput
            ref="fileInput"
            :multiple="true"
            :accept="fileTypes"
            @filesSelected="addFiles"
          />
          <HiddenInput
            ref="folderInput"
            :directory="true"
            :accept="fileTypes"
            @filesSelected="addFolder"
          />
          <v-list>
            <v-list-item @click="$refs.fileInput.$refs.input.click()">
              <v-list-item-title>Add Files</v-list-item-title>
            </v-list-item>
            <v-list-item @click="$refs.folderInput.$refs.input.click()">
              <v-list-item-title>Add Folder</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-btn v-if="uploadActive" class="mr-4" color="error" @click="onStop">
          Stop <v-icon right aria-hidden="true">fa-stop</v-icon>
        </v-btn>
        <v-btn v-else color="primary" class="mr-4" @click="onSubmit">
          Submit <v-icon right>fa-cloud-upload</v-icon>
        </v-btn>
        <v-btn @click="onClear">
          Clear <v-icon right>fa-times</v-icon>
        </v-btn>
      </v-row>
    </v-form>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import TagInput from '@/components/TagInput.vue';
import HiddenInput from '@/components/HiddenInput.vue';

export default {
  name: 'BinUpload',
  components: {
    HiddenInput,
    TagInput,
  },
  data: () => ({
    // Form Data
    uploadActive: false,
    fileTypes: ['.bin', '.xml', '.h5'],
    datasetName: '',
    projectName: '',
    action: 'http://localhost:3000/upload/',
  }),
  methods: {
    ...mapActions([
      'addFilesToUpload',
      'clearFilesToUpload',
      'storeBinUploadFormData',
      'uploadFiles']),
    addFiles(event) {
      console.log('addFiles');
      this.addFilesToUpload(event.target.files);
      this.onFilesSelected();
    },
    addFolder(event) {
      console.log('addFolder');
      this.addFilesToUpload(event.target.files);
      this.onFilesSelected();
    },
    onFilesSelected() {
      console.log(`Total Files selected: ${this.getTotalFilesToUpload}`);
    },
    onSubmit() {
      if (this.validateUpload()) {
        this.storeBinUploadFormData({
          datasetName: this.datasetName,
          projectName: this.projectName,
          tags: this.tags,
        });
        this.uploadFiles();
      }
    },
    onStop() {
      this.uploadActive = false;
    },
    validateUpload() {
      if (!this.xmlFile) {
        this.$root.$emit('snackbar', {
          text: 'No Metadata XML Selected!',
          color: 'error',
        });
        return false;
      }
      if (!this.binFiles.length > 0) {
        this.$root.$emit('snackbar', {
          text: 'No Images Selected!',
          color: 'error',
        });
        return false;
      }
      if (!this.datasetName) {
        this.$root.$emit('snackbar', {
          text: 'Missing Dataset Name!',
          color: 'error',
        });
        return false;
      }
      if (!this.projectName) {
        this.$root.$emit('snackbar', {
          text: 'Missing Project Name!',
          color: 'error',
        });
        return false;
      }
      return true;
    },
    onClear() {
      this.clearFilesToUpload();
      this.$refs.form.reset();
    },
  },
  computed: {
    ...mapGetters(['getTotalFilesToUpload']),
    ...mapState({
      binFiles: state => state.binUpload.binFiles,
      xmlFile: state => state.binUpload.xmlFile,
      uploadProgress: state => state.binUpload.uploadProgress,
    }),
  },
};
</script>

<style scoped>
  #upload-form {
    padding: 1em;
  }
</style>
