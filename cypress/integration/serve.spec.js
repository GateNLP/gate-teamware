describe('Site serve test', () => {

    beforeEach(() => {
        // Run setup if needed
        if (Cypress.env('TESTENV') == 'container') {
            cy.exec('docker-compose exec -T backend ./migrate-integration.sh')
        } else {
            cy.exec('npm run migrate:integration')
        }

    })

    it('About page', () => {
        cy.visit("/")
        cy.contains('About').click()
        cy.contains('About GATE Annotate')
        expect(true).to.equal(true) // Example assert
        cy.contains('TEAMWARE')
    })

    /**
     * Tests the entire annotation cycle including loggin in, creating a project, configuring a project, upload
     * documents, add self as annotator and annotating something.
     */
    it('Test app annotation cycle', () => {
        cy.login("admin", "testpassword").then((response) => {
            cy.visit("/")

            // Goes to project page
            cy.contains("Projects").click()
            cy.get("h1").should("contain", "Projects")

            // Create a project
            cy.contains("Create project").click()
            cy.get("h1").should("contain", "New project")

            cy.contains("Improperly configured project")

            // Change project name
            cy.get("input[name='project_name']").clear().type("New project name")

            // Chagne project id field
            cy.get("input[name='project_document_id_field']").clear().type("id")


            cy.get("[data-cy='editor']").type("{backspace}{backspace}{del}{del}")
            cy.fixture("project_config_sentiment.json").then((configObj) => {
                let outStr = JSON.stringify(configObj).replace(/([\{\}])/g,'{$1}')
                cy.get("[data-cy='editor']").type(outStr)
                cy.contains("Save").click()

                // Change project prop
                cy.contains("Documents & Annotations").click()
                cy.contains("Upload").click()
                cy.get(".modal-dialog").get('[data-cy="file-input"]').attachFile('documents_20_items.json')
                cy.get(".modal-dialog button").contains("Upload").click()
                cy.get(".modal-dialog button").contains("Close").click()

                // Add admin user as annotator
                cy.contains("Annotators").click()
                cy.get("h2").contains("Annotators Management").parent().contains("admin").click()

                cy.contains("Improperly configured project").should("not.exist")

                //Check project name changed in project list
                cy.contains("Projects").click()
                cy.contains("New project name")


                //Check can annotate
                cy.contains("Annotate").click()
                cy.contains("New project name")
                cy.contains("Document 1")
                cy.contains("Negative").click()
                cy.contains("Submit").click()
                cy.contains("Document 2")

                //Check annotation exists in documents list
                cy.contains("Projects").click()
                cy.contains("New project name").click()
                cy.contains("Documents & Annotations").click()
                cy.wait(500)
                cy.get("[data-role='annotation-display-container']").first().contains("admin")

            })

            }
        )
    })

})
