import { projectsPageStr, annotatePageStr, adminUsername, password } from '../support/params.js';

describe('Annotation tests', () => {

    beforeEach(() => {
        const fixtureName = 'create_db_users'
        cy.migrate_integration_db(fixtureName)
    })

    /**
     * Tests the entire annotation cycle including logging in, creating a project, configuring a project, upload
     * documents, add self as annotator and annotating something.
     */
    it('Test app annotation cycle', () => {
        // Login through JSON request
        cy.login( adminUsername, password)

        cy.visit("/")

        // Goes to project page
        cy.contains(projectsPageStr).click()
        cy.get("h1").should("contain", projectsPageStr)

        // Create a project
        cy.contains("Create project").click()
        cy.get("h1").should("contain", "New project")

        cy.contains("Improperly configured project").should("be.visible")

        // Change project name
        let newProjectName = "New project name";
        cy.get("input[name='project_name']").clear().type(newProjectName)

        // Change project id field
        cy.get("input[name='project_document_id_field']").clear().type("id")

        // Change project annotation config
        cy.get("[data-cy='editor']").type("{backspace}{backspace}{del}{del}")
        cy.fixture("project_config_sentiment.json").then((configObj) => {
            let outStr = JSON.stringify(configObj).replace(/([\{\}])/g, '{$1}')
            cy.get("[data-cy='editor']").type(outStr)
        })
        cy.contains("Save").click()

        // Upload documents to project
        cy.contains("Documents & Annotations").click()
        cy.contains("Upload").click()
        cy.get(".modal-dialog").get('[data-cy="file-input"]').attachFile('documents_20_items.json')
        cy.get(".modal-dialog button").contains("Upload").click()
        cy.get(".modal-dialog button").contains("Close").click()

        // Add admin user as annotator
        cy.contains("Annotators").click()
        cy.get(".btn").contains("+ Add annotators").click()
        cy.get(".list-group-item").contains("admin").click()
        cy.get(".btn").contains("OK").click()

        cy.contains("Improperly configured project").should("not.exist")

        //Check project name changed in project list
        cy.contains(projectsPageStr).click()
        cy.contains("New project name")


        //Check can annotate
        cy.contains(annotatePageStr).click()
        cy.contains("New project name")
        cy.contains("Start annotating").click()

        // Check tooltip prompt is visible, hovers aren't supported in cypress, see: https://docs.cypress.io/api/commands/hover
        cy.get('.annotation-help-prompt').should('be.visible')

        cy.contains("Negative").click()
        cy.contains("Submit").click()

        //Check annotation exists in documents list
        cy.contains(projectsPageStr).click()
        cy.contains("New project name").click()
        cy.contains("Documents & Annotations").click()
        cy.wait(500)
        cy.get('select[data-role="num-documents-select"]').first().select("100") // Show all documents
        cy.wait(500)
        cy.get("[data-role='annotation-display-container']").first().contains(adminUsername)

        //Check annotation exists in user profile
        cy.get(".navbar").contains(adminUsername).click()
        cy.contains("My annotations").click()
        cy.wait(500)
        cy.contains(newProjectName).click()
        cy.wait(500)
        cy.get('select[data-role="num-documents-select"]').first().select("100") // Show all documents
        cy.wait(500)
        cy.get("[data-role='annotation-display-container']").first().contains(adminUsername)
    })

    /**
     * Tests the entire annotation cycle including logging in, creating a project, configuring a project, upload
     * documents, add self as annotator and annotating something.
     */
    it('Test annotator training and test', () => {
        // Login through JSON request
        cy.login(adminUsername, password)

        cy.visit("/")

        // Goes to project page
        cy.contains(projectsPageStr).click()
        cy.get("h1").should("contain", projectsPageStr)

        // Create a project
        cy.contains("Create project").click()
        cy.get("h1").should("contain", "New project")

        cy.contains("Improperly configured project").should("be.visible")

        // Change project name
        let newProjectName = "New project name";
        cy.get("input[name='project_name']").clear().type(newProjectName)

        // Change project id field
        cy.get("input[name='project_document_id_field']").clear().type("id")

        // Change project annotation config
        cy.get("[data-cy='editor']").type("{backspace}{backspace}{del}{del}")
        cy.fixture("project_config_sentiment.json").then((configObj) => {
            let outStr = JSON.stringify(configObj).replace(/([\{\}])/g, '{$1}')
            cy.get("[data-cy='editor']").type(outStr)
        })

        // Enable training and test modes
        cy.get("label[for='project-has-training-stage']").click()
        cy.contains("Training stage enabled").should("be.visible")
        cy.get("label[for='project-has-testing-stage']").click()
        cy.contains("Testing stage enabled").should("be.visible")
        cy.contains("Save").click()

        cy.contains("Can annotate after passing").should("be.visible")

        // Upload documents to project
        cy.contains("Documents & Annotations").click()
        cy.get("[title='Upload documents'").filter(':visible').click()
        cy.get(".modal-dialog").get('[data-cy="file-input"]').attachFile('documents_20_items.json')
        cy.get(".modal-dialog button").contains("Upload").click()
        cy.get(".modal-dialog button").contains("Close").click()

        // Upload training documents
        cy.contains("Training Documents").click()
        cy.get("[title='Upload documents'").filter(':visible').click()
        cy.get(".modal-dialog").get('[data-cy="file-input"]').attachFile('training_document.json')
        cy.get(".modal-dialog button").contains("Upload").click()
        cy.get(".modal-dialog button").contains("Close").click()

        // Upload test documents
        cy.contains("Testing Documents").click()
        cy.get("[title='Upload documents'").filter(':visible').click()
        cy.get(".modal-dialog").get('[data-cy="file-input"]').attachFile('test_document.json')
        cy.get(".modal-dialog button").contains("Upload").click()
        cy.get(".modal-dialog button").contains("Close").click()

        // Add admin user as annotator
        cy.contains("Annotators").click()
        cy.get(".btn").contains("+ Add annotators").click()
        cy.get(".list-group-item").contains("admin").click()
        cy.get(".btn").contains("OK").click()
        
        cy.contains("Improperly configured project").should("not.exist")
        
        //Check project name changed in project list
        cy.contains(projectsPageStr).click()
        cy.contains("New project name")

        //Check training mode functioning
        cy.contains(annotatePageStr).click()
        cy.contains("New project name")
        cy.contains("Training stage")
        cy.contains("Start annotating").click()
        cy.contains("Negative").click()
        cy.contains("Incorrect").should("be.visible")
        cy.contains("Example explanation").should("be.visible")
        cy.contains("Positive").click()
        cy.contains("Correct").should("be.visible")
        cy.contains("Example explanation").should("be.visible")
        cy.contains("Submit").click()

        // Check test mode begins after training complete
        cy.contains(annotatePageStr).click()
        cy.contains("New project name")
        cy.contains("Test stage")
        cy.contains("Start annotating").click()
        cy.contains("Negative").click()
        cy.contains("Incorrect").should("not.exist")
        cy.contains("Example explanation").should("not.exist")
        cy.contains("Positive").click()
        cy.contains("Correct").should("not.exist")
        cy.contains("Example explanation").should("not.exist")
        cy.contains("Submit").click()

        //Check can annotate
        cy.contains(annotatePageStr).click()
        cy.contains("New project name")
        cy.contains("Start annotating").click()
        cy.contains("Negative").click()
        cy.contains("Submit").click()

        //Check annotation exists in documents list
        cy.contains(projectsPageStr).click()
        cy.contains("New project name").click()
        cy.contains("Documents & Annotations").click()
        cy.wait(500)
        cy.get('select[data-role="num-documents-select"]').first().select("100") // Show all documents
        cy.wait(500)
        cy.get("[data-role='annotation-display-container']").first().contains(adminUsername)

        //Check annotation exists in user profile
        cy.get(".navbar").contains(adminUsername).click()
        cy.contains("My annotations").click()
        cy.wait(500)
        cy.get(".list-group", {timeout: 8000}).contains(newProjectName).click()
        cy.wait(500)
        cy.get('select[data-role="num-documents-select"]').first().select("100") // Show all documents
        cy.wait(500)
        cy.get("[data-role='annotation-display-container']").first().contains(adminUsername)
    })


})
