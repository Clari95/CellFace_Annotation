<template>
  <div>
    <v-container>

      <v-card>
        <v-card-title>
          Datasets
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="fa-search"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>

        <v-data-table
        :headers="headers"
        :items="files"
        :search="search"
        :loading="loading"
        item-key="name"
        class="elevation-1"
        no-data-text="There are no files available..."
        @click:row="changeSelection"
        >
          <template v-slot:item.is_folder="{ item }">
            <v-icon v-if="item.is_folder">fa-folder</v-icon>
            <v-icon v-else-if="item.name.endsWith('.phase')">fa-book</v-icon>
            <v-icon v-else-if="item['type/mime'].split('/')[0]=='text'">fa-file-text-o</v-icon>
            <v-icon v-else-if="item['type/mime'].split('/')[0]=='image'">fa-file-image-o</v-icon>
            <v-icon v-else-if="item['type/mime'].split('/')[0]=='application'">fa-database</v-icon>
            <v-icon v-else>fa-file-o</v-icon>
          </template>
          <template v-slot:item.created="{ item }">
            {{item.created.substr(0, 10)}}
          </template>
          <template v-slot:item.size="{ item }">
            {{(item.size || item.size === 0 ? formatSize(item.size) : '-')}}
          </template>
          <template v-slot:item.modified="{ item }">
            {{item.modified.substr(0, 10)}}
          </template>
          <template v-slot:item.tags="{ item }">
            <div v-if="item.tags">
              <v-chip v-for="(tag, idx) in item.tags" :key=idx label class="ma-2">
                {{tag}}
              </v-chip>
            </div>
          </template>
        </v-data-table>
      </v-card>

    </v-container>
  </div>
</template>

<script>
import { HTTP } from '@/http.common';
import { sizeToHumanReadable } from '@/utils.common';

export default {
  props: {
    path: {
      type: String,
      required: true,
    },
  },

  data: () => ({
    loading: true,
    search: '',
    headers: [
      { text: '', value: 'is_folder', width: 1 },
      { text: 'Name', value: 'name', width: 4 },
      { text: 'Size', value: 'size', width: 4 },
      { text: 'Date Created', value: 'created', width: 4 },
      { text: 'Date Modified', value: 'modified', width: 4 },
      { text: 'MIME', value: 'type/mime', width: 4 },
      { text: 'Type', value: 'type', width: 4 },
      { text: 'Tags', value: 'tags', width: 6 },
    ],
    files: [],
  }),

  methods: {
    changeSelection(event) {
      const selected = { ...event }; // deconstruct row observer
      this.$emit('selected', selected);
    },

    updateFiles() {
      HTTP
        .get(this.path)
        .then((response) => {
          this.files = response.data.response;
          this.loading = false;
        });
    },

    formatSize(size) {
      return sizeToHumanReadable(size);
    },
  },

  mounted() {
    this.updateFiles();
  },

  watch: {
    path() {
      this.updateFiles();
    },
  },
};
</script>

<style lang="scss" scoped>

</style>
