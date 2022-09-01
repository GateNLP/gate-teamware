describe('Annotator Management Test', () => {

    let projectsPageStr = "Projects"
    let adminUsername = "admin"
    let adminEmail = "admin@test.com"
    let password = "testpassword"

    beforeEach(()=>{
        // Run setup if needed
        if (Cypress.env('TESTENV') == 'container') {
            cy.exec('docker-compose exec -T backend ./migrate-integration.sh -n=project_with_annotators')
        } else if (Cypress.env('TESTENV') == 'ci') {
            cy.exec('DJANGO_SETTINGS_MODULE=teamware.settings.deployment docker-compose exec -T backend ./migrate-integration.sh -n=project_with_annotators')
        }
        else{
            cy.exec('npm run migrate:integration -- -n=project_with_annotators', {log:true})
        }

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
        cy.contains('Select all')
        

        // TODO reject annotator and confirm rejected
        // TODO make annotator active and confirm
        
    })
})
