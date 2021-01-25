<template>
  <div class="wrapper" id="overall">
    <v-row fill-width>
      <!--- Main component starts here --->
      <v-row class="mx-auto mt-4 main">
        <v-col dense class="column">
          <v-row>
            <v-card-text class="pb-0 pt-0"><b>General Information page <br/>
              about the Annotation process and the categories you have
              to label.</b>
            </v-card-text>
            <v-col dense>
              <v-container>
                <v-row dense>
                  <v-col cols="12">
                    <v-img
                      :aspect-ratio="16 / 2"
                      src="../assets/cellsorange.jpg"
                      style="opacity: 0.8"
                    >
                    <div
                      class="
                        display-1 white--text"
                    >
                      Categories
                    </div>
                    </v-img>
                  </v-col>

                  <v-col v-for="(item, i) in item1" :key="i" cols="12">
                    <v-card :color="item.color" height="100">
                      <div class="flex-no-wrap justify-space-between">
                        <div>
                          <v-card-title
                            class="headline orange--text"
                            v-text="item.title"
                          ></v-card-title>
                          <!--<v-card-actions>-->
                          <v-btn
                            text
                            @click="
                              dialog1 = true;
                              dialog1_text = item.title;
                              dialog1_text1 = item.text;
                              image_src = item.src;
                              aggregate = item.aggregate;
                            "
                          >
                            More!</v-btn
                          >
                          <!--</v-card-actions>-->
                        </div>
                        <v-avatar class="ma-3" size="125" tile>
                          <!--<v-img :src="item.src"></v-img>-->
                        </v-avatar>
                      </div>
                    </v-card>
                  </v-col>
                </v-row>
              </v-container>
              <v-dialog v-model="dialog1" justify="center" width="800">
                <v-card width="800" justify="center">
                  <v-card-title
                    class="headline orange lighten-2"
                    primary-title
                    >{{ dialog1_text }}</v-card-title
                  >
                  <v-card-text style="font-size: 1em">
                    <br />
                    <b>{{ dialog1_text1 }}</b>
                  </v-card-text>
                  <v-card-text> Example Images: </v-card-text>
                  <v-img
                    :src="
                      require(`../assets/CellCategory/${this.dialog1_text}.png`)
                    "
                  >
                  </v-img>
                  <v-card-text v-if="aggregate === true">
                    If you are not sure, it is better to assign them to the
                    category Other than a fixed one:
                  </v-card-text>
                  <v-img
                    v-if="aggregate === true"
                    width="250"
                    align-center
                    justify-center
                    :src="require(`../assets/CellCategory/others.png`)"
                  >
                  </v-img>
                  <v-divider></v-divider>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" text @click="dialog1 = false"
                      >Close</v-btn
                    >
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-col>
            <!--<v-col>
            <v-row> -->
            <v-col dense>
              <v-container>
                <v-row dense>
                  <v-col cols="12">
                    <v-img
                      style="opacity: 0.8"
                      :aspect-ratio="16 / 2"
                      src="../assets/CellsBlue.jpg">
                    <div
                      class="
                        display-1 white--text"
                    >
                      Technology
                    </div>
                    </v-img>
                  </v-col>

                  <v-col v-for="(item, i) in item2" :key="i" cols="12">
                    <v-card :color="item.color" :height="item.height">
                      <div class="flex-no-wrap justify-space-between">
                        <div>
                          <v-card-title
                            class="headline purple--text"
                            v-text="item.title"
                          ></v-card-title>

                          <v-card-subtitle v-text="item.text"></v-card-subtitle>
                          <!--<v-card-actions>-->
                          <v-btn
                            text
                            @click="
                              dialog2 = true;
                              dialog2_text = item.title;
                              (dialog2_text2 = item.text2),
                                (dialog2_textSize = item.text_size),
                                (image_size2 = item.image_size);
                              image = item.src;
                            "
                          >
                            More!</v-btn
                          >
                          <!--</v-card-actions>-->
                        </div>
                        <v-avatar class="ma-3" size="125" tile>
                          <!--<v-img :src="item.src"></v-img>-->
                        </v-avatar>
                      </div>
                    </v-card>
                  </v-col>
                </v-row>
              </v-container>
              <v-dialog v-model="dialog2" justify="center" width="800">
                <v-card width="800" justify="center">
                  <v-card-title
                    class="headline purple lighten-2"
                    primary-title
                    >{{ dialog2_text }}</v-card-title
                  >

                  <v-card-text style="font-size: 1em">
                    <br />
                    <b>{{ dialog2_text2 }}</b>
                  </v-card-text>
                  <v-card-text
                    style="font-size: 1em"
                    v-if="dialog2_textSize != ''"
                  >
                    {{ dialog2_textSize }}
                  </v-card-text>
                  <v-img
                    align-center
                    justify-center
                    :width="image_size2"
                    :src="require(`../assets/${this.image}.png`)"
                  >
                  </v-img>
                  <v-divider></v-divider>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" text @click="dialog2 = false"
                      >Close</v-btn
                    >
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-col>
          </v-row>
          <v-row dense>
            <div class="justify-center">
              <v-card color="grey lighten-4" height="120" width="590">
                <v-img style="opacity: 0.8" :aspect-ratio="16 / 1" src="../assets/symbolbild1.jpg">
                  <div
                    class="
                      display-1 white--text"
                  >
                    General
                  </div>
                </v-img>
                <div>
                  <v-row>
                    <v-col>
                      <v-card-title class="headline lime--text"
                        >CellFace</v-card-title
                      >
                      <v-card-subtitle
                        >Link to offical homepage.</v-card-subtitle
                      >
                    </v-col>
                    <v-col>
                      <a
                        href="https://wiki.tum.de/display/ldv/CellFace"
                        target="_blank"
                      >
                        <v-btn
                          text
                          @click="
                            dialog3 = false;
                            dialog3_text = item3.title;
                          "
                        >
                          <br />More!
                        </v-btn>
                      </a>
                    </v-col>
                  </v-row>
                </div>
              </v-card>
            </div>
          </v-row>
        </v-col>

        <v-col cols="4">
          <v-container>
            <v-row class="mt-6" dense>
              <v-col cols="12">
                <v-img style="opacity: 0.7" :aspect-ratio="16 / 2" src="../assets/Cellsteal.jpg">
                  <div
                      class="
                        display-1 white--text"
                    >
                      Annotation
                  </div>
                </v-img>
              </v-col>

              <v-col v-for="(item3, i) in item3" :key="i" cols="12">
                <v-card :color="item3.color" height="150">
                  <div class="flex-no-wrap justify-space-between">
                    <div>
                      <v-card-title
                        class="headline teal--text"
                        v-text="item3.title"
                      ></v-card-title>

                      <v-card-subtitle v-text="item3.text"></v-card-subtitle>
                      <!--<v-card-actions>-->
                      <v-btn
                        text
                        @click="
                          dialog3 = true;
                          dialog3_text = item3.title;
                          text_card = item3.text_card;
                          image = item3.src;
                          width_image = item3.width;
                        "
                      >
                        More!</v-btn
                      >
                      <!--</v-card-actions>-->
                    </div>
                    <v-avatar class="ma-3" size="125" tile>
                      <!--<v-img :src="item.src"></v-img>-->
                    </v-avatar>
                  </div>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
          <v-dialog v-model="dialog3" justify="center" width="1000">
            <v-card justify="center">
              <v-card-title class="headline teal lighten-2" primary-title>{{
                dialog3_text
              }}</v-card-title>

              <v-card-text style="font-size: 1em">
                <br />
                <b>{{ text_card }}</b>
              </v-card-text>
              <v-img
                :width="width_image"
                :src="require(`../assets/${this.image}.png`)">
              </v-img>
              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" text @click="dialog3 = false"
                  >Close</v-btn
                >
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-col>
      </v-row>

      <!--- Main component ends here --->

      <div class="nav-arrow">
        <v-btn
          small
          @click="updateComponent('next')"
          color="primary"
          class="mr-4"
        >
          <v-icon left>mdi-arrow-right-circle</v-icon>Next
          <v-icon>fast-forward</v-icon>
        </v-btn>
      </div>
    </v-row>
  </div>
