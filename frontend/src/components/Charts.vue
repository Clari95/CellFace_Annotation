<template>
<div>
  <v-row justify="space-around" dense>
    <v-col cols="6">
      <v-card
        class="mt-4 mx-auto"
        max-width="400"
      >
        <v-sheet
          class="v-sheet--offset mx-auto"
          color="teal lighten-5"
          elevation="9"
          max-width="calc(100% - 32px)"
        >
          <v-sparkline
            show-labels
            :value="values_areas"
            color="teal"
            line-width="2"
            padding="16"
          ></v-sparkline>
        </v-sheet>

        <v-card-text class="pt-0">
          <div class="subheading font-weight-light grey--text">
            <br/>
          </div>
          <div class="title font-weight-light mb-2">Accuracy labled areas Level 1-5 [%]</div>
          <div class="subheading font-weight-light grey--text">
            Accuracy: number of labled areas / number of all areas
          </div>
        </v-card-text>
      </v-card>
     </v-col>
     <v-col cols="6">
      <v-card
        class="mt-4 mx-auto"
        max-width="400"
      >
        <v-sheet
          class="v-sheet--offset mx-auto"
          color="teal lighten-5"
          elevation="9"
          max-width="calc(100% - 32px)"
        >
          <v-sparkline
            show-labels
            :labels="labels_correct"
            :value="values_correct"
            color="teal"
            line-width="2"
            padding="16"
          ></v-sparkline>
        </v-sheet>

        <v-card-text class="pt-0">
          <div class="subheading font-weight-light grey--text">
            <br/>
          </div>
          <div class="title font-weight-light mb-2">Accuracy correctness Level 1-5 [%]</div>
          <div class="subheading font-weight-light grey--text">
            Accuracy: number of correct lables / all labeled areas
          </div>
        </v-card-text>
      </v-card>
     </v-col>
     <!--<v-col cols="2">
      <v-card
        class="mt-4 mx-auto"
        max-width="400"
        height = "70"
      >
      <div class='text-center help'>
    <v-dialog v-model='dialog' width='1000'>
      <template v-slot:activator='{ on, attrs }'>
        <v-btn small color='teal' dark v-bind='attrs' v-on='on'>See SegMasks</v-btn>
      </template>

      <v-card >
        <v-card-title class='headline grey lighten-2'
        primary-title>Results</v-card-title>
        <v-divider></v-divider>
        <v-card-actions>
          <div class="scrollbar" id="grid" v-if="ImagesResults">
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
                        width="260"
                        height="155"
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
                            SegMask for image <b>{{i + 1}}</b>
                        </v-card-text>

                      </v-card>
                    </v-item>
                  </v-col>
                </v-row>
              </v-container>
            </v-item-group>
          </div>
          <v-spacer></v-spacer>
          <v-btn color='primary' text @click="dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
      </v-card>
     </v-col>-->
  </v-row>
</div>
</template>

<script>

export default {
  props: {
    accuracies: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    // ImagesResults: null,
    dialog: false,
    labels_areas: ['Level1', 'Level2', 'Level3', 'Level4', 'Level5'], // 5Level
    labels_correct: [0, 0, 0, 0, 0],
    values_areas: [0, 0, 0, 0, 0],
    values_correct: [0, 0, 0, 0, 0],
  }),
  mounted() {
    this.renderChart();
  },

  methods: {
    renderChart() {
      this.accuracy_now = Math.round(this.accuracy_now * 100);
      this.values_areas = [Math.round(this.accuracies[0][0] * 100),
        Math.round(this.accuracies[1][0] * 100),
        Math.round(this.accuracies[2][0] * 100),
        Math.round(this.accuracies[3][0] * 100),
        Math.round(this.accuracies[4][0] * 100)];
      this.values_correct = [Math.round(this.accuracies[0][2] * 100),
        Math.round(this.accuracies[1][2] * 100),
        Math.round(this.accuracies[2][2] * 100),
        Math.round(this.accuracies[3][2] * 100),
        Math.round(this.accuracies[4][2] * 100)];
    },
  },
};
</script>

<style>

#overlay-btn {
  position: absolute;
  top: 1em;
  right: 1em;
}
.scrollbar{
  height: 320px;
  width: 100%;
  overflow: scroll;
}

</style>
