<template>
<v-card
  width="800"
  justify="center"
>
      <v-card-title class='headline grey lighten-2'
      primary-title>Guidline</v-card-title>
      <v-img
        :src='require(`../assets/CellCategory/${this.CellCategroy}.png`)'
        height="400"
        contain
      >
      </v-img>
      <v-card>
        Here you find an explanation for the possible options during labeling task:
        <ul>
          <li>never annotate one area with two labels</li></ul>
      </v-card>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color='primary' text @click="closeInfo()">Close</v-btn>
      </v-card-actions>
    </v-card>
</template>

<script>
// import colormap from 'colormap';

export default {
  props: {
    dialog: {
      type: Boolean,
      default: false,
    },
    CellCategroy: {
      type: String,
      default: 'SingelCell',
    },
  },

  data: () => ({
    imageSrc: '',
    overlay: false,
  }),

  mounted() {
    this.getCategory();
  },

  methods: {
    getCategory() {
      console.log('getCategory');
      console.log(this.CellCategroy);
    },
    closeInfo() {
      console.log('closeInfo');
      this.$emit('showInfo', false);
    },
    handleArgChange() {
      this.renderImage();
    },
  },


  watch: {
    minCropVal(to, from) {
      if (to !== from) { this.handleArgChange(); }
    },

    maxCropVal(to, from) {
      if (to !== from) { this.handleArgChange(); }
    },

    invertBackground(to, from) {
      if (to !== from) { this.handleArgChange(); }
    },

    colormap(to, from) {
      if (to !== from) { this.handleArgChange(); }
    },

    image() {
      this.handleArgChange();
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

</style>
