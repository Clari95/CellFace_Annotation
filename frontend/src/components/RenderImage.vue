<template>
<div>
  <v-img
    contain
    :src="imageSrc"
    @click="overlay = true"
  ></v-img>
  <v-overlay v-if="overlay" z-index=10>
    <v-img :src="imageSrc"
      :max-height="getHeight()"
      :max-width="getWidth()"
      contain
    ></v-img>
    <v-btn
      id="overlay-btn"
      icon
      color="primary"
      @click="overlay = false"
      >
      <v-icon>fa-times</v-icon>
    </v-btn>
  </v-overlay>
</div>
</template>

<script>
import colormap from 'colormap';

export default {
  props: {
    image: {
      type: Array,
      required: true,
    },
    minCropVal: {
      type: Number,
      required: true,
    },
    maxCropVal: {
      type: Number,
      required: true,
    },
    invertBackground: {
      type: Boolean,
      required: true,
    },
    colormap: {
      type: String,
      default: 'none',
    },
    opacity: {
      type: Number,
      required: true,
      default: 255,
    },
  },

  data: () => ({
    imageSrc: '',
    overlay: false,
  }),

  mounted() {
    this.renderImage();
  },

  methods: {

    getHeight() {
      return this.image.length;
    },

    getWidth() {
      return this.image[0].length;
    },

    renderImage() {
      if (!this.image) return;

      // create an offscreen canvas
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');

      // size the canvas to your desired image
      canvas.width = this.getWidth();
      canvas.height = this.getHeight();

      // get the imageData and pixel array from the canvas
      const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const { data } = imgData;

      const colors = this.colormap !== 'None' ? colormap({
        colormap: this.colormap,
        nshades: 256,
        format: 'rga',
        alpha: 1,
      }) : null;

      // compute pixel values
      for (let i = 0; i < data.length; i += 4) {
        const pixelIdx = Math.floor(i / 4);
        const yIdx = Math.floor(pixelIdx / this.getWidth());
        const xIdx = Math.floor(pixelIdx % this.getWidth());

        const greyShadeFloat = this.image[yIdx][xIdx];
        const intColor = this.floatToIntColor(greyShadeFloat);

        // apply colormap
        const red = colors ? colors[intColor][0] : intColor;
        const green = colors ? colors[intColor][1] : intColor;
        const blue = colors ? colors[intColor][2] : intColor;

        data[i] = red;
        data[i + 1] = green;
        data[i + 2] = blue;
        data[i + 3] = this.opacity; // opacity
      }

      // put the modified pixels back on the canvas
      ctx.putImageData(imgData, 0, 0);
      // set the img.src to the canvas data url
      this.imageSrc = canvas.toDataURL();
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
