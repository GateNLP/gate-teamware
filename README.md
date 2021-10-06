# Gate Annotation Service

A service for collaborative document annotation. Project plan can be found here:

[https://docs.google.com/document/d/1NDV17vQKugBOffT56NANtxEiRU0EuJ6MzdKhfC5rAII](https://docs.google.com/document/d/1NDV17vQKugBOffT56NANtxEiRU0EuJ6MzdKhfC5rAII)


## Django settings files

Django settings are located in `annotation_tool/setttings` folder. The app will use `base.py` setting by default
and this must be overridden depending on use.

### secret.py

A `secret.py` should be created to hold settings that should not be made public by tracking through version
control. A `secret_default.py` exists as a guide and to provide default value for testing. 


## Installation

The service depends on a combination of python and js libraries. conda is recommended as it's able to install
python libraries and nodejs which is used to install js libraries.

* Install anaconda/miniconda
* Create a virtual conda env and install python dependencies
  ```bash
  conda env create -f environment. yml
  ```
* Activate conda environment
  ```bash
  source activate annotation-tool
  ```
* Install nodejs dependencies
  ```bash
  npm install
  ```



## Updating packages
To update packages after a merge, run the following commands:

```bash
# Activate the conda environment
source activate annotation-tool
# Update any packages changed in the environnment.yml
conda env update -f environment.yml
# Update any packages changed in package.json
npm install
```

## Development server
The application uses django's dev server to serve page contents and run the RPC API, it also uses Vue CLI's 
development server to serve dynamic assets such as javascript or stylesheets allowing for hot-reloading
during development.

To run both servers together:

```bash
npm run serve
```

To run separately:

* Django server
  ```bash
  npm run serve:backend
  ```
* Vue CLI dev server
  ```bash
  npm run serve:frontend
  ```
  
## Testing

All the tests can be run using the following command:

```bash
npm run test
```

### Backend Testing
Pytest is used for testing the backend.

```bash
npm run test:backend
```

#### Backend test files

* Unit test files are located in `/backend/tests`

### Frontend testing
[Jest](https://jestjs.io/) is used for frontend testing. 
The [Vue testing-library](https://testing-library.com/docs/vue-testing-library/intro/) is used for testing
Vue components.

```bash
npm run test:frontend
```

#### Frontend test files

* Frontend test files are located in `/fontend/tests/unit` and should the extension `.spec.js`

#### Testing JS functions

```javascript
describe("Description of a group of tests to be run", () =>{

    beforeAll(() =>{
        //The code here is run before each test
    })

    it("A single test's description", async () =>{

        // Assertions are done with the expect() function e.g.
        let funcOutput = 30 + 10
        expect(funcOutput).toBe(40)
      

    })
})

```

#### Mocking JS classes

This is an example of a mock harness for the JRPCClient class.

A mock file is created inside a ``__mock__`` directory placed next to the file that's being mocked, e.g.
for our JRPCClient class at `/frontend/src/jrpc/index.js`, the mock file is `/frontend/src/jrpc/__mock__/index.js`.


Inside the mock file `/frontend/src/jrpc/__mock__/index.js`:
```javascript
// Mocking jrpc/index.js
//Mocking the JRPCClient class
//Replacing the call function with a custom mockCall function
export const mockCall = jest.fn(()=> 30);
const mock = jest.fn().mockImplementation(() => {
  return {call: mockCall};
});

export default mock;
```


Inside the test file `*.spec.js`:
```javascript
import JRPCClient from "@/jrpc";
jest.mock('@/jrpc')

import store from '@/store'
//Example on how to mock the jrpc call

describe("Vuex functions testing", () =>{

    beforeAll(() =>{

        //Re-implement custom mock call implementation if needed
        JRPCClient.mockImplementation(()=>{
            return {
                call(){
                    return 50
                }
            }
        })

    })

    it("testfunc", async () =>{

        const noutput = await store.dispatch("testnormal")
        expect(noutput).toBe("Hello world")

        const aoutput = await store.dispatch("testasync")
        expect(aoutput).toBe("Hello world")

        const rpc = new JRPCClient("/")
        const result = await rpc.call("some param")
        expect(result).toBe(50)

    })
})
```

#### Testing Vue components


```javascript
//Example of how a component could be tested
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

```


### Integration testing
[Cypress](https://www.cypress.io/) is used for integration testing.

The integration settings are located at `annotation_tool/settings/integration.py`

To run the integration test:
```bash
npm run test:integration
```

The test can also be run in **interactive mode** using:

```bash
npm run serve:cypressintegration
```

#### Integration test files
Files related to integration testing are located in `/cypress`

* Test files are located in the `/cypress/integration` directory and should have the extension `.spec.js`.

#### Re-seeding the database

The command `npm run migrate:integration` resets the database and performs migration, use with `beforeEach` to run it
before every test case in a suite:

```js
describe('Example test suite', () => {

    beforeEach(() => {
        // Resets the database every time before
        // the test is run
        cy.exec('npm run migrate:integration')
    })

    it('Test case 1', () => {
        // Test something
    })
  
    it('Test case 2', () => {
        // Test something
    })
})
```

## Deployment
Deployment is via docker-compose, using nginx to serve static content.

A deployment script is provided to launch the docker-compose stack with the correct environment variables. This also runs `./generate-env.sh` to create a `.env` file containing randomly generated secrets which are mounted as envrionment variables into the container.

First build the images via:
```bash
./build-images.sh
```

then deploy the stack with

```bash
./deploy.sh production # (or prod) to deploy with production settings
./deploy.sh staging # (or stag) to deploy with staging settings
```