<template>
    <v-card outlined height="700" class="mx-3 my-3">

        <!--- Here the user makes the selection between basic and by hand labeling --->
        <v-row class="approach" v-if="labelingApproach === 'none'">
            <v-hover v-slot:default="{ hover }">
              <v-card
                class="mx-auto"
                color="grey lighten-4"
                width="520"
                min-width="520"
                height ="630"
              >
                <v-img
                  :aspect-ratio="16/9"
                  src="../assets/Cellsteal.jpg"
                >
                  <v-expand-transition>
                    <div
                      v-if="hover"
                      class="d-flex transition-fast-in-fast-out teal darken-2 v-card--reveal
                        display-3 white--text"
                      style="height: 100%;"
                    >
                      Let's label!
                    </div>
                  </v-expand-transition>
                </v-img>
                <v-card-text
                  class="pt-6"
                  style="position: relative;"
                >
                 <!-- <div class="font-weight-light grey--text title mb-2"></div>-->
                  <h3 class="display-1 font-weight-light teal--text mb-2">Basic Tool</h3>
                  <v-card-text class="font-weight-light title mb-2">
                    This Tool get developed <br> after the evaluation of the frist version.
                  </v-card-text>
                </v-card-text>
                <div>
                <v-layout row align-center justify-center>
                  <v-col sm="6" md="8" justify-center>
                    <v-text-field
                      class = "max-auto"
                      v-model="UserID"
                      counter="12"
                      label="UserID"
                      placeholder="__ __ __ __ __ __ __ __ "
                      outlined
                      :rules="rules"
                    ></v-text-field>
                    <div sm = "6" class="save-button-id">
                    <v-btn @click="createUserID()"
                    color="primary" sm ="6" class="mr-4 save-button-id" name="save"
                    id="save-button-id"
                    v-on:click="selectApproach('basic')">
                    SAVE
                    </v-btn>
                    <div>
                    <v-card-text sm ="6" style="font-size:10px">
                      {{missingUserID}}
                    </v-card-text>
                    </div>
                    </div>
                  </v-col>
                </v-layout>
                </div>
              </v-card>
            </v-hover>
        </v-row>

        <!--- If the user has chosen basic labeling --->
        <v-col class="content" v-if="labelingApproach === 'basic'">
            <div class="root" align="center">
                <div class="wrapper-mains" align="center">
                    <div class="left-align">
                        <step-progress :stepInfo="Steps"></step-progress>
                    </div>
                </div>
            </div>

            <div class="comp-space">
                <!--<keep-alive>-->
                    <component class="main-component" :is="currentComponent"
                    :allProperties="currentProperties"
                    @updateDatasetTyp ="updateDatasetTyp($event)"
                    @updateComponent="updateComponent($event)"
                    @restart="restart()"
                    @updateScores ="updateScores($event)"
                    @updateAccuracy ="updateAccuracy($event)"
                    @updateSection="updateSection($event)"
                    ></component>
                <!--</keep-alive>-->
            </div>
        </v-col>
    </v-card>
</template>

<script>
import StepProgress from '@/components/StepProgressSlider.vue';
import LabelingInfo from '@/components/PWLabelingBasicInfo.vue';
// import LabelingInfoGame from '@/components/PWLabelingGameInfo.vue';
import LabelingGetData from '@/components/PWLabelingBasicData.vue';
import LabelingTask from '@/components/PWLabelingBasicTask.vue';
import LabelingReview from '@/components/PWLabelingBasicReview.vue';
// import LabelingReviewGame from '@/components/PWLabelingGameReview.vue';

