import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    dark: false,
    themes: {
      light: {
        // primary: '#4889ce',
        primary: '#3070b3',
        secondary: '#64a0c8',
        accent: '#005293',
        error: '#f44336',
        warning: '#ff9800',
        info: '#cddc39',
        success: '#4caf50',
      },
      dark: {
        primary: '#005293',
        secondary: '#4889ce',
      },
    },
  },
});
