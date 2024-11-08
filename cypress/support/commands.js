// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

import 'cypress-file-upload'

// Send an rpc request to frontend

Cypress.Commands.add("rpcRequest", (method, params, doFailOnStatusCode=true) => {

    cy.request("get", "/").then(() => {
        cy.getCookies().then((cookies) => {
            let csrf = null
            for (let c of cookies) {
                if (c.name === "csrftoken") {
                    csrf = c.value
                }
            }

            let requestBody = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": 1
            }

            return cy.request({
                failOnStatusCode: doFailOnStatusCode,
                method: "post",
                url: "/rpc/",
                body: requestBody,
                headers: {
                    "X-CSRFToken": csrf,
                }
            })
        })
    })
})

// Login to frontend though RPC request
Cypress.Commands.add("login", (username, password, doFailOnStatusCode=true) => {
    return cy.rpcRequest("login", [{username: username, password: password}], doFailOnStatusCode)
})

// Logout using RPC
Cypress.Commands.add("logout", () => {
    return cy.rpcRequest("logout")
})


//Migrate integration db
Cypress.Commands.add("migrate_integration_db", (fixtureName) => {

    const testenv = Cypress.env('TESTENV');
    if (testenv === 'container' || testenv === 'ci') {
        // find the right docker compose command
        cy.exec("docker compose").then(({code}) => {
            const compose = (code === 0 ? 'docker compose' : 'docker-compose')
            if (testenv === 'container') {
                cy.exec(`${compose} exec -T backend ./migrate-integration.sh -n=${fixtureName}`)
            } else if (testenv === 'ci') {
                cy.exec(`DJANGO_SETTINGS_MODULE=teamware.settings.deployment ${compose} exec -T backend ./migrate-integration.sh -n=${fixtureName}`)
            }
        });
    }
    else{
        cy.exec(`npm run migrate:integration -- -n=${fixtureName}`, {log:true})
    }
})