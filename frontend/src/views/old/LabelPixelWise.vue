<template>
    <v-card outlined class="mx-3 my-3">

        <!--- Here the user makes the selection between assisted and by hand labeling --->
        <v-row class="approach" v-if="labelingApproach === 'none'">
            <v-hover v-slot:default="{ hover }">
              <v-card
                class="mx-auto"
                color="grey lighten-4"
                width="520"
                min-width="520"
                height ="580"
              >
                <v-img
                  :aspect-ratio="16/9"
                  src="../assets/usability-test.jpg"
                  v-on:click="selectApproach('assisted')"
                >
                  <v-expand-transition>
                    <div
                      v-if="hover"
                      class="d-flex transition-fast-in-fast-out orange darken-2 v-card--reveal
                        display-3 white--text"
                      style="height: 100%;"
                    >
                      Click here to start!
                    </div>
                  </v-expand-transition>
                </v-img>
                <v-card-text
                  class="pt-6"
                  style="position: relative;"
                >
                 <!-- <div class="font-weight-light grey--text title mb-2"></div>-->
                  <h3 class="display-1 font-weight-light orange--text mb-2">Usability Test</h3>
                  <div class="font-weight-light title mb-2">
                    The test is split in four sections: <br>
                    First Look, Test Time, Close Look and Attractiveness.<br>
                    You can find the same sections in the questionnaire.
                  </div>
                </v-card-text>
                <div>
                <v-layout row justify-center>
                  <a href = "https://docs.google.com/forms/d/e/1FAIpQLSfSQznwaVyLGWuqul62sSu2JUgWi-ynAoSBYgQgLEapw8ajmw/viewform?usp=sf_link" target="_blank">
                  <v-btn color="primary" class="mr-4 save-button-id"
                  name="save" id="save-button-id">
                  <v-icon left>mdi-download</v-icon>
                  get questionnaire
                  </v-btn>
                  </a>
                </v-layout>
                </div>
              </v-card>
            </v-hover>
        </v-row>

        <!--- If the user has chosen assisted labeling --->
        <v-col class="content" v-if="labelingApproach === 'assisted'">
            <div class="root" align="center">
                <div class="wrapper-mains" align="center">
                    <div class="left-align">
                        <step-progress :stepInfo="assistedSteps"></step-progress>
                    </div>
                </div>
            </div>

            <div class="comp-space">
                <keep-alive>
                    <component class="main-component" :is="currentComponent"
                    :allProperties="currentProperties"
                    @selectProcedure="selectProcedure($event)"
                    @updateClasses="updateClasses($event)"
                    @colorSelect="colorSelect($event)"
                    @updateClassCount="updateClassCount($event)"
                    @uploadRectangles="uploadRectangles($event)"
                    @selectAlgorithm="selectAlgorithm($event)"
                    @updateComponent="updateComponent($event)"
                    @saveRequest="saveRequest($event)"
                    @verifyBoxes="verifyBoxes($event)"
                    @skipBoxes="skipBoxes($event)"
                    @deleteBoxes="deleteBoxes($event)"
                    @updateBoxes="updateBoxes($event)"
                    @restart="restart()"
                    ></component>
                </keep-alive>
            </div>
        </v-col>

        <!--- If the user has chosen by-hand labeling --->
        <v-col class="content" v-if="labelingApproach === 'byhand'">
            <div class="root" align="center">
                <div class="wrapper-mains" align="center">
                    <div class="left-align">
                        <step-progress :stepInfo="byHandSteps"></step-progress>
                    </div>
                </div>
            </div>

            <div class="comp-space">
                <keep-alive>
                    <component class="main-component" :is="currentComponent"
                    :allProperties="currentProperties"
                    @selectProcedure="selectProcedure($event)"
                    @colorSelect="colorSelect($event)"
                    @selectAlgorithm="selectAlgorithm($event)"
                    @updateComponent="updateComponent($event)"
                    @saveRequest="saveRequest($event)"
                    @keepTraining="keepTraining()"
                    @verifyBoxes="verifyBoxes($event)"
                    @skipBoxes="skipBoxes($event)"
                    @updateBoxes="updateBoxes($event)"
                    ></component>
                </keep-alive>
            </div>
        </v-col>
    </v-card>
</template>

<script>
import LabelingStart from '@/components/PWLabelingStart.vue';
import LabelingAlgorithm from '@/components/LabelingAlgorithm.vue';
import LabelingTrain from '@/components/LabelingTrain.vue';
import StepProgress from '@/components/StepProgressSlider.vue';
import LabelingFinish from '@/components/LabelingFinish.vue';
import LabelingReview from '@/components/LabelingReview.vue';
import LabelingFirstLook from '@/components/PWLabelingInitialize.vue';
import LabelingTestTime from '@/components/PWLabelingTestTime.vue';
import LabelingCloseLook from '@/components/PWLabelingCloseLook.vue';
import LabelingAttractiveness from '@/components/PWLabelingAttractiveness.vue';
import UsabilityTest from '@/components/usabilityTest.vue';

