<template>
  <div class="wrapper" id="overall">
    <v-row fill-width>
      <!--- Back arrow (return to labeling title screen) --->
      <div class="nav-arrow">
        <v-btn
          small
          @click="updateComponent('back')"
          color="primary"
          class="mr-4"
        >
          <v-icon left>mdi-arrow-left-circle</v-icon>back
        </v-btn>
      </div>

      <!--- Main component starts here --->
      <v-col class="mx-auto mt-4 main">
        <!--- Title --->
        <div class="data">
        <v-card-title class="mx-1 mt-2 title justify-center">
          Select the datatyp you want to analyse
        </v-card-title>
        <v-row justify="space-around" dense>
          <v-icon left>mdi-paperclip</v-icon>
          <v-col class="d-flex" cols="9" sm="9">
            <v-select
              v-model="cellTyp"
              :items="items"
              item-text="name"
              label="Select Data"
              dense
              persistent-hint
              return-object
              single-line
            ></v-select>
          </v-col>
          <v-btn
            v-if="cellTyp === null"
            small
            @click="updateDatatyp()"
            color="primary"
            class="mr-4"
            disabled
          >
            Select
          </v-btn>
          <v-btn
            v-else
            small
            @click="updateDatatyp()"
            color="primary"
            class="mr-4"
          >
            Save selection
          </v-btn>
        </v-row>
        <!--- Delete button for this class --->
        <!--<template v-slot:item.delete="{ item }">
          <v-btn color="primary" text @click="deleteClass(item)">
            Delete
          </v-btn>
        </template>-->
        </div>
      </v-col>
      <!--- Main component ends here --->

      <div class="nav-arrow">
        <v-btn
          v-if="nextButton"
          small
          @click="updateComponent('next')"
          color="primary"
          class="mr-4"
          :disabled="nextButton"
        >
          Select Data
        </v-btn>
        <v-btn
          v-else
          small
          @click="updateComponent('next')"
          color="primary"
          class="mr-4"
          :disabled="nextButton"
        >
          <v-icon left>mdi-arrow-right-circle</v-icon>Next
          <v-icon>fast-forward</v-icon>
        </v-btn>
      </div>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'LabelingStart',
  props: ['allProperties'],
  data: () => ({
    cellTyp: null,
    items: [
      { value: 'Neutrophils', name: 'Neutrophils' },
      { value: 'Monocytes', name: 'Monocytes' },
      { value: 'Eosinophils', name: 'Eosinophils' },
      { value: 'Lymphocytes', name: 'Lymphocytes' },
    ],
    nextButton: true,
    saveButton: true,
    dataSelection: false,
  }),
  computed: {
    numberOfClasses() {
      return this.labelingClasses.length;
    },
  },
  methods: {
    selectProcedure(event) {
      this.$emit('selectProcedure', event);
    },
    updateComponent(event) {
      this.$emit('updateComponent', event);
    },
    updateDatatyp() {
      this.$emit('updateDatasetTyp', this.cellTyp.value);
      this.nextButton = false;
      // console.log(this.allProperties);
      // this.allProperties.dataset = this.cellTyp.value;
      console.log(this.cellTyp.value);
      this.saveButton = false;
    },
  },
  mounted() {},
};
</script>

<style scoped>
.wrapper {
  text-align: center;
  text-justify: center;
}

.prompt {
  text-align: center;
}

.main {
  height: 480px;
  width: 750px;
  min-width: 750px;
}

.nav-arrow {
  padding-top: 550px;
  padding-left: 15px;
  text-justify: right;
}

.data{
  padding-top: 120px;
}
</style>
