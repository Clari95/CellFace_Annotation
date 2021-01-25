<template>
  <!-- TODO: possible add reload button -->

  <v-card justify-end>
    <template v-for="item in tasks_status">
      <v-list-item :key="item.task_name">
        <v-list-item-action>
          <v-progress-circular
            size=24
            width="3"
            color="primary"
            indeterminate
          ></v-progress-circular>
        </v-list-item-action>
        <v-list-item-content class="body-2">
          {{item.task_name}}
        </v-list-item-content>
      </v-list-item>
    </template>
  </v-card>
</template>

<script>
import { HTTP } from '@/http.common';

export default {
  data: () => ({
    tasks_status: [],
  }),

  created() {
    // update Status Bar every 10 seconds:
    // this.timer = setInterval(this.updateStatus, 1000000);
    return 1;
  },

  methods: {
    updateStatus() {
      HTTP
        .get('status/')
        .then((response) => {
          this.tasks_status = response.data.response;
          // console.info(this.tasks_status[0].task_name);
          // TODO: Add information about errors, running or waiting etc.
        })
        .catch(e => console.warn(e));
    },
  },

  mounted() {
    // this.updateStatus();
    return 1;
  },

  beforeDestroy() {
    clearInterval(this.timer);
  },
};
</script>

<style scoped>

</style>
