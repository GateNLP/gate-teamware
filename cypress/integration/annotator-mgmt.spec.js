import { projectsPageStr, adminUsername, password } from '../support/params.js';

describe('Annotator Leaving Test', () => {
    
    beforeEach(()=>{
        const fixtureName = 'create_db_users_with_project_admin_is_annotator'
        cy.migrate_integration_db(fixtureName)
        cy.login(adminUsername, password)
    })
    
    it('Tests annotator leaving project', () => {
        cy.visit("/annotate")
        cy.contains('Leave project').click()
        cy.contains('Unlock').click()
        cy.get(".modal-dialog button").contains('Leave project').click()
        cy.visit("/annotate")
        cy.get("h1").should("contain", "Nothing to annotate")
    })

    it('Tests annotator being removed from project', () => {
        cy.visit("/projects")

        cy.contains('Test project').click()

        // Go to annotator management tab
        cy.contains('Annotators').click()

        // Verify that annotator table is present
        cy.get('table').contains('td', 'annotator').should('be.visible');

        // Mark annotator as completed
        cy.contains('td', 'admin')
            .siblings().contains('Complete')
            .click()

        cy.contains('td', 'admin')
            .siblings().should('contain','Completed')

        // Create a new project
        cy.visit("/project/1")
        cy.contains('Clone project').click()
        cy.wait(1) // wait for DOM to render after cloning
        cy.contains('Documents & Annotations').click()
        cy.contains("Upload").click()
        cy.get(".modal-dialog").get('[data-cy="file-input"]').attachFile('documents_20_items.json')
        cy.get(".modal-dialog button").contains("Upload").click()
        cy.get(".modal-dialog button").contains("Close").click()

        // Go to annotator management tab
        cy.contains('Annotators').click()

        cy.get(".btn").contains("+ Add annotators").click()
        cy.get(".list-group-item").contains("admin").click()
        cy.get(".btn").contains("OK").click()

        cy.contains('td', 'admin')
            .siblings().should('contain','Annotating')

    })

})

describe('Annotator Management Test', () => {

    beforeEach(()=>{
        const fixtureName = 'project_with_annotators'
        cy.migrate_integration_db(fixtureName)
        cy.login(adminUsername, password)
    })

    it('Tests annotator management view', () => {

        cy.visit("/")

        // Goes to project page
        cy.contains(projectsPageStr).click()
        cy.get("h1").should("contain", projectsPageStr)

        cy.contains('Test project').click()

        // Go to annotator management tab
        cy.contains('Annotators').click()
        
        // Verify that annotator table is present
        cy.get('table').contains('td', 'annotator').should('be.visible');
        
        // Verify that without selections, batch button actions are not active
        cy.get('.btn-group').contains('Make annotator').should('be.disabled')
        cy.get('.btn-group').contains('Make active').should('be.disabled')
        cy.get('.btn-group').contains('Complete').should('be.disabled')
        cy.get('.btn-group').contains('Reject').should('be.disabled')

        // Verify that to start with, no users are selected
        cy.get('tr')
            .siblings()
            .contains("[aria-selected=true]")
            .should('not.exist')
        
        // select all and verify all are selected
        cy.get('.btn').contains('Select all').click()
        cy.get('tr')
            .siblings()
            .contains("[aria-selected=false]")
            .should('not.exist')

        // clear selection and verify none are selected
        cy.get('.btn').contains('Clear selected').click()
        cy.get('tr')
            .siblings()
            .contains("[aria-selected=true]")
            .should('not.exist')

        // test batch action
        cy.contains('td', 'trainer').click()
        cy.contains('td', 'tester').click()
        cy.get('.btn-group').contains('Make annotator').should('not.be.disabled').click()
        cy.contains('td', 'trainer')
            .siblings().contains('Annotating')
        cy.contains('td', 'tester')
            .siblings().contains('Annotating')

        cy.contains('td', 'completer')
            .siblings().contains('Complete')
            .click()
        cy.contains('td', 'completer')
            .siblings().should('contain','Completed')

        // reject annotator and confirm rejected
        cy.contains('td', 'failer')  // gives you the cell 
            .siblings()              // gives you all the other cells in the row
            .contains('Reject')      // finds the button
            .click()
        cy.contains('td', 'failer').siblings().contains('Rejected')
            
        // make annotator active and confirm
        cy.contains('td', 'failer')
            .siblings()
            .contains('Make active')
            .click()
        cy.contains('td', 'failer').siblings().should('contain','Waiting')

        // make annotator and confirm
        cy.contains('td', 'failer')
            .siblings()
            .contains('Make annotator')
            .click()
        cy.contains('td', 'failer').siblings().should('contain','Annotating')
        
    })
})
