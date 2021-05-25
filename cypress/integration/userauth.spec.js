describe('User Registration Test', () => {

    beforeEach(()=>{
        // Run setup if needed
    })

    it('registers a user', () => {
        cy.visit("/register")

        cy.contains('Register')
        cy.contains('Username').type('tester')
        cy.contains('Email').type('test@test.com')
        cy.contains('Password').type('123456')
        cy.contains('Confirm Password').type('123456')
        cy.get('form').contains('Register').click()
        cy.contains('GATE Annotation Tool')
    })

  it('tests password mismatch', () => {
    cy.visit("/register")

    cy.contains('Register')
    cy.contains('Password').type('123456')
    cy.contains('Confirm Password').type('789')
    cy.contains('Password must match')
    })

    it('tests username in use error', () => {
        //relies on above test running first to register user
        cy.visit("/register")
    
        cy.contains('Username').type('tester')
        cy.contains('Email').type('test@test.com')
        cy.contains('Password').type('123456')
        cy.contains('Confirm Password').type('123456')
        cy.get('form').contains('Register').click()
        cy.contains('Username already exists')
        })
})
