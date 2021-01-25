<template>
  <v-card outlined class="mx-3 my-3 upload">
    <v-card-title class="mx-1 mt-2">Upload a new Dataset</v-card-title>
    <BinUpload />
  </v-card>
</template>

<script>
// import BinUpload from '@/components/BinUpload.vue';


export default {
  name: 'Upload',
  components: {
    // BinUpload,
  },

  data: () => ({
  }),

  methods: {
  },
};
</script>

<style lang="scss" scoped>

</style>
