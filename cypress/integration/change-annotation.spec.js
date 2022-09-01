describe('Annotation Change Test', () => {

    let annotatorUsername = "annotator"
    let annotatorEmail = "annotator@test.com"

    let managerUsername = "manager"
    let managerEmail = "manager@test.com"

    let adminUsername = "admin"
    let adminEmail = "admin@test.com"
    let password = "testpassword"

    beforeEach(()=>{
        // Run setup if needed
        if (Cypress.env('TESTENV') == 'container') {
            cy.exec('docker-compose exec -T backend ./migrate-integration.sh -n=create_db_users_with_project_and_annotation')
        } else if (Cypress.env('TESTENV') == 'ci') {
            cy.exec('DJANGO_SETTINGS_MODULE=teamware.settings.deployment docker-compose exec -T backend ./migrate-integration.sh -n=create_db_users_with_project_and_annotation')
        }
        else{
            cy.exec('npm run migrate:integration -- -n=create_db_users_with_project_and_annotation', {log:true})
        }
    })

    it("Change annotation in My annotations", () => {
        cy.login(annotatorUsername, password)
        cy.visit("/")
        cy.get(".navbar").contains(annotatorUsername).click()
        cy.contains("My annotations").click()
        cy.get(".list-group-item").contains("Test project").click()


        cy.get("[data-role='annotation-display-container']").first().then(container => {
            //Change an annotation twice
            cy.wrap(container).contains("Change annotation").click()
            cy.wrap(container).contains("Negative").click()
            cy.wrap(container).contains("Submit").click()
            cy.wait(1001)
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

        cy.get("[data-role='annotation-display-container']").first().then(container => {
            //Change an annotation twice
            cy.wrap(container).contains("Change annotation").click()
            cy.wrap(container).contains("Negative").click()
            cy.wrap(container).contains("Submit").click()

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
