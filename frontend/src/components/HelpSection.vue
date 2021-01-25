<template>
<div class='text-center help'>
    <v-dialog class="dialog" v-model='dialog' width='850'>
      <template v-slot:activator='{ on, attrs }'>
        <v-btn small color='teal' dark v-bind='attrs' v-on='on'>help</v-btn>
      </template>

      <v-card>
        <v-card-title v-if="currentLevel !== 0" class='headline teal lighten-2'
        primary-title>Guidline Level {{currentLevel}}</v-card-title>
        <v-card-title v-if="currentLevel === 0" class='headline teal lighten-2'
        primary-title>Guidline Basic Tool</v-card-title>
        <!--BasicTool-->
        <v-card-text v-if="currentLevel === 0"
          style="font-size: 1em"
          class="grey--text">
          <v-list>
            <v-list-item>
              Label all areas selected on the Labelmask
              <mark>
                (except for cells that are cut off from the edge of the image)</mark> </v-list-item
            >
            <v-list-item
              >Provided tools for the assignment of objects to classes
              <mark>(only those marked with LabelMask)</mark>
            </v-list-item>
            <v-list-item>
              <ul>
                <li>
                  Single Objects with one click
                </li>
                <li>
                  Whole areas with more objects: dragging bounding boxes
                </li>
              </ul>
            </v-list-item>
            <v-list-item>
              If you are not sure about the category, assign it to category Other. </v-list-item
            >
            <v-list-item>
              If you want to assign objects not marked at mask to a category,
              just add it to the mask (change Mode).</v-list-item
            >
            <v-list-item>
              Check out the different view options on the left
              side!</v-list-item
            >
              <v-list-item>
              <ul>
                <li>
                  Change Cell Image with the help of a Colormap to see more details
                </li>
                <li>
                  You can deactivate the OrgImage or change the intensity to see more details
                </li>
                <li>
                  You can deactivate the LabelMask to see only the pure Cells
                </li>
              </ul>
            </v-list-item>
            <v-list-item>
              On the right side you can see your current result.
            </v-list-item>
          </v-list>
          You can reopen this information at any time with the HELP button.
        </v-card-text>
        <!--Level 1-->
        <v-card-text v-else-if="currentLevel === 1"
          style="font-size: 1em"
          class="grey--text">
          <v-list>
            <v-list-item>
              Label all areas selected on the Labelmask
              <mark>(except for cells that are cut off from the edge of the image)
                </mark></v-list-item
            >
            <v-list-item
              >You can easily assign Cells with a click to category
              <mark>(only those marked in LabelMask)</mark>
            </v-list-item>
            <v-list-item>
              If you are not sure about the category, assign it to category Other.
            </v-list-item>
            <v-list-item>
              Check out the different view options on the left
              side!</v-list-item
            >
              <v-list-item>
              <ul>
                <li>
                  Change Cell Image with the help of a <b> Colormap </b> to see more details
                </li>
                <li>
                  You can deactivate the OrgImage
                  or <b> change the intensity </b> to see more details
                </li>
                <li>
                  You can <b> deactivate </b> the LabelMask to see only the pure Cells
                </li>
              </ul>
            </v-list-item>
          </v-list>
        </v-card-text>
        <!--Level 2 -->
        <v-card-text v-else-if="currentLevel === 2"
          style="font-size: 1em"
          class="grey--text">
          <br/>
          <b>New labels provided! You can label Singel Cells, Aggregates
          and Platelets. To label faster also a new Tool is avaiable. Check it out!</b>
          <v-list>
            <v-list-item>
              Label all areas selected on the Labelmask
              (except for cells that are cut off from the edge of the image) </v-list-item
            >
            <b><v-list-item
              >Provided tools for the assignment of objects to classes
              (only those marked with LabelMask):
            </v-list-item>
            <v-list-item>
              <ul>
                <li>
                  Single Objects with one click
                </li>
                <li>
                  Whole areas with more objects: dragging bounding boxes
                </li>
              </ul>
            </v-list-item></b>
            <v-list-item>
              If you are not sure about the category, assign it to category Other. </v-list-item
            >
            <v-list-item>
              Check out the different view options on the left
              side!</v-list-item
            >
              <v-list-item>
              <ul>
                <li>
                  Change Cell Image with the help of a Colormap to see more details
                </li>
                <li>
                  You can deactivate the OrgImage or change the intensity to see more details
                </li>
                <li>
                  You can deactivate the LabelMask to see only the pure Cells
                </li>
              </ul>
            </v-list-item>
          </v-list>.
        </v-card-text>
        <!--Level3-->
        <v-card-text v-else-if="currentLevel === 3"
          style="font-size: 1em"
          class="grey--text">
          <br/>
          <b>Some objects are not recognized by LabelMask, but this is mandatory to label all cells.
          Add them to the mask and get extra points!<br/></b>
           <v-list>
            <v-list-item>
              Label all areas selected on the Labelmask
              (except for cells that are cut off from the edge of the image) </v-list-item
            >
            <v-list-item
              >Provided tools for the assignment of objects to classes
              (only those marked with LabelMask):
            </v-list-item>
            <v-list-item>
              <ul>
                <li>
                  Single Objects with one click
                </li>
                <li>
                  Whole areas with more objects: dragging bounding boxes
                </li>
              </ul>
            </v-list-item>
            <v-list-item>
              If you are not sure about the category, assign it to category Other. </v-list-item
            >
            <b><v-list-item>
              If you want to assign objects not marked at mask to a category,
              just add it to the Labelmask (change Mode).</v-list-item
            ></b>
            <v-list-item>
              Check out the different view options on the left
              side!</v-list-item
            >
              <v-list-item>
              <ul>
                <li>
                  Change Cell Image with the help of a Colormap to see more details
                </li>
                <li>
                  You can deactivate the OrgImage or change the intensity to see more details
                </li>
                <li>
                  You can deactivate the LabelMask to see only the pure Cells
                </li>
              </ul>
            </v-list-item>
            <v-list-item>
              On the right side you can see your current result.
            </v-list-item>
          </v-list>
        </v-card-text>
        <!--Last Levels-->
        <v-card-text v-else
          style="font-size: 1em"
          class="grey--text">
          <br/>
          <b>On the last two levels all functions for labeling objects are provided
            as quickly and accurately as possible.<br/>
            Try to label as many areas as possible to get a high completeness score.
            Watch out for incorrect labeling
            It worsens your result! <br/>
            Your Accuracy get tracked depening on number of labeled areas
            and correctness of the label.</b>
          <br />
          <v-list>
            <v-list-item>
              Label all areas selected on the Labelmask
              (except for cells that are cut off from the edge of the image) </v-list-item
            >
            <v-list-item
              >Provided tools for the assignment of objects to classes
              (only those marked with LabelMask):
            </v-list-item>
            <v-list-item>
              <ul>
                <li>
                  Single Objects with one click
                </li>
                <li>
                  Whole areas with more objects: dragging bounding boxes
                </li>
              </ul>
            </v-list-item>
            <v-list-item>
              If you are not sure about the category, assign it to category Other. </v-list-item
            >
            <v-list-item>
              If you want to assign objects not marked at mask to a category,
              just add it to the mask (change Mode).</v-list-item
            >
            <v-list-item>
              Check out the different view options on the left
              side!</v-list-item
            >
              <v-list-item>
              <ul>
                <li>
                  Change Cell Image with the help of a Colormap to see more details
                </li>
                <li>
                  You can deactivate the OrgImage or change the intensity to see more details
                </li>
                <li>
                  You can deactivate the LabelMask to see only the pure Cells
                </li>
              </ul>
            </v-list-item>
            <v-list-item>
              On the right side you can see your current result.
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color='primary' text @click="dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>

export default {
  props: {
    currentLevel: {
      type: Number,
      required: true,
    },
    /* image: {
      type: Array,
      required: true,
    },
    minCropVal: {
      type: Number,
      required: true,
    },
    maxCropVal: {
      type: Number,
      required: true,
    },
    invertBackground: {
      type: Boolean,
      required: true,
    },
    colormap: {
      type: String,
      default: 'none',
    },
    opacity: {
      type: Number,
      required: true,
      default: 255,
    }, */
  },

  data: () => ({
    dialog: false,
  }),

  mounted() {
    if (this.currentLevel === 0) {
      this.dialog = true;
    }
    this.renderHelpSection();
  },

  methods: {

    updateComponent(event) {
      this.$emit('updateComponent', event);
    },
    renderHelpSection() {
      console.log('in render help section');
      console.log(this.currentLevel);
    },
  },
};
</script>

<style>

#overlay-btn {
  position: absolute;
  top: 1em;
  right: 1em;
}
.help {
  position: relative;
  top: 20px;
}
.v-dialog {
    position: relative;
    bottom: 40px;
    left: 120px;
}
.dialog {
}

</style>
