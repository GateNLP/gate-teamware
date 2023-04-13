# Frontend

Web GUI of Teamware is built with [vue.js](https://vuejs.org) version 2.7.x. 

[Bootstrap](https://getbootstrap.com/) (and [Bootstrap vue](https://bootstrap-vue.org/)) provides the visual styling.

[Vite.js](https://vitejs.dev/) is used to bundle Vue code and other javascript dependencies for deployment and serve as a frontend dev server (which runs alongside django dev server) while testing or debugging.

## Getting started

### Installation
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Testing

**Tools used for testing:**
* [Jest](https://jestjs.io) - Our main frontend test harness. Integrated into vue cli.
* [Vue testing library](https://testing-library.com/docs/vue-testing-library/intro/) - Used for rendering vue component 
    allows it to be mounted for unit testing. Officially recommended by Vue.js.

Tests for the frontend are all located in `tests` folder.

Unit test files should all be placed in `tests/unit/` folder and have an extension `.spec.js`.


To run the test:

```
npm run test
```

## Notes when coming from the previous version <=2.0.0

- The `@` alias can still be used when doing module imports but file extensions should now be used when importing `.vue` files e.g. 
  - Before: `import DeleteModal from "@/components/DeleteModal" 
  - Now:  `import DeleteModal from "@/components/DeleteModal.vue"`
- For code that is intended to run on the browser, e.g. in all `.vue` files, imports should use the ES 6 compliant `import`  command and not node/commonjs's `require`
	- Exceptions can be made for code that is run directly by node, e.g. scripts used in the build chain, config files and test files used by build tools that run on node (e.g. vuepress or cypress)


## Explantion of the frontend

### Vue and Vite

Instead of separating html, css and javascript files, Vue has its own `single-file component` format normally with `.vue` extension ([reason why this file format is used](https://vuejs.org/guide/scaling-up/sfc.html)). Here is an example `.vue` file:

```vue
<script>
export default {
  data() {
    return {
      greeting: 'Hello World!'
    }
  }
}
</script>

<template>
  <p class="greeting">{{ greeting }}</p>
</template>

<style>
.greeting {
  color: red;
  font-weight: bold;
}
</style>
```

This means that `.vue` files cannot be directly imported into a standard html page. A tool has to be used for converting `.vue` file into standard javascript and/or css files, this is where [Vite.js](https://vitejs.dev/) comes in. 

[Vite.js](https://vitejs.dev/) is a tool that, amongst many other things, provides a dev server allowing hot module replacement (ability to immediately see changes in the UI during development) and bundling of javascript modules and other resources (css, images, etc.) i.e. not having to individually import each javascript and their dependencies from the main page. A [Vue plugin](https://github.com/vitejs/vite-plugin-vue2) is used to automatically convert `.vue` files into plain javascript as part of the bundling process.

### App entrypoint (main.js) and routing 

The application's main entrypoint is `/frontend/src/main.js` which loads dependencies like Vue, Bootstrap Vue as well as loading the main component `AnnotationApp.vue` into a html page that contains a `<div id="app"></div>` tag.

The `AnnotationApp.vue` component contains the special `<router-view></router-view>` tag ([vue router](https://router.vuejs.org/)) which allows us to map url paths to specific vue components. The routing configuration can be found in `/frontend/src/router/index.js`, for example:

```js
const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: {guest: true},
    },
...
```

The route shown above maps the root path e.g. `https://your-deployed-teamware-domain.com/` to the `Home.vue` component. Specifically, when pointing your browser to that path, the `Home.vue` component is inserted inside `<router-view></router-view>`. 

### index.html, templates and bundling

A html page is required to place our application in. Teamware uses Django to serve up the main html page which is located at `/frontend/templates/index.html` (see `MainView` class in `/backend/views.py`). This `index.html` page has to know where to load the generated javascript files. Where these files are differ depending on whether you're in development (debug) or production mode.  

#### In debug mode (Django's `settings.DEBUG` is `true`)
In debug mode, we expect to be running the vite dev server alongside django server (when running `npm run serve` from the root of the project). In this case `index.html` imports javascript directly from the vite dev server:

```html
<script type="module" src="http://localhost:5173/@vite/client"></script>
<script type="module" src="http://localhost:5173/src/main.js"></script>
```


#### In production mode (Django's `settings.DEBUG` is `false`)
In production mode, vite converts `.vue` files into plain javascript and bundles them to `/frontend/dist/static` directory. The `/frontend/src/main.js` becomes `/frontend/dist/static/assets/main-bb58d055.js`. The scripts are imported as static asset of going through the vite server, for example:

```html
<link rel="stylesheet" href="/static/assets/main-89ece1f8.css" />
<script type="module" src="/static/assets/main-bb58d055.js"></script>
```

#### index.html generation

You may have noticed that a hash is added to the generated asset files (e.g. `main-bb58d055.js`) and this hash changes every time Vite builds the code. This means the `index.html` must also be re-generated after every Vite build as well.

A simple build script which runs after every vite build `/frontend/build_template.js` performs this generation by taking the base template `/frontend/base_index.html`, merging it with Vite's generated manifest `/frontend/dist/manifest.json` and the output with the correct import path to `/frontend/templates/index.html`.

