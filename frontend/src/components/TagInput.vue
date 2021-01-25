<template>
  <div>
    <v-icon left>fa-tag</v-icon>
    <vue-tags-input
      v-model="tag"
      :tags="datasetTags"
      :allow-edit-tags="true"
      :add-only-from-autocomplete="true"
      :autocomplete-items="items"
      class="tags-input"
      @tags-changed="newTags => datasetTags = newTags"
    >
      <div
        slot="tag-center"
        slot-scope="props"
      >
      <span
        v-if="!props.edit"
        @click="props.performOpenEdit(props.index)"
      >
        {{ props.tag.text }}
      </span>
        <div
          v-else
          class="inputs"
        >
          <select
            v-model="props.tag.text"
            @change="props.validateTag(props.index)"
          >
            <option v-for="(t, index) in tags" :key="index">{{ t }}</option>
          </select>
          <i
            class="material-icons"
            @click="props.performSaveEdit(props.index)"
          >
            check
          </i>
        </div>
      </div>
    </vue-tags-input>
  </div>
</template>

<script>
import VueTagsInput from '@johmun/vue-tags-input';
import { mapState } from 'vuex';

export default {
  name: 'TagInput',
  components: {
    VueTagsInput,
  },
  data: () => ({
    datasetTags: [],
    tag: '',
  }),
  computed: {
    ...mapState(['tags']),
    items() {
      return this.tags.filter(
        a => a.toLowerCase().indexOf(this.tag.toLowerCase()) !== -1,
      ).map(a => ({ text: a }));
    },
  },
};
</script>

<style scoped>
  .ti-input {
    border-top-width: 0;
  }

  .tags-input .inputs {
    display: flex;
  }

  .tags-input .inputs i {
    font-size: 20px;
    cursor: pointer;
  }

  .vue-tags-input {
    display: inline-flex;
  }
</style>
