<template>
  <div class="root">
      <v-stepper v-model="stepInfo.current" class="elevation-0">
        <v-stepper-header>
          <template v-for="(n, index) in stepInfo.steps">
            <v-stepper-step
              :key="index"
              :complete="stepInfo.current > index + 1"
              :step="index + 1"
            >
              {{ n }}
            </v-stepper-step>

            <v-divider
              v-if="index !== stepInfo.steps.length - 1"
              :key="n"
            ></v-divider>
          </template>
        </v-stepper-header>
      </v-stepper>
  </div>
</template>
<script>
export default {
  name: 'StepProgress',
  props: ['stepInfo'],
  data() {
    return {
      e1: 1,
      steps: 4,
    };
  },
};
</script>

<style scoped>
.root{
    height: 180px;
    width: 100%;
}

.container{
  width: 100%;
  height: 100%;
  z-index: 1;
}
.progressbar{
  counter-reset: step;
  list-style: none;
}
.progressbar li{
  float: left;
  width: 16.28%;
  position: relative;
  text-align: center;
}
.progressbar li:before{
  content:counter(step);
  counter-increment: step;
  width: 30px;
  height: 30px;
  border: 2px solid #bebebe;
  display: block;
  margin: 0 auto 10px auto;
  border-radius: 50%;
  line-height: 27px;
  background: white;
  color: #bebebe;
  text-align: center;
  font-weight: bold;
}
.progressbar li:after{
  content: '';
  position: absolute;
  width:100%;
  height: 3px;
  background: #979797;
  top: 15px;
  left: -50%;
  z-index: -1;
}
.progressbar li.active:before{
 border-color: #4070ae;
 background: #4070ae;
 color: white
}
.progressbar li.active:after{
 background: #4070ae;
}
.progressbar li.active-li:after{
 background: #4070ae;
}
.progressbar li.active-li:before{
 border-color: #4070ae;
 background: #4070ae;
 color: white
}
.progressbar li:first-child:after{
 content: none;
}
</style>
