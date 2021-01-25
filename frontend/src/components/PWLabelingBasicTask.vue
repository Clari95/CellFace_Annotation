<template>
  <!--<div class='wrapper'>-->
  <v-row fill-width>
    <div class="nav-arrow-back" id="back-button">
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
    <v-col class="mx-auto mt-0 main">
      <v-row class="canvas-wrapper">
        <div class="options" style="width: 170px">
           <div>
            <v-subheader class="pl-3" style="font-size: 1.2em">
            <b>Tools:</b></v-subheader>
            <v-btn
                  @click="
                    selectTool('labelSingle')
                  "
                  @mouseover="hoverSingle = true"
                  @mouseleave="hoverSingle = false"
                  class="ml-3 mb-4 white--text"
                  :color="colorSing"
                  :elevation="elevToolSing"
                  :disabled="disabled_modi"
                  ><v-icon>mdi-close</v-icon>
            </v-btn>
            <v-card-text
              class="hoverSingle black--text grey lighten-4" v-if="hoverSingle">
              Annotate Single Objects
            </v-card-text>
            <v-btn
                  @click="
                    selectTool('labelRegion')
                  "
                  @mouseover="hoverArea = true"
                  @mouseleave="hoverArea = false"
                  class="ml-3 mb-4 white--text"
                  :color="colorReg"
                  :elevation="elevToolReg"
                  :disabled="disabled_modi"
                  ><v-icon>mdi-vector-difference-ab</v-icon>
            </v-btn>
            <v-card-text
              class="hoverArea black--text grey lighten-4" v-if="hoverArea">
              Bounding boxes: annotate more Objects.
            </v-card-text>
           </div>
           <!--for add region-->
          <v-divider class="mx-4"></v-divider>
          <v-subheader class="pl-3" style="font-size: 1.2em">
            <b>Image view:</b></v-subheader
          >
          <input
            class="ml-3"
            type="checkbox"
            id="checkbox"
            v-model="colormap"
            @change="options('colormap')"
          />
          <label class="pl-3"> Colormap </label>
          <v-switch
            v-model="disabled_org"
            class="ma-2"
            label="OrgImage"
            color="teal"
            @change="options('up')"
          ></v-switch>
          <v-slider
            v-model="slider"
            class="mb-0 slider"
            :max="max"
            :min="min"
            :disabled="!disabled_org"
            @change="options('slider')"
            thumb-label="always"
            :thumb-size="24"
          >
          </v-slider>
          <v-switch
            v-model="disabled_mask"
            class="ma-2 mt-0"
            label="LabelMask"
            color="teal"
            @change="options('down')"
          ></v-switch>
          <!--modis.-->
          <v-divider class="mx-4"></v-divider>
          <v-subheader class="pl-3" style="font-size: 1.2em"
            ><b>Mode:</b></v-subheader
          >
          <v-switch
            v-model="disabled_modi"
            class="ma-2"
            label="Add Objects to mask"
            color="warning"
            @change="options('modi1')"
            @mouseover="hoverObject = true"
            @mouseleave="hoverObject = false"
          ></v-switch>
          <v-card-text
            class="hoverObject black--text grey lighten-4" v-if="hoverObject">
            Click exact at all missing objects before adding to LabelMask.
          </v-card-text>
             <label class="pl-3">Reset #{{this.imageRef_num}}</label>
            <v-btn small justify="center" align="center"
                  @click="
                    hideContextMenu();
                    resetArea()
                  "
                  class="ml-3 white--text"
                  color="grey lighten-2"
                  :elevation="3"
                  ><v-icon>mdi-autorenew</v-icon>
            </v-btn>
        </div>
        <div class="canvas">
          <v-card-text class="pa-1 infoEdge black--text grey lighten-4"
              v-if="this.imageRef_num === 1 && this.edge == true">
              Example for cell too <br/>close at image edge
              <v-icon> mdi-arrow-collapse-down </v-icon>
          </v-card-text>
          <canvas
            ref="canvas"
            id="rectangleDraw"
            width="512"
            height="384"
            class="covering"
          ></canvas>
          <v-img
            id="image-mask_water"
            class="covered"
            width="512"
            height="384"
            alt
          >
            <RenderImage
              v-if="newImageMask"
              :image="newImageMask"
              :minCropVal="preprocessArgsInUseMask.cropMin"
              :maxCropVal="preprocessArgsInUseMask.cropMax"
              :invertBackground="preprocessArgsInUseMask.invertBackground"
              :colormap="preprocessArgsInUseMask.colormap"
              :opacity="preprocessArgsInUseMask.opacity"
            />
          </v-img>
          <v-img
            id="image-mask_org"
            class="covered_transparent"
            width="512"
            height="384"
            alt="waiting"
          >
            <RenderImage
              v-if="newImage"
              :image="newImage"
              :minCropVal="preprocessArgsInUse.cropMin"
              :maxCropVal="preprocessArgsInUse.cropMax"
              :invertBackground="preprocessArgsInUse.invertBackground"
              :colormap="preprocessArgsInUse.colormap"
              :opacity="preprocessArgsInUse.opacity"
            />
          </v-img>
          <div id="contextMenu" class="context-menu text-center">
            <ul id="label" class="labelCheck">
              <li
                value="Cell"
                @click="colorSelect('Single Cell')"
                @contextmenu="colorSelect('Single Cell')"
              >
                Single Cell
              </li>
              <li
                value="Aggregates"
                @click="colorSelect('Aggregate')"
                @contextmenu="colorSelect('Aggregate')"
              >
                Aggregate
              </li>
              <li
                value="Platelet"
                @click="colorSelect('Platelet')"
                @contextmenu="colorSelect('Platelet')"
              >
                Platelet
              </li>
              <li class="separator"></li>
              <li
                value="Other"
                @click="colorSelect('Other')"
                @contextmenu="colorSelect('Other')"
              >
                Other
              </li>
            </ul>
            <v-btn x-small
              @click="hideContextMenu('break')"
              block
              tile
              color="grey lighten-3"
                  >
              <v-icon>mdi-close</v-icon>Close
            </v-btn>
          </div>
          <v-row class="mainfunctions">
            <v-col>
              <v-btn
                v-if="disabled_modi"
                @click="
                  disableButton('previous');
                  previousImage();
                "
                class="ml-3"
                color="warning"
                disabled
                >previous image</v-btn
              >
              <v-btn
                v-else
                @click="
                  disableButton('previous');
                  previousImage();
                "
                class="ml-3"
                dark
                :disabled="disabled_prev"
                :loading="loading_prev"
                color="teal"
                >previous image</v-btn
              >
            </v-col>
            <v-col>
              <v-btn v-if="disabled_modi" @click="undo()" color="warning">
                <v-icon left>mdi-step-backward</v-icon>undo</v-btn
              >
              <v-btn
                v-else
                @click="undo()"
                dark
                color="teal"
                :disabled="disabled_undo"
                align-center
                justify-center
              >
                <v-icon left>mdi-step-backward</v-icon>undo</v-btn
              >
              <div>
                <p></p>
                <p class="status_message">{{ this.text_button }}</p>
              </div>
            </v-col>
            <v-col>
              <v-btn
                v-if="disabled_modi"
                @click="
                  disableButton('addtoMask');
                  checkLabels('');
                "
                color="warning"
                class="mr-0"
                :disabled="disabled_next"
                :loading="loading_next"
                >Add to mask</v-btn
              >
              <v-btn
                v-else
                @click="
                  disableButton('next');
                  checkLabels('next_image');
                "
                dark
                color="teal"
                class="mr-0"
                :disabled="disabled_next"
                :loading="loading_next"
                >next image</v-btn
              >
            </v-col>
          </v-row>
        </div>
        <div class="rightside">
          <v-card-text
            class="text-center"
            v-if="allProperties.labelingApproach === 'basic'"
          >
            user: <b>{{ allProperties.UserID }}</b> <br />
            Dataset of <b>{{ allProperties.dataset_typ }}</b> <br />
            <b>Image {{ imageRef_num }}</b>
            <br />Time: {{ this.seconds }} seconds
          </v-card-text>
          <v-card-text
            class="text-center"
            v-if="allProperties.labelingApproach === 'game'"
          >
            user: <b>{{ allProperties.UserID }}</b> <br />
            GAME!!! <br />
            <b>Image {{ this.imageRef }}</b>
          </v-card-text>
          <section v-if="allProperties.labelingApproach === 'game'">
            <transition name="bounce">
              <img
                v-if="bounce"
                alt="flash"
                :src="require(`../assets/${animation}.jpg`)"
                width="100"
                class="center"
              />
            </transition>
            <transition name="roll">
              <img
                v-if="roll"
                alt="Star"
                :src="require(`../assets/${animation}.jpg`)"
                width="100"
                class="center"
              />
            </transition>
          </section>
          <!--preview starts here-->
          <div
            class="SegMaskDIV"
            v-if="allProperties.labelingApproach === 'basic'"
          >
            <canvas
              ref="canvasSegMask"
              class="SegMask"
              id="SegMask"
              width="192"
              height="145"
            ></canvas>
            <v-img
              id="SegMask_id"
              class="SegMaskImage"
              width="192"
              height="144"
              alt="waiting"
            >
              <RenderImage
                v-if="SegMask"
                :image="SegMask"
                :minCropVal="preprocessArgsInUseMask.cropMin"
                :maxCropVal="preprocessArgsInUseMask.cropMax"
                :invertBackground="preprocessArgsInUseMask.invertBackground"
                :colormap="preprocessArgsInUseMask.colormap"
                :opacity="preprocessArgsInUseMask.opacity"
              />
            </v-img>
          </div>
          <div
            class="SegMaskTitle"
            v-if="allProperties.labelingApproach === 'basic'"
          >
            <v-card-text class="text-center">
              Segmentation Mask <br/>
              (current Result)
            </v-card-text>
          </div>
          <!-- for game -->
          <HelpSection :currentLevel="0" />
        </div>
      </v-row>
      <!--achieving goals-->
      <v-row v-if="imageRef_num == 16">
        <div class="text-center help">
          <v-dialog v-model="dialog" width="500">
            <v-card>
              <v-app-bar dark color="teal">
                <v-toolbar-title>Goal: 15 Images</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-app-bar>
              <v-card>
                <!--<div class="d-flex flex-no-wrap justify-space-between">-->
                <br />
                <div>
                  <v-card-text class="acc text-center" style="font-size: 1.7em">
                    You labeled 15 images! <br /><br />You can do more!
                  </v-card-text>
                  <v-card-text class="acc text-center" style="font-size: 0.9em">
                    or stop the Task
                  </v-card-text>
                </div>
                <!--</div>-->
              </v-card>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" text @click="dialog = false"
                  >Close</v-btn
                >
              </v-card-actions>
            </v-card>
          </v-dialog>
        </div>
      </v-row>
    </v-col>
    <!--- Main component ends here --->
    <div class="nav-arrow-next">
      <v-btn
        small
        @click="
          checkLabels('last');
          updateScores(allProperties.labelingApproach, 'review');
        "
        color="primary"
      >
        <v-icon left>mdi-arrow-right-circle</v-icon>next
      </v-btn>
    </div>
  </v-row>
  <!--</div>-->
