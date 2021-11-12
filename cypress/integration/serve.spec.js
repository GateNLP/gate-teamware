describe('Site serve test', () => {

    beforeEach(() => {
        // Run setup if needed
        if (Cypress.env('TESTENV') == 'dev'){
            cy.exec('npm run migrate:integration')
        } else if (Cypress.env('TESTENV') == 'container') {
            cy.exec('docker-compose exec -T backend ./migrate-integration.sh')
        }
    })

    it('About page', () => {
        cy.visit("/")

        cy.contains('GATE Annotation Tool')
        cy.contains('About').click()
        cy.contains('About GATE Annotate')
        expect(true).to.equal(true) // Example assert
    })

})
