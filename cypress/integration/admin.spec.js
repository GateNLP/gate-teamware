import { adminUsername, password, manageUsersPageStr } from '../support/params.js';

describe("Test admin user management", () => {

    let newAnnotatorName = "ChangedAnnotatorName"
    let newAnnotatorEmail = "changedemail@test.com"
    let newPassword = "newpassword"
    let wrongPassword = "wrongPassword"

    beforeEach(() => {
        // Login through JSON request
        cy.login(adminUsername, password)


        // Go to the Manage users page
        cy.visit("/")
        cy.contains(manageUsersPageStr).click()

    })

    it('Change user (annotator) details', () => {


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