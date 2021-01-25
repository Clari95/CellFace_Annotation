<template>
  <!--<div class='wrapper'>-->
    <v-row fill-width>
      <div class='nav-arrow-back'  id='back-button'  v-if="bounce_nextLevel === false">
            <v-btn small @click="updateComponent('back')" color='primary' class='mr-4'>
            <v-icon left>mdi-arrow-left-circle</v-icon>back
            </v-btn>
      </div>
      <!--- Main component starts here --->
      <v-col class='mx-auto mt-0 main'>
          <v-row class='canvas-wrapper' v-if="bounce_nextLevel === false">
            <div class='options'  style="width: 170px">
              <v-subheader class="pl-3"
              style="font-size:1.2em">
                <b>Image view:</b></v-subheader>
              <input  class="checkboxColormap" type="checkbox"
                id="checkbox" v-model="colormap" @click="options('colormap')">
              <label class="pl-3"> Colormap</label>
              <v-switch v-model="disabled_org" class="ma-2"
              label="OrgImage" color='teal' @click="options('up')"></v-switch>
              <v-slider
                      v-model="slider"
                      class="slider"
                      :max="max"
                      :min="min"
                      :disabled="!disabled_org"
                      @click="options('slider')"
                      thumb-label="always"
                      :thumb-size="24"
                    >
                    </v-slider>
              <v-switch v-model="disabled_mask" class="ma-2"
              label="LabelMask" color='teal' @click="options('down')"></v-switch>
              <!--modis.-->
              <v-divider
                class="mx-4"
              ></v-divider>
              <!--<v-subheader class="pl-3" style="font-size:1.2em"><b>Modi:</b></v-subheader>
              <v-switch v-model="disabled_modi" class="ma-2"
              label="Add Regions" color='warning' @click="options('modi1')"></v-switch>-->
              <!--<v-switch v-model="disabled_measurement" class="ma-2"
              label ="Measure Distance"
              color='purple' @click="options('measurement')">
              </v-switch>-->
            </div>
            <div class='canvas'>
              <v-subheader class="pl-3 level"
              style="font-size:1.2em">
                <b class="teal--text">Level 2: New feature! <br/>
                  <p style="font-size:0.8em">You can drag whole bounding boxes around areas
                  with right click! <br/> To select the category,
                  click also with the right mouse button!</p>
                  <p style="font-size:0.7em">(If you are not sure, assign it to Other)</p></b>
              </v-subheader>
              <canvas ref='canvas' id='rectangleDraw'
              width='512' height='384' class='covering'></canvas>
              <v-img
                id='image-mask_water'
                class='covered'
                width='512'
                height='384'
                alt
              >
              <RenderImage v-if="newImageMask"
                :image="newImageMask"
                :minCropVal="preprocessArgsInUseMask.cropMin"
                :maxCropVal="preprocessArgsInUseMask.cropMax"
                :invertBackground="preprocessArgsInUseMask.invertBackground"
                :colormap="preprocessArgsInUseMask.colormap"
                :opacity="preprocessArgsInUseMask.opacity"
                />
              </v-img>
              <v-img
                id='image-mask_org'
                class='covered_transparent'
                width='512'
                height='384'
                alt='waiting'>
                <RenderImage v-if="newImage"
                :image="newImage"
                :minCropVal="preprocessArgsInUse.cropMin"
                :maxCropVal="preprocessArgsInUse.cropMax"
                :invertBackground="preprocessArgsInUse.invertBackground"
                :colormap="preprocessArgsInUse.colormap"
                :opacity="preprocessArgsInUse.opacity"
                />
              </v-img>
              <!--:src='require(`../assets/example_images/Mono_${this.imageRef}.png`)'-->
              <div id='contextMenu' class='context-menu text-center'>
                <ul id='label'>
                  <li value='Cell' @click="colorSelect('red')"
                  @contextmenu="colorSelect('red')">Single Cell</li>
                  <li value='Aggregates' @click="colorSelect('orange')"
                  @contextmenu="colorSelect('orange')">Aggregate</li>
                  <li value='Platelet' @click="colorSelect('#66ff33')"
                  @contextmenu="colorSelect('#66ff33')">Platelet</li>
                   <!--<li value='background' @click="colorSelect('#ff66ff')">Background</li>-->
                  <li class='separator'></li>
                  <li value='Other' @click="colorSelect('blue')"
                  @contextmenu="colorSelect('blue')">Other</li>
                </ul>
              </div>
              <v-row class='mainfunctions'> <!-- v-if="disabled_modi" color='warning'>-->
                <v-col>
                <v-btn
                v-if="disabled_modi || disabled_measurement"
                  @click="disableButton('previous'); previousImage()"
                  class= 'ml-3'
                  color='warning'
                  disabled
                >previous image</v-btn>
                <v-btn
                  v-else-if="disabled_modi_region"
                  @click="disableButton('previous'); previousImage()"
                  class= 'ml-3'
                  dark
                  :disabled='disabled_prev'
                  :loading='loading_prev'
                  color='purple'
                >previous image</v-btn>
                <v-btn
                  v-else
                  @click="disableButton('previous'); previousImage()"
                  class= 'ml-3'
                  dark
                  :disabled='disabled_prev'
                  :loading='loading_prev'
                  color='teal'
                >previous image</v-btn>
                </v-col>
                <v-col>
                  <v-btn v-if="disabled_modi"
                  @click="undo()"
                  color='warning'
                  >
                    <v-icon left>mdi-step-backward</v-icon>undo</v-btn>
                  <v-btn v-else-if="disabled_measurement"
                  @click="undo()"
                  dark color='purple'
                  :disabled='disabled_undo'>
                    <v-icon left>mdi-step-backward</v-icon>undo</v-btn>
                  <v-btn v-else
                  @click="undo()" dark color='teal' :disabled='disabled_undo'
                  align-center justify-center>
                    <v-icon left>mdi-step-backward</v-icon>undo</v-btn>
                <div>
                  <p></p>
                 <p class='status_message'>{{this.text_button}}</p>
                </div>
                </v-col>
                <v-col>
                <v-btn
                  v-if="disabled_modi"
                  @click="disableButton('addtoMask'); checkLabels('')"
                  color='warning'
                  class= 'mr-0'
                  :disabled='disabled_next'
                  :loading='loading_next'
                >Add to mask</v-btn>
                <v-btn
                  v-else-if="disabled_modi_region"
                  @click="disableButton('next'); checkLabels('')"
                  dark
                  color='purple'
                  class= 'mr-0'
                  :disabled='disabled_next'
                  :loading='loading_next'
                >next image</v-btn>
                <v-btn
                  v-else-if="disabled_measurement"
                  color='purple'
                  class= 'mr-0'
                  disabled
                >next image</v-btn>
                <v-btn
                  v-else
                  @click="disableButton('next'); checkLabels('next_image');"
                  dark
                  color='teal'
                  class= 'mr-0'
                  :disabled='disabled_next'
                  :loading='loading_next'
                >next image</v-btn>
                </v-col>
                </v-row>
            </div>
            <div class='rightside'>
              <section>
                <transition name="bounce">
                  <img v-if="bounce" alt="flash"
                  :src='require(`../assets/${animation}`)'
                  width="100"
                  class="center"/>
                </transition>
                <transition name="roll">
                  <img v-if="roll" alt="Star"
                  :src='require(`../assets/${animation}`)'
                  width="100"
                  class="center"/>
                </transition>
              </section>
              <!-- for game -->
               <v-col cols="12" v-if="allProperties.labelingApproach === 'game'">
                <v-card dense elevation='10' width="180" class="scores">
                  <v-card-text class='text-center'>
                      <b class="teal--text" style="font-size:1.5em">
                        {{allProperties.UserID}}</b> <br/>
                      <v-divider
                        class="mx-4"
                      ></v-divider>
                      <b>Image {{this.imageRef_num}} / {{numberImagesLevel}}</b>
                      <!--<br/>
                      labeled cells: <b>{{numberCells}}</b> <br/>
                      labeled regions: <b>{{numberRegions}}</b> <br/>
                      added areas: <b>{{addedAreas}}</b> <br/>
                      wrong labels: <b>{{minusPoints / 5}}</b>-->
                      <br />Time:
                      <b>{{this.seconds}} seconds</b><br/>
                      Your Points: <br/>
                      <b class="display-3 font-weight-bold teal--text">
                        {{allProperties.points}}</b><br/>
                      Overall:
                      <b class="font-weight-bold teal--text">
                      {{allProperties.points + allProperties.allPoints}}</b>
                      <br/>
                      labeled areas: <b>
                        {{this.currentAccuracy}}%</b>
                      <br/>
                      correctness: <b>
                        {{this.currentAccuracy_correct}}%</b>
                      <br/>
                      <v-divider
                        class="mx-4"
                      ></v-divider>
                      <br/>
                      <b>Highscore:</b><br/>
                      <b class="font-weight-bold purple--text">
                        for Level 2: {{highscore_level}}
                      </b><br/>
                      <b class="font-weight-bold purple--text">
                        Overall: {{highscore}}
                      </b>
                  </v-card-text>
                </v-card>
                <HelpSection
                  :currentLevel="allProperties.currentLevel"
                />
                </v-col>
            </div>
          </v-row>
          <v-row v-if="bounce_nextLevel === true" class='nextLevel' align="center"
      justify="center" @click="updateComponent('next'); checkLabels('last');">
              <NextLevel
                :bounce="nextLevelprops.bounce"
                :animation="nextLevelprops.animation"
                :points="allProperties.points"
                :maxPoints="nextLevelprops.maxPoints"
                :text="nextLevelprops.text"
                :accuracy="nextLevelprops.accuracyForScoring"
                :accuracy_correct="nextLevelprops.accuracyForScoring_correct"
                />
          </v-row>
      </v-col>
      <!--- Main component ends here --->
     <div class='nav-arrow-next'>
            <v-btn small @click="checkLabels('last');
            updateScores(allProperties.labelingApproach, 'review')"
            color='primary'>
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
import HelpSection from '@/components/HelpSection.vue';
// import { Howl } from 'howler';

