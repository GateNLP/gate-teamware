# frontend

Web GUI built with [vue.js](https://vuejs.org).

## Project setup
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

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
