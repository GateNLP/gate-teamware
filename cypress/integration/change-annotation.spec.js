import { annotatorUsername, annotatorEmail, managerUsername, managerEmail, adminUsername, password } from '../support/params.js';

describe('Annotation Change Test in Project documents view and User My annotations view', () => {

    beforeEach(()=>{
        const fixtureName = "create_db_users_with_project_and_annotation"
        cy.migrate_integration_db(fixtureName)
    })

    it("Change annotation in My annotations", () => {
        cy.login(annotatorUsername, password)
        cy.visit("/")
        cy.get(".navbar").contains(annotatorUsername).click()
        cy.contains("My annotations").click()
        cy.get(".list-group-item").contains("Test project").click()
        cy.wait(500)
        cy.get('select[data-role="num-documents-select"]').first().select("100") // Show all documents
        cy.wait(500)


        cy.get("[data-role='annotation-display-container']").first().then(container => {
            //Change an annotation twice
            cy.wrap(container).contains("Change annotation").click()
            cy.wrap(container).contains("Negative").click()
            cy.wrap(container).contains("Submit").click()
            cy.wait(1000)
            cy.wrap(container).contains("Change annotation").click()
            cy.wrap(container).contains("Neutral").click()
            cy.wrap(container).contains("Submit").click()

            // Default annotation should be the latest
            cy.wrap(container).contains('"sentiment": "neutral"')


        })

        // Open up the history
        cy.contains("Show change history").click({force:true})

        // Should not have delete button
        cy.get("[data-role='annotation-change-delete']").should("not.exist")

        // It should show all annotations
        cy.get("[data-role='annotation-display-container']").first().then(container => {
            cy.wrap(container).contains('"sentiment": "positive"')
            cy.wrap(container).contains('"sentiment": "negative"')
            cy.wrap(container).contains('"sentiment": "neutral"')

        })

    })

    it("Change annotation in Project documents", () => {
        cy.login(managerUsername, password)
        cy.visit("/")
        cy.get(".navbar").contains("Projects").click()
        cy.contains("Test project").click()
        cy.contains("Documents & Annotations").click()
        cy.wait(500)
        cy.get('select[data-role="num-documents-select"]').first().select("100") // Show all documents
        cy.wait(500)

        cy.get("[data-role='annotation-display-container']").first().then(container => {
            //Change an annotation twice
            cy.wrap(container).contains("Change annotation").click()
            cy.wrap(container).contains("Negative").click()
            cy.wrap(container).contains("Submit").click()
            cy.wait(1000)

            cy.wrap(container).contains("Change annotation").click()
            cy.wrap(container).contains("Neutral").click()
            cy.wrap(container).contains("Submit").click()

            // Default annotation should be the latest
            cy.wrap(container).contains('"sentiment": "neutral"')


        })

        // Open up the history
        cy.contains("Show change history").click({force:true})

        // It should show all annotations
        cy.get("[data-role='annotation-display-container']").first().then(container => {
            cy.wrap(container).contains('"sentiment": "positive"')
            cy.wrap(container).contains('"sentiment": "negative"')
            cy.wrap(container).contains('"sentiment": "neutral"')

        })

    })

    it("Delete annotation in Project documents", () => {
        cy.login(managerUsername, password)
        cy.visit("/")
        cy.get(".navbar").contains("Projects").click()
        cy.contains("Test project").click()
        cy.contains("Documents & Annotations").click()
        cy.wait(500)
        cy.get('select[data-role="num-documents-select"]').first().select("100") // Show all documents
        cy.wait(500)

        cy.get("[data-role='annotation-display-container']").first().then(container => {
            //Change an annotation twice
            cy.wrap(container).contains("Change annotation").click()
            cy.wrap(container).contains("Negative").click()
            cy.wrap(container).contains("Submit").click()
            cy.wait(1000)
            cy.wrap(container).contains("Change annotation").click()
            cy.wrap(container).contains("Neutral").click()
            cy.wrap(container).contains("Submit").click()

            // Default annotation should be the latest
            cy.wrap(container).contains('"sentiment": "neutral"')


        })

        // Open up the history
        cy.contains("Show change history").click({force:true})

        // It should show all annotations
        cy.get("[data-role='annotation-display-container']").first().then(container => {
            cy.wrap(container).contains('"sentiment": "positive"')
            cy.wrap(container).contains('"sentiment": "negative"')
            cy.wrap(container).contains('"sentiment": "neutral"')
            cy.wrap(container).get("[data-role='annotation-change-delete']").first().click({force:true})

        })
        cy.wait(1000)
        cy.get(".modal-dialog .btn-danger").contains("Delete").click({force: true})
        cy.get(".modal-dialog").should("not.exist")
        cy.get("[data-role='annotation-display-container']").first().then(container => {
            cy.wrap(container).contains('"sentiment": "positive"').should("not.exist")
            cy.wrap(container).contains('"sentiment": "negative"')
            cy.wrap(container).contains('"sentiment": "neutral"')
        })

    })

})

describe('Annotation Change Test in Annotate view', () => {

    beforeEach(()=>{
        const fixtureName = "create_db_users_with_project_admin_is_annotator"
        cy.migrate_integration_db(fixtureName)
    })

    it("Change annotation in Annotate view", () => {
        cy.login(adminUsername, password)
        cy.visit("/")
        cy.get(".navbar").contains("Annotate").click()
        cy.contains("Start annotating").click()
        // All task navigation buttons should start disabled
        cy.contains("Previous task").should("be.disabled")
        cy.contains("Next task").should("be.disabled")
        cy.contains("Current task").should("be.disabled")

        // Complete first task
        cy.contains("Neutral").click()
        cy.contains("Submit").click()
        cy.wait(100)
        cy.contains("Previous task").should("be.enabled")
        cy.contains("Next task").should("be.disabled")
        cy.contains("Current task").should("be.disabled")

        // Complete second task
        cy.contains("Neutral").click()
        cy.contains("Submit").click()
        cy.wait(100)
        cy.contains("Previous task").should("be.enabled")
        cy.contains("Next task").should("be.disabled")
        cy.contains("Current task").should("be.disabled")

        // Go back to second task
        cy.contains("Previous task").click()
        cy.wait(100)
        cy.contains("Previous task").should("be.enabled")
        cy.contains("Next task").should("be.enabled")
        cy.contains("Current task").should("be.enabled")
        cy.contains("Negative").click()
        cy.contains("Submit").click()
        cy.contains("Annotation changed")

        // Go back to first task
        cy.contains("Previous task").click()
        cy.wait(100)
        cy.contains("Previous task").should("be.disabled")
        cy.contains("Next task").should("be.enabled")
        cy.contains("Current task").should("be.enabled")
        cy.contains("Positive").click()
        cy.contains("Submit").click()
        cy.contains("Annotation changed")

        // Forward to second task
        cy.contains("Next task").click()
        cy.wait(100)
        cy.get("input[type='radio'][value='negative']").should('be.checked')

        // Back again to first task
        cy.contains("Previous task").click()
        cy.wait(100)
        cy.get("input[type='radio'][value='positive']").should('be.checked')

        // Back to the latest task, should be blank
        cy.contains("Current task").click()
        cy.wait(100)
        cy.get("input[type='radio'][value='negative']").should('not.be.checked')
        cy.get("input[type='radio'][value='positive']").should('not.be.checked')
        cy.get("input[type='radio'][value='neutral']").should('not.be.checked')


    })

})
