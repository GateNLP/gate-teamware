import { projectsPageStr, adminUsername, password } from '../support/params.js';

describe('User Interface Permissions Test', () => {

    beforeEach(()=>{
        const fixtureName = 'create_db_users'
        cy.migrate_integration_db(fixtureName)
    })

    it('tests changing project name', () => {
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
        cy.get('input[name="project_name"]').clear().type(projNameChange)
        cy.contains('Save').click()
        cy.contains('Projects').click()
        cy.contains(projNameChange)

    })

    it('Test deleting project', () => {
        // Login through JSON request
        cy.login(adminUsername, password)

         cy.visit("/")

        // Goes to project page
        cy.contains(projectsPageStr).click()
        cy.get("h1").should("contain", projectsPageStr)

        // Create a project
        cy.contains("Create project").click()
        cy.get("h1").should("contain", "New project")

        // Checks the main project page
        cy.get("a").contains("Projects").click()
        cy.get("div[data-role='project_container']").should("exist")
        cy.get("a").contains("New project").click()

        // Delete the project
        cy.contains("Delete").click()
        cy.contains("Unlock").click()
        cy.get(".modal-dialog").within(()=>{
            cy.get("button").contains("Delete").click()
        })
        cy.contains("Project deleted").should("be.visible")

        cy.get("h1").should("contain", projectsPageStr)
        cy.get("div[data-role='project_container']").should("not.exist")


    })
})
