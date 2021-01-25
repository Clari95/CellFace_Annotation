<template>
    <div class="wrapper">
      <v-row fill-width>
        <div class="nav-arrow"  id="back-button">
            <v-btn @click="updateComponent('again')" color="primary" class="mr-4">
            <v-icon left>mdi-rocket-outline</v-icon>Play <br/>again!
            </v-btn>
        </div>
        <!--- Main component starts here --->
        <v-col class="mx-auto mt-0 main">
        <div id = "labelingarea" class="labelingarea">
          <v-card-title>
            some review, data, number of cells graphics time etc...
          </v-card-title>
          <div class="scrollbar" id="grid" v-if="ImagesResults"> <!--v-if="images"-->
                            <v-item-group ref="tileGrid">
                              <v-container>
                                <v-row>
                                  <v-col
                                    v-for="(n,i) in ImagesResults"
                                    :key="i"
                                    cols="12"
                                    md="2"
                                  >
                                    <v-item>
                                      <v-card
                                        class="mx-auto"
                                        max-width="244"
                                        height="145"
                                      >
                                        <v-img
                                        class="label-overlay-new"
                                        contain></v-img>
                                        <RenderImage
                                        v-if="ImagesResults"
                                        class="miniature-new"
                                        :image="n"
                                        :minCropVal="preprocessArgsInUse.cropMin"
                                        :maxCropVal="preprocessArgsInUse.cropMax"
                                        :invertBackground="preprocessArgsInUse.invertBackground"
                                        :colormap="preprocessArgsInUse.colormap"
                                        :opacity="preprocessArgsInUse.opacity"
                                        />

                                        <v-card-text class="explanation">
                                            image number {{i + 1}}
                                        </v-card-text>

                                      </v-card>
                                    </v-item>
                                  </v-col>
                                </v-row>
                              </v-container>
                            </v-item-group>
                          </div>

        </div>
        </v-col>
        <!--- Main component ends here --->
        <!--<div class="nav-arrow" id ="finish-button">
            <v-btn small @click="updateComponent('next')" color="primary" class="mr-4">
            <v-icon left>mdi-arrow-right-circle</v-icon>Finish
            <v-icon>fast-forward</v-icon>
            </v-btn>
        </div>-->
      </v-row>
    </div>
</template>

<script>
import { HTTP } from '@/http.common';
import RenderImage from '@/components/RenderImage.vue';

export default {

  name: 'LabelingInitialize',
  props: ['allProperties'],
  components: {
    RenderImage,
  },

  data: () => ({
    // UserID: 'testperson',
    ImagesResults: null,
    NewImage: null,
    preprocessArgsInUse: {
      cropMin: -0.5,
      cropMax: 5,
      invertBackground: true,
      colormap: 'velocity-blue',
      backgroundSubtraction: false,
      opacity: 255,
    },
    firstImages: true,
    NumberImages: 0,
    rules: [v => !!v || 'Req',
      v => v.length <= 4 || 'Max 4 signs'],
    counterEn: false,
    counter: 0,
    missingUserID: '',
    icons: {
    },
    dialog: false,
  }),
  methods: {
    updateComponent(event) {
      this.$emit('updateComponent', event);
    },
    switchImage(toImage) {
      this.imageRef = toImage;
      this.selectedRectangle = -1;
      this.redrawContent();
    },
    getData() {
      console.log('get results');
      console.log(typeof this.UserID);
      HTTP.post(
        `segmask/${this.allProperties.UserID}/${this.allProperties.dataset_typ}`,
      ).then(async (response) => {
        this.ImagesResults = response.data.SegMasksResults;
        this.NumberImages = response.data.numberOfimages;
        console.log(this.ImagesResults);
        // this.newImages.push(response.data.image);
        // this.newImageMasks.push(response.data.label_mask);
        console.log('Received in Review');
        // this.NewImage = this.ImagesResults[0];
        // this.newImage = this.newImages[this.image_section][0];
        // this.newImageMask = this.newImageMasks[this.image_section][0];
      }).catch((e) => {
        console.warn(e);
      });
      return 'Complete';
    },
    // computedPath() {
    //   return require('@/assets/test_sample2.png'); // ${this.justForTest}.png');;
    // },
    ImageResult(n, i) {
      console.log('Image Result');
      console.log(n);
      console.log(i);
      console.log(typeof this.ImagesResults);
      console.log(this.ImagesResults[0]);
      console.log(this.NumberImages);
      this.NewImage = this.ImagesResults[n];
      // const object = {};
      /* if (n === this.NumberImages - 1) {
        console.log('in if ImageResult');
        this.firstImages = false;
      } */
      return this.NewImage;
      // console.log(this.NewImage);
    },
    colorSelect(color) {
      this.color = color;
    },
  },
  mounted() {
    this.getData();
  },
};
</script>

<style scoped>
    .wrapper{
        text-align: center;
        text-justify: center;
    }
    .nav-arrow{
        padding-top: 550px;
        padding-left: 15px;
        text-justify: right;
    }
    .main{
      height: 480px;
      width: 750px;
      min-width: 750px;
      border: 0px solid #fcfcfc;
      text-justify: center;
    }
    .scrollbar{
      height: 520px;
      width: 100%;
      overflow: scroll;
    }


</style>
