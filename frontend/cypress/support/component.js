// ***********************************************************
// This example support/component.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands'

// Alternatively you can use CommonJS syntax:
// require('./commands')

import Vue from 'vue'

// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


//Importing scss assets needs an @/ in front of it

import "@/assets/sass/app.scss"


import {BootstrapVue, BootstrapVueIcons} from "bootstrap-vue";
import VJsoneditor from 'v-jsoneditor'
import MarkdownItVue from 'markdown-it-vue'

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(VJsoneditor)
Vue.use(MarkdownItVue)



import {mount} from 'cypress/vue2'


Cypress.Commands.add('mount', (component, options = {}) => {

    // Setup options object
    options.global = options.global || {}
    options.global.plugins = options.global.plugins || []
    options.global.plugins.push(BootstrapVue)
    options.global.plugins.push(BootstrapVueIcons)


    return mount(component, options)
})


// The following command allows us to access emitted events through the vue test util wrapper, source:
// https://css-tricks.com/testing-vue-components-with-cypress/#aa-accessing-the-vue-test-utils-wrapper
Cypress.Commands.add('vue', () => {
  return cy.wrap(Cypress.vueWrapper);
});