</template>

<script>
import { HTTP } from '@/http.common';
import RenderImage from '@/components/RenderImage.vue';
import HelpSection from '@/components/HelpSection.vue';

export default {
  name: 'LabelingInitialize',
  props: ['allProperties'],
  components: {
    RenderImage,
    HelpSection,
  },

  data: () => ({
    num: 0,
    newImage: null,
    newImageMask: null,
    newImages: [],
    newImageMasks: [],
    image_update: 0,
    SegMaskImage: null,
    SegMask: null,
    SegMaskNumber: '__',
    SegMaskAll: [],
    preprocessArgsInUse: {
      cropMin: 0,
      cropMax: 255,
      invertBackground: false,
      colormap: 'None',
      backgroundSubtraction: false,
      opacity: 255,
    },
    preprocessArgsInUseMask: {
      cropMin: -0.5,
      cropMax: 3.0,
      invertBackground: true,
      colormap: 'velocity-blue',
      backgroundSubtraction: true,
      opacity: 255,
    },
    colormap: false,
    loading_save: false,
    disabled_next: false,
    loading_next: false,
    disabled_prev: false,
    loading_prev: false,
    disabled_undo: false,
    canvas: null,
    context: null,
    button: null,
    imageRef: '00001',
    imageRef_num: 1,
    image_section: 0,
    startX: '',
    startY: '',
    // drawing rect for region labeling
    firstClick: [0, 0],
    secondClick: [0, 0],
    init_rect: '',
    width_region: '',
    height_region: '',
    isDrawing: false,
    rectBefore: [0, 0, 0],
    regionData: '',
    labelAreas: [],
    labelAreasAll: [],
    labelAreasRegion: [],
    labelAreasRegionAll: [],
    lastLabeledElement: [],
    lastLabeledElementAll: [],
    newAreas: [],
    newAreasAll: [],
    cellData: '',
    label: '',
    label_region: '',
    color: '',
    text_button: '',
    dialog: true,
    // dialog_rules: true,
    elementMainOrg: null,
    elementMainMask: null,
    optionStatus: 'transparent',
    upStatus: 'org',
    downStatus: 'mask',
    seconds: 0,
    isRunning: false,
    interval: null,
    // change Tool
    labelSingle: true,
    labelRegion: false,
    elevToolSing: 10,
    elevToolReg: 2,
    colorSing: 'purple',
    colorReg: 'purple lighten-4',
    empty: false,
    edge: false,
    // change modi
    disabled_modi: false,
    disabled_org: true,
    disabled_mask: true,
    min: 100,
    max: 255,
    slider: 255,
    clicks: 0,
    hoverObject: false,
    hoverArea: false,
    hoverSingle: false,
    // game, here comparing data later
    numberCells: 0,
    numberRegions: 0,
    addedAreas: 0,
    minusPoints: 0,
    highscore: '__',
    bounce: false,
    roll: false,
    animated: false,
    animation: 'Star',
    accuracyTotal: [],
  }),
  methods: {
    updateComponent(event) {
      this.$emit('updateComponent', event);
    },
    switchImage(toImage) {
      this.imageRef = toImage;
      this.selectedRectangle = -1;
      this.redrawContentCell();
    },
    colorSelect(labelNew) {
      const label = labelNew.trim();
      if (label === 'Single Cell') {
        this.color = 'red';
      } else if (label === 'Platelet') {
        this.color = '#66ff33';
      } else if (label === 'Aggregate') {
        this.color = 'purple';
      } else if (label === 'Background') {
        this.color = '#ff66ff';
      } else if (label === 'Other') {
        this.color = '#00ACC1';
      }
      // this.color = color;
    },
    selectTool(tool) {
      if (tool === 'labelSingle') {
        this.labelSingle = true;
        this.labelRegion = false;
        this.elevToolSing = 10;
        this.elevToolReg = 2;
        this.colorSing = 'purple';
        this.colorReg = 'purple lighten-4';
        this.canvas.addEventListener('click', this.selectCell);
        this.canvas.removeEventListener('mousedown', this.startRectRegion);
        this.canvas.removeEventListener('mousemove', this.selectRegion);
        this.canvas.removeEventListener('mouseup', this.MouseupRegion);
      } else if (tool === 'labelRegion') {
        this.labelSingle = false;
        this.labelRegion = true;
        this.elevToolSing = 2;
        this.elevToolReg = 10;
        this.colorSing = 'purple lighten-4';
        this.colorReg = 'purple';
        this.canvas.removeEventListener('click', this.selectCell);
        this.canvas.addEventListener('mousedown', this.startRectRegion);
        this.canvas.addEventListener('mousemove', this.selectRegion);
        this.canvas.addEventListener('mouseup', this.MouseupRegion);
      }
    },
    resetArea() {
      while (!this.empty) {
        this.undo('all');
      }
      this.uploadData();
      this.SegMask = null;
      this.empty = false;
      this.disabled_modi = false;
      this.selectTool('labelSingle');
    },
    selectCell(e) {
      this.text_button = '';
      if (this.labelSingle) {
        this.text_button = '';
        if (e.button === 2) {
          // Block right-click menu thru preventing default action.
          e.preventDefault();
        }
        const rect = this.canvas.getBoundingClientRect();
        this.startX = e.clientX - rect.left;
        this.startY = e.clientY - rect.top;
        if (this.disabled_modi) { // && !this.disabled_measurement) {
          this.NewContent();
        } else if (this.labelSingle) {
          this.showContextMenu(this.startX, this.startY);
        }
        this.isDrawing = false;
      }
    },
    showContextMenu(x, y) {
      document
        .getElementById('label')
        .removeEventListener('click', this.getRegionLabel);
      document.getElementById('contextMenu').style.display = 'inline';
      document.getElementById('contextMenu').style.left = `${x}px`;
      document.getElementById('contextMenu').style.top = `${y}px`;
      document
        .getElementById('label')
        .addEventListener('click', this.getCellLabel);
      document.body
        .addEventListener('click', this.hideContextMenu, true);

      return false;
    },
    getCellLabel(event) {
      if (this.startX !== '') {
        console.log(`label: ${event.target.innerHTML}`);
        this.hideContextMenu();
        // getting previous labeling, labelAreas/Region delted after sending data
        if (this.labelAreasAll[this.imageRef_num - 1] !== 0) {
          this.labelAreas = this.labelAreasAll[this.imageRef_num - 1];
        }
        if (this.labelAreasRegionAll[this.imageRef_num - 1] !== 0) {
          this.labelAreasRegion = this.labelAreasRegionAll[
            this.imageRef_num - 1
          ];
        }
        this.label = event.target.innerHTML;
        this.cellData = [this.startX, this.startY, this.label];
        this.labelAreas.push(this.cellData);
        this.labelAreasAll[this.imageRef_num - 1] = this.labelAreas;
        this.lastLabeledElement.push('cell');
        this.lastLabeledElementAll[
          this.imageRef_num - 1
        ] = this.lastLabeledElement;
        this.startX = '';
        this.startY = '';
        this.redrawContentCell('cell');
        this.numberCells = this.numberCells + 1;
      }
    },
    redrawContentCell() {
      const x = this.cellData[0];
      const y = this.cellData[1];
      this.context.beginPath();
      this.context.moveTo(x - 5, y - 5);
      this.context.lineTo(x + 5, y + 5);
      this.context.moveTo(x + 5, y - 5);
      this.context.lineTo(x - 5, y + 5);
      this.context.strokeStyle = this.color;
      this.context.lineWidth = 3;
      this.context.stroke();
      this.checkLabels('during');
    },
    startRectRegion(e) {
      this.text_button = '';
      console.log('startRectRegion');
      /* document
        .getElementById('label')
        .addEventListener('click', this.getRegionLabel); */
      if (this.disabled_modi) {
        const rect = this.canvas.getBoundingClientRect();
        this.startX = e.clientX - rect.left;
        this.startY = e.clientY - rect.top;
        this.NewContent();
        /* } else if (this.disabled_measurement) {
          this.MeasureCell(e); */
      } else if (this.labelRegion) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        this.firstClick = [x, y];
        this.isDrawing = true;
      }
    },
    MouseupRegion() {
      this.isDrawing = false;
      if (this.labelRegion) {
        /* document
          .getElementById('label')
          .addEventListener('click', this.getRegionLabel); */
        this.showContextMenuRegion(
          this.rectBefore[0][0] + this.rectBefore[1] + 2,
          this.rectBefore[0][1] + this.rectBefore[2],
        );
      }
    },
    selectRegion(e) {
      if (this.labelRegion) {
        const x = e.offsetX; // e.clientX - rect.left;
        const y = e.offsetY; // e.clientY - rect.top;
        this.secondClick = [x, y];
        if (e.button === 2) {
          // Block right-click menu thru preventing default action.
          e.preventDefault();
        }
        if (this.isDrawing === true) {
          if (
            this.firstClick[0] < this.secondClick[0]
            && this.firstClick[1] < this.secondClick[1]
          ) {
            this.init_rect = this.firstClick;
            this.width_region = this.secondClick[0] - this.firstClick[0];
            this.height_region = this.secondClick[1] - this.firstClick[1];
          }
          if (
            this.firstClick[0] > this.secondClick[0]
            && this.firstClick[1] > this.secondClick[1]
          ) {
            this.init_rect = [this.secondClick[0], this.secondClick[1]];
            this.width_region = this.firstClick[0] - this.secondClick[0];
            this.height_region = this.firstClick[1] - this.secondClick[1];
          }
          if (
            this.firstClick[0] > this.secondClick[0]
            && this.firstClick[1] < this.secondClick[1]
          ) {
            this.init_rect = [this.secondClick[0], this.firstClick[1]];
            this.width_region = this.firstClick[0] - this.secondClick[0];
            this.height_region = this.secondClick[1] - this.firstClick[1];
          }
          if (
            this.firstClick[0] < this.secondClick[0]
            && this.firstClick[1] > this.secondClick[1]
          ) {
            this.init_rect = [this.firstClick[0], this.secondClick[1]];
            this.width_region = this.secondClick[0] - this.firstClick[0];
            this.height_region = this.firstClick[1] - this.secondClick[1];
          }
          this.context.clearRect(
            this.rectBefore[0][0] - 2,
            this.rectBefore[0][1] - 2,
            this.rectBefore[1] + 4,
            this.rectBefore[2] + 4,
          );
          this.context.beginPath();
          this.context.rect(
            this.init_rect[0],
            this.init_rect[1],
            this.width_region,
            this.height_region,
          );
          this.context.lineWidth = 2;
          this.context.strokeStyle = 'white';
          this.context.stroke();
        }
        this.rectBefore = [this.init_rect, this.width_region, this.height_region];
      }
    },
    showContextMenuRegion(x, y) {
      document
        .getElementById('label')
        .removeEventListener('click', this.getCellLabel);
      document
        .getElementById('label')
        .addEventListener('click', this.getRegionLabel);
      document.getElementById('contextMenu').style.display = 'inline';
      document.getElementById('contextMenu').style.left = `${x}px`;
      document.getElementById('contextMenu').style.top = `${y}px`;
      /* document.body
        .addEventListener('contextmenu', this.hideContextMenu('break'), true); */
    },
    getRegionLabel(event) {
      if (this.init_rect !== '') {
        if (event.button === 2) {
          // Block right-click menu thru preventing default action.
          event.preventDefault();
        }
        this.hideContextMenu();
        // getting previous labeling, labelAreas/Region delted after sending data
        if (this.labelAreasRegionAll[this.imageRef_num - 1] !== 0) {
          this.labelAreasRegion = this.labelAreasRegionAll[
            this.imageRef_num - 1
          ];
        }
        // getting previous labeling
        if (this.labelAreasAll[this.imageRef_num - 1] !== 0) {
          this.labelAreas = this.labelAreasAll[this.imageRef_num - 1];
        }
        this.label_region = event.target.innerHTML;
        this.regionData = [
          this.init_rect,
          this.width_region,
          this.height_region,
          this.label_region,
        ];
        this.labelAreasRegion.push(this.regionData);
        this.labelAreasRegionAll[this.imageRef_num - 1] = this.labelAreasRegion;
        this.redrawContentRegion('region');
        this.lastLabeledElement.push('region');
        this.lastLabeledElementAll[
          this.imageRef_num - 1
        ] = this.lastLabeledElement;
        this.init_rect = '';
        this.width_region = '';
        this.height_region = '';
        this.numberRegions = this.numberRegions + 1;
      }
    },
    redrawContentRegion() {
      this.context.clearRect(
        this.init_rect[0] - 2,
        this.init_rect[1] - 2,
        this.width_region + 4,
        this.height_region + 4,
      );
      this.context.beginPath();
      this.context.rect(
        this.init_rect[0],
        this.init_rect[1],
        this.width_region,
        this.height_region,
      );
      this.context.lineWidth = 2;
      this.context.strokeStyle = this.color;
      this.context.stroke();
      this.checkLabels('during');
    },
    hideContextMenu(breakDelete) {
      document.body.removeEventListener('click', this.hideContextMenu, true);
      console.log('in hideContextMenu');
      if (!document.getElementById('contextMenu')) {
        return;
      }
      const ele = document.getElementById('contextMenu');
      ele.style.display = 'none';
      if (breakDelete === 'break') {
        this.context.clearRect(
          this.rectBefore[0][0] - 2,
          this.rectBefore[0][1] - 2,
          this.rectBefore[1] + 4,
          this.rectBefore[2] + 4,
        );
      }
    },
    // for add Regions
    NewContent() {
      this.newXY = [this.startX, this.startY];
      this.newAreas.push(this.newXY);
      this.newAreasAll[this.imageRef_num - 1] = this.newAreas;
      // this.newAreas.push(this.newXY);
      // this.context.beginPath();
      /* this.context.rect(this.startX - 20, this.startY - 20, 40, 40);
      this.context.strokeStyle = 'red';
      this.context.stroke(); */
      this.context.beginPath();
      this.context.moveTo(this.startX, this.startY - 3);
      this.context.lineTo(this.startX - 4, this.startY + 4);
      this.context.lineTo(this.startX + 4, this.startY + 4);
      this.context.closePath();
      this.context.fillStyle = 'orange';
      // this.context.fill();
      this.context.strokeStyle = 'orange';
      this.context.lineWidth = 3;
      this.context.stroke();
      // counting added region
      this.addedAreas = this.addedAreas + 1;
    },
    // redraw content that is previously drawn, for going to previous image
    redrawOldContent(labeled) {
      let x = [];
      let y = [];
      let height = [];
      let width = [];
      if (!this.disabled_modi || labeled) {
        console.log('in redraw Old content');
        const currentData = this.labelAreasAll[this.imageRef_num - 1];
        const currentDataRegion = this.labelAreasRegionAll[
          this.imageRef_num - 1
        ];
        for (let i = 1; i <= currentData.length; i += 1) {
          const Label = currentData[i - 1];
          x = Label[0];
          y = Label[1];
          this.colorSelect(Label[2]);
          this.context.beginPath();
          this.context.moveTo(x - 5, y - 5);
          this.context.lineTo(x + 5, y + 5);
          this.context.moveTo(x + 5, y - 5);
          this.context.lineTo(x - 5, y + 5);
          this.context.strokeStyle = this.color;
          this.context.lineWidth = 3;
          this.context.stroke();
        }
        for (let i = 1; i <= currentDataRegion.length; i += 1) {
          const Label = currentDataRegion[i - 1];
          x = Label[0][0];
          y = Label[0][1];
          width = Label[1];
          height = Label[2];
          this.colorSelect(Label[3]);
          this.context.beginPath();
          this.context.rect(x, y, width, height);
          this.context.strokeStyle = this.color;
          this.context.lineWidth = 2;
          this.context.stroke();
        }
      } else {
        const currentDataNew = this.newAreasAll[this.imageRef_num - 1];
        for (let i = 1; i <= currentDataNew.length; i += 1) {
          const Label = currentDataNew[i - 1];
          x = Label[0];
          y = Label[1];
          this.context.beginPath();
          this.context.rect(x - 20, y - 20, 40, 40);
          this.context.strokeStyle = 'red';
          this.context.stroke();
        }
      }
    },
    // for checking selected content by user, by bext image or add to Mask
    checkLabels(section) {
      if (
        Object.keys(this.labelAreas).length === 0
        && Object.keys(this.newAreas).length === 0
        && Object.keys(this.labelAreasRegion).length === 0
        && this.disabled_modi === false
        && section !== 'last'
      ) {
        console.log('no data - next image');
        this.nextImage();
      } else if (
        !this.disabled_modi
        && (Object.keys(this.labelAreas).length !== 0
        || Object.keys(this.labelAreasRegion).length !== 0)
      ) {
        // this.disabled_save = true;
        // this.loading_save = true;
        if (section === 'next_image') {
          this.text_button = 'save image...';
        }
        this.uploadData(section);
      } else if (
        this.disabled_modi
        && Object.keys(this.newAreas).length !== 0
      ) {
        console.log('ADD REGIONS');
        // this.disabled_save = true;
        // this.loading_save = true;
        this.text_button = 'get LabelMask';
        this.uploadNewData();
      } else if (
        this.disabled_modi
        && Object.keys(this.newAreas).length === 0
      ) {
        this.disabled_next = false;
        this.loading_next = false;
        this.disabled_prev = false;
        this.loading_prev = false;
        this.disabled_modi = false;
        // this.disabled_measurement = false;
      } else if (
        !this.disabled_modi
        && Object.keys(this.newAreas).length !== 0
      ) {
        if (section === 'next_image') {
          this.text_button = 'save image...';
        }
        this.uploadData(section);
        // this.text_button = '';
        this.newAreas = [];
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        // this.redrawOldContent(true);
      } else {
        console.log('error in checkLabels');
      }
    },
    // upload labels
    uploadData(section) {
      console.log('uploadData start');
      if (this.labelAreas.length === 0) {
        this.labelAreas = 'none';
      }
      if (this.labelAreasRegion.length === 0) {
        this.labelAreasRegion = 'none';
      }
      this.labelAreas = String(this.labelAreas);
      this.labelAreasRegion = String(this.labelAreasRegion);
      const length = this.lastLabeledElementAll[this.imageRef_num - 1].length;
      const lastEle = this.lastLabeledElementAll[this.imageRef_num - 1][length - 1];
      console.log(lastEle);
      HTTP.post(
        `label/${this.labelAreas}/${this.labelAreasRegion}/${lastEle}/${this.imageRef_num}/${this.allProperties.UserID}/${this.allProperties.dataset_typ}/0/${this.allProperties.labelingApproach}`,
      )
        .then(async (response) => {
          // this.newImage = response.data.image;
          console.log(
            `labels recieved and segMask calcualted for image ${response.data.image_num}.`,
          );
          this.SegMaskAll = response.data.seg_masks;
          this.SegMaskNumber = response.data.image_num;
          this.SegMask = this.SegMaskAll[this.SegMaskNumber - 1];
          console.log(`wrong label: ${response.data.wrong_label}`);
          console.log(this.SegMaskAll);
          if (response.data.wrong_label === true) {
            this.animation = 'flash';
            this.bounce = true;
            this.minusPoints = this.minusPoints + 5;
          }
          if (response.data.wrong_label === false) {
            this.animation = 'coin';
            this.roll = true;
          }
          this.labelAreas = [];
          this.labelAreasRegion = [];
        })
        .catch((e) => {
          console.warn(e);
          this.labelAreas = [];
          this.labelAreasRegion = [];
          this.undo();
          this.text_button = 'last label failed, label again';
        });
      if (section === ('next_image' || 'during')) {
        this.nextImage();
      }

      return 'Complete';
    },
    // for updated LabelMask
    uploadNewData() {
      console.log('uploadnewData start');
      this.newImageMask = null;
      this.newAreas = String(this.newAreas);
      HTTP.post(
        `newAreas/${this.newAreas}/${this.imageRef_num}/${this.allProperties.UserID}/${this.allProperties.dataset_typ}/0`,
      )
        .then(async (response) => {
          this.newImageMasks[this.image_section][this.image_update] = response.data.New_label_mask;
          this.newImageMask = response.data.New_label_mask;
          console.log('Received: new LabelMask');
          this.disabled_next = false;
          this.loading_next = false;
          this.disabled_prev = false;
          this.loading_prev = false;
          this.disabled_modi = false;
          if (this.labelSingle) {
            const tool = 'labelSingle';
            this.selectTool(tool);
          } else {
            const tool = 'labelRegion';
            this.selectTool(tool);
          }
          // this.disabled_measurement = false;
          this.text_button = '';
          this.newAreas = [];
          this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
          this.redrawOldContent(true);
        })
        .catch((e) => {
          console.warn(e);
        });
      return 'Complete';
    },
    // diabled buttons for different modi
    disableButton(options) {
      if (options === 'next') {
        this.disabled_next = true;
        this.loading_next = true;
        this.text_button = 'getting images...';
      }
      if (options === 'previous' && this.imageRef_num > 1) {
        this.disabled_prev = true;
        this.loading_prev = true;
        this.text_button = 'getting images...';
      }
      if (options === 'addtoMask') {
        this.disabled_next = true;
        this.loading_next = true;
      }
      if (options === 'all') {
        this.disabled_next = true;
        // this.loading_next = true;
        this.disabled_prev = true;
        // this.loading_prev = true;
        this.disabled_undo = true;
        this.text_button = 'getting images...';
      }
    },
    nextImage() {
      // deltet circles
      console.log('next Image');
      this.SegMask = null;
      this.empty = false;
      this.edge = false;
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.imageRef_num = this.imageRef_num + 1;
      this.lastLabeledElement = [];
      if (
        this.labelAreasAll[this.imageRef_num - 1] !== 0
        || this.labelAreasRegionAll[this.imageRef_num - 1] !== 0
      ) {
        this.SegMask = this.SegMaskAll[this.imageRef_num - 1];
        this.redrawOldContent(false);
      }
      this.imageRef = this.imageRef_num.toString();
      while (this.imageRef.length < 5) {
        this.imageRef = `0${this.imageRef}`;
      }
      console.log(`image number: ${this.imageRef}`);
      // get next 10 iamges
      if ((this.imageRef_num - 1) % 10 === 0) {
        this.image_section = this.image_section + 1;
        this.updateScores(0, 'after10');
        // only if it did not get before, check if for this section already images there
        if (this.newImages[this.image_section] === undefined) {
          console.log(`getData for next section : ${this.image_section}`);
          this.image_update = 0;
          this.getData(false);
          // console.log(this.newImages[this.image_section]);
        } else {
          this.image_update = 0;
          this.updateImages();
        }
      } else {
        this.image_update = this.image_update + 1;
        this.updateImages();
      }
      if (this.allProperties.labelingApproach === 'basic') {
        document.getElementById('SegMask').style.display = 'inline';
      }
    },
    previousImage() {
      // deltet circles
      console.log('previous Image');
      this.SegMask = null;
      this.empty = false;
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
      if (this.imageRef_num > 1) {
        this.imageRef_num = this.imageRef_num - 1;
        if (this.imageRef_num % 10 === 0) {
          this.image_section = this.image_section - 1;
          this.image_update = 10;
        }
        if (
          this.labelAreasAll[this.imageRef_num - 1] !== 0
          || this.labelAreasRegionAll[this.imageRef_num - 1] !== 0
        ) {
          this.SegMask = this.SegMaskAll[this.imageRef_num - 1];
          this.redrawOldContent(false);
        }
        this.imageRef = this.imageRef_num.toString();
        while (this.imageRef.length < 5) {
          this.imageRef = `0${this.imageRef}`;
        }
        this.image_update = this.image_update - 1;
        this.updateImages();
      } else {
        this.text_button = 'no previous image';
      }
    },
    // new Images at label area
    updateImages() {
      this.newImage = this.newImages[this.image_section][this.image_update];
      this.newImageMask = this.newImageMasks[this.image_section][
        this.image_update
      ];
      this.disabled_next = false;
      this.loading_next = false;
      this.disabled_prev = false;
      this.loading_prev = false;
      this.text_button = '';
    },
    // after each 10 images get new 10 images from backend
    getData(mounted) {
      this.disableButton('all');
      console.log('get 10 images');
      // let celltyp = '';
      this.newImage = null;
      this.newImageMask = null;
      HTTP.post(
        `getData/${this.imageRef_num}/${mounted}/${this.allProperties.UserID}/${this.image_section}/${this.allProperties.dataset_typ}/${this.allProperties.labelingApproach}/0`,
      )
        .then(async (response) => {
          this.newImages.push(response.data.image);
          this.newImageMasks.push(response.data.label_mask);
          console.log('Received');
          if (mounted === true) {
            this.highscore = response.data.highscore;
            console.log('Start Timer');
            this.toggleTimer();
          }
          this.newImage = this.newImages[this.image_section][0];
          this.newImageMask = this.newImageMasks[this.image_section][0];
          this.disabled_next = false;
          this.loading_next = false;
          this.disabled_prev = false;
          this.loading_prev = false;
          this.disabled_undo = false;
          this.edge = true;
          this.text_button = '';
        })
        .catch((e) => {
          console.warn(e);
        });
      return 'Complete';
    },
    // undo last selected element by user
    undo(all) {
      console.log('undo last element or reset all');
      const length = this.lastLabeledElementAll[this.imageRef_num - 1].length;
      if ((!this.disabled_modi || all === 'all')
        && (this.labelAreasAll[this.imageRef_num - 1].length !== 0
        || this.labelAreasRegionAll[this.imageRef_num - 1].length !== 0)
        && this.lastLabeledElementAll[this.imageRef_num - 1][length - 1] !== undefined) {
        console.log(this.labelAreasAll[this.imageRef_num - 1].length);
        console.log(this.labelAreasRegionAll[this.imageRef_num - 1].length);
        console.log(this.lastLabeledElementAll[this.imageRef_num - 1][length - 1]);
        console.log(this.lastLabeledElementAll[this.imageRef_num - 1]);
        if (
          this.lastLabeledElementAll[this.imageRef_num - 1][length - 1] === 'cell'
        ) {
          const currentData = this.labelAreasAll[this.imageRef_num - 1];
          const lastElement = currentData[currentData.length - 1];
          this.context.clearRect(
            lastElement[0] - 20 - 2,
            lastElement[1] - 20 - 2,
            20 * 2 + 4,
            20 * 2 + 4,
          );
          currentData.pop();
          this.lastLabeledElementAll[this.imageRef_num - 1].pop();
          this.labelAreasAll[this.imageRef_num - 1] = currentData; // .length - 1] = 0;
          this.numberCells = this.numberCells - 1;
        } else if (
          this.lastLabeledElementAll[this.imageRef_num - 1][length - 1] === 'region'
        ) {
          const currentData = this.labelAreasRegionAll[this.imageRef_num - 1];
          const lastElement = currentData[currentData.length - 1];
          this.context.clearRect(
            lastElement[0][0] - 2,
            lastElement[0][1] - 2,
            lastElement[1] + 4,
            lastElement[2] + 4,
          );
          currentData.pop();
          this.lastLabeledElementAll[this.imageRef_num - 1].pop();
          this.labelAreasRegionAll[this.imageRef_num - 1] = currentData;
          this.numberRegions = this.numberRegions - 1;
        } else {
          console.log('no elements');
          //  this.empty = true;
        }
      /* } else if (this.disabled_measurement) {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.redrawOldContent(); */
      } else if (this.newAreasAll[this.imageRef_num - 1] !== undefined) {
        const currentData = this.newAreasAll[this.imageRef_num - 1];
        if (this.newAreasAll[this.imageRef_num - 1] !== 0
          && !(currentData.length === 0 || currentData.length === undefined)) {
          const lastElement = currentData[currentData.length - 1];
          this.context.clearRect(
            lastElement[0] - 20 - 2,
            lastElement[1] - 20 - 2,
            20 * 2 + 4,
            20 * 2 + 4,
          );
          currentData.pop();
          this.newAreasAll[this.imageRef_num - 1] = currentData; // .length - 1] = 0;
          this.addedAreas = this.addedAreas - 1;
        } else if (all === 'all' && (this.newAreasAll[this.imageRef_num - 1] === 0
            || currentData.length === 0)) {
          this.empty = true;
        } else {
          console.log('no elements');
          // this.empty = true;
        }
      }
      if (this.newAreasAll[this.imageRef_num - 1].length === 0
        && this.labelAreasRegionAll[this.imageRef_num - 1] === 0
        && this.labelAreasAll[this.imageRef_num - 1] === 0) {
        this.empty = true;
      }
      if (this.labelAreasAll[this.imageRef_num - 1] !== 0) {
        this.labelAreas = this.labelAreasAll[this.imageRef_num - 1];
      }
      if (this.labelAreasRegionAll[this.imageRef_num - 1] !== 0) {
        this.labelAreasRegion = this.labelAreasRegionAll[
          this.imageRef_num - 1
        ];
      }
      if (all !== 'all') {
        console.log('uploaddata in undo');
        this.uploadData();
      }
    },
    /* // measure distance between two clicked points
    MeasureCell() {
      const ctx = this.context;
      const x = this.startX; // this.getClick(e)[0]; // - this.offsetLeft;
      const y = this.startY; // this.getClick(e)[1]; // - this.offsetTop;

      if (this.clicks !== 1) {
        this.clicks += 1;
      } else {
        ctx.beginPath();
        ctx.moveTo(this.firstClick[0], this.firstClick[1]);
        ctx.lineTo(x, y, 6);

        ctx.lineWidth = 2;
        ctx.strokeStyle = 'purple';
        ctx.stroke();

        const a = this.firstClick[0] - x;
        const b = this.firstClick[1] - y;
        let distance = Math.sqrt(a * a + b * b) * 0.345; // 1px = 0.345 nm
        distance = Math.round((distance + Number.EPSILON) * 100) / 100;
        ctx.fillStyle = 'purple';
        ctx.font = '15px Arial';
        ctx.fillText(`${distance} µm`, this.startX, this.startY);

        this.clicks = 0;
      }
      this.firstClick = [x, y];
    }, */
    // changes view of images, opacity, intesity of Orgimage and colormap
    changeModi(click) {
      if (this.disabled_org === false && this.disabled_mask === true) {
        this.elementMainOrg.style.opacity = '0';
        this.elementMainMask.style.opacity = '1';
      }
      if (this.disabled_mask === false && this.disabled_org === true) {
        this.elementMainOrg.style.opacity = '1';
        this.elementMainMask.style.opacity = '0';
      }
      if (this.disabled_mask === false && this.disabled_org === false) {
        this.elementMainOrg.style.opacity = '0';
        this.elementMainMask.style.opacity = '0';
      }
      if (this.disabled_mask === true && this.disabled_org === true) {
        this.elementMainOrg.style.opacity = '0.5';
        this.elementMainMask.style.opacity = '1';
      }
      if (click === 'modi1' && this.disabled_modi === false) {
        if (this.labelSingle) {
          const tool = 'labelSingle';
          this.selectTool(tool);
        } else {
          const tool = 'labelRegion';
          this.selectTool(tool);
        }
      } else if (click === 'modi1' && this.disabled_modi === true) {
        this.canvas.removeEventListener('mousemove', this.selectRegion);
        this.canvas.removeEventListener('mouseup', this.MouseupRegion);
      }
      /* if (click === 'modi2' && this.disabled_modi_measure === true) {
        this.disabled_modi = false;
      } */
      if (click === 'slider') {
        this.preprocessArgsInUse.cropMax = this.slider;
      }
      if (click === 'colormap' && this.colormap === true) {
        console.log('change colormap');
        this.preprocessArgsInUse.colormap = 'jet';
      } else if (click === 'colormap' && this.colormap === false) {
        this.preprocessArgsInUse.colormap = 'None';
      }
    },
    options(selectedOption) {
      setTimeout(this.changeModi, 100, selectedOption);
    },
    // timer for session
    toggleTimer() {
      if (this.isRunning) {
        clearInterval(this.interval);
        console.log('timer stops');
      } else {
        this.interval = setInterval(this.incrementTime, 1000);
      }
      this.isRunning = !this.isRunning;
    },
    incrementTime() {
      this.seconds = parseInt(this.seconds, 10) + 1;
    },
    updateScores(all, review) {
      // console.log(`CURRENT LEVEL: ${this.allProperties.currentLevel}`);
      const wrongAreas = this.minusPoints / 5;
      console.log(`updateScores for current imagenumber: ${this.imageRef_num}`);
      // const AccuracyAll = [0, 0, 0, 0];
      // console.log('upload scores');
      let points = this.numberCells * 10
      + this.numberRegions * 30
      + this.addedAreas * 50
      - this.minusPoints;
      // const allScores = String(this.allProperties.AllScores);
      // const date = this.getDate();
      // console.log(typeof date); */
      HTTP.post()
        // `getAccuracy/${this.allProperties.labelingApproach}/
        // ${this.allProperties.UserID}/${this.allProperties.dataset_typ}/
        // ${this.image_section}/${this.imageRef_num}`,
        // `updateScore/${tooltyp}/${this.allProperties.UserID}/
        // ${this.allProperties.AllScores}/${this.imageRef_num}/
        // ${this.allProperties.dataset_typ}`,
        .then(async () => {
          // this.$emit('updateAccuracy', response.data.accuracy);
          // this.nextLevelprops.accuracyForScoring = response.data.accuracy[0];
          // this.nextLevelprops.accuracyForScoring_correct = response.data.accuracy[2];
          const accuracy = [0, 0, 0, 0];
          // const points = 0;
          const Scores = [
            this.imageRef_num,
            this.numberCells,
            this.numberRegions,
            wrongAreas,
            this.addedAreas,
            this.seconds,
            points,
            accuracy,
            this.allProperties.currentSection,
          ];
          // const Scores = [this.numberCells, this.numberRegions, this.addedAreas, this.seconds];
          this.$emit('updateScores', Scores);
          // this.$emit('updateAccuracy', response.data.accuracy);
          if (review === 'after10') {
            this.$emit('updateSection', this.image_section);
          }
          if (review === 'review') {
            //  this.updateBreak();
            this.updateComponent('review');
          }
          this.bounce_nextLevel = true;
          this.numberCells = 0;
          this.numberRegions = 0;
          points = 0;
          // this.seconds = 0;
        })
        .catch((e) => {
          console.warn(e);
        });
      return 'Complete';
    },
    getDate() {
      const currentdate = new Date();
      const datetime = `${currentdate.getDate()}.${
        currentdate.getMonth() + 1
      }.${currentdate.getFullYear()}@${currentdate.getHours()}:${currentdate.getMinutes()}:${currentdate.getSeconds()}`;
      console.log(datetime);

      return datetime;
    },
  },
  mounted() {
    // true to get an empty folder for starting labeling process at the backend side
    this.getData(true);
    console.log(`labelingapproach: ${this.allProperties.labelingApproach}`);
    // for labeling area
    this.canvas = this.$refs.canvas;
    this.context = this.canvas.getContext('2d');
    if (this.allProperties.labelingApproach === 'basic') {
      document.getElementById('SegMask').style.display = 'inline';
    }
    (this.labelAreasAll = []).length = 250;
    this.labelAreasAll.fill(0);
    (this.labelAreasRegionAll = []).length = 250;
    this.labelAreasRegionAll.fill(0);
    (this.newAreasAll = []).length = 250;
    this.newAreasAll.fill(0);
    // for undo last element
    (this.lastLabeledElementAll = []).length = 250;
    this.lastLabeledElementAll.fill(0);
    this.canvas.addEventListener('click', this.selectCell);
    this.elementMainOrg = document.getElementById('image-mask_org');
    this.elementMainMask = document.getElementById('image-mask_water');
    this.elementMainOrg.style.opacity = '0.5';
    this.elementMainMask.style.opacity = '1';
  },
};
</script>

