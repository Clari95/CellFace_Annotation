<template>
  <div>

    <v-card outlined class="mx-3 my-3">
      <v-card-title>Detailed View</v-card-title>
      <v-card-text>Name: {{ this.file.name }}</v-card-text>
      <v-card-text>Size: {{ this.formatSize(this.file.size) }}</v-card-text>
      <v-card-text>Type: {{ this.file.type }}</v-card-text>

      <v-card-actions v-if="this.isDataset(this.file.name)">
        <v-btn text block color="primary"
          :to="{
            path: '/preview',
            query: { dataset: this.file.name, contextPath: this.contextPath }
            }"
          replace
          >
          Preview Dataset
          <v-icon right>fa-folder-open</v-icon>
        </v-btn>
      </v-card-actions>

    </v-card>
  </div>
</template>

<script>
import { sizeToHumanReadable } from '@/utils.common';

export default {
  props: {
    file: {
      type: Object,
      required: true,
    },
    contextPath: String,
  },

  methods: {
    formatSize(size) {
      return sizeToHumanReadable(size);
    },

    isDataset(name) {
      return name.endsWith('.raw');
    },
  },

  watch: {
  },
};
</script>
