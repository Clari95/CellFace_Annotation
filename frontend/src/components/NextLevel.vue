<template>
<div class="nextLevel">
  <section class="image">
      <transition name="bounce">
        <img v-if="bounce_now" alt="flash"
        @click="updateComponent('next')"
        :src='require(`../assets/${animation_now}`)'
        :width="width_def"
        class="center"/>
      </transition>
  </section>
  <v-card
  width="500"
  height="270"
  class="info_level">
  <v-card-title justify="center">
    You achieved {{points_now}} points <br/>
    Completness: {{accuracy_now}} %
    <v-card-text class="acc" style="font-size:0.7em">
    [average over all images of #labeled areas/#areas in image] <br/>
    </v-card-text>
    Correctness: {{accuracy_now_correct}} %
    <v-card-text class="acc" style="font-size:0.7em">
    [average over all images of #correct labels/#labeled areas] <br/>
    </v-card-text>
  </v-card-title>
  <v-subheader class="pl-3 teal--text" align="center"
      justify="center"
  style="font-size:1.2em">
  <b>{{text_now}}</b></v-subheader>
  </v-card>
</div>
</template>

<script>

export default {
  props: {
    bounce: {
      type: Boolean,
      required: true,
    },
    animation: {
      type: String,
      required: true,
    },
    points: {
      type: Number,
      required: true,
    },
    maxPoints: {
      type: Number,
      required: true,
    },
    text: {
      type: String,
      required: false,
    },
    accuracy: {
      type: Number,
      required: true,
    },
    accuracy_correct: {
      type: Number,
      required: false,
    },
    currentLevel: {
      type: Number,
      required: false,
    },
  },

  data: () => ({
    imageSrc: '',
    bounce_now: false,
    accuracy_now: 0,
    accuracy_now_correct: 0,
    overlay: false,
    text_now: '',
    animation_now: '',
    points_now: 0,
    width_def: 0,
  }),

  mounted() {
    this.renderNextLevel();
  },

  methods: {

    updateComponent(event) {
      this.$emit('updateComponent', event);
    },
    renderNextLevel() {
      console.log(' in next level render');
      this.bounce_now = this.bounce;
      this.accuracy_now = this.accuracy;
      this.accuracy_now_correct = this.accuracy_correct;
      console.log(`accurcay now : ${this.accuracy_now}`);
      console.log(this.currentLevel);
      this.accuracy_now = Math.round(this.accuracy_now * 100);
      this.accuracy_now_correct = Math.round(this.accuracy_now_correct * 100);
      if (this.accuracy_now === 0) {
        this.accuracy_now_correct = '__';
      }
      if (this.currentLevel !== 5) {
        if (this.accuracy_now < 50) {
          this.text_now = 'You can improve your labeling ;) Try to lable all areas marked in the LabelMask! Click on the face to continue';
          this.animation_now = 'sad.png';
          this.points_now = this.points;
          this.width_def = 150;
        } else if (this.accuracy_now < 85) {
          this.text_now = 'Next Level! Click on the Star to continue';
          this.animation_now = 'Star.jpg';
          this.width_def = 150;
          this.points_now = this.points;
        } else {
          this.text_now = 'Good Job! You get 20 extra Points. Click on the Star to continue';
          this.animation_now = 'StarSpecial.jpg';
          this.width_def = 200;
          console.log('UPDATE ALL POINTS1');
          this.points_now = this.points;
        }
      } else {
        this.text_now = 'You made it! Get next to see review!';
        this.animation_now = 'StarSpecial.jpg';
        this.width_def = 200;
        this.points_now = this.points;
      }
    },

    floatToIntColor(x) {
      const cropRange = this.maxCropVal - this.minCropVal;
      let intValue = Math.min(Math.round(
        Math.max(x - this.minCropVal, 0) * 255 / cropRange,
      ), 255);

      if (this.invertBackground) {
        intValue = 255 - intValue;
      }

      return intValue;
    },

    handleArgChange() {
      this.renderNextLevel();
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
.nextLevel {
  padding-top: 30px;
  padding-right: 100px;
}
.acc {
  padding-top: 0px;
  padding-left: 0px;
}
.bounce-enter-active {
  animation: bounce-in 1.5s;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.8);
  }
  100% {
    transform: scale(1);
  }
}
.image {
  z-index: 20;
  text-justify: center;
  text-align: center;
}
.info_level {
  top: 40px;
  z-index: 0;
}

</style>
