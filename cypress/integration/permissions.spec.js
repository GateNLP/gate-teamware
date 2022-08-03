describe('User Interface Permissions Test', () => {

    beforeEach(()=>{
        // Run setup if needed
        if (Cypress.env('TESTENV') == 'container') {
            cy.exec('docker-compose exec -T backend ./migrate-integration.sh')
        }
        else{
            console.log("Printing test")
            cy.exec('npm run migrate:integration -- -n=create_db_users', {log:true})
        }
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

    it('Project page', () => {
        const projNameChange = "Test change project name"
        cy.visit("/login")

        cy.contains('Username').type('manager')
        cy.contains('Password').type('testpassword')
        cy.get('form').contains('Sign In').click()

        //Goes to projects page, create a project, change project name then see if
        //a new project has been created in project list
        cy.contains('Projects').click()
        cy.contains('Create project').click()
        cy.contains('Project')
        cy.get('input[name="project_name"]').type(projNameChange)
        cy.contains('Save').click()
        cy.contains('Projects').click()
        cy.contains(projNameChange)


    })
})
