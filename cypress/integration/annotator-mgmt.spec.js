describe('Annotator Management Test', () => {

    let projectsPageStr = "Projects"
    let adminUsername = "admin"
    let adminEmail = "admin@test.com"
    let password = "testpassword"

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
