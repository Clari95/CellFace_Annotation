<template>
  <div class="wrapper">
    <v-row fill-width>
      <!--<div class="nav-arrow-back"  id="back-button">
            <v-btn small @click="updateComponent('again'); restart()" color='primary' class='mr-4'>
            <v-icon left>mdi-rocket-outline</v-icon>Play <br/>again!
            </v-btn>
        </div>-->
      <!--- Main component starts here --->
      <v-col class="mx-auto mt-0 main">
        <div>
          <div>
            <v-row justify="space-around" dense>
              <v-col cols="10">
                <v-card height="150">
                  <v-card-text style="margin: 0px 0px; padding: 2px 5px">
                    <p>
                      <b class="display-1 font-weight-light teal--text mb-2"
                        >Info</b
                      >
                      for <b>{{ allProperties.UserID }}</b> | number labeled
                      cells: {{ data_ges[65][0] }} | number labeled regions:
                      {{ data_ges[66][0] }}| number added Areas:
                      {{ data_ges[68][0] }}
                    </p>
                  </v-card-text>
                  <v-sheet
                    class="v-sheet--offset mx-auto"
                    color="teal lighten-5"
                    elevation="8"
                    max-width="calc(100% - 32px)"
                  >
                    <v-data-table
                      dense
                      disable-sort
                      :headers="leaderboardHeaders"
                      :items="yourData"
                      :items-per-page="1"
                      item-key="date"
                      hide-default-footer
                      class="teal lighten-5 font-weight-light"
                      style="margin: 5px 5px; padding: 5px 5px"
                    >
                    </v-data-table>
                  </v-sheet>
                </v-card>
              </v-col>
              <v-col cols="2">
                <v-card height="150">
                  <v-card-text
                    class="pt-0"
                    style="margin: 0px 0px; padding: 2px 5px"
                  >
                    <p>
                      <b class="display-1 font-weight-light teal--text mb-2"
                        >Results</b
                      >
                      <br />Here you can see <br />your results
                    </p>
                  </v-card-text>
                  <SeeResults :ImagesResults="ImagesResults"> </SeeResults>
                </v-card>
              </v-col>
            </v-row>
          </div>

          <div style="margin: 0px 0px; padding: 0px 0px">
            <Charts
              :accuracies="allProperties.accuracy_list"
              :ImagesResults="ImagesResults"
            >
            </Charts>
          </div>
          <div style="margin: 10px 0px; padding: 0px 0px">
            <v-card height="200">
              <v-card-text style="margin: 0px 0px; padding: 2px 5px">
                <p>
                  <b class="display-1 font-weight-light teal--text mb-2"
                    >Leaderboard</b
                  >
                </p>
              </v-card-text>
              <v-sheet
                class="v-sheet--offset mx-auto"
                color="teal lighten-5"
                elevation="8"
                max-width="calc(100% - 32px)"
              >
                <v-data-table
                  dense
                  disable-sort
                  :headers="leaderboardHeaders"
                  :items="Leaderboard"
                  :items-per-page="4"
                  item-key="date"
                  hide-default-footer
                  class="teal lighten-5 font-weight-light"
                  style="margin: 0px 0px; padding: 0px 0px"
                >
                </v-data-table>
              </v-sheet>
            </v-card>
          </div>
        </div>
      </v-col>
      <!--- Main component ends here --->
      <v-col>
        <div class="nav-arrow-back" id="back-button">
          <v-btn
            small
            @click="updateComponent('again')"
            color="primary"
            class="mr-4"
          >
            <v-icon left>mdi-rocket-outline</v-icon>Play <br />again!
          </v-btn>
        </div>
        <div class="nav-arrow" id="finish-button">
          <v-btn
            small
            @click="updateComponent('next')"
            color="primary"
            class="mr-4"
            deactivate
          >
            <v-icon left>mdi-arrow-right-circle</v-icon>Finish
            <v-icon>fast-forward</v-icon>
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { HTTP } from '@/http.common';
// import RenderImage from '@/components/RenderImage.vue';
import Charts from '@/components/Charts.vue';
import SeeResults from '@/components/SeeResults.vue';