</template>

<script>
// import VcardCellImages from '@/components/V-cardCellImages.vue';

export default {
  name: 'LabelingStart',
  props: ['allProperties'],
  components: {
    // VcardCellImages,
  },
  data: () => ({
    item1: [
      {
        color: 'grey lighten-4',
        font: 'purple',
        src: './assets/CellsBlue.jpg',
        title: 'SingelCell',
        text:
          'Singel cells are also called leukocytes (white blood cells). Since we use purified blood in this project, you can see blood that contains only monocytes, neutrophils, esinophils or lymphocytes',
        aggregate: false,
      },
      {
        color: 'grey lighten-4',
        font: 'teal',
        src: '../assets/CellCategory/SingelCell.png',
        title: 'Aggregates',
        text:
          'Aggregates are loosely grouped cells. For example a single cell and a platelet. Platelets form aggregates to stop an injury from bleeding',
        aggregate: true,
      },
      {
        color: 'grey lighten-4',
        font: 'teal',
        src: '../assets/CellCategory/SingelCell.png',
        title: 'Platelets',
        text:
          'Blood platelets, also called thrombocytes, are responsible for blood clotting. Areas marked in red are examples of platelets. The yellow marked area is an example of an aggregate: single cell + platelets,',
        aggregate: false,
      },
    ],
    item2: [
      {
        color: 'grey lighten-4',
        font: 'purple',
        src: 'dhm',
        title: 'Digital Holographic Microscopy (DHM)',
        text: 'Why look these images so different?',
        text2:
          'For most people, pictures from the DHM look unusual. The DHM does not work with blood smear analyses. It records images of blood flowing through a small cannula. Another difference is that the images are phase images. It provides intercellular information. Operating principle: The reflected light wave is recorded. It receives amplitude and phase information. With this information about optical instances a topographic image (3D image of the surface) can be reconstructed',
        text_size: '',
        height: '180',
        image_size: '800',
      },
      {
        color: 'grey lighten-4',
        font: 'purple',
        src: 'measure',
        title: 'Blood Cell Images',
        text: 'average size celltypes',
        text2:
          'Here it is important to mention that the size is smaller than that of normal blood cell images that work with blood smears. This is because during the process of blood smear analysis, the cells are broken up a little and end up looking larger. With the DHM we look at the whole, unaltered 3D cell',
        text_size:
          'Monocytes are the largest cells of the blood (averaging 15–18 μm in diameter). The neutrophils are 12-14 µm diameter. Eosinophils are 12 - 17 µm in diameter. Basophil are 14-16 µm in diameter. For more inforamtion: https://www.histology.leeds.ac.uk/blood/blood_wbc.php. ',
        height: '130',
        image_size: '800',
      },
    ],
    item3: [
      {
        color: 'grey lighten-4',
        font: 'teal',
        src: 'Process',
        title: 'Process',
        text: 'The idea behind the process',
        text_card:
          'The goal of the tool is to support the annotator as much as possible during the annotation process in order to obtain precisely labeled data. The first step is to create a LabelMask. This helps to identify regions of interest and to recognize small details in the image. After that it is the users turn! With a click it is possible to assign the marked regions to a category.To see the progress, a SegMask with the current status is displayed on the left side. At the end the segmentation mask is saved automatically',
        width: '1000',
      },
      {
        color: 'grey lighten-4',
        font: 'teal',
        src: 'LabelMaskNeutro',
        title: 'LabelMask',
        text: 'How to use it',
        text_card:
          'The purpose of the LabelMask is to support the annotator during the labeling process. It marks regions/objects of interest. All marked regions can be assigned to a specific category: Single cells, aggregates, platlets and others. Here is an example of a LabelMask with neutrophil cells',
        width: '450',
      },
      {
        color: 'grey lighten-4',
        font: 'teal',
        src: 'AddRegion',
        title: 'Add Objects',
        text: 'Change Modi add objects: why and how.',
        text_card: 'Sometimes not all important parts are marked by the LabelMask. But this is necessary to assign a category to areas. With the function "Add object" the user has the possibility to add new regions/objects of interest to the mask and to label them afterwards',
        width: '1000',
      },
    ],
    // info about cells
    dialog1: false,
    dialog1_text: 'SingelCell',
    dialog1_text1: 'none',
    image_src: '../assets/CellCategory/SingelCell.png',
    aggregate: false,
    // info about dhm und measure
    dialog2: false,
    dialog2_text: 'none',
    dialog2_text2: 'none',
    dialog2_textSize: 'none',
    image_size2: '400',
    image: 'dhm',
    // info about process tool
    dialog3: false,
    dialog3_text: 'none',
    text_card: 'none',
    width_image: '800',
    /* dialog_SingelCell: false,
    dialog_Aggregates: false,
    dialog_Platelets: false, */
    CellCategory: 'none',
    dataSelection: false,
    search: '',
    datasetHeaders: [
      { text: '', value: 'is_folder', width: 1 },
      { text: 'Name', value: 'name', width: 4 },
      { text: 'Size', value: 'size', width: 4 },
      { text: 'Date Created', value: 'created', width: 4 },
      { text: 'Date Modified', value: 'modified', width: 4 },
      { text: 'MIME', value: 'type/mime', width: 4 },
      { text: 'Type', value: 'type', width: 4 },
      { text: 'Tags', value: 'tags', width: 6 },
    ],
    classSetup: false,
    ids: [0, 1, 2, 3, 4],
    /* max15chars: (v) => v.length <= 15 || 'Input too long!',
    availableColors: [
      'red',
      'orange',
      'green',
      'teal',
      'blue',
      'purple',
      'brown',
      'grey',
    ], */
    /* classHeaders: [
      {
        text: 'Name',
        align: 'start',
        sortable: false,
        value: 'name',
      },
      {
        text: 'Color',
        align: 'start',
        sortable: false,
        value: "color",
      },
      {
        text: "Class of Interest",
        align: "start",
        sortable: false,
        value: "inFinal",
      },
      {
        text: "",
        align: "start",
        sortable: false,
        value: "delete",
      },
    ], */
    labelingClasses: '',
    dataFiles: '',
    trainedModel: '',
    // This data attribute is just included to avoid warnings
    tempSelection: 'createNew',
    // dataset: 'none',
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
    updateDataset() {
      this.$emit('updateDataset');
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
  height: 520px;
  width: 750px;
  min-width: 750px;
}

.nav-arrow {
  padding-top: 550px;
  padding-left: 15px;
  text-justify: right;
}

.title {
  justify-content: center;
}
.column {
  position: relative;
  bottom: 30px;
}


</style>
