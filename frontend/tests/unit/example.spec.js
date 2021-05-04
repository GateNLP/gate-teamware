import { render, fireEvent } from '@testing-library/vue'
import HelloWorld from '@/components/HelloWorld.vue'

//Testing a component e.g. HelloWorld
describe('HelloWorld.vue', () => {

  it('renders props.msg when passed', () => {
    const msg = 'new message'
    const { getByText } = render(HelloWorld)

    getByText("Installed CLI Plugins")
  })
})