export default {
  name: 'LabelingInitialize',
  props: ['allProperties'],
  components: {
    // RenderImage,
    Charts,
    SeeResults,
  },

  data: () => ({
    // UserID: 'testperson',
    ImagesResults: [],
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
    // ules: [(v) => !!v || 'Req', (v) => v.length <= 4 || 'Max 4 signs'],
    counterEn: false,
    counter: 0,
    missingUserID: '',
    icons: {},
    dialog: false,
    data_ges: [],
    leader: [],
    leader2: [],
    leader3: [],
    leaderboardHeaders: [
      { text: 'Name', value: 'name' },
      { text: 'All points', value: 'points' },
      { text: 'accuracy 4', value: 'accuracy_4' },
      { text: 'accuracy 5', value: 'accuracy_5' },
      { text: 'Time', value: 'time' },
      { text: 'Date', value: 'date' },
    ],
    leaderboardForTesting: [
      {
        name: 'Hans',
        points: 300,
        accuracy_4: 0.8,
        accuracy_5: 0.9,
        time: 30,
        date: '2020-05-14',
      },
      {
        name: 'Peter',
        points: 400,
        accuracy_4: 0.7,
        accuracy_5: 0.5,
        time: 300,
        date: '2020-06-14',
      },
      /* {
        name: 'Gerd',
        points: 400,
        accuracy_4: 0.7,
        accuracy_5: 0.5,
        time: 300,
        date: '2020-06-14',
      }, */
    ],
    yourData: [{}],
    Leaderboard: [{}],
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
    /* newLeaderboard() {
      const currentDate = 'Today';
      // const leaders = this.leaderboardForTesting.concat(
      this.yourData =
        {
          name: this.allProperties.UserID,
          points: this.data_ges[71][0],
          accuracy_4: this.data_ges[71][0],
          accuracy_5: this.data_ges[71][0],
          time: this.data_ges[63][0],
          date: currentDate,
        },
      // const sortedLeaders = leaders.sort(this.leaderSpeedSort);
      // return leaders; // sortedLeaders.slice(0, 3); */
    getData() {
      console.log('numberLabeld Images: ');
      console.log(this.allProperties.currentLevel);
      console.log(
        this.allProperties.AllScores[this.allProperties.currentLevel - 1][0],
      );
      const numberLabeledImages = this.allProperties.AllScores[
        this.allProperties.currentLevel - 1
      ][0];
      HTTP.post(
        `getDataReview/${this.allProperties.UserID}/${this.allProperties.dataset_typ}/${this.allProperties.labelingApproach}/${numberLabeledImages}`,
      )
        .then(async (response) => {
          // console.log(typeof response.data.SegMasksResults);
          this.ImagesResults = response.data.SegMasksResults;
          // this.NumberImages = response.data.numberOfimages;
          // console.log(this.ImagesResults);
          console.log('Received in Review data');
          this.leader = response.data.leader;
          this.leader2 = response.data.leader2;
          this.leader3 = response.data.leader3;
          // console.log(response.data.leader);
          // const leadersforTesting = [];
          const leaders = this.leaderboardForTesting.concat(
            {
              name: this.leader[0][0],
              points: this.leader[1][0],
              accuracy_4: Math.round(this.leader[46][0] * 100) / 100,
              accuracy_5: Math.round(this.leader[58][0] * 100) / 100,
              time: this.leader[69][0],
              date: this.leader[63][0],
            },
            {
              name: this.leader2[0][0],
              points: this.leader2[1][0],
              accuracy_4: Math.round(this.leader2[46][0] * 100) / 100,
              accuracy_5: Math.round(this.leader2[58][0] * 100) / 100,
              time: this.leader2[69][0],
              date: this.leader2[63][0],
            },
            {
              name: this.leader3[0][0],
              points: this.leader3[1][0],
              accuracy_4: Math.round(this.leader3[46][0] * 100) / 100,
              accuracy_5: Math.round(this.leader3[58][0] * 100) / 100,
              time: this.leader3[69][0],
              date: this.leader3[63][0],
            },
          );
          console.log('LEADERS');
          console.log(leaders);
          this.data_ges = response.data.data_ges;
          console.log(this.data_ges);
          console.log(typeof this.data_ges);
          this.yourData = {
            name: this.allProperties.UserID,
            points: this.data_ges[1][0],
            accuracy_4: Math.round(this.data_ges[46][0] * 100) / 100,
            accuracy_5: Math.round(this.data_ges[58][0] * 100) / 100,
            time: this.data_ges[69][0],
            date: this.data_ges[63][0],
          };
          console.log(this.yourData);
          // leaders = leaders.concat(this.yourData);
          this.yourData = [this.yourData];
          const sortedLeaders = leaders.sort(this.leaderSpeedSort);
          this.Leaderboard = sortedLeaders.slice(0, 3);
          // console.log(this.yourData);
        })
        .catch((e) => {
          console.warn(e);
        });
      return 'Complete';
    },
    colorSelect(color) {
      this.color = color;
    },
    leaderSpeedSort(a, b) {
      if (a.points > b.points) {
        return -1;
      }
      if (a.points < b.points) {
        return 1;
      }
      return 0;
    },
    updateScoresReview() {
      const allScores = String(this.allProperties.AllScores);
      const date = this.getDate();
      HTTP.post(
        `updateScoreGame/${this.allProperties.labelingApproach}/${this.allProperties.UserID}/${this.allProperties.dataset_typ}/${allScores}/${date}`,
        // `updateScore/${tooltyp}/${this.allProperties.UserID}/
        // ${this.allProperties.AllScores}/${this.imageRef_num}/
        // ${this.allProperties.dataset_typ}`,
      )
        .then(async (response) => {
          console.log(response.data.Status);
          this.getData();
          // console.log(`accuracy ${response.data.accuracy5}`);
          // this.$emit('updateAccuracy', response.data.accuracy5);
          // this.$emit('updateAccuracy', response.data.accuracy);
          // this.nextLevelprops.accuracyForScoring = response.data.accuracy5[0];
          // this.bounce_nextLevel = true;
          // this.updateComponent('next');
          // this.numberCells = 0;
          // this.numberRegions = 0;
          // points = 0;
          // this.seconds = 0;
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
    (this.data_ges = []).length = 71;
    this.data_ges.fill([0]);
    // console.log(this.data_ges[12][0]);
    // console.log(typeof this.data_ges);
    // this.data_ges.push([]);
    console.log(`skipped: ${this.allProperties.skipped}`);
    if (
      this.allProperties.skipped === true
      && this.allProperties.currentLevel !== 5
    ) {
      console.log('skipped current level: ');
      console.log(this.allProperties.currentLevel);
      let i = this.allProperties.currentLevel;
      while (i < 5) {
        this.$emit('updateScores', [0, 0, 0, 0, 0, 0, 0, [0, 0, 0, 0], i + 1]);
        this.$emit('updateAccuracy', [0, 0, 0, 0, i + 1]);
        i += 1;
      }
      this.updateScoresReview();
    } else {
      this.updateScoresReview();
      this.getData();
    }
    // console.log(this.allProperties.numberLabeledCells);
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
  top: 530px;
  left: 9px;
  text-justify: right;
  position: relative;
}
.main {
  height: 480px;
  width: 850px;
  min-width: 850px;
  border: 0px solid black;
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
</style>
