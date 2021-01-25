<template>
  <v-subheader v-if="currentLevel == 1" class="pl-3 level"
    style="font-size:1.2em">
      <b class="teal--text">Level {{currentLevel}}: <br/>
      <p style="font-size:0.8em">Label all marked areas
        (excluding cells that are cut off from the image) <br/>
        with a left click!
        Explore different image views!
      </p>
      <p style="font-size:0.7em">(If you are not sure, assign it to Other)</p></b>
  </v-subheader>
  <v-subheader v-else-if="currentLevel == 2" class="pl-3 level"
    style="font-size:1.2em">
      <b class="teal--text">Level 2: New feature! <br/>
      <p style="font-size:0.8em">Try dragging bounding boxes around
        areas with objects of the same <br/>
        category and label easy and fast more objects!</p>
      <p style="font-size:0.7em">(If you are not sure, assign it to Other)</p></b>
  </v-subheader>
  <v-subheader v-else-if="currentLevel == 3" class="pl-3 level"
    style="font-size:1.2em">
      <b class="teal--text">Level 3: Practice to add regions ;) <br/>
      <p style="font-size:0.8em">A new mode is available!
        <br/> Help for adding new objects to LabelMask und get 50 points!.
      </p>
      <p style="font-size:0.7em">(Maybe the slider on the left side
        can help you to see small platelets better)</p></b>
  </v-subheader>
  <v-subheader v-else-if="currentLevel == 4" class="pl-3 level"
    style="font-size:1.2em">
      <b class="teal--text">Level 4: Label 10 images <br/>
      <p style="font-size:0.8em">Now all funtions are available
        <br/>Try to label as accurate as possible
        to get more points</p></b>
  </v-subheader>
  <v-subheader v-else-if="currentLevel == 5" class="pl-3 level"
  style="font-size:1.2em">
    <b class="teal--text">Level 5: Label 10 images <br/>
    <p style="font-size:0.8em">All funtions are available
      <br/>Your accuracy is not visible anymore,
      trust your own skills!</p></b>
  </v-subheader>
</template>

<script>
// import { Howl, Howler } from 'howler';

export default {
  props: {
    currentLevel: {
      type: Number,
      required: true,
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
    // this.renderNextLevel();
  },

  methods: {

    updateComponent(event) {
      this.$emit('updateComponent', event);
    },
    handleArgChange() {
      this.renderNextLevel();
    },
  },
};
</script>

<style>


.level {
  height: 20px;
  padding-bottom: 50px;
}

</style>
