import {adminUsername, annotatePageStr, password, projectsPageStr} from "../support/params";

describe('Pre annotation test', () => {

    beforeEach(() => {
        const fixtureName = 'create_db_users_with_project_admin_is_annotator'
        cy.migrate_integration_db(fixtureName)
    })

    it('Test turning pre-annotation on and off ', () => {
        // Login through JSON request
        cy.login(adminUsername, password)

        cy.visit("/")

        // There shouldn't be any pre-annotation initially
        cy.contains(annotatePageStr).click()
        cy.contains("Start annotating").click()
        cy.get("input[name='sentiment'][value='positive']").should("not.be.checked")
        cy.get("input[name='sentiment'][value='negative']").should("not.be.checked")
        cy.get("input[name='sentiment'][value='neutral']").should("not.be.checked")

        // Turn on pre-annotation
        cy.contains(projectsPageStr).click()
        cy.get("a").contains("Test project").click()
        cy.get("input[name='pre-annotation-field']").clear().type("preanno")
        cy.contains("Save").click()

        cy.contains(annotatePageStr).click()
        cy.contains("Start annotating").click()

        for(let i = 0 ; i < 2; i++){
            // Should have have pre-annotation as positive
            cy.get("input[name='sentiment'][value='positive']").should("be.checked")
            cy.get("input[name='sentiment'][value='negative']").should("not.be.checked")
            cy.get("input[name='sentiment'][value='neutral']").should("not.be.checked")
            cy.contains("Submit").click()
        }

        // Turn off pre-annotation
        cy.contains(projectsPageStr).click()
        cy.get("a").contains("Test project").click()
        cy.wait(500) //Wait for page load
        cy.get("input[name='pre-annotation-field']").clear()
        cy.contains("Save").click()
        // Make sure the pre-annotation field is actually empty
        cy.contains(projectsPageStr).click()
        cy.get("a").contains("Test project").click()
        cy.wait(500) //Wait for page load
        cy.get("input[name='pre-annotation-field']").should("be.empty")

        // Pre-annotations should now be turned off when pre-annotation field is cleared
        cy.contains(annotatePageStr).click()
        cy.get("input[name='sentiment'][value='positive']").should("not.be.checked")
        cy.get("input[name='sentiment'][value='negative']").should("not.be.checked")
        cy.get("input[name='sentiment'][value='neutral']").should("not.be.checked")




    })

})
