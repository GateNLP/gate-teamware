describe('User Interface Permissions Test', () => {

    beforeEach(()=>{
        const fixtureName = 'create_db_users'
        cy.migrate_integration_db(fixtureName)
    })

    it('tests admin UI permissions', () => {
        cy.visit("/login")

        cy.contains('Username').type('admin')
        cy.contains('Password').type('testpassword')
        cy.get('form').contains('Sign In').click()

        cy.contains('Manage Users').click()
        cy.url().should('include', '/manageusers')
    })

    it('tests manager UI permissions', () => {
        cy.visit("/login")

        cy.contains('Username').type('manager')
        cy.contains('Password').type('testpassword')
        cy.get('form').contains('Sign In').click()
        cy.contains('Manage Users').should('not.exist')
        cy.contains('Projects').click()
        cy.url().should('include', '/projects')

    })

    it('tests annotator UI permissions', () => {
        cy.visit("/login")

        cy.contains('Username').type('annotator')
        cy.contains('Password').type('testpassword')
        cy.get('form').contains('Sign In').click()
        cy.contains('Manage Users').should('not.exist')
        cy.contains('Projects').should('not.exist')
        cy.visit('/annotate')

    })

})
