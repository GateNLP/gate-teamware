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

})
