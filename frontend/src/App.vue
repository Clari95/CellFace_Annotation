<template>
  <v-app>
    <router-view></router-view>

    <v-snackbar
      v-model="snackbar"
      bottom
      :color="snackbarColor"
    >
      {{ snackbarText }}
      <v-btn
        color="white"
        text
        @click="snackbar = false"
      >
        Close
      </v-btn>
    </v-snackbar>

  </v-app>
</template>

<script>
export default {
  data: () => ({
    snackbar: false,
    snackbarText: '',
    snackbarColor: 'success',
  }),

  mounted() {
    this.$root.$on('snackbar', this.handleSnackbar);
  },

  beforeDestroy() {
    this.$root.$off('snackbar');
  },

  methods: {
    handleSnackbar(event) {
      this.snackbar = true;
      this.snackbarText = event.text;
      this.snackbarColor = event.color;
    },
  },
};
</script>

<style>

</style>
