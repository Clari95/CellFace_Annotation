<template>
  <v-col>
    <v-row>
      <BarChart :labels="getHistogramCenters()" :datasets="[getHistogramDataset()]"/>
    </v-row>
    <v-row>
      <v-col>Min: {{statistics.min.toFixed(2)}}</v-col>
      <v-col>Max: {{statistics.max.toFixed(2)}}</v-col>
      <v-col>Avg.: {{statistics.average_val.toFixed(2)}}</v-col>
      <v-col>Std.: {{statistics.std.toFixed(2)}}</v-col>
    </v-row>
  </v-col>
</template>

<script>
// NOTE: could also use D3 charts
// https://saigesp.github.io/vue-d3-charts/#/barchart
import BarChart from '@/components/BarChart.vue';

export default {
  props: {
    statistics: {
      type: Object,
      required: true,
    },
  },

  components: {
    BarChart,
  },

  data: () => ({

  }),

  mounted() {
  },

  methods: {

    getHistogramCenters() {
      const histBoundaries = this.statistics.hist_boundaries;
      const histogramCenters = [];
      histBoundaries.forEach((el, idx) => {
        if (idx < histBoundaries.length - 1) {
          histogramCenters.push((el + histBoundaries[idx + 1]) / 2);
        }
      });
      return histogramCenters;
    },

    getHistogramDataset() {
      return {
        label: 'Frequency of pixels',
        backgroundColor: '#f87979',
        data: this.statistics.hist_frequencies,
        borderWidth: this.statistics.hist_boundaries[1] - this.statistics.hist_boundaries[0],
      };
    },

  },

};
</script>

<style>

</style>
