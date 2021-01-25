<template>
  <div class="wrapper">
    <v-row fill-width>
      <div class="nav-arrow-back" id="back-button">
        <v-btn
          small
          @click="updateComponent('back')"
          color="primary"
          class="mr-4"
        >
          <v-icon left>mdi-arrow-left-circle</v-icon>back
        </v-btn>
      </div>
      <!--- Main component starts here --->
      <v-col class="mx-auto mt-0 main">
        <div id="labelingarea" class="labelingarea">
          <!--<v-card-title>
            some review, data, number of cells graphics time etc...
          </v-card-title>-->
          <v-card class="mx-auto" max-width="500">
            <v-toolbar color="white" dark elevation="0">
              <v-toolbar-title
                class="display-1 font-weight-light teal--text mb-2"
              >
                Info
              </v-toolbar-title>
            </v-toolbar>

            <v-container fluid>
              <v-row dense>
                <v-col :cols="6">
                  <v-card outlined height="120">
                    <v-card-text class="font-weight-light mb-2">
                      for <b>{{ allProperties.UserID }}</b> <br />
                      number labeled images:
                      {{ allProperties.AllScores[0][0] +
                        this.NumberImages5 }}<br />
                      number labeled cells:
                      {{
                        allProperties.AllScores[0][1] +
                        allProperties.AllScores[1][1]
                      }}<br />
                      number labeled regions:
                      {{
                        allProperties.AllScores[0][2] +
                        allProperties.AllScores[1][2]
                      }}
                    </v-card-text>
                  </v-card>
                </v-col>
                <v-col :cols="6">
                  <v-card outlined height="120" center>
                    <v-card-text class="font-weight-light mb-2 text-center">
                      <br />
                      in
                      {{
                        allProperties.AllScores[0][5] +
                        allProperties.AllScores[1][5]
                      }}
                      seconds <br />
                      Correctness: {{ accuracy }}% <br/>
                      Completeness: {{accuracyComplete}}%
                    </v-card-text>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
          <!--<v-card class="mx-auto"
                cols="12"
                width="600"
                height="190">
            <v-card-text
            >
              <h3 class="display-1 font-weight-light teal--text mb-2">Info</h3>
            </v-card-text>
                <h3 class="display-1 font-weight-light teal--text mb-2">Info</h3>
               <v-card-text class="font-weight-light mb-2">
              for <b>{{allProperties.UserID}}</b> <br/>
              number labeled images: {{allProperties.numberLabeledImages}}<br/>
              number labeled cells: {{allProperties.numberLabeledCells}}<br/>
              number labeled regions: {{allProperties.numberLabeledRegions}} <br/>
              in {{allProperties.labelTime}} seconds <br/>
              Accuracy: {{allProperties.accuracy}}
              </v-card-text>
          </v-card>-->
          <div class="scrollbar" id="grid" v-if="ImagesResults">
            <!--v-if="images"-->
            <v-item-group ref="tileGrid">
              <v-container>
                <v-row>
                  <v-col
                    v-for="(n, i) in ImagesResults"
                    :key="i"
                    cols="12"
                    md="2"
                  >
                    <v-item>
                      <v-card class="mx-auto" width="260" height="155">
                        <v-img class="label-overlay-new" contain></v-img>
                        <RenderImage
                          v-if="ImagesResults"
                          class="miniature-new"
                          :image="n"
                          :minCropVal="preprocessArgsInUse.cropMin"
                          :maxCropVal="preprocessArgsInUse.cropMax"
                          :invertBackground="
                            preprocessArgsInUse.invertBackground
                          "
                          :colormap="preprocessArgsInUse.colormap"
                          :opacity="preprocessArgsInUse.opacity"
                        />

                        <v-card-text class="explanation">
                          SegMask for image <b>{{ i + 1 }}</b>
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
      cropMax: 3,
      invertBackground: true,
      colormap: 'velocity-blue',
      backgroundSubtraction: false,
      opacity: 255,
    },
    firstImages: true,
    NumberImages: 0,
    NumberImages5: 0,
    // rules: [(v) => !!v || 'Req', (v) => v.length <= 4 || 'Max 4 signs'],
    counterEn: false,
    counter: 0,
    missingUserID: '',
    icons: {},
    dialog: false,
    accuracy: '__',
    accuracyComplete: '__',
  }),
  methods: {
    updateComponent(event) {
      this.$emit('updateComponent', event);
    },
    restart() {
      this.$emit('restart');
    },
    switchImage(toImage) {
      this.imageRef = toImage;
      this.selectedRectangle = -1;
      this.redrawContent();
    },
    getData() {
      console.log('getting Data');
      HTTP.post(
        `getDataReview/${this.allProperties.UserID}/${this.allProperties.dataset_typ}/${this.allProperties.labelingApproach}/${this.allProperties.numberLabeledImages}`,
      )
        .then(async (response) => {
          this.ImagesResults = response.data.SegMasksResults;
          this.NumberImages = response.data.numberOfimages;
          console.log(this.ImagesResults);
          console.log('Received in Review');
        })
        .catch((e) => {
          console.warn(e);
        });
      return 'Complete';
    },
    colorSelect(color) {
      this.color = color;
    },
    updateScores() {
      const allScores = String(this.allProperties.AllScores);
      const date = this.getDate();
      HTTP.post(
        `updateScore/${this.allProperties.labelingApproach}/${this.allProperties.UserID}/${this.allProperties.dataset_typ}/${allScores}/${date}`,
      )
        .then(async (response) => {
          console.log(response.data.Status);
          this.accuracy = Math.round(response.data.accuracy[2] * 100);
          this.accuracyComplete = Math.round(response.data.accuracy[0] * 100);
          this.getData();
        })
        .catch((e) => {
          console.warn(e);
        });
      return 'Complete';
    },
    getDate() {
      const currentdate = new Date();
      const datetime = `${currentdate.getDate()}.${
        currentdate.getMonth() + 1
      }.${currentdate.getFullYear()}@${currentdate.getHours()}:${currentdate.getMinutes()}:${currentdate.getSeconds()}`;

      return datetime;
    },
  },
  mounted() {
    // this.getData();
    console.log('in review load scores');
    // console.log(this.allProperties.AllScores.length);
    if (
      this.allProperties.skipped === true
      && this.allProperties.currentSection !== 1
    ) {
      console.log('skipped current level: ');
      console.log(this.allProperties.currentSection);
      let i = this.allProperties.currentSection;
      while (i < 1) {
        this.$emit('updateScores', [0, 0, 0, 0, 0, 0, 0, [0, 0, 0, 0], i + 1]);
        // this.$emit('updateAccuracy', [0, 0, 0, 0, i + 1]);
        i += 1;
      }
    }
    this.updateScores();
    if (this.allProperties.AllScores[1][0] !== 0) {
      this.NumberImages4 = this.allProperties.AllScores[0][0] - 1;
      this.NumberImages5 = this.allProperties.AllScores[1][0] - 11;
    }
  },
};
</script>

<style scoped>
.wrapper {
  text-align: center;
  text-justify: center;
}
.nav-arrow {
  padding-top: 550px;
  padding-left: 15px;
  text-justify: right;
}
.nav-arrow-back {
  top: 550px;
  left: 15px;
  text-justify: right;
  position: relative;
}
.main {
  height: 480px;
  width: 750px;
  min-width: 750px;
  border: 0px solid #fcfcfc;
  text-justify: center;
}
.scrollbar {
  height: 320px;
  width: 100%;
  overflow: scroll;
}
.info_label {
  top: 50px;
}
.labeling {
  top: 20px;
}
.scores {
  padding-bottom: 20px;
}
</style>
