<template>
  <div class="preview">
    <v-container fill-height fluid>
      <v-row no-gutters>

        <v-col cols="4" id="metadata">

          <!-- Card for Dataset Metadata -->
          <v-card class="options-card">
            <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-header>
                <div class="overline">
                  DATASET METADATA
                </div>
              </v-expansion-panel-header>

            <v-expansion-panel-content>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title class="headline">
                  {{this.dataset}}
                </v-list-item-title>

                <v-container v-if="metadata !== null">

                  <v-row v-for="(elem, i) in getScalarMetadata()" :key="i" justify="space-around">
                    <v-col><i>{{elem.name}}</i></v-col>
                    <v-col>{{elem.data}}</v-col>
                  </v-row>

                  <v-row
                    v-for="(item, key) in metadata[metadata.length - 1].data"
                    :key="key"
                    >
                    <v-col>
                      <v-row>
                      <v-btn text @click="metaDropdownStatus[key] = !metaDropdownStatus[key]">
                        <v-icon left v-if="metaDropdownStatus[key]">fa-caret-up</v-icon>
                        <v-icon left v-else-if="!metaDropdownStatus[key]">fa-caret-down</v-icon>
                        {{key}}
                      </v-btn>
                      </v-row>

                      <v-row v-if="metaDropdownStatus[key]">

                        <v-col>
                        <v-row
                          v-for="(inner_item, inner_key) in item"
                          :key="inner_key"
                          justify="space-around">

                          <v-col><i>{{inner_key}}</i></v-col>
                          <v-col v-if="!editableMetadata">{{inner_item}}</v-col>
                          <v-text-field v-else
                            v-model="metadata[metadata.length - 1].data[key][inner_key]"
                            :hint="inner_key"
                            dense>
                          </v-text-field>
                        </v-row>
                        </v-col>

                      </v-row>
                    </v-col>
                  </v-row>

                </v-container>
              </v-list-item-content>
            </v-list-item>

            <v-card-actions>
              <v-row justify="center" class="mb-3">
              <v-btn
                @click="editableMetadata = !editableMetadata"
                color="primary"
                class="mx-4"
                >
                {{editableMetadata ? "Cancel" : "Edit"}}
              </v-btn>
              <v-btn
                :disabled="!editableMetadata"
                @click="submitEditedMetadata"
                color="primary"
                class="mx-4"
                >
                Submit
              </v-btn>
              </v-row>
            </v-card-actions>

            </v-expansion-panel-content>
            </v-expansion-panel>
            </v-expansion-panels>
          </v-card>


          <!-- Card for Image Rendering Arguments -->
          <v-card class="options-card">
          <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header>
              <div class="overline">
                IMAGE RENDER ARGUMENTS
              </div>
            </v-expansion-panel-header>

            <v-expansion-panel-content>
              <v-list-item>
                <v-list-item-content>
                  <v-row>
                    <v-col>
                      <v-text-field
                        label="Crop starting at (minimum)"
                        v-model="preprocessArgs.cropMin"
                        :rules="[validCropRange]"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                      <v-text-field
                        label="Crop ending at (maximum)"
                        v-model="preprocessArgs.cropMax"
                        :rules="[validCropRange]"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                        <v-select
                          v-model="preprocessArgs.colormap"
                          :items="colorScales"
                          label="Colormap"
                        ></v-select>
                      </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                        <v-checkbox
                          v-model="preprocessArgs.invertBackground"
                          label="Invert background color ?"
                        ></v-checkbox>
                      </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                        <v-checkbox
                          v-model="preprocessArgs.backgroundSubtraction"
                          label="Subtract median background ?"
                        ></v-checkbox>
                      </v-col>
                  </v-row>
                </v-list-item-content>
              </v-list-item>

              <v-card-actions>
                <v-row justify="center" class="mb-3">
                <v-btn
                  @click="handlePreviewRequest"
                  color="primary"
                  class="mx-4"
                  >
                  Preview
                </v-btn>
                <v-btn
                  :disabled="!previewed"
                  @click="submitDataPreprocessing"
                  color="primary"
                  class="mx-4"
                  >
                  Preprocess Data
                </v-btn>
                </v-row>
              </v-card-actions>
            </v-expansion-panel-content>
          </v-expansion-panel>
          </v-expansion-panels>
          </v-card>

        </v-col>


        <v-col cols="8">

          <v-card class="options-card">

          <v-overlay absolute :value="loadingPreview">
            <v-progress-circular v-if="loadingPreview" indeterminate size="64">
            </v-progress-circular>
          </v-overlay>

          <v-expansion-panels :value="0">
          <v-expansion-panel>
            <v-expansion-panel-header>
              <div class="overline">
                IMAGE PREVIEW
              </div>
            </v-expansion-panel-header>

            <v-expansion-panel-content>
            <v-list-item>
            <v-list-item-content class="pa-0">
              <v-container>
                <v-row>
                  <v-col v-for="(img, idx) in images" :key="idx">
                    <RenderImage
                      :key="idx"
                      :image="img.data"
                      :minCropVal="preprocessArgsInUse.cropMin"
                      :maxCropVal="preprocessArgsInUse.cropMax"
                      :invertBackground="preprocessArgsInUse.invertBackground"
                      :colormap="preprocessArgsInUse.colormap"
                      />
                  </v-col>
                </v-row>
              </v-container>

            </v-list-item-content>
            </v-list-item>

            <v-list-item>
            <v-list-item-content>
              <v-slider
                v-model="pageNumber"
                class="align-center mt-4"
                label="Image Number"
                :max="getNumPages()"
                :min="1"
                thumb-label
              >
                <template v-slot:append>
                  <v-text-field
                    validate-on-blur
                    id="pageNumTextInput"
                    class="mt-0 pt-0"
                    hide-details
                    single-line
                    type="number"
                    style="width: 80px"
                    @change="updatePageNum"
                  ></v-text-field>
                </template>
              </v-slider>
            </v-list-item-content>
            </v-list-item>

            </v-expansion-panel-content>
          </v-expansion-panel>
          </v-expansion-panels>
          </v-card>


          <v-card class="options-card">
            <v-col>

          <!-- <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header> -->
              <div class="overline">
                DATASET STATISTICS
              </div>
            <!-- </v-expansion-panel-header>
            <v-expansion-panel-content> -->
              <DatasetStatistics
                v-if="metadata"
                :statistics="getStatistics()"
                />
            <!-- </v-expansion-panel-content>
          </v-expansion-panel>
          </v-expansion-panels> -->
            </v-col>

          </v-card>

        </v-col>

      </v-row>
    </v-container>
  </div>
