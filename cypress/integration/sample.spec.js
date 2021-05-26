describe('My First Test', () => {

    beforeEach(() => {
        // Run setup if needed
        cy.exec('npm run migrate:integration')
    })

    it('About page', () => {
        cy.visit("/")

        cy.contains('GATE Annotation Tool')
        cy.contains('About').click()
        cy.contains('This is an about page')
        expect(true).to.equal(true) // Example assert
    })

    it('Project page', () => {
        const projNameChange = "Test change project name"
        cy.visit("/")

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
