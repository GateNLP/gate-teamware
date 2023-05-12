

describe("Test connection errors", () =>{

    it("Test initialise with 404 response", () => {

        cy.intercept("POST", "/rpc/",
          {
            statusCode: 404,
              body: {

              }
          }
        ).as('rpcCalls') // and assign an alias
        cy.visit("/")
        cy.contains("TEAMWARE").should("be.visible")
    })

    it("Test initialise with blank response", () =>{
        cy.intercept(
          {
            method: 'POST', // Route all GET requests
            url: '/rpc/', // that have a URL that matches '/users/*'
          },
          [] // and force the response to be: []
        ).as('rpcCalls') // and assign an alias
        cy.visit("/")
        cy.contains("TEAMWARE").should("be.visible")
    })

})