</template>

<script>
import colorScales from 'colormap/colorScale';
import { HTTP } from '@/http.common';
import { handleStatusResponse } from '@/utils.common';
import RenderImage from '@/components/RenderImage.vue';
import DatasetStatistics from '@/components/DatasetStatistics.vue';

export default {
  props: {
    dataset: {
      type: String,
      required: true,
    },
    contextPath: String,
  },

  components: {
    RenderImage,
    DatasetStatistics,
  },

  data: () => ({
    h5Data: null,
    metadata: null,
    images: null,
    index: null,
    imgHeight: null,
    imgWidth: null,
    totalNumImages: null,
    pageNumber: 1,
    numImgsPerPage: 1,
    editableMetadata: false,
    metaDropdownStatus: {},
    colorScales: ['None', ...Object.keys(colorScales)],
    preprocessArgs: {
      cropMin: -0.5,
      cropMax: 3.0,
      invertBackground: true,
      colormap: 'None',
      backgroundSubtraction: true,
    },
    preprocessArgsInUse: {
      cropMin: -0.5,
      cropMax: 3.0,
      invertBackground: true,
      colormap: 'None',
      backgroundSubtraction: true,
    },
    previewed: false,
    loadingPreview: false,
  }),

  async mounted() {
    this.h5Data = await this.fetchH5Data();
    this.metadata = await this.fetchMetaData();
    await this.loadNewImagePage();

    this.metaDropdownStatus = {};

    Object.keys(this.metadata[this.metadata.length - 1].data).forEach((k) => {
      this.$set(this.metaDropdownStatus, k, false); // needed to update reactive element
    });
  },

  watch: {
    metadata(to) {
      if (to === null) return;

      // Update image sizes
      const [x, y] = to[0].data.split(' ');
      this.imgHeight = parseInt(x.substr(1), 10);
      this.imgWidth = parseInt(y.substr(0, y.length - 1), 10);
      this.totalNumImages = this.h5Data.image.length;
    },

    numImgsPerPage() {
      this.loadNewImagePage();
    },

    pageNumber(newPageNum) {
      this.loadNewImagePage();
      document.getElementById('pageNumTextInput').value = newPageNum;
    },

    preprocessArgs() {
      this.previewed = false;
    },
  },

  methods: {

    validCropRange() {
      this.previewed = false;

      const minVal = parseFloat(this.preprocessArgs.cropMin);
      const maxVal = parseFloat(this.preprocessArgs.cropMax);

      const isValid = !Number.isNaN(minVal) && !Number.isNaN(maxVal) && minVal < maxVal;
      return isValid || 'Invalid crop range';
    },

    getQueryUrl() {
      const folderTree = this.contextPath.split('/').slice(2);
      return `preview/${folderTree.join('/')}${folderTree.length > 0 ? '/' : ''}${this.dataset}`;
    },

    getScalarMetadata() {
      return this.metadata.filter(el => !['xml', 'statistics', 'background'].includes(el.name));
    },

    getStatistics() {
      return this.metadata ? this.metadata.filter(el => el.name === 'statistics')[0].data : {};
    },

    async fetchH5Data() {
      const queryUrl = this.getQueryUrl();

      return HTTP
        .get(queryUrl)
        .then(response => response.data.response);
    },

    async fetchMetaData() {
      if (this.h5Data === null) return new Promise();

      const queryUrl = this.getQueryUrl();
      return Promise.all(this.h5Data.meta.map(elem => (
        HTTP
          .get(`${queryUrl}/meta/${elem}`)
          .then(resp => ({
            name: elem,
            data: resp.data.response,
          })))));
    },

    fetchImagePromises(start = 0, end = -1) {
      if (this.h5Data === null) return new Promise();

      const queryUrl = this.getQueryUrl();
      const imgPromises = [];
      const lastIdx = (
        end > 0 ? Math.min(end, this.h5Data.image.length) : this.h5Data.image.length
      );

      for (let i = start; i < lastIdx; i += 1) {
        const imageId = this.h5Data.image[i];
        const imgQueryUrl = `${queryUrl}/image/${imageId}?backgroundSubtraction=${this.preprocessArgsInUse.backgroundSubtraction}`;
        imgPromises.push(
          HTTP
            .get(imgQueryUrl)
            .then(resp => ({
              id: imageId,
              caption: imageId,
              data: resp.data.response,
            })),
        );
      }

      return imgPromises;
    },

    async loadNewImagePage() {
      const startIdx = (this.pageNumber - 1) * this.numImgsPerPage;
      const endIdx = this.pageNumber * this.numImgsPerPage;
      this.loadingPreview = true;
      this.images = await Promise.all(this.fetchImagePromises(startIdx, endIdx));
      this.loadingPreview = false;
    },

    getNumPages() {
      return this.totalNumImages !== null
        ? Math.ceil(this.totalNumImages / this.numImgsPerPage) : 10;
    },

    updatePageNum(event) {
      this.pageNumber = event;
    },

    // Page number validation
    pageNumValid(pageNum) {
      return pageNum >= 1 && pageNum <= this.getNumPages();
    },

    submitEditedMetadata() {
      const queryUrl = `${this.getQueryUrl()}/meta/xml`;
      const xml = this.metadata[this.metadata.length - 1].data;

      const data = new FormData();
      data.append('xml', JSON.stringify(xml));

      const responsePromise = HTTP.post(
        queryUrl,
        data,
      );

      handleStatusResponse.call(this, responsePromise);
      this.editableMetadata = false;
    },

    submitDataPreprocessing() {
      // Construct url route
      const folderTree = this.contextPath.split('/').slice(2);
      const url = `preprocess/${folderTree.join('/')}${folderTree.length > 0 ? '/' : ''}${this.dataset}`;

      // Send HTTP request
      const responsePromise = HTTP.post(url, this.preprocessArgsInUse);
      handleStatusResponse.call(this, responsePromise);
    },

    handlePreviewRequest() {
      this.previewed = true;
      if (this.preprocessArgsInUse.backgroundSubtraction
          !== this.preprocessArgs.backgroundSubtraction) {
        this.preprocessArgsInUse.backgroundSubtraction = this.preprocessArgs.backgroundSubtraction;
        this.loadNewImagePage();
      }

      this.preprocessArgsInUse.cropMin = parseFloat(this.preprocessArgs.cropMin);
      this.preprocessArgsInUse.cropMax = parseFloat(this.preprocessArgs.cropMax);
      this.preprocessArgsInUse.invertBackground = this.preprocessArgs.invertBackground;
      this.preprocessArgsInUse.colormap = this.preprocessArgs.colormap;
    },

  },

};
</script>

<style lang="scss" scoped>

  .v-card.options-card {
    margin: 1em;

    // Having trouble selecting framework-generated classes...
    div[class^="v-expansion-panel-content"] > * {
      padding: 0;
    }
  }

// For debugging -.-'
// * {
//   border: solid 1px;
// }

</style>
