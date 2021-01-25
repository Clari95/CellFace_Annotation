import Vue from 'vue';
import VueRouter from 'vue-router';
import TemplateView from '@/views/TemplateView.vue';
// import Home from '@/views/Home.vue';
import Explorer from '@/views/Explorer.vue';
import Preview from '@/views/Preview.vue';
import Upload from '@/views/Upload.vue';
import Folder from '@/views/Folder.vue';
import Login from '@/views/Login.vue';
// import Labeling from '@/views/Labeling.vue';
// import LabelingPixelWise from '@/views/LabelPixelWise.vue';
import LabelingPixelWiseBasic from '@/views/LabelPixelWiseBasic.vue';
import LabelingPixelWiseGame from '@/views/LabelPixelWiseGame.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
  },
  {
    path: '/',
    component: TemplateView,
    children: [
      /* {
        path: '',
        name: 'home',
        component: Home,
      }, */
      {
        path: 'explorer',
        name: 'explorer',
        component: Explorer,
      },
      {
        path: 'explorer/*',
        name: 'explorer',
        component: Explorer,
      },
      {
        path: 'preview',
        name: 'preview',
        component: Preview,
        props: route => route.query,
      },
      {
        path: 'upload',
        name: 'upload',
        component: Upload,
      },
      /* {
        path: 'labeling',
        name: 'labeling',
        component: Labeling,
      }, */
      /* {
        path: 'labelingPW',
        name: 'labelingPW',
        component: LabelingPixelWise,
      }, */
      {
        path: 'labelingPWBasic',
        name: 'labelingPWBasic',
        component: LabelingPixelWiseBasic,
      },
      {
        path: 'labelingPWGame',
        name: 'labelingPWGame',
        component: LabelingPixelWiseGame,
      },
      {
        path: 'folder',
        name: 'folder',
        component: Folder,
      },
      {
        path: 'about',
        name: 'about',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
      },
    ],
  },
];

const router = new VueRouter({
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('isLoggedIn');
  if (!isAuthenticated && to.path !== '/login') next('/login');
  else next();
});

export default router;
