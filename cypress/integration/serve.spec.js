describe('Site serve test', () => {

    beforeEach(() => {
        // Run setup if needed
        cy.exec('npm run migrate:integration')
    })

    it('About page', () => {
        cy.visit("/")

        cy.contains('GATE Annotation Tool')
        cy.contains('About').click()
        cy.contains('About GATE Annotate')
        expect(true).to.equal(true) // Example assert
    })

})
