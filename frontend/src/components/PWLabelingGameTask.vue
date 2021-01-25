<template>
  <!--<div class='wrapper'>-->
  <v-row fill-width>
    <div
      class="nav-arrow-back"
      id="back-button"
      v-if="bounce_nextLevel === false"
    >
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
      <v-row class="canvas-wrapper" v-if="bounce_nextLevel === false">
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
                  v-if="allProperties.currentLevel !== 1"
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
          <label class="pl-3"> Colormap</label>
          <v-switch
            v-model="disabled_org"
            class="ml-2 mb-0"
            label="OrgImage"
            color="teal"
            @change="options('up')"
          ></v-switch>
          <v-slider
            v-model="slider"
            class="slider ml-2 mr-2 mb-0 mt-0"
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
            class="ml-2 mt-0"
            label="LabelMask"
            color="teal"
            @change="options('down')"
          ></v-switch>
          <!--modis.-->
          <v-divider class="mx-4 mb-3"></v-divider>
          <v-subheader
            v-if="
              allProperties.currentLevel !== 1 &&
              allProperties.currentLevel !== 2
            "
            class="pl-3"
            style="font-size: 1.2em"
            ><b>Mode:</b>
          </v-subheader>
          <v-switch
            v-if="
              allProperties.currentLevel !== 1 &&
              allProperties.currentLevel !== 2
            "
            v-model="disabled_modi"
            class="ml-2 mt-0"
            label="Add Objects to mask"
            color="warning"
            @change="options('modi1')"
            @mouseover="hoverObject = true"
            @mouseleave="hoverObject = false"
          >
          </v-switch>
          <!--not necessary anymore -->
          <!--<v-switch v-model="disabled_measurement" class="ma-2"
              label ="Measure Distance"
              color='purple' @click="options('measurement')">
              </v-switch>-->
          <v-card-text
            class="hoverObject black--text grey lighten-4" v-if="hoverObject">
            Click exact at all missing objects before adding to LabelMask.
          </v-card-text>
          <label class="pl-3 pt-2">Reset #{{this.imageRef_num}}</label>
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
          <Titels
            v-if="allProperties.currentLevel"
            :currentLevel="allProperties.currentLevel"
          >
          </Titels>
            <v-card-text class="pa-1 infoEdge black--text grey lighten-4"
              v-if="allProperties.currentLevel === 1 && imageRef_num === 2">
              <v-icon> mdi-arrow-collapse-up </v-icon><br/>
              Example for cell too <br/>close at image edge
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
          <div id="contextMenu" class="context-menu text-center"
            style="z-index: 999">
            <ul id="label">
              <li
                value="Cell"
                @click="colorSelect('Single Cell')"
                @contextmenu="colorSelect('Single Cell')"
              >
                Single Cell
              </li>
              <li
                v-if="allProperties.currentLevel !== 1"
                value="Aggregates"
                @click="colorSelect('Aggregate')"
                @contextmenu="colorSelect('Aggregate')"
              >
                Aggregate
              </li>
              <li
                v-if="allProperties.currentLevel !== 1"
                value="Platelet"
                @click="colorSelect('Platelet')"
                @contextmenu="colorSelect('Platelet')"
              >
                Platelet
              </li>
              <!--<li
                v-if="allProperties.currentLevel !== 1"
                value="background"
                @click="colorSelect('#ff66ff')"
              >
                Background
              </li>-->
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
            <!-- v-if="disabled_modi" color='warning'>-->
            <v-col>
              <v-btn
                v-if="disabled_modi || disabled_measurement"
                @click="
                  disableButton('previous');
                  previousImage();
                "
                class="ml-3"
                color="warning"
                disabled
                >previous image</v-btn
              >
              <!--<v-btn
                v-else-if="disabled_modi_region"
                @click="
                  disableButton('previous');
                  previousImage();
                "
                class="ml-3"
                dark
                :disabled="disabled_prev"
                :loading="loading_prev"
                color="purple"
                >previous image</v-btn
              >-->
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
              <!--<v-btn
                v-else-if="disabled_measurement"
                @click="undo()"
                dark
                color="purple"
                :disabled="disabled_undo"
              >
                <v-icon left>mdi-step-backward</v-icon>undo</v-btn
              >-->
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
              <!--<v-btn
                v-else-if="disabled_modi_region"
                @click="
                  disableButton('next');
                  checkLabels('');
                "
                dark
                color="purple"
                class="mr-0"
                :disabled="disabled_next"
                :loading="loading_next"
                >next image</v-btn
              >
              <v-btn
                v-else-if="disabled_measurement"
                color="purple"
                class="mr-0"
                disabled
                >next image</v-btn
              >-->
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
          <section>
            <transition name="bounce">
              <img
                v-if="bounce"
                alt="flash"
                :src="require(`../assets/${animation}`)"
                width="100"
                class="center"
              />
            </transition>
            <transition name="roll">
              <img
                v-if="roll"
                alt="Star"
                :src="require(`../assets/${animation}`)"
                width="100"
                class="center"
              />
            </transition>
          </section>
          <!--preview starts here-->
          <!--<div class='SegMaskDIV' v-if="allProperties.labelingApproach === 'basic'">
                <canvas ref='canvasSegMask' class='SegMask' id='SegMask'
                width='192' height='144'></canvas>
                <v-img
                id='SegMask_id'
                class='SegMaskImage'
                width='192'
                height='144'
                alt='waiting'
              >
              <RenderImage v-if="SegMask"
                :image="SegMask"
                :minCropVal="preprocessArgsInUseMask.cropMin"
                :maxCropVal="preprocessArgsInUseMask.cropMax"
                :invertBackground="preprocessArgsInUseMask.invertBackground"
                :colormap="preprocessArgsInUseMask.colormap"
                :opacity="preprocessArgsInUseMask.opacity"
                />
              </v-img>
              </div>
              <div class = 'SegMaskTitle' v-if="allProperties.labelingApproach === 'basic'">
              <v-card-text class=text-center>
                Segmentation Mask <br/>
              </v-card-text>
              </div>-->
          <!-- for game -->
          <v-col cols="12" v-if="allProperties.labelingApproach === 'game'">
            <v-card dense elevation="10" width="180" class="scores">
              <v-card-text class="text-center">
                <b class="teal--text" style="font-size: 1.5em">
                  {{ allProperties.UserID }}</b
                >
                <br />
                <v-divider class="mx-4"></v-divider>
                <b
                  >Image {{ this.imageRef_num }} /
                  {{
                    allProperties.numberImagesLevel[
                      this.allProperties.currentLevel - 1
                    ]
                  }}</b
                >
                <br />Time: <b>{{ this.seconds }} seconds</b><br />
                Your Points: <br />
                <b class="display-3 font-weight-bold teal--text">
                  {{ allProperties.points }}</b
                ><br />
                Overall:
                <b class="font-weight-bold teal--text">
                  {{ allProperties.points + allProperties.allPoints }}</b
                >
                <br />
                <div v-if="allProperties.currentLevel !== 5">
                completeness: <b> {{ this.currentAccuracy }}%</b>
                <br />
                correctness: <b> {{ this.currentAccuracy_correct }}%</b>
                <br />
                </div>
                <v-divider class="mx-4"></v-divider>
                <br />
                <b>Highscore:</b><br />
                <b class="font-weight-bold purple--text">
                  for current Level: {{ highscore_level - 20}} </b
                ><br />
                <b class="font-weight-bold purple--text">
                  Overall: {{ highscore }}
                </b>
              </v-card-text>
            </v-card>
            <HelpSection :currentLevel="allProperties.currentLevel" />
          </v-col>
        </div>
      </v-row>
      <v-row
        v-if="bounce_nextLevel === true"
        class="nextLevel"
        align="center"
        justify="center"
        @click="
          updateComponent('next');
          checkLabels('last');
          getDataLevel(allProperties.currentLevel + 1);
          // resetParam();
          bounce_nextLevel = false;
        "
      >
        <NextLevel
          :bounce="nextLevelprops.bounce"
          :animation="nextLevelprops.animation"
          :points="allProperties.points"
          :maxPoints="nextLevelprops.maxPoints"
          :accuracy="nextLevelprops.accuracyForScoring"
          :accuracy_correct="nextLevelprops.accuracyForScoring_correct"
          :currentLevel="allProperties.currentLevel"
        />
      </v-row>
      <!-- goal keeping -->
      <v-row v-if="(allProperties.allPoints + allProperties.points) >= 1700">
            <div class='text-center help'>
              <v-dialog v-model='dialog_1700' width='500'>
                <v-card>
                  <v-app-bar
                    dark
                    color="teal"
                  >
                    <v-toolbar-title>1700 Points!!!</v-toolbar-title>
                    <v-spacer></v-spacer>
                  </v-app-bar>
                  <v-card>
                    <div class="d-flex flex-no-wrap justify-space-between">
                      <div>
                        <br/>
                        <v-card-text class="acc text-center" style="font-size:1.7em">
                        You achieved 1700 points! <br/><br/>Do more to get more!!!
                        </v-card-text>
                        <v-card-text class="acc text-center" style="font-size:0.7em">
                        or stop the Game  </v-card-text>
                      </div>
                      <v-avatar
                        class="ma-3"
                        size="125"
                        tile
                      >
                        <v-img :src='require(`../assets/coin.jpg`)'></v-img>
                      </v-avatar>
                    </div>
                  </v-card>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color='primary' text @click="dialog_1700 = false">Close</v-btn>
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
        <v-icon left>mdi-emoticon-sad</v-icon>Stop Game
      </v-btn>
    </div>
  </v-row>
  <!--</div>-->
