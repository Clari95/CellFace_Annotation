<template>
    <v-card outlined height="720" class="mx-3 my-3">

        <!--- Here the user makes the selection between game and by hand labeling --->
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
                  src="../assets/CellsBlue.jpg"
                >
                  <v-expand-transition>
                    <div
                      v-if="hover"
                      class="d-flex transition-fast-in-fast-out purple darken-2 v-card--reveal
                        display-3 white--text"
                      style="height: 100%;"
                    >
                      Let's Play!
                    </div>
                  </v-expand-transition>
                </v-img>
                <v-card-text
                  class="pt-6"
                  style="position: relative;"
                >
                 <!-- <div class="font-weight-light grey--text title mb-2"></div>-->
                  <h3 class="display-1 font-weight-light purple--text mb-2">Game</h3>
                  <div class="font-weight-light title mb-2">
                    It's time for playing! <br>
                    <b> Try to achieve 1700 points! </b>
                  </div>
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
                    v-on:click="selectApproach('game')">
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

        <!--- If the user has chosen game labeling --->
        <v-col class="content" v-if="labelingApproach === 'game'">
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
                    :key="currentStep"
                    :allProperties="currentProperties"
                    @selectProcedure="selectProcedure($event)"
                    @colorSelect="colorSelect($event)"
                    @updateDatasetTyp ="updateDatasetTyp($event)"
                    @updateComponent="updateComponent($event)"
                    @restart="restart()"
                    @updateScores ="updateScores($event)"
                    @updateAccuracy ="updateAccuracy($event)"
                    @updatePoints ="updatePoints($event)"
                    ></component>
                <!--</keep-alive>-->
            </div>
        </v-col>
    </v-card>
</template>

<script>
import StepProgress from '@/components/StepProgressSlider.vue';
import LabelingInfo from '@/components/PWLabelingGameInfo.vue';
import LabelingGetData from '@/components/PWLabelingGameData.vue';
// import LabelingGameTask from '@/components/PWLabelingGameTaskLevel1.vue';
// import LabelingLevel2 from '@/components/PWLabelingGameTaskLevel2.vue';
// import LabelingLevel3 from '@/components/PWLabelingGameTaskLevel3.vue';
// import LabelingFinal from '@/components/PWLabelingGameTaskFinal.vue'; // final Task
// import LabelingLevel4 from '@/components/PWLabelingGameTaskLevel4.vue';
// import LabelingLevel5 from '@/components/PWLabelingGameTaskLevel5.vue';
import LabelingGameTask from '@/components/PWLabelingGameTask.vue';
import LabelingReview from '@/components/PWLabelingGameReview.vue';

