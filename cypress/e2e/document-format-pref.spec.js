import {adminUsername, password} from "../support/params";

describe("Tests for document format preference changes", () => {
    beforeEach(()=>{
        const fixtureName = "create_db_users_with_project_and_annotation"
        cy.migrate_integration_db(fixtureName)
    })

    it("Test JSON doc format display", () => {
        // Login and set preference to JSON
        cy.login(adminUsername, password)
        cy.visit("/")
        cy.get(".navbar").contains(adminUsername).click()
        cy.contains("Account").click()
        cy.contains("JSON").click()

        //Check project config
        cy.contains("Projects").click()
        cy.contains("Test project").click()
        cy.contains("Documents & Annotations").click()
        cy.get("[data-role='annotation-display-json']").should("have.length.above", 0)
        cy.get("[data-role='annotation-display-csv']").should("have.length.below", 1)

        //Check user annotations
        cy.get(".navbar").contains(adminUsername).click()
        cy.contains("My annotations").click()
        cy.contains("Test project").click()
        cy.get("[data-role='annotation-display-json']").should("have.length.above", 0)
        cy.get("[data-role='annotation-display-csv']").should("have.length.below", 1)


    })

    it("Test CSV doc format display", () => {
        // Login and set preference to JSON
        cy.login(adminUsername, password)
        cy.visit("/")
        cy.get(".navbar").contains(adminUsername).click()
        cy.contains("Account").click()
        cy.contains("CSV").click()

        //Check project config
        cy.contains("Projects").click()
        cy.contains("Test project").click()
        cy.contains("Documents & Annotations").click()
        cy.get("[data-role='annotation-display-csv']").should("have.length.above", 0)
        cy.get("[data-role='annotation-display-json']").should("have.length.below", 1)

        //Check user annotations
        cy.get(".navbar").contains(adminUsername).click()
        cy.contains("My annotations").click()
        cy.contains("Test project").click()
        cy.get("[data-role='annotation-display-csv']").should("have.length.above", 0)
        cy.get("[data-role='annotation-display-json']").should("have.length.below", 1)

    })

    it.only("Test CSV project config document preview", () =>{
        // Login and set preference to JSON
        cy.login(adminUsername, password)
        cy.visit("/")
        cy.get(".navbar").contains(adminUsername).click()
        cy.contains("Account").click()
        cy.wait(1000)
        cy.contains("CSV").click()
        cy.wait(1000)

        cy.contains("Projects").click()
        cy.contains("Test project").click()
        //Upload test csv
        cy.get('[data-cy="csv-display-file-input"]').attachFile('document_flat.csv')
        //Should have already selected the first row and value displayed in the
        //annotation renderer output
        cy.get('[data-cy="annotation-renderer"]').contains("Test 1 csv")
        //Test selecting the second row
        cy.contains("Test 2 csv").click()
        cy.get('[data-cy="annotation-renderer"]').contains("Test 2 csv")
        //Test annotation output is displayed as a table
        cy.get('[data-cy="annotation-renderer"]').contains("Neutral").click()
        cy.get('[data-role="annotation-output-csv"]').contains("neutral")
    })


})
