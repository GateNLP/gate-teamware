import { render, fireEvent } from '@testing-library/vue'
import { routes } from '@/router'

import { createLocalVue, mount } from '@vue/test-utils'

// create an extended `Vue` constructor
const localVue = createLocalVue()

import BootstrapVue from 'bootstrap-vue'
// install plugins as normal
localVue.use(BootstrapVue)

// pass the `localVue` to the mount options
import Project from '@/views/Project.vue'
mount(Project, {
  localVue
})



/** Example of how a component could be tested

import HelloWorld from '@/components/HelloWorld.vue'

//Testing a component e.g. HelloWorld
describe('HelloWorld.vue', () => {

  it('renders props.msg when passed', () => {
    const msg = 'new message'
    const { getByText } = render(HelloWorld)

    getByText("Installed CLI Plugins")
  })
})

 **/


describe('Project.vue', () => {
  it('Validates JSON input as project configuration', () => {
    const $route = { params: {id: 1} };
    const { getByText } = render(Project, {routes, stubs: [$route]}, (vue, store, router) => {
      router.push('/projects/1')
    });
    // Asserts initial state.
    getByText('Project Configuration');
  })
})
