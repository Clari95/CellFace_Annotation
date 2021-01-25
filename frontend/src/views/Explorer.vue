<template>
  <div class="explorer">
    <v-navigation-drawer
    v-if="this.activeFile !== null"
    app
    right
    clipped
    permanent
    >
    <FileView v-if="this.activeFile !== null" :file="activeFile" :contextPath="activePath"/>
    </v-navigation-drawer>

    <FileSelection
      v-bind:path="activePath"
      @selected="updateSelection"
    />

  </div>
</template>

<script>
// import FileSelection from '@/components/FileSelection.vue';
// import FileView from '@/components/FileView.vue';

export default {
  components: {
    // FileSelection,
    // FileView,
  },

  data: () => ({
    activeFile: null,
    activePath: 'explorer',
  }),

  mounted() {
    this.activePath = String(this.$route.path);
  },

  methods: {
    updateSelection(selection) {
      if (selection.is_folder) {
        this.$router.push(`${this.activePath}/${selection.name}`)
          .then((newPath) => {
            this.activePath = newPath.path;
            this.activeFile = null;
          });
      } else {
        this.activeFile = selection;
      }
    },
  },

  watch: {
    $route(to) {
      this.activePath = to.fullPath;
    },
  },
};
</script>

<style lang="scss" scoped>

</style>