<style scoped>
.wrapper {
  text-align: center;
  text-justify: center;
  border: 2px solid black;
}
.nav-arrow-next {
  top: 42px;
  left: 913px;
  text-justify: right;
  position: relative;
}
.nav-arrow-back {
  top: 550px;
  left: 3px;
  text-justify: right;
  position: relative;
}
.main {
  height: 480px;
  min-width: 1150px;
  padding-left: 80px;
  text-justify: center;
}
.canvas-wrapper {
  height: 100%;
  width: 115%;
  padding-right: 252px;
  border: 0px solid black;
}
.button_down {
  width: 100%;
  top: 510px;
}
.mainfunctions {
  border: 0px solid black;
  text-justify: center;
  text-align: center;
}
.tools {
  padding-bottom: 20px;
}
.options {
  position: relative;
  bottom: 50px;
}
.hoverSingle {
  position: absolute;
  z-index: 100;
  top: 80px;
  height: 50px;
  width: 190px;
  opacity: 0.8;
}
.hoverArea {
  position: absolute;
  z-index: 100;
  top: 80px;
  left: 80px;
  height: 70px;
  width: 180px;
  opacity: 0.8;
}
.hoverObject {
  position: absolute;
  z-index: 100;
  top: 460px;
  height: 90px;
  width: 190px;
  opacity: 0.8;
}
.infoEdge {
  position: absolute;
  z-index: 100;
  opacity: 0.6;
  bottom: 100px;
  left: 145px;
  width: 170px;
}
.save-button-id {
  margin-left: 5px;
}
.canvas {
  border: 0px solid black;
  height: 100%;
  width: '384';
  left: 7px;
  top: 15px;
  display: inline-block;
  z-index: 1;
  position: relative;
}
.context-menu {
  background: #f6f6f6;
  width: 200px;
  height: auto;
  position: absolute;
  display: none;
  overflow: visible;
  z-index: 1000;
}
.context-menu ul {
  list-style: none;
  padding: 5px 0px 5px 0px;
  overflow: visible;
  z-index: 999;
}
.context-menu ul li:not(.separator) {
  padding: 10px 5px 10px 5px;
  border-left: 4px solid transparent;
  cursor: pointer;
  overflow: visible;
  z-index: 999;
}
.context-menu ul li:hover {
  background: #eee;
  border-left: 4px solid #666;
  overflow: visible;
  z-index: 999;
}
.separator {
  height: 1px;
  background: #dedede;
  margin: 2px 0px 2px 0px;
}
.labelOverview {
  height: 20%;
  width: 100%;
  align-content: bottom;
}
.covering {
  border: 1px solid #000000;
  cursor: crosshair;
  z-index: 10;
  position: relative;
}
.rightside {
  left: 8px;
  position: relative;
}
.SegMaskDIV {
  position: static;
  height: 0%;
  top: 20px;
  display: inline-block;
  /*right: 100px;*/
  position: relative;
}
.SegMask {
  position: static;
  border: 1px solid #000000;
  cursor: move;
  z-index: 2;
  top: 30px;
}
.SegMaskImage {
  position: absolute;
  z-index: 0;
  right: 1px;
  top: 2px;
}
.SegMaskTitle {
  top: 15px;
  position: relative;
}
.covered {
  position: absolute;
  z-index: 0;
  top: 1px;
  left: 0px;
}
.covered_transparent {
  position: absolute;
  z-index: 1;
  top: 1px;
  left: 0px;
}
.scores {
  position: static;
  z-index: 10;
}
section {
  min-height: 100px;
  text-align: center;
  z-index: 50;
}
.bounce-enter-active {
  animation: bounce-in 0.5s;
}
/* .bounce-leave-active {
  animation: bounce-in .5s reverse;
} */
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(3);
  }
  100% {
    transform: scale(1);
  }
}
.roll-enter-active {
  animation: roll-in 0.5s;
}
/* .roll-leave-active {
  animation: roll-in .5s reverse;
} */
@keyframes roll-in {
  0% {
    transform: scale(0) rotateZ(0deg) translateX(-250px);
    opacity: 0;
  }
  25% {
    opacity: 1;
  }
  100% {
    transform: scale(1) rotateZ(360deg) translateX(0px);
    opacity: 1;
  }
}
</style>
