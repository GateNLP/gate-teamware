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
     * Tests the entire annotation cycle including logging in, creating a project, configuring a project, upload
     * documents, add self as annotator and annotating something.
     */
    it('Test app annotation cycle', () => {
        // Login through JSON request
        cy.login("admin", "testpassword")

        cy.visit("/")

        // Goes to project page
        cy.contains("Projects").click()
        cy.get("h1").should("contain", "Projects")

        // Create a project
        cy.contains("Create project").click()
        cy.get("h1").should("contain", "New project")

        cy.contains("Improperly configured project").should("be.visible")

        // Change project name
        cy.get("input[name='project_name']").clear().type("New project name")

        // Change project id field
        cy.get("input[name='project_document_id_field']").clear().type("id")


        cy.get("[data-cy='editor']").type("{backspace}{backspace}{del}{del}")
        cy.fixture("project_config_sentiment.json").then((configObj) => {
            let outStr = JSON.stringify(configObj).replace(/([\{\}])/g, '{$1}')
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
    })

    describe("Test admin user management", () => {

        it('Change user (annotator) details', () => {
            // Login through JSON request
            cy.login("admin", "testpassword")

            let newAnnotatorName = "annotatornamechanged"
            let newAnnotatorEmail = "annotatormail@changed.com"


            // Go to the Manage users page
            cy.visit("/")
            cy.contains("Manage Users").click()


            // Form should be empty
            cy.get("input[name='username']").should("be.empty")
            cy.get("input[name='email']").should("be.empty")
            cy.get("input[name='manager_checkbox']").should("not.be.checked")
            cy.get("input[name='admin_checkbox']").should("not.be.checked")


            // Select the annotator user
            cy.contains("annotator").click()

            // Change annotator details
            cy.get("input[name='username']").clear().type(newAnnotatorName)
            cy.get("input[name='email']").clear().type(newAnnotatorEmail)
            cy.get("input[name='manager_checkbox']").check({force: true})
            cy.get("input[name='admin_checkbox']").check({force: true})


            cy.contains("Save").click()
            cy.contains("User details saved").should("be.visible")

            // Make sure the user's list on the left is updated
            cy.get("#users").within(() => {
                cy.contains(newAnnotatorName)
            })

            // Check value persists after reload
            cy.reload()
            cy.contains(newAnnotatorName).click()
            cy.get("input[name='username']").should("have.value", newAnnotatorName)
            cy.get("input[name='email']").should("have.value", newAnnotatorEmail)
            cy.get("input[name='manager_checkbox']").should("be.checked")
            cy.get("input[name='admin_checkbox']").should("be.checked")
        })

        it("Change password wrong confirmation", () => {
            // Login through JSON request
            cy.login("admin", "testpassword")

            let newPassword = "newpassword"
            let wrongPassword = "wrongPassword"

            // Go to the Manage users page
            cy.visit("/")
            cy.contains("Manage Users").click()

            // Password field should be empty
            cy.get("input[name='password']").should("be.empty")
            cy.get("input[name='password_confirm']").should("be.empty")

            // Select the annotator user
            cy.contains("annotator").click()

            // Using wrong confirmation password
            cy.get("input[name='password']").clear().type(newPassword)
            cy.get("input[name='password_confirm']").clear().type(wrongPassword)

            cy.contains("Change Password").click()
            cy.contains("Password does not match").should("be.visible")

        })

        it("Change password right confirmation", () => {
            // Login through JSON request
            cy.login("admin", "testpassword")

            let newPassword = "newpassword"
            let wrongPassword = "wrongPassword"

            // Go to the Manage users page
            cy.visit("/")
            cy.contains("Manage Users").click()

            // Password field should be empty
            cy.get("input[name='password']").should("be.empty")
            cy.get("input[name='password_confirm']").should("be.empty")

            // Select the annotator user
            cy.contains("annotator").click()

            // Using right confirmation password
            cy.get("input[name='password']").clear().type(newPassword)
            cy.get("input[name='password_confirm']").clear().type(newPassword)

            cy.contains("Change Password").click()
            cy.contains("User password changed").should("be.visible")

        })

    })


})
