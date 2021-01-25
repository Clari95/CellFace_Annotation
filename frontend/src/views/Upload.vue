<template>
  <v-card outlined class="mx-3 my-3 upload">
    <v-card-title class="mx-1 mt-2">Upload a new Dataset</v-card-title>

    <v-form id="upload-form"
      ref="form"
      v-model="formValid"
      @submit="submitForm"
      clearable
      >
      <v-text-field
        v-model="datasetName"
        label="Dataset Name"
        prepend-icon="fa-file-archive-o"
        required
      >
      </v-text-field>
      <v-text-field
        v-model="projectName"
        label="Project Name"
        prepend-icon="fa-user"
        required
        >
      </v-text-field>
      <div>
        <vue-tags-input
        v-model="tag"
        :tags="tags"
        @tags-changed="newTags => tags = newTags"
        />
      </div>
      <v-file-input
        v-model="xmlFile"
        chips
        accept=".xml"
        label="XML File">
      </v-file-input>
      <v-file-input
        v-model="binaryFiles"
        chips
        multiple
        accept=".bin"
        label="Binary Files">
      </v-file-input>

      <!-- <v-btn class="mr-4" @click="submitForm">Submit</v-btn> -->
      <v-row class="mx-auto mt-4">

        <v-btn color="primary" type="submit" class="mr-4" >
          Submit
          <v-icon right>fa-cloud-upload</v-icon>
        </v-btn>

        <v-btn @click="resetForm">
          Clear
          <v-icon right>fa-times</v-icon>
        </v-btn>

      </v-row>
    </v-form>
  </v-card>

</template>

<script>
import VueTagsInput from '@johmun/vue-tags-input';
import { HTTP } from '@/http.common';
import { handleStatusResponse } from '@/utils.common';

export default {
  components: {
    VueTagsInput,
  },

  data: () => ({
    formValid: true,
    datasetName: '',
    projectName: '',
    xmlFile: [],
    binaryFiles: [],
    tag: '',
    tags: [],
  }),

  methods: {
    async submitForm() {
      const data = new FormData();
      data.append('title', this.datasetName);
      data.append('project', this.projectName);
      data.append('xml_file', this.xmlFile);
      this.tags.forEach((elem) => {
        data.append('tags', elem.text);
      });
      this.binaryFiles.forEach((elem) => {
        data.append('bin_list', elem);
      });

      const responsePromise = HTTP.post(
        'upload/',
        data,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        },
        {
          progress: (progressEvent) => {
            console.log(`Progress: ${progressEvent.loaded / progressEvent.total}`);
          },
        },
      );

      handleStatusResponse.call(this, responsePromise)
        .then(() => this.resetForm());
    },

    resetForm() {
      this.$refs.form.reset();
    },
  },

};
</script>

<style lang="scss" scoped>

  #upload-form {
    padding: 1em;
  }

</style>
