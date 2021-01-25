<template>
  <input
    type="file"
    :class="{ hidden: hidden }"
    ref="input"
    :multiple="multiple"
    :directory="directory"
    :webkitdirectory="directory"
    :accept="accept"
    @change="onFilesSelected"
  />
</template>

<script>
export default {
  name: 'HiddenInput',
  props: {
    hidden: { type: Boolean, default: true },
    multiple: { type: Boolean, default: false },
    directory: { type: Boolean, default: false },
    accept: Array,
  },
  methods: {
    onFilesSelected(event) {
      this.$emit('filesSelected', event);
    },
  },
};
</script>

<style scoped>
  .hidden {
    display: none;
  }
</style>