export default {
  components: {
    StepProgress,
    LabelingInfo,
    LabelingGetData,
    // LabelingLevel1,
    // LabelingLevel2,
    // LabelingLevel3,
    // LabelingFinal,
    // LabelingLevel4,
    // LabelingLevel5,
    LabelingGameTask,
    LabelingReview,
  },
  data: () => ({
    reload: 1,
    currentComponent: 'LabelingInfo',
    labelingApproach: 'none',
    steps: [
      'Info',
      'Data',
      'Level 1',
      'Level 2',
      'Level 3',
      'Level 4',
      'Level 5',
      'Review',
    ],
    currentStep: 1,
    dataset: 'none',
    // for getting info about cells
    dialog_SingelCell: false,
    UserID: '',
    rules: [v => !!v || 'Req',
      v => v.length <= 12 || 'Max 12 signs'],
    counterEn: false,
    counter: 0,
    missingUserID: '',
    points: 0,
    // amount levels here 4
    allPoints: 0,
    AllScores: [0, 0, 0, 0, 0],
    accuracy_list: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    numberImagesLevel: [3, 4, 2, 10, 10],
    currentLevel: 1,
    skipped: false,
  }),
  computed: {
    currentProperties() {
      if (this.currentComponent === 'LabelingLevel1') {
        return {
          dataset_typ: this.dataset,
          UserID: this.UserID,
          numberLabeledCells: this.numberLabeledCells,
          numberLabeledRegions: this.numberLabeledRegions,
          labelTime: this.labelTime,
          addedAreas: this.addedAreas,
          labelingApproach: this.labelingApproach,
          points: this.points,
          AllScores: this.AllScores,
          allPoints: this.allPoints,
          currentLevel: this.currentLevel,
        };
      }
      if (this.currentComponent === 'LabelingLevel2') {
        return {
          dataset_typ: this.dataset,
          UserID: this.UserID,
          numberLabeledCells: this.numberLabeledCells,
          numberLabeledRegions: this.numberLabeledRegions,
          labelTime: this.labelTime,
          addedAreas: this.addedAreas,
          labelingApproach: this.labelingApproach,
          AllScores: this.AllScores,
          allPoints: this.allPoints,
          points: this.points,
          currentLevel: this.currentLevel,
        };
      }
      if (this.currentComponent === 'LabelingLevel3') {
        return {
          dataset_typ: this.dataset,
          UserID: this.UserID,
          numberLabeledCells: this.numberLabeledCells,
          numberLabeledRegions: this.numberLabeledRegions,
          labelTime: this.labelTime,
          addedAreas: this.addedAreas,
          labelingApproach: this.labelingApproach,
          AllScores: this.AllScores,
          allPoints: this.allPoints,
          points: this.points,
          currentLevel: this.currentLevel,
        };
      }
      if (this.currentComponent === 'LabelingLevel4') {
        return {
          dataset_typ: this.dataset,
          UserID: this.UserID,
          numberLabeledCells: this.numberLabeledCells,
          numberLabeledRegions: this.numberLabeledRegions,
          labelTime: this.labelTime,
          addedAreas: this.addedAreas,
          labelingApproach: this.labelingApproach,
          points: this.points,
          AllScores: this.AllScores,
          allPoints: this.allPoints,
          currentLevel: this.currentLevel,
        };
      }
      if (this.currentComponent === 'LabelingLevel5') {
        return {
          dataset_typ: this.dataset,
          UserID: this.UserID,
          numberLabeledCells: this.numberLabeledCells,
          numberLabeledRegions: this.numberLabeledRegions,
          labelTime: this.labelTime,
          addedAreas: this.addedAreas,
          labelingApproach: this.labelingApproach,
          points: this.points,
          AllScores: this.AllScores,
          allPoints: this.allPoints,
          currentLevel: this.currentLevel,
        };
      }
      if (this.currentComponent === 'LabelingGameTask') {
        return {
          dataset_typ: this.dataset,
          UserID: this.UserID,
          numberLabeledCells: this.numberLabeledCells,
          numberLabeledRegions: this.numberLabeledRegions,
          labelTime: this.labelTime,
          addedAreas: this.addedAreas,
          labelingApproach: this.labelingApproach,
          points: this.points,
          AllScores: this.AllScores,
          allPoints: this.allPoints,
          currentLevel: this.currentLevel,
          numberImagesLevel: this.numberImagesLevel,
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
          labelingApproach: this.labelingApproach,
          accuracy_list: this.accuracy_list,
          currentLevel: this.currentLevel,
          skipped: this.skipped,
          AllScores: this.AllScores,
          points: this.points,
        };
      }
      return {
        labelingApproach: this.labelingApproach,
      };
    },
    Steps() {
      const a = this.steps.slice(0, 8);
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
    updatePoints(points) {
      this.points = points;
      console.log(`ponts in main: ${this.points}`);
    },
    updateScores(Scores) {
      console.log('UPDTAESCORES');
      this.numberLabeledImages = Scores[0];
      this.numberLabeledCells = Scores[1];
      this.numberLabeledRegions = Scores[2];
      this.addedAreas = Scores[4];
      this.labelTime = Scores[5];
      this.allPoints = this.allPoints + Scores[6];
      this.accuracy = Scores[7];
      const level = Scores[8];
      this.AllScores[level - 1] = Scores;
      console.log(this.AllScores);
      console.log(this.allPoints);
      console.log(`current level: ${this.currentLevel}`);
    },
    updateAccuracy(accuracyNew) {
      if (this.skipped === false) {
        console.log(`in update accuracy: ${accuracyNew} for level ${this.currentLevel}!`);
        this.accuracy_list[this.currentLevel - 1] = accuracyNew;
      } else {
        const level = accuracyNew[4];
        accuracyNew.pop();
        this.accuracy_list[level - 1] = accuracyNew;
        console.log(this.accuracy_list);
        if (level === 5) {
          this.skipped = false;
        }
      }
    },
    showInfo(showDialog) {
      this.dialog_SingelCell = showDialog;
    },
    updateComponent(update) {
      console.log('updatecomp');
      console.log(this.currentStep);
      if (update === 'next') {
        switch (this.currentComponent) {
          case 'LabelingInfo':
            this.currentComponent = 'LabelingGetData';
            this.currentStep = 2;
            this.currentLevel = 0;
            break;
          case 'LabelingGetData':
            console.log('here');
            this.currentComponent = 'LabelingGameTask';
            this.currentStep = 3;
            this.currentLevel = 1;
            break;
          case 'LabelingGameTask':
            if (this.currentLevel < 5) {
              this.currentComponent = 'LabelingGameTask';
              this.currentStep += 1;
              this.currentLevel += 1;
              console.log(`in next comp current Level: ${this.currentLevel}`);
            } else {
              this.currentComponent = 'LabelingReview';
              this.currentStep = 8;
              // this.currentLevel = 0;
            }
            break;
          case this.currentLevel === 5:
            this.currentComponent = 'LabelingReview';
            this.currentStep = 8;
            // this.currentLevel = 0;
            break;
          default:
            break;
        }
      } else if (update === 'back') {
        switch (this.currentComponent) {
          case 'LabelingReview':
            this.currentComponent = 'LabelingGameTask';
            this.currentStep = 7;
            this.currentLevel = 5;
            break;
          case 'LabelingGameTask':
            if (this.currentLevel > 1) {
              this.currentComponent = 'LabelingGameTask';
              this.currentStep -= 1;
              this.currentLevel -= 1;
            } else {
              this.currentComponent = 'LabelingGetData';
              this.currentStep = 2;
              this.currentLevel = 0;
            }
            break;
          case this.currentLevel === 1:
            this.currentComponent = 'LabelingGetData';
            this.currentStep = 2;
            this.currentLevel = 0;
            break;
          case 'LabelingGetData':
            this.currentComponent = 'LabelingInfo';
            this.currentStep = 1;
            this.currentLevel = 0;
            break;
          case 'LabelingInfo':
            break;
          default:
            break;
        }
      } else if (update === 'again') {
        this.currentComponent = 'LabelingGetData';
        this.currentStep = 2;
        this.currentLevel = 0;
        this.allPoints = 0;
        this.points = 0;
      } else if (update === 'review') {
        console.log('in update to review');
        this.currentComponent = 'LabelingReview';
        this.currentStep = 8;
        // this.currentLevel = 0;
        this.skipped = true;
      }
    },
    selectApproach(approachType) {
      this.labelingApproach = approachType;
    },
    colorSelect(color) {
      this.selectedColor = color;
    },
    restart() {
      console.log('RESTART');
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
    .save-button-id{
      margin-left: 5px;
    }
</style>