export default {
  components: {
    StepProgress,
    LabelingInfo,
    // LabelingInfoGame,
    LabelingGetData,
    LabelingTask,
    LabelingReview,
    // LabelingReviewGame,
  },
  data: () => ({
    currentComponent: 'LabelingInfo',
    labelingApproach: 'none',
    steps: [
      'Info',
      'Data',
      'Task',
      'Review',
    ],
    currentStep: 1,
    // for getting data
    dataset: 'none',
    // for getting info about cells
    dialog_SingelCell: false,
    UserID: '',
    rules: [v => !!v || 'Req',
      v => v.length <= 12 || 'Max 12 signs'],
    counterEn: false,
    counter: 0,
    missingUserID: '',
    // counter labeling
    numberLabeledImages: 0,
    numberLabeledCells: 0,
    numberLabeledRegions: 0,
    addedAreas: 0,
    labelTime: 0,
    accuracy: 0,
    AllScores: [0, 0],
    currentSection: 0,
    skipped: false,
  }),
  computed: {
    currentProperties() {
      if (this.currentComponent === 'LabelingTask') {
        return {
          dataset_typ: this.dataset,
          UserID: this.UserID,
          numberLabeledCells: this.numberLabeledCells,
          numberLabeledRegions: this.numberLabeledRegions,
          labelTime: this.labelTime,
          addedAreas: this.addedAreas,
          labelingApproach: this.labelingApproach,
          currentSection: this.currentSection,
        };
      }
      if (this.currentComponent === 'LabelingReview') {
        return {
          dataset_typ: this.dataset,
          UserID: this.UserID,
          numberLabeledImages: this.numberLabeledImages,
          numberLabeledCells: this.numberLabeledCells,
          numberLabeledRegions: this.numberLabeledRegions,
          labelTime: this.labelTime,
          addedAreas: this.addedAreas,
          accuracy: this.accuracy,
          labelingApproach: this.labelingApproach,
          AllScores: this.AllScores,
          skipped: this.skipped,
          currentSection: this.currentSection,
        };
      }
      return {
        labelingApproach: this.labelingApproach,
      };
    },
    Steps() {
      const a = this.steps.slice(0, 5);
      // const b = this.steps.slice(5, 7);
      return { steps: a, current: this.currentStep }; // .concat(b)
    },
  },
  methods: {
    createUserID() {
      console.log('createUserID');
      console.log(this.UserID);
    },
    updateDatasetTyp(typ) {
      this.dataset = typ;
    },
    updateSection(section) {
      console.log(`update section ${section}`);
      this.currentSection = section;
    },
    updateScores(Scores) {
      console.log('UPDTAESCORES');
      console.log(Scores);
      // this.imageRef_num, this.numberCells, this.numberRegions, wrongAreas,
      //    this.addedAreas, this.seconds,
      //   this.allProperties.points, response.data.accuracy_all, this.allProperties.currentLevel
      this.numberLabeledImages = Scores[0];
      this.numberLabeledCells = Scores[1];
      this.numberLabeledRegions = Scores[2];
      this.addedAreas = Scores[4];
      this.labelTime = Scores[5];
      this.allPoints = this.allPoints + Scores[6];
      this.accuracy = Scores[7];
      const level = Scores[8];
      this.AllScores[level] = Scores;
      // this.currentLevel = this.currentLevel + 1;
      // console.log(`current level: ${this.currentLevel}`);
      console.log('scores: ');
      console.log(this.AllScores);
    },
    updateAccuracy(accuracy) {
      console.log(`in update accuracy: ${accuracy}`);
      // const accuracyAverage = Math.round(accuracy[3] * 100) / 100;
      // console.log(`update acc: ${accuracyAverage}`);
      const accuracyNumAreas = Math.round(accuracy[0] * 100) / 100;
      console.log(`update acc: ${accuracyNumAreas}`);
      this.accuracy = accuracyNumAreas;
    },
    showInfo(showDialog) {
      console.log('showInfo');
      this.dialog_SingelCell = showDialog;
      console.log(this.dialog_SingelCell);
    },
    updateComponent(update) {
      console.log('updatecomp');
      if (update === 'next') {
        switch (this.currentComponent) {
          case 'LabelingInfo':
            this.currentComponent = 'LabelingGetData';
            this.currentStep = 2;
            break;
          case 'LabelingGetData':
            this.currentComponent = 'LabelingTask';
            this.currentStep = 3;
            break;
          case 'LabelingTask':
            this.currentComponent = 'LabelingReview';
            this.currentStep = 4;
            break;
          default:
            break;
        }
      } else if (update === 'back') {
        switch (this.currentComponent) {
          case 'LabelingReview':
            this.currentComponent = 'LabelingTask';
            this.currentStep = 3;
            break;
          case 'LabelingTask':
            this.currentComponent = 'LabelingGetData';
            this.currentStep = 2;
            break;
          case 'LabelingGetData':
            // this.labelingApproach = 'none';
            this.currentComponent = 'LabelingInfo';
            this.currentStep = 1;
            break;
          case 'LabelingInfo':
            // this.labelingApproach = 'none';
            // this.currentStep = 1;
            break;
          default:
            break;
        }
      } else if (update === 'review') {
        console.log('in update to review');
        this.currentComponent = 'LabelingReview';
        this.currentStep = 4;
        // this.currentLevel = 0;
        this.skipped = true;
      }
    },
    selectApproach(approachType) {
      this.labelingApproach = approachType;
    },
    restart() {
      this.labelingApproach = 'none';
      this.currentComponent = 'LabelingInitialize';
      this.currentStep = 1;
      // Not completely working yet, needs to reset all data attributes as well
      this.$forceMount();
    },
    /* keepTraining() {
      this.trainingProgress = this.trainingProgress + 50;
    }, */
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
    .save-button-id{
      margin-left: 5px;
    }
</style>
