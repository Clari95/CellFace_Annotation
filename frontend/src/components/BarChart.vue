<script>
import { Bar } from 'vue-chartjs';

export default {

  extends: Bar,

  props: {
    labels: {
      type: Array,
      required: true,
    },
    datasets: {
      type: Array,
      required: true,
    },
  },

  data: () => ({

  }),

  mounted() {
    this.renderChart({
      labels: this.labels,
      datasets: this.datasets,
    });
  },
};
</script>