</template>

<script>
import { HTTP } from '@/http.common';
import RenderImage from '@/components/RenderImage.vue';
import NextLevel from '@/components/NextLevel.vue';
import Titels from '@/components/Titels.vue';
import HelpSection from '@/components/HelpSection.vue';

export default {
  name: 'LabelingInitialize',
  props: ['allProperties'],
  components: {
    RenderImage,
    NextLevel,
    Titels,
    HelpSection,
  },

  data: () => ({
    // for saving images from server
    newImage: null,
    newImageMask: null,
    newImages: [],
    newImageMasks: [],
    image_update: 0,
    SegMaskImage: null,
    SegMask: null,
    SegMaskNumber: '__',
    SegMaskAll: [],
    // display images
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
    // for buttons
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
    // save labeled datat (x,y,label)
    regionData: '',
    labelAreas: [],
    labelAreasAll: [],
    labelAreasRegion: [],
    labelAreasRegionAll: [],
    lastLabeledElement: [],
    newAreas: [],
    newAreasAll: [],
    cellData: '',
    label: '',
    label_region: '',
    color: '',
    text_button: '',
    dialog_1700: false,
    once1700: true,
    // for changing views
    elementMainOrg: null,
    elementMainMask: null,
    optionStatus: 'transparent',
    upStatus: 'org',
    downStatus: 'mask',
    // change Tool
    labelSingle: true,
    labelRegion: false,
    elevToolSing: 10,
    elevToolReg: 2,
    colorSing: 'purple',
    colorReg: 'purple lighten-4',
    empty: false,
    // change modi
    disabled_modi: false,
    disabled_modi_region: false,
    disabled_measurement: false,
    disabled_org: true,
    disabled_mask: true,
    // time tracking
    seconds: 0,
    isRunning: false,
    interval: null,
    // for image intenstiy
    min: 100,
    max: 255,
    slider: 255,
    clicks: 0,
    // hover info
    hoverObject: false,
    hoverArea: false,
    hoverSingle: false,
    // game, here comparing data later
    numberCells: 0,
    numberRegions: 0,
    addedAreas: 0,
    minusPoints: 0,
    highscore: '__',
    highscore_level: '__',
    bounce: false,
    roll: false,
    animated: false,
    animation: 'Star',
    bounce_nextLevel: false,
    // Game parameter
    nextLevelprops: {
      bounce: true,
      animation: 'StarSpecial',
      maxPoints: 100,
      text: '',
      accuracyForScoring: 0,
      accuracyForScoring_correct: 0,
    },
    accuracyTotal: [],
    currentAccuracy: '_',
    currentAccuracy_correct: '_',
    // contextmenu, clicks cjange later with modes
    display_contextmenuRegion: false,
    rightClick: false,
    display_contextmenu: false,
  }),
  methods: {
    updateComponent(event) {
      this.$emit('updateComponent', event);
      if (event !== 'review') {
        this.$emit('updatePoints', 0);
      }
    },
    updatePoints() {
      const points = this.numberCells * 10
        + this.numberRegions * 30
        + this.addedAreas * 50
        - this.minusPoints;
      this.$emit('updatePoints', points);
      if (this.allProperties.allPoints + this.allProperties.points >= 1700
      && this.once1700 === true) {
        this.dialog_1700 = true;
        this.once1700 = false;
      }
    },
    switchImage(toImage) {
      this.imageRef = toImage;
      this.selectedRectangle = -1;
      this.redrawContentCell();
    },
    // computedPath() {
    //   return require('@/assets/test_sample2.png'); // ${this.justForTest}.png');;
    // },
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
      // this.uploadData();
      this.accuracyTotal[this.imageRef_num - 1] = [0, 0, 0];
      this.currentAccuracy = Math.round(
        this.accuracyTotal[this.imageRef_num - 1][0] * 100,
      );
      this.currentAccuracy_correct = Math.round(
        this.accuracyTotal[this.imageRef_num - 1][2] * 100,
      );
      this.numberRegions = 0;
      this.numberCells = 0;
      this.minusPoints = 0;
      this.updatePoints();
      this.SegMask = null;
      this.empty = false;
      this.disabled_modi = false;
      this.selectTool('labelSingle');
    },
    selectCell(e) {
      this.roll = false;
      this.bounce = false;
      this.text_button = '';
      if (e.button === 2) {
        // Block right-click menu thru preventing default action.
        e.preventDefault();
      }
      const rect = this.canvas.getBoundingClientRect();
      this.startX = e.clientX - rect.left;
      this.startY = e.clientY - rect.top;
      /* = x;
      this.startY = y; */
      if (this.disabled_modi && !this.disabled_measurement) {
        this.NewContent();
      } else if (this.disabled_measurement) {
        this.MeasureCell(e);
      } else if (this.labelSingle) {
        this.showContextMenu(this.startX, this.startY);
      }
      this.isDrawing = false;
    },
    showContextMenu(x, y) {
      document
        .getElementById('label')
        .removeEventListener('click', this.getRegionLabel);
      document.getElementById('contextMenu').style.display = 'inline';
      document.getElementById('contextMenu').style.left = `${x}px`;
      document.getElementById('contextMenu').style.top = `${y + 49}px`;
      document
        .getElementById('label')
        .addEventListener('click', this.getCellLabel);
      document.body
        .addEventListener('click', this.hideContextMenu, true);
      // document.body.addEventListener('click', this.hideContextMenu, true);

      return false;
    },
    getCellLabel(event) {
      if (this.startX !== '') {
        this.hideContextMenu();
        this.display_contextmenu = false;
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
        console.log('label: ');
        console.log(this.label);
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
        // this.numberCells = this.numberCells + 1;
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
      // this.context.arc(this.startX, this.startY, 2, 0, 2 * Math.PI);
      this.context.strokeStyle = this.color;
      this.context.lineWidth = 3;
      this.context.stroke();
      this.checkLabels('during');
    },
    startRectRegion(e) {
      this.roll = false;
      this.bounce = false;
      this.text_button = '';
      if (e.button === 2) {
        // Block right-click menu thru preventing default action.
        e.preventDefault();
      }
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
        this.showContextMenuRegion(
          this.rectBefore[0][0] + this.rectBefore[1] + 2,
          this.rectBefore[0][1] + this.rectBefore[2],
        );
      }
      // extShowCont = true;
    },
    selectRegion(e) {
      // const rect = this.canvas.getBoundingClientRect();
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
        // ctx.lineTo(x, y, 6);
        this.context.lineWidth = 2;
        this.context.strokeStyle = 'white';
        this.context.stroke();
      }
      this.rectBefore = [this.init_rect, this.width_region, this.height_region];
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
    },
    getRegionLabel(event) {
      console.log('in get Region Label');
      // schlechtes if think about
      // if you save it in variables. check for example with init_rec
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
        this.lastLabeledElement.push('region');
        console.log(`push last element ${this.lastLabeledElement}`);
        this.lastLabeledElementAll[
          this.imageRef_num - 1
        ] = this.lastLabeledElement;
        this.redrawContentRegion('region');
        this.init_rect = '';
        this.width_region = '';
        this.height_region = '';
        // this.numberRegions = this.numberRegions + 1;
      }
    },
    redrawContentRegion() {
      // const x = this.startX;
      // const y = this.startY;
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
      // ctx.lineTo(x, y, 6);
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
    /* listenKeys(e) {
      const keyCode = e.which || e.keyCode;
      if (keyCode === 27) {
        this.hideContextMenu();
        this.bounce = false;
        this.roll = false;
        this.animated = false;
      }
    }, */
    // for add Regions
    NewContent() {
      this.newXY = [this.startX, this.startY];
      this.newAreas.push(this.newXY);
      this.newAreasAll[this.imageRef_num - 1] = this.newAreas;
      // this.newAreas.push(this.newXY);
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
          this.context.moveTo(this.startX, this.startY - 3);
          this.context.lineTo(this.startX - 4, this.startY + 4);
          this.context.lineTo(this.startX + 4, this.startY + 4);
          this.context.closePath();
          this.context.strokeStyle = 'orange';
          this.context.lineWidth = 3;
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
      ) {
        console.log('no new data - next image if not last');
        // adoption: there werde cells but user did not label
        // ( here we can do that, because we know solution and just look at images with cells)
        if (this.accuracyTotal[this.imageRef_num - 1] === undefined) {
          console.log('set accuracy to zero');
          this.accuracyTotal[this.imageRef_num - 1] = [0, 0, 0];
          // this.currentAccuracy = 0;
        }
        if (section !== 'last') {
          this.nextImage();
        }
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
        this.disabled_measurement = false;
      } else {
        console.log('error in checkLabels');
      }
    },
    // upload labels
    uploadData(section) {
      console.log('uploadData start Level');
      let number = this.imageRef_num;
      if (this.allProperties.currentLevel === 5) {
        number += 10;
      }
      console.log(number);
      if (this.labelAreas.length === 0) {
        this.labelAreas = 'none';
      }
      if (this.labelAreasRegion.length === 0) {
        this.labelAreasRegion = 'none';
      }
      console.log(this.labelAreas);
      this.labelAreas = String(this.labelAreas);
      console.log(this.labelAreas);
      this.labelAreasRegion = String(this.labelAreasRegion);
      const length = this.lastLabeledElementAll[this.imageRef_num - 1].length;
      const lastEle = this.lastLabeledElementAll[this.imageRef_num - 1][length - 1];
      console.log(lastEle);
      HTTP.post(
        `label_level/${this.labelAreas}/${this.labelAreasRegion}/${lastEle}/${number}/${this.allProperties.UserID}/${this.allProperties.dataset_typ}/${this.allProperties.currentLevel}/${this.allProperties.labelingApproach}`,
      )
        .then(async (response) => {
          // this.newImage = response.data.image;
          console.log(
            `labels recieved and segMask calcualted for image ${response.data.image_num}.`,
          );
          console.log(response.data.accuracy);
          this.accuracyTotal[response.data.image_num - 1] = response.data.accuracy;
          this.currentAccuracy = Math.round(
            this.accuracyTotal[response.data.image_num - 1][0] * 100,
          );
          this.currentAccuracy_correct = Math.round(
            this.accuracyTotal[response.data.image_num - 1][2] * 100,
          );
          if (response.data.wrong_label === true) {
            this.animation = 'sad.png';
            // this.playSound('Sad_Trombone.mp3');
            this.bounce = true;
            this.minusPoints = this.minusPoints + 5;
          }
          // setTimeout(this.bounce = false, 1000);
          if (response.data.wrong_label === false) {
            this.animation = 'coin.jpg';
            // this.playSound('poker-chips.mp3');
            // myTrack.play();
            // console.log(myTrack.state());
            this.roll = true;
            if (this.labelAreas !== 'none') {
              this.numberCells = this.numberCells + 1;
            }
            if (this.labelAreasRegion !== 'none') {
              this.numberRegions = this.numberRegions + 1;
            }
            // setTimeout(this.bounce = false, 10000);
          }
          this.updatePoints();
          this.labelAreas = [];
          this.labelAreasRegion = [];
        })
        .catch((e) => {
          console.warn(e);
          this.labelAreas = [];
          this.labelAreasRegion = [];
          this.undo('fail');
          this.text_button = 'last label failed, label again';
          // this.trainingErrorFlag = true;
          // this.imageLoadingErrorFlag = false;
        });
      if (section === ('next_image' || 'during')) {
        console.log(section);
        console.log('uploaded data next image');
        this.nextImage();
      }

      return 'Complete';
    },
    // for updated LabelMask
    uploadNewData() {
      console.log('uploadnewData start');
      this.newImageMask = null;
      this.newAreas = String(this.newAreas);
      let number = this.imageRef_num;
      if (this.allProperties.currentLevel === 5) {
        number += 10;
      }
      HTTP.post(
        `newAreas/${this.newAreas}/${number}/${this.allProperties.UserID}/${this.allProperties.dataset_typ}/${this.allProperties.currentLevel}`,
      )
        .then(async (response) => {
          // this.newImage = response.data.image;
          this.newImageMasks[this.image_section][this.image_update] = response.data.New_label_mask;
          this.newImageMask = response.data.New_label_mask;
          console.log('Received: new LabelMask');
          this.disabled_next = false;
          this.loading_next = false;
          this.disabled_prev = false;
          this.loading_prev = false;
          this.disabled_modi = false;
          this.disabled_measurement = false;
          if (this.labelSingle) {
            const tool = 'labelSingle';
            this.selectTool(tool);
          } else {
            const tool = 'labelRegion';
            this.selectTool(tool);
          }
          this.text_button = '';
          this.newAreas = [];
          this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
          this.redrawOldContent(true);
          this.updatePoints();
        })
        .catch((e) => {
          console.warn(e);
          // this.trainingErrorFlag = true;
          // this.imageLoadingErrorFlag = false;
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
      // this.SegMask = null;
      // document.getElementById('image-mask').style.display = 'none';
      const number = this.allProperties.numberImagesLevel[
        this.allProperties.currentLevel - 1
      ];
      if (this.imageRef_num < number) {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.imageRef_num = this.imageRef_num + 1;
        if (
          this.labelAreasAll[this.imageRef_num - 1] !== 0
          || this.labelAreasRegionAll[this.imageRef_num - 1] !== 0
        ) {
          // this.SegMask = this.SegMaskAll[this.imageRef_num - 1];
          this.redrawOldContent(false);
        }
        this.imageRef = this.imageRef_num.toString();
        while (this.imageRef.length < 5) {
          this.imageRef = `0${this.imageRef}`;
        }
        this.currentAccuracy = '_';
        this.currentAccuracy_correct = '_';
        this.updateImages();
      } else {
        this.updateScores();
      }
    },
    previousImage() {
      // deltet circles
      console.log('previous Image');
      this.SegMask = null;
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
      if (this.imageRef_num > 1) {
        this.imageRef_num = this.imageRef_num - 1;
        if (this.imageRef_num % 10 === 0) {
          // console.log(`getData for next section : ${this.image_section}`);
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
        // this.image_update = this.image_update - 1;
        this.updateImages();
      } else {
        this.text_button = 'no previous image';
      }
    },
    // new Images at label area
    updateImages() {
      this.newImage = this.newImages[this.imageRef_num - 1];
      this.newImageMask = this.newImageMasks[this.imageRef_num - 1];
      this.disabled_next = false;
      this.loading_next = false;
      this.disabled_prev = false;
      this.loading_prev = false;
      this.text_button = '';
    },
    // after each 10 images get new 10 images from backend
    getDataLevel(level) {
      if (level <= 5) {
        this.disableButton('all');
        console.log('get 10 images for level: ');
        console.log(level);
        // let celltyp = '';
        this.newImage = null;
        this.newImageMask = null;
        // const level = 1;
        HTTP.post(
          `getDataLevel/${this.allProperties.UserID}/${this.allProperties.labelingApproach}/${this.allProperties.dataset_typ}/${level}`,
        )
          .then(async (response) => {
            this.highscore = response.data.highscore[0];
            this.highscore_level = response.data.highscore[1];
            console.log(this.highscore_level);
            this.newImages = response.data.images;
            this.newImageMasks = response.data.label_masks;
            // console.log(this.newImages);
            // console.log(this.newImageMasks);
            // celltyp = response.data.celltyp;
            console.log('Recieved Level');
            // this.highscore = response.data.highscore;
            console.log('Start Timer');
            this.toggleTimer();
            this.newImage = this.newImages[0];
            this.newImageMask = this.newImageMasks[0];
            // console.log(this.newImage);
            // console.log(this.newImageMask);
            this.disabled_next = false;
            this.loading_next = false;
            this.disabled_prev = false;
            this.loading_prev = false;
            this.disabled_undo = false;
            this.text_button = '';
            // this.getCelltyp(celltyp);
          })
          .catch((e) => {
            console.warn(e);
          });
        return 'Complete';
      }
      return 'Complete';
    },
    // undo last selected element by user
    /* undo() {
      console.log('undo last element');
      if (!this.disabled_modi && !this.disabled_measurement) {
        if (
          this.lastLabeledElement[this.lastLabeledElement.length - 1] === 'cell'
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
          this.lastLabeledElement.pop();
          this.labelAreasAll[this.imageRef_num - 1] = currentData; // .length - 1] = 0;
          this.numberCells = this.numberCells - 1;
        } else if (
          this.lastLabeledElement[this.lastLabeledElement.length - 1] === 'region') {
          const currentData = this.labelAreasRegionAll[this.imageRef_num - 1];
          const lastElement = currentData[currentData.length - 1];
          this.context.clearRect(
            lastElement[0][0] - 2,
            lastElement[0][1] - 2,
            lastElement[1] + 4,
            lastElement[2] + 4,
          );
          currentData.pop();
          this.lastLabeledElement.pop();
          this.labelAreasRegionAll[this.imageRef_num - 1] = currentData;
          this.numberRegions = this.numberRegions - 1;
        } else {
          console.log('no elements');
        }
      } else if (this.disabled_measurement) {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.redrawOldContent();
      } else {
        const currentData = this.newAreasAll[this.imageRef_num - 1];
        if (currentData.length !== 0) {
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
        }
      }
      if (this.labelAreasAll[this.imageRef_num - 1] !== 0) {
        this.labelAreas = this.labelAreasAll[this.imageRef_num - 1];
      }
      if (this.labelAreasRegionAll[this.imageRef_num - 1] !== 0) {
        this.labelAreasRegion = this.labelAreasRegionAll[
          this.imageRef_num - 1
        ];
      }
      this.uploadData();
    }, */
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
          this.updatePoints();
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
          this.updatePoints();
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
          this.updatePoints();
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
      if (all !== 'all' && all !== 'fail') {
        console.log('uploaddata in undo');
        this.uploadData();
      }
    },
    // measure distance between two clicked points
    /* MeasureCell() {
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
    // timeout otherwise varaibles were not updated!?
    options(selectedOption) {
      // timeout: take few secs to update varaibles for switches
      setTimeout(this.changeModi, 100, selectedOption);
    },
    // timer for session
    toggleTimer() {
      if (this.isRunning) {
        clearInterval(this.interval);
        console.log('timer starts again');
        this.interval = setInterval(this.incrementTime, 1000);
      } else {
        this.interval = setInterval(this.incrementTime, 1000);
      }
      this.isRunning = !this.isRunning;
    },
    incrementTime() {
      this.seconds = parseInt(this.seconds, 10) + 1;
    },
    updateScores(all, review) {
      console.log('in updateScores');
      const wrongAreas = this.minusPoints / 5;
      this.accuracyTotal = String(this.accuracyTotal);
      let path = '';
      if (
        this.allProperties.currentLevel === 4
        || this.allProperties.currentLevel === 5
      ) {
        // this.imageRef_num = this.imageRef_num - 1;
        console.log('in get path');
        path = `getAccuracy/${this.allProperties.labelingApproach}/${this.allProperties.UserID}/${this.allProperties.dataset_typ}/${this.allProperties.currentLevel}/${this.imageRef_num}`;
      } else {
        path = `getAccuracy_level/${this.allProperties.currentLevel}/${this.imageRef_num}/${this.accuracyTotal}`;
      }
      HTTP.post(path)
        .then(async (response) => {
          console.log(response.data.accuracy_all);
          this.nextLevelprops.accuracyForScoring = response.data.accuracy_all[0];
          this.nextLevelprops.accuracyForScoring_correct = response.data.accuracy_all[2];
          console.log('accuracy revieved');
          console.log(response.data.accuracy_all);
          this.$emit('updateAccuracy', response.data.accuracy_all);
          let points = this.allProperties.points;
          if (this.nextLevelprops.accuracyForScoring >= 0.85) {
            points += 20;
            this.$emit('updatePoints', points);
          }
          const Scores = [
            this.imageRef_num,
            this.numberCells,
            this.numberRegions,
            wrongAreas,
            this.addedAreas,
            this.seconds,
            points,
            response.data.accuracy_all,
            this.allProperties.currentLevel,
          ];
          this.$emit('updateScores', Scores);
          if (review === 'review') {
            this.updateComponent('review');
          }
          this.bounce_nextLevel = true;
          // this.numberCells = 0;
          // this.numberRegions = 0;
          // points = 0;
          // this.seconds = 0;
        })
        .catch((e) => {
          console.warn(e);
        });
      return 'Complete';
    },
  },
  mounted() {
    // true to get an empty folder for starting labeling process at the backend side
    this.getDataLevel(this.allProperties.currentLevel);
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
    // deactivated in level 1
    // this.canvas.addEventListener('contextmenu', this.startRectRegion);
    // this.canvas.addEventListener('mouseup', this.MouseupRegion);
    // this.canvas.addEventListener('mousemove', this.selectRegion);
    this.elementMainOrg = document.getElementById('image-mask_org');
    this.elementMainMask = document.getElementById('image-mask_water');
    this.elementMainOrg.style.opacity = '0.5';
    this.elementMainMask.style.opacity = '1';
    // document.getElementById('contextMenu').style.display = 'none';
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
  top: 62px;
  left: 913px;
  text-justify: right;
  position: relative;
}
.nav-arrow-back {
  top: 570px;
  left: 3px;
  text-justify: right;
  position: relative;
  z-index: 500;
}
.main {
  border: 0px solid black;
  height: 480px;
  min-width: 1150px;
  padding-left: 50px;
  padding-top: 15px;
  text-justify: center;
}
.canvas-wrapper {
  border: 0px solid black;
  height: 100%;
  width: 115%;
  padding-right: 252px;
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
  bottom: 5px;
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
  top: 440px;
  height: 90px;
  width: 190px;
  opacity: 0.8;
}
.infoEdge {
  position: absolute;
  z-index:100;
  opacity: 0.8;
  width: 135px;
  bottom: 305px;
  left: 14px;
}
.save-button-id {
  margin-left: 5px;
}
.canvas {
  height: 100%;
  width: '384';
  left: 7px;
  top: 15px;
  display: inline-block;
  z-index: 4;
  position: relative;
}
.level {
  height: 20px;
  padding-bottom: 50px;
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
  bottom: 20px;
  left: 8px;
  position: relative;
}
.SegMaskDIV {
  height: 0%;
  top: 8px;
  display: inline-block;
  /*right: 100px;*/
  position: relative;
}
.SegMask {
  border: 1px solid #000000;
  cursor: move;
  z-index: 1;
  position: relative;
  top: 20px;
}
.SegMaskImage {
  position: absolute;
  z-index: 0;
  right: 0px;
  top: 20px;
}
.SegMaskTitle {
  top: 15px;
  position: relative;
}
.covered {
  position: absolute;
  z-index: 0;
  top: 50px;
  left: 0px;
}
.covered_transparent {
  position: absolute;
  z-index: 1;
  top: 50px;
  left: 0px;
}
.scores {
  position: relative;
  z-index: 1;
  top: 0px;
}
section {
  min-height: 100px;
  text-align: center;
  text-justify: center;
  z-index: 50;
}
.bounce-enter-active {
  animation: bounce-in 0.7s;
}
/* .bounce-leave-active {
  animation: bounce-in .5s reverse;
} */
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.5);
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
/* section_nextLevel {
  min-height: 100px;
  text-align: center;
  z-index: 50;
}
.bounce-enter-active {
  animation: bounce-in .5s;
}
/* .bounce-leave-active {
  animation: bounce-in .5s reverse;
}
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
} */
</style>
