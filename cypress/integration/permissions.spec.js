describe('User Interface Permissions Test', () => {

    beforeEach(()=>{
        cy.exec('npm run migrate:integration')
    })

    it('logs in as admin and attempts user management', () => {
        cy.visit("/login")

        cy.contains('Username').type('admin')
        cy.contains('Password').type('testpassword')
        cy.get('form').contains('Sign In').click()

        cy.contains('Manage Users')
    })

    // it('Project page', () => {
    //     const projNameChange = "Test change project name"
    //     cy.visit("/")

    //     //Goes to projects page, create a project, change project name then see if
    //     //a new project has been created in project list
    //     cy.contains('Projects').click()
    //     cy.contains('Create project').click()
    //     cy.contains('Project')
    //     cy.get('input[name="project_name"]').type(projNameChange)
    //     cy.contains('Save').click()
    //     cy.contains('Projects').click()
    //     cy.contains(projNameChange)


    // })
})