export default {
  components: {
    LabelingStart,
    LabelingAlgorithm,
    LabelingTrain,
    StepProgress,
    LabelingFinish,
    LabelingReview,
    UsabilityTest,
    LabelingFirstLook,
    LabelingTestTime,
    LabelingCloseLook,
    LabelingAttractiveness,
  },
  data: () => ({
    currentComponent: 'LabelingFirstLook',
    labelingApproach: 'none',
    steps: [
      'First Look',
      'Test Time',
      'Close Look',
      'Attractiveness',
      'Finish',
      /* 'Data Setup',
      'Initialization',
      'Algorithm Selection',
      'Assisted Training',
      'Labeling',
      'Review',
      'Finish', */
    ],
    currentStep: 1,
    labelingClasses: [
      {
        name: 'Single Cell',
        color: 'red',
        inFinal: true,
        delete: 'Delete',
        count: 0,
        id: Date.now(),
      },
      {
        name: 'Aggregate',
        color: 'orange',
        inFinal: true,
        delete: 'Delete',
        count: 0,
        id: Date.now() + 1,
      },
      {
        name: 'Parasite',
        color: 'green',
        inFinal: true,
        delete: 'Delete',
        count: 0,
        id: Date.now() + 2,
      },
      {
        name: 'Other',
        color: 'blue',
        inFinal: true,
        delete: 'Delete',
        count: 0,
        id: Date.now() + 3,
      },
      {
        name: 'Background',
        color: 'grey',
        inFinal: false,
        delete: 'Delete',
        count: 0,
        id: Date.now() + 4,
      },
    ],
    classCounts: [],
    procedure: 'createNew',
    selectedColor: 'red',
    algorithm: 'none',
    trainingProgress: 0,
    storeParameters: 'P',
  }),
  computed: {
    currentProperties() {
      if (this.currentComponent === 'LabelingStart') {
        return { procedure: this.procedure, labelingClasses: this.labelingClasses };
      }
      if (this.currentComponent === 'LabelingFirstLook') {
        return {
          importedFiles: this.importedFiles,
          labelingClasses: this.labelingClasses,
          classCounts: this.classCounts,
          color: this.selectedColor,
        };
      }
      if (this.currentComponent === 'LabelingAlgorithm') {
        return { algorithm: this.algorithm, labelingClasses: this.labelingClasses };
      }
      if (this.currentComponent === 'LabelingTrain') {
        return {
          trainingProgress: this.trainingProgress,
          boundingBoxes: this.boundingBoxes,
          labelingClasses: this.labelingClasses,
        };
      }
      return { property: 'none' };
    },
    assistedSteps() {
      const a = this.steps.slice(0, 5);
      // const b = this.steps.slice(5, 7);
      return { steps: a, current: this.currentStep }; // .concat(b)
    },
    byHandSteps() {
      const a = this.steps.slice(0, 1);
      const b = this.steps.slice(4, 7);
      return { steps: a.concat(b), current: this.currentStep };
    },
  },
  methods: {
    updateComponent(update) {
      if (update === 'next') {
        switch (this.currentComponent) {
          /* case 'LabelingStart':
            if (this.labelingApproach === 'assisted') {
              this.currentComponent = 'LabelingFirstLook';
              this.currentStep = 2;
            } else if (this.labelingApproach === 'byhand') {
              this.currentComponent = 'LabelingFirstLook';
              this.currentStep = 2;
            }
            break; */
          case 'LabelingFirstLook':
            if (this.labelingApproach === 'assisted') {
              this.currentComponent = 'LabelingTestTime';
              this.currentStep = 2;
            } else if (this.labelingApproach === 'byhand') {
              this.currentComponent = 'LabelingReview';
              this.currentStep = 2;
            }
            break;
          case 'LabelingTestTime':
            this.currentComponent = 'LabelingCloseLook';
            this.currentStep = 3;
            break;
          case 'LabelingCloseLook':
            this.currentComponent = 'LabelingAttractiveness';
            this.currentStep = 4;
            break;
          case 'LabelingAttractiveness':
            if (this.labelingApproach === 'assisted') {
              this.currentComponent = 'UsabilityTest';
              this.currentStep = 5;
            } else if (this.labelingApproach === 'byhand') {
              this.currentComponent = 'LabelingFinish';
              this.currentStep = 4;
            }
            break;
          case 'UsabilityTest':
            if (this.labelingApproach === 'assisted') {
              this.currentComponent = 'LabelingFinish';
              this.currentStep = 7;
            } else if (this.labelingApproach === 'byhand') {
              this.currentComponent = 'LabelingFinish';
              this.currentStep = 5;
            }
            break;
          default:
            break;
        }
      } else if (update === 'back') {
        switch (this.currentComponent) {
          case 'UsabilityTest':
            if (this.labelingApproach === 'assisted') {
              this.currentComponent = 'LabelingAttractiveness';
              this.currentStep = 4;
            } else if (this.labelingApproach === 'byhand') {
              this.currentComponent = 'LabelingReview';
              this.currentStep = 3;
            }
            break;
          case 'LabelingAttractiveness':
            if (this.labelingApproach === 'assisted') {
              this.currentComponent = 'LabelingCloseLook';
              this.currentStep = 3;
            } else if (this.labelingApproach === 'byhand') {
              this.currentComponent = 'LabelingInitialize';
              this.currentStep = 2;
            }
            break;
          case 'LabelingCloseLook':
            this.currentComponent = 'LabelingTestTime';
            this.currentStep = 2;
            break;
          case 'LabelingTestTime':
            this.currentComponent = 'LabelingFirstLook';
            this.currentStep = 1;
            break;
          case 'LabelingFirstLook':
            this.labelingApproach = 'none';
            break;
          case 'LabelingStart':
            this.labelingApproach = 'none';
            break;
          default:
            break;
        }
      }
    },
    selectApproach(approachType) {
      this.labelingApproach = approachType;
    },
    selectProcedure(procedureType) {
      if (procedureType === 'createNew') {
        this.procedure = 'create';
      } else if (procedureType === 'extendOld') {
        this.procedure = 'extend';
      }
    },
    updateClasses(labelingClasses) {
      this.labelingClasses = JSON.parse(JSON.stringify(labelingClasses));
    },
    colorSelect(color) {
      this.selectedColor = color;
    },
    updateClassCount(countUpdate) {
      this.labelingClasses.find(
        temp => temp.id === countUpdate.classId,
      ).count += countUpdate.update;
    },
    uploadRectangles(rectangles) {
      this.boundingBoxes = JSON.parse(JSON.stringify(rectangles));
    },
    selectAlgorithm(algorithmType) {
      if (algorithmType === 'threshold') {
        this.algorithm = 'threshold';
      } else if (algorithmType === 'rcnn') {
        this.algorithm = 'rcnn';
      } else if (algorithmType === 'yolo') {
        this.algorithm = 'yolo';
      }
    },
    verifyBoxes(index) {
      this.boundingBoxes[index].uncertainty = 'reviewed';
    },
    skipBoxes(index) {
      this.boundingBoxes[index].uncertainty = 'skipped';
      const classId = this.labelingClasses.find(
        temp => temp.name === 'Other',
      ).id;
      if (classId !== undefined) {
        this.boundingBoxes[index].class = classId;
      }
    },
    deleteBoxes(index) {
      this.boundingBoxes[index].uncertainty = 'deleted';
    },
    updateBoxes(boundingBox) {
      const index = boundingBox.index;
      this.boundingBoxes[index].class = boundingBox.class;
      this.boundingBoxes[index].ref = boundingBox.ref;
      this.boundingBoxes[index].x = boundingBox.x;
      this.boundingBoxes[index].y = boundingBox.y;
      this.boundingBoxes[index].width = boundingBox.width;
      this.boundingBoxes[index].height = boundingBox.height;
      this.boundingBoxes[index].uncertainty = boundingBox.uncertainty;
    },
    saveRequest(saveParameters) {
      console.log(saveParameters.series);
    },
    restart() {
      this.labelingApproach = 'none';
      this.currentComponent = 'LabelingInitialize';
      this.currentStep = 1;
      // Not completely working yet, needs to reset all data attributes as well
      this.$forceMount();
    },
    keepTraining() {
      this.trainingProgress = this.trainingProgress + 50;
    },
  },
};
</script>

<style scoped>

    .wrapper-mains{
        width: 100%;
        height: 100%;
        text-align: center;
        margin: auto;
        padding: 1px 1px 1px 1px;
    }
    .textarea{
        display: block;
        width: 100%;
        height: 70px;
        border-radius: 5px;
    }

    .root{
        height: 80px;
        z-index: 3;
    }

    .main-component{
        z-index: 1;
        width: 1000px;
        height: 500px;
        margin: auto;
    }

    .nav-arrow{
        margin: 400px 20px 30px 30px;
    }

    .hidden{
        visibility: hidden;
    }

    .comp-space{
        width: 100%;
        height: 100%;
    }

    .content{
        width: 100%;
        height: 100%;
    }

    .highlight{
        border: 3px solid black;
    }

    .min-block{
        min-width: 1020px;
    }

    .approach{
      /*min-width: 400px;*/
      width: 100%;
      /*min-height: 400px;*/
      height: 100%;
      margin: 49px auto;
    }

    .v-card--reveal {
      align-items: center;
      bottom: 0;
      justify-content: center;
      opacity: .5;
      position: absolute;
      width: 100%;
    }
</style>