export default {
  name: 'LabelingInitialize',
  props: ['allProperties',
    'dataset'],
  components: {
    RenderImage,
    NextLevel,
    HelpSection,
  },

  data: () => ({
    num: 0,
    images: null,
    newImage: null,
    newImageMask: null,
    newImages: [],
    newImageMasks: [],
    // celltyp: '___',
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
    show: false,
    // disabled_save: false,
    loading_save: false,
    disabled_next: false,
    loading_next: false,
    disabled_prev: false,
    loading_prev: false,
    disabled_undo: false,
    canvas: null,
    canvas2: null,
    context: null,
    // labelingarea: '',
    finishButton: '',
    backButton: '',
    // contextMenu: null,
    button: null,
    imageRef: '00001',
    imageRef_num: 1,
    image_section: 0,
    currentX: '',
    currentY: '',
    startX: '',
    startY: '',
    x: '',
    y: '',
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
    regionLabel: false,
    newAreas: [],
    newAreasAll: [],
    cellData: '',
    label: '',
    label_region: '',
    check_result: 'None',
    color: '',
    mask: [],
    text: 'test',
    imageLink: '1_image_watershed.png', // ../assets/label_masks/1_image_watershed.png',
    startTime: '',
    text_button: '',
    /* user_id: '',
    UserID: 'testperson',
    rules: [v => !!v || 'Req', v => v.length <= 4 || 'Max 4 signs'],
    counterEn: false,
    counter: 0,
    missingUserID: '', */
    icons: {},
    dialog: false,
    elementMainOrg: null,
    elementMainMask: null,
    optionStatus: 'transparent',
    upStatus: 'org',
    downStatus: 'mask',
    seconds: 0,
    isRunning: false,
    interval: null,
    // for zoom
    translatePos: {
      x: 512 / 2,
      y: 384 / 2,
    },
    scale: 1.0,
    scaleMultiplier: 0.9,
    startDragOffset: {},
    mouseDown: false,
    lastX: 0,
    lastY: 0,
    scaleFactor: 1.1,
    xCanvas2: -256,
    yCanvas2: -192,
    // change modi
    disabled_modi: false,
    disabled_modi_region: false,
    disabled_measurement: false,
    disabled_org: true,
    disabled_mask: true,
    min: 0,
    max: 255,
    slider: 255,
    clicks: 0,
    // tutorial for checking precision
    tutorialFinished: false,
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
    // four images in this level could be 5
    numberImagesLevel: 4,
    nextLevelText: '',
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
    region: false,
    display_contextmenuRegion: false,
    rightClick: false,
    display_contextmenu: false,
  }),
  methods: {
    /* playSound(file) {
      const sound = new Howl({
        src: [file],
        volume: 0.15,
      });
      sound.play();
    }, */
    updateComponent(event) {
      this.$emit('updateComponent', event);
      this.$emit('updatePoints', 0);
    },
    switchImage(toImage) {
      this.imageRef = toImage;
      this.selectedRectangle = -1;
      this.redrawContentCell();
    },
    // computedPath() {
    //   return require('@/assets/test_sample2.png'); // ${this.justForTest}.png');;
    // },
    colorSelect(color) {
      this.color = color;
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
      } else if (this.display_contextmenu === false) {
        this.showContextMenu(this.startX, this.startY);
      } else {
        console.log('here in select Cell; display true');
        this.hideContextMenu();
        this.display_contextmenu = false;
        // document.body.addEventListener('click', this.hideContextMenu, true);
      }
      this.isDrawing = false;
    },
    showContextMenu(x, y) {
      this.display_contextmenu = true;
      document.getElementById('contextMenu').style.display = 'inline';
      document.getElementById('contextMenu').style.left = `${x}px`;
      document.getElementById('contextMenu').style.top = `${y + 49}px`;
      document.getElementById('label').addEventListener('click', this.getCellLabel);
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
          this.labelAreasRegion = this.labelAreasRegionAll[this.imageRef_num - 1];
        }
        this.label = event.target.innerHTML;
        this.cellData = [this.startX, this.startY, this.label];
        this.labelAreas.push(this.cellData);
        this.labelAreasAll[this.imageRef_num - 1] = this.labelAreas;
        this.lastLabeledElement.push('cell');
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
      this.rightClick = true;
      this.roll = false;
      this.bounce = false;
      if (e.button === 2) {
      // Block right-click menu thru preventing default action.
        e.preventDefault();
      }
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      this.firstClick = [x, y];
      this.isDrawing = true;
    },
    MouseupRegion() {
      this.isDrawing = false;
      if (this.rightClick === true) {
        this.showContextMenuRegion(this.rectBefore[0][0] + this.rectBefore[1] + 2,
          this.rectBefore[0][1] + this.rectBefore[2]);
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
        if (this.firstClick[0] < this.secondClick[0] && this.firstClick[1] < this.secondClick[1]) {
          this.init_rect = this.firstClick;
          this.width_region = this.secondClick[0] - this.firstClick[0];
          this.height_region = this.secondClick[1] - this.firstClick[1];
        }
        if (this.firstClick[0] > this.secondClick[0] && this.firstClick[1] > this.secondClick[1]) {
          this.init_rect = [this.secondClick[0], this.secondClick[1]];
          this.width_region = this.firstClick[0] - this.secondClick[0];
          this.height_region = this.firstClick[1] - this.secondClick[1];
        }
        if (this.firstClick[0] > this.secondClick[0] && this.firstClick[1] < this.secondClick[1]) {
          this.init_rect = [this.secondClick[0], this.firstClick[1]];
          this.width_region = this.firstClick[0] - this.secondClick[0];
          this.height_region = this.secondClick[1] - this.firstClick[1];
        }
        if (this.firstClick[0] < this.secondClick[0] && this.firstClick[1] > this.secondClick[1]) {
          this.init_rect = [this.firstClick[0], this.secondClick[1]];
          this.width_region = this.secondClick[0] - this.firstClick[0];
          this.height_region = this.firstClick[1] - this.secondClick[1];
        }
        this.context.clearRect(this.rectBefore[0][0] - 2, this.rectBefore[0][1] - 2,
          this.rectBefore[1] + 4, this.rectBefore[2] + 4);
        this.context.beginPath();
        this.context.rect(this.init_rect[0], this.init_rect[1],
          this.width_region, this.height_region);
        // ctx.lineTo(x, y, 6);
        this.context.lineWidth = 2;
        this.context.strokeStyle = 'black';
        this.context.stroke();
      }
      this.rectBefore = [this.init_rect, this.width_region, this.height_region];
    },
    showContextMenuRegion(x, y) {
      if (this.display_contextmenuRegion === false) {
        this.display_contextmenuRegion = true;
        // this.rightClick = false;
        document.getElementById('contextMenu').style.display = 'inline';
        document.getElementById('contextMenu').style.left = `${x}px`;
        document.getElementById('contextMenu').style.top = `${y + 49}px`;
        document.getElementById('label').addEventListener('contextmenu', this.getRegionLabel);
      } else {
        this.hideContextMenu();
        this.display_contextmenuRegion = false;
      }
      return false;
    },
    getRegionLabel(event) {
      // schlechtes if think about
      // if you save it in variables. check for example with init_rec
      if (this.init_rect !== '') {
        if (event.button === 2) {
        // Block right-click menu thru preventing default action.
          event.preventDefault();
        }
        this.hideContextMenu();
        this.display_contextmenuRegion = false;
        this.rightClick = false;
        // getting previous labeling, labelAreas/Region delted after sending data
        if (this.labelAreasRegionAll[this.imageRef_num - 1] !== 0) {
          this.labelAreasRegion = this.labelAreasRegionAll[this.imageRef_num - 1];
        }
        // getting previous labeling
        if (this.labelAreasAll[this.imageRef_num - 1] !== 0) {
          this.labelAreas = this.labelAreasAll[this.imageRef_num - 1];
        }
        this.label_region = event.target.innerHTML;
        this.regionData = [this.init_rect, this.width_region,
          this.height_region, this.label_region];
        this.labelAreasRegion.push(this.regionData);
        this.labelAreasRegionAll[this.imageRef_num - 1] = this.labelAreasRegion;
        this.redrawContentRegion('region');
        this.lastLabeledElement.push('region');
        this.init_rect = '';
        this.width_region = '';
        this.height_region = '';
        // this.numberRegions = this.numberRegions + 1;
      }
    },
    redrawContentRegion() {
      // const x = this.startX;
      // const y = this.startY;
      this.context.clearRect(this.init_rect[0] - 2, this.init_rect[1] - 2,
        this.width_region + 4, this.height_region + 4);
      this.context.beginPath();
      this.context.rect(this.init_rect[0], this.init_rect[1],
        this.width_region, this.height_region);
      // ctx.lineTo(x, y, 6);
      this.context.lineWidth = 2;
      this.context.strokeStyle = this.color;
      this.context.stroke();
      this.checkLabels('during');
    },
    hideContextMenu() {
      if (!document.getElementById('contextMenu')) {
        return;
      }
      document.getElementById('contextMenu').style.display = 'none';
      // return false;
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
      this.context.rect(this.startX - 20, this.startY - 20, 40, 40);
      this.context.strokeStyle = 'red';
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
        const currentDataRegion = this.labelAreasRegionAll[this.imageRef_num - 1];
        for (let i = 1; i <= currentData.length; i += 1) {
          const Label = currentData[i - 1];
          x = Label[0];
          y = Label[1];
          if (Label[2] === 'Single Cell') {
            this.color = 'red';
          } else if (Label[2] === 'Platelet') {
            this.color = '#66ff33';
          } else if (Label[2] === 'Aggregate') {
            this.color = 'orange';
          } else if (Label[2] === 'Background') {
            this.color = '#ff66ff';
          } else if (Label[2] === 'Other') {
            this.color = 'blue';
          }
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
          if (Label[3] === 'Single Cell') {
            this.color = 'red';
          } else if (Label[3] === 'Platelet') {
            this.color = '#66ff33';
          } else if (Label[3] === 'Aggregate') {
            this.color = 'orange';
          } else if (Label[3] === 'Background') {
            this.color = '#ff66ff';
          } else if (Label[3] === 'Other') {
            this.color = 'blue';
          }
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
      if ((Object.keys(this.labelAreas).length === 0)
      && Object.keys(this.newAreas).length === 0
      && (Object.keys(this.labelAreasRegion).length === 0)
      && this.disabled_modi === false) {
        console.log('no data - next image');
        if (this.accuracyTotal[this.imageRef_num - 1] === undefined) {
          console.log('set accuracy to zero');
          this.accuracyTotal[this.imageRef_num - 1] = [0, 0, 1];
          // this.currentAccuracy = 0;
        }
        if (section !== 'last') {
          this.nextImage();
        }
      } else if ((!this.disabled_modi) && ((Object.keys(this.labelAreas).length !== 0)
        || (Object.keys(this.labelAreasRegion).length !== 0))) {
        // this.disabled_save = true;
        // this.loading_save = true;
        if (section === 'next_image') {
          this.text_button = 'save image...';
        }
        this.uploadData(section);
      } else if ((this.disabled_modi) && (Object.keys(this.newAreas).length !== 0)) {
        console.log('ADD REGIONS');
        // this.disabled_save = true;
        // this.loading_save = true;
        this.text_button = 'get LabelMask';
        this.uploadNewData();
      } else if ((this.disabled_modi) && (Object.keys(this.newAreas).length === 0)) {
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
      console.log('uploadData start Level 2');
      if (this.labelAreas.length === 0) {
        this.labelAreas = 'none';
      }
      if (this.labelAreasRegion.length === 0) {
        this.labelAreasRegion = 'none';
      }
      this.labelAreas = String(this.labelAreas);
      this.labelAreasRegion = String(this.labelAreasRegion);
      HTTP.post(
        // 'http://localhost:3000/labelmask/'
        `label_level/${this.labelAreas}/${this.labelAreasRegion}/${this.imageRef_num}/${this.allProperties.UserID}/${this.allProperties.dataset_typ}/2/${this.allProperties.labelingApproach}`,
      ).then(async (response) => {
        // this.newImage = response.data.image;
        console.log(`labels recieved and segMask calcualted for image ${response.data.image_num}.`);
        this.accuracyTotal[response.data.image_num - 1] = response.data.accuracy;
        this.currentAccuracy = Math.round(this.accuracyTotal[response.data.image_num - 1][0] * 100);
        this.currentAccuracy_correct = Math.round(
          this.accuracyTotal[response.data.image_num - 1][2] * 100,
        );
        // this.SegMaskAll = response.data.seg_masks;
        // this.SegMaskNumber = response.data.image_num;
        // this.SegMask = this.SegMaskAll[this.SegMaskNumber - 1];
        // if (section === 'next_image') {
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
        const points = this.numberCells * 10 + this.numberRegions * 30
            + this.addedAreas * 50 - this.minusPoints;
        this.$emit('updatePoints', points);
        this.labelAreas = [];
        this.labelAreasRegion = [];
      }).catch((e) => {
        console.warn(e);
        this.labelAreas = [];
        this.labelAreasRegion = [];
        this.undo();
        this.text_button = 'last label failed, label again';
        // this.trainingErrorFlag = true;
        // this.imageLoadingErrorFlag = false;
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
        // 'http://localhost:3000/labelmask/'
        `newAreas/${this.newAreas}/${this.imageRef_num}/${this.allProperties.UserID}/${this.allProperties.dataset_typ}`,
      ).then(async (response) => {
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
        this.text_button = '';
        this.newAreas = [];
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.redrawOldContent(true);
      }).catch((e) => {
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
      if (this.imageRef_num < this.numberImagesLevel) {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.imageRef_num = this.imageRef_num + 1;
        if (this.labelAreasAll[this.imageRef_num - 1] !== 0
        || this.labelAreasRegionAll[this.imageRef_num - 1] !== 0) {
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
        // this.bounce_nextLevel = true;
        // this.bounce = true;
        // this.animation = 'StarSpecial2';
        this.updateScores();
      }
      // this.getData(false);
      // get next 10 iamges
      /* if (((this.imageRef_num - 1) % 10 === 0)) {
        // this.roll = true;
        // this.animation = 'StarSpecial';
        this.image_section = this.image_section + 1;
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
        // console.log(this.image_update);
        this.updateImages();
      }
      if (this.allProperties.labelingApproach === 'basic') {
        document.getElementById('SegMask').style.display = 'inline';
      } */
      // this.draw(this.scale, this.scaleMultiplier);
    },
    previousImage() {
      // deltet circles
      console.log('previous Image');
      this.SegMask = null;
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
      if (this.imageRef_num > 1) {
        this.imageRef_num = this.imageRef_num - 1;
        if (((this.imageRef_num) % 10 === 0)) {
        // console.log(`getData for next section : ${this.image_section}`);
          this.image_section = this.image_section - 1;
          this.image_update = 10;
        }
        if ((this.labelAreasAll[this.imageRef_num - 1] !== 0)
        || this.labelAreasRegionAll[this.imageRef_num - 1] !== 0) {
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
    getDataLevel2() {
      this.disableButton('all');
      console.log('get 10 images');
      // let celltyp = '';
      this.newImage = null;
      this.newImageMask = null;
      const level = 2;
      HTTP.post(
        `getDataLevel/${this.allProperties.UserID}/${this.allProperties.labelingApproach}/${this.allProperties.dataset_typ}/${level}`,
      ).then(async (response) => {
        this.highscore = response.data.highscore[0];
        this.highscore_level = response.data.highscore[1];
        this.newImages = response.data.images;
        this.newImageMasks = response.data.label_masks;
        // celltyp = response.data.celltyp;
        console.log('Received Level 2');
        console.log('Start Timer');
        this.toggleTimer();
        this.newImage = this.newImages[0];
        this.newImageMask = this.newImageMasks[0];
        this.disabled_next = false;
        this.loading_next = false;
        this.disabled_prev = false;
        this.loading_prev = false;
        this.disabled_undo = false;
        this.text_button = '';
        // this.getCelltyp(celltyp);
      }).catch((e) => {
        console.warn(e);
      });
      return 'Complete';
    },
    // get celltyp of dataset after getting images from backend
    /* getCelltyp(celltyp) {
      if (celltyp === 'Mon') {
        this.celltyp = 'Monocytes';
      }
      if (celltyp === 'Neu') {
        this.celltyp = 'Neutrophils';
      }
      if (celltyp === 'Eos') {
        this.celltyp = 'Eosinophils';
      }
      if (celltyp === 'Lym') {
        this.celltyp = 'Lymphocytes';
      }
      if (celltyp === 'Basophils') {
        this.celltyp = 'Basophils';
      }
    }, */
    // undo last selected element by user
    undo() {
      console.log('undo last element');
      if (!this.disabled_modi && !this.disabled_measurement) {
        if (this.lastLabeledElement[this.lastLabeledElement.length - 1] === 'cell') {
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
        } else if (this.lastLabeledElement[this.lastLabeledElement.length - 1] === 'region') {
          const currentData = this.labelAreasRegionAll[this.imageRef_num - 1];
          const lastElement = currentData[currentData.length - 1];
          this.context.clearRect(lastElement[0][0] - 2, lastElement[0][1] - 2,
            lastElement[1] + 4, lastElement[2] + 4);
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
    },
    // measure distance between two clicked points
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
        distance = (Math.round((distance + Number.EPSILON) * 100) / 100);
        ctx.fillStyle = 'purple';
        ctx.font = '15px Arial';
        ctx.fillText(`${distance} µm`, this.startX, this.startY);

        this.clicks = 0;
      }
      this.firstClick = [x, y];
    },
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
      if (click === 'modi1' && this.disabled_modi === true) {
        this.disabled_modi_region = false;
      }
      if (click === 'modi2' && this.disabled_modi_region === true) {
        this.disabled_modi = false;
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
      /* if (click === 'measurement' && !this.disabled_measurement) {
        this.undo('delete_measure');
      } */
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
      const wrongAreas = this.minusPoints / 5;
      this.accuracyTotal = String(this.accuracyTotal);
      HTTP.post(
        `getAccuracy_level/${this.allProperties.currentLevel}/${this.imageRef_num}/${this.accuracyTotal}`,
      ).then(async (response) => {
        this.nextLevelprops.accuracyForScoring = response.data.accuracy_all[0];
        this.nextLevelprops.accuracyForScoring_correct = response.data.accuracy_all[2];
        console.log('accuracy recieved');
        // console.log(response.data.accuracy_all);
        this.$emit('updateAccuracy', response.data.accuracy_all);
        const Scores = [this.imageRef_num, this.numberCells, this.numberRegions, wrongAreas,
          this.addedAreas, this.seconds,
          this.allProperties.points, response.data.accuracy_all, this.allProperties.currentLevel];
        // const Scores = [this.numberCells, this.numberRegions, this.addedAreas, this.seconds];
        this.$emit('updateScores', Scores);
        // this.$emit('updateAccuracy', response.data.accuracy);
        // this.nextLevelprops.accuracyForScoring = response.data.accuracy[3];
        if (review === 'review') {
        //  this.updateBreak();
          this.updateComponent('review');
        }
        this.bounce_nextLevel = true;
        // this.numberCells = 0;
        // this.numberRegions = 0;
        // points = 0;
        // this.seconds = 0;
      }).catch((e) => {
        console.warn(e);
      });
      return 'Complete';
    },
    /* calAccuracyAverage() {
      console.log(`all accurcays: ${this.accuracyTotal}`);
      let accuracyAreas = 0; // lables areas / all possible areas
      let accuracyPixel = 0; // lables pixel / all possibel pixel
      let accuracyLabel = 0; // correct labeled areas / all labeled areas
      for (let i = 0; i < this.accuracyTotal.length; i += 1) {
        accuracyAreas += this.accuracyTotal[i][0];
        accuracyPixel += this.accuracyTotal[i][1];
        accuracyLabel += this.accuracyTotal[i][2];
      }
      console.log(accuracyAreas);
      accuracyAreas /= this.accuracyTotal.length;
      accuracyPixel /= this.accuracyTotal.length;
      accuracyLabel /= this.accuracyTotal.length;
      const accuracySpecified = [accuracyAreas, accuracyPixel, accuracyLabel];
      // const accuracyTotalValue = (accuracySpecified[0] + accuracySpecified[1]
      // + accuracySpecified[2]) / 3;
      this.nextLevelprops.accuracyForScoring = (accuracySpecified[0] + accuracySpecified[2]) / 2;
      console.log(`scoring: ${this.nextLevelprops.accuracyForScoring}`);

      return [accuracySpecified, this.nextLevelprops.accuracyForScoring];
    }, */
  },
  mounted() {
    // true to get an empty folder for starting labeling process at the backend side
    this.getDataLevel2(true);
    console.log('labelingapproach');
    console.log(this.allProperties.labelingApproach);
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
    this.canvas.addEventListener('click', this.selectCell);
    this.canvas.addEventListener('contextmenu', this.startRectRegion);
    this.canvas.addEventListener('mouseup', this.MouseupRegion);
    this.canvas.addEventListener('mousemove', this.selectRegion);
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
  z-index: 500;
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
.options {
  position: relative;
  top: 70px;
}
.userID {
  height: 100%;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  text-justify: start;
}
.save-button-id {
  margin-left: 5px;
}
.canvas {
  /* top: 49px; */
  height: 100%;
  width: '384';
  left: 7px;
  display: inline-block;
  z-index: 1;
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
.covered_transparent{
  position: absolute;
  z-index: 1;
  top: 50px;
  left: 0px;
}
.scores {
  position: static;
  z-index: 10;
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
  animation: roll-in .5s;
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
