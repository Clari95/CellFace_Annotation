<template>
<div>
  <v-navigation-drawer
  v-model="drawer"
  app
  :color="darkMode ? '#435070' : 'grey lighten-4'"
  :mini-variant="drawerMinified"
  >
  <v-layout fill-height column ma-0 justify-space-between>
    <v-list>
      <router-link to="/">
        <v-img
          :src="require('@/assets/cellface_logo_3.png')"
          class="mx-auto mb-5"
          contain
          width="80%"
        ></v-img>
      </router-link>

      <template v-for="(route, i) in routes">
        <v-list-item :key="i" link :to="route.to">
          <v-list-item-action><v-icon>{{ route.icon }}</v-icon></v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ route.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-list>

  <StatusBar/>

  </v-layout>
  </v-navigation-drawer>

  <v-app-bar
    color="primary"
    app
    dark
    clipped-right
  >
      <v-app-bar-nav-icon
        @click="handleNavToggle()"
      />

      <v-breadcrumbs :items="breadcrumbs">
        <template v-slot:divider>
          <v-icon>mdi-chevron-right</v-icon>
        </template>
      </v-breadcrumbs>

      <!-- TODO: custom buttons on the right side -->
      <v-spacer></v-spacer>

      <v-btn text disabled outlined color="white" class="mx-2" v-if="logoutSanityCheck()">
        {{getLastName() + ', ' + getFirstName()}}
      </v-btn>

      <v-btn icon @click="switchDarkMode()" class="mx-2">
        <v-icon>{{darkMode ? 'fa-sun-o' : 'fa-moon-o'}}</v-icon>
      </v-btn>

      <v-btn
        outlined text
        class="mx-2" color="white"
        @click="requestLogout"
        :disabled="!logoutSanityCheck()"
      >
        Logout
      </v-btn>
    </v-app-bar>

  <v-content>
    <router-view></router-view>
  </v-content>

</div>
</template>

<script>
import StatusBar from '@/components/StatusBar.vue';
import { HTTP } from '@/http.common';

export default {
  components: {
    StatusBar,
  },

  data: () => ({
    drawer: true,
    drawerMinified: false,
    breadcrumbs: [],
    routes: [
      /* {
        to: '/explorer',
        title: 'Explorer',
        icon: 'fa-archive',
      },
      {
        to: '/upload',
        title: 'Upload',
        icon: 'fa-upload',
      },
      {
        to: '/folder',
        title: 'Folder',
        icon: 'fa-upload',
      },
      {
        to: '/labeling',
        title: 'Labeling',
        icon: 'fa-tags',
      }, */
      /* {
        to: '/labelingPW',
        title: 'Labeling pixel-wise',
        icon: 'fa-tags',
      }, */
      {
        to: '/labelingPWBasic',
        title: 'LabelingPW Basic',
        icon: 'fa-tags',
      },
      {
        to: '/labelingPWGame',
        title: 'LabelingPW Game',
        icon: 'fa-rocket',
      },
      /* {
        to: '/analyze',
        title: 'Analyze',
        icon: 'fa-search',
      },
      {
        to: '/deployment',
        title: 'Deployment',
        icon: 'fa-rocket',
      }, */
    ],
    darkMode: false,
  }),

  methods: {
    constructBreadcrumbs(path) {
      const breadcrumbs = [];
      let parsedPath = path;
      if (parsedPath[0] === '/') { parsedPath = parsedPath.substr(1); }
      if (parsedPath.length === 0) { return breadcrumbs; }

      let currentPath = '';
      parsedPath.split('/').forEach(
        (el) => {
          currentPath += `/${el}`;
          breadcrumbs.push({
            text: el,
            to: currentPath,
            exact: true,
          });
        },
      );
      return breadcrumbs;
    },

    handleNavToggle() {
      if (!this.drawer) {
        this.drawer = true;
      } else {
        this.drawerMinified = !this.drawerMinified;
      }
    },

    switchDarkMode() {
      this.darkMode = !this.darkMode;
      this.$vuetify.theme.dark = this.darkMode;
    },

    requestLogout() {
      HTTP.post('logout')
        .then(() => {
          localStorage.removeItem('isLoggedIn');
          this.$router.push('login');
        });
    },

    logoutSanityCheck() {
      return !!localStorage.getItem('isLoggedIn');
    },

    getFirstName() {
      return localStorage.getItem('firstName');
    },

    getLastName() {
      return localStorage.getItem('lastName');
    },

  },

  mounted() {
    this.breadcrumbs = this.constructBreadcrumbs(this.$route.path);
  },

  watch: {
    $route(to) {
      this.breadcrumbs = this.constructBreadcrumbs(to.path);
    },
  },
};
</script>


<style lang="scss">

  .v-breadcrumbs .v-breadcrumbs__item {
    color: white;
  }

  #status-card {
    padding-top: 1em;
    padding-bottom: 1em;
}

</style>
