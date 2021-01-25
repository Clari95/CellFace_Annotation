# frontend

## Project Organization
* ```package.json``` : dependencies and running configurations;
* ```.env``` : configuration file for environment variables;
* ```.eslintrc.js``` : configuration file for linter and prettifier, enforces the [AirBnB JS style guide](https://github.com/airbnb/javascript);
* ```.editorconfig``` : configuration for code editor (_e.g._ max characters per line);
* ```start_prod.sh``` : starts production deployment of frontend server (still needs to be properly configured, _e.g._ the environment variables);
* ```Dockerfile``` : Dockerfile for building standard development container;
* ```Dockerfile.prod``` : Dockerfile for building production deployment container;
* ```src``` : project's source code;
* ```src/assets``` : static assets for the website;
* ```src/plugins``` : vue plugins installed;
  - currently only _vuetify_ for general material design components;
  - change ```vuetify.js``` for general visual settings (such as color theme/palette);
* ```src/router``` : vue router;
  - if you want to add a new page you must link it here (providing the correct URI and Component); general pages are under the _TemplateView_ template (provides consistent navigation controls _e.g._ navigation bar, drawer, snackbar);
* ```src/views``` : components corresponding to different pages, or page templates;
* ```src/components``` : reusable components, each with their own independent behavior;
* ```src/http.common.js``` : defines axios instance to correctly access backend HTTP API;
* ```src/utils.common.js``` : defines general utility functions;
* ```src/App.vue``` : root Vue instance/component (parent of all other components);
* ```src/main.js``` : program entry-point;


### Architecture Overview
* Components are organized in a tree structure;
* _App_ component is the root;
  - Two children: _Login_ and _TemplateView_;
  - _TemplateView_ is the parent of all other pages;
  - All pages are handled by the vue router, and are injected on the respective ```<router-view></router-view>``` of the parent;
* You must login before accessing the website
  - Using your TUM credentials (open only to LDV members);
  - Each subsequent request using _axios_ automatically sends the required credentials and headers;


## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Run your unit tests
```
yarn test:unit
```

### Lints and fixes files
```
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
