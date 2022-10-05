import { projectsPageStr, annotatePageStr, manageUsersPageStr, documentationPageStr, aboutPageStr, signInPageStr, registerPageStr,
    annotatorAccessLevel, managerAccessLevel, adminAccessLevel,
    annotatorUsername, managerUsername, adminUsername, annotatorEmail, password } from '../support/params.js';

describe('User Registration Test', () => {

    beforeEach(()=>{
        const fixtureName = 'create_db_users'
        cy.migrate_integration_db(fixtureName)
    })

    it('registers a user', () => {
        cy.visit("/register")

        cy.contains('Register')
        cy.contains('Username').type('tester')
        cy.contains('Email').type('test@test.com')
        cy.contains('Password').type('123456')
        cy.contains('Confirm Password').type('123456')
        cy.get('form').contains('Register').click()
        cy.contains('TEAMWARE')
    })

    it('tests password mismatch', () => {
        cy.visit("/register")

        cy.contains('Register')
        cy.contains('Password').type('123456')
        cy.contains('Confirm Password').type('789')
        cy.get('form').contains('Register').click()
        cy.contains('Password must match')
        })

    it('tests username in use error', () => {
        cy.visit("/register")
    
        cy.contains('Username').type('annotator')
        cy.contains('Email').type('annotator@test.com')
        cy.contains('Password').type('123456')
        cy.contains('Confirm Password').type('123456')
        cy.get('form').contains('Register').click()
        cy.contains('Username already exists')
        })
})



describe('User options', () => {


    beforeEach(() => {
        const fixtureName = 'create_db_users'
        cy.migrate_integration_db(fixtureName)
    })

    it('About page', () => {
        cy.visit("/")
        cy.contains('About').click()
        cy.contains('About GATE Annotate')
        expect(true).to.equal(true) // Example assert
        cy.contains('TEAMWARE')
    })

    function loggedOutCheck() {
        cy.get("a").contains(projectsPageStr).should("not.exist")
        cy.get("a").contains(annotatePageStr).should("not.exist")
        cy.get("a").contains(manageUsersPageStr).should("not.exist")
        cy.get("a").contains(documentationPageStr)
        cy.get("a").contains(aboutPageStr)
        cy.get("a").contains(signInPageStr)
        cy.get("a").contains(registerPageStr)

    }

    function loggedInCheck(username, accessLevel) {
        cy.get("a").contains(projectsPageStr).should(accessLevel >= managerAccessLevel ? "exist" : "not.exist")
        cy.get("a").contains(annotatePageStr).should(accessLevel >= annotatorAccessLevel ? "exist" : "not.exist")
        cy.get("a").contains(manageUsersPageStr).should(accessLevel >= adminAccessLevel ? "exist" : "not.exist")
        cy.get("a").contains(documentationPageStr)
        cy.get("a").contains(aboutPageStr)
        cy.get("a").contains(signInPageStr).should("not.exist")
        cy.get("a").contains(registerPageStr).should("not.exist")
        cy.get("a").contains(username)
    }


    it("Test access when not logged in", () => {
        cy.visit("/")
        loggedOutCheck()
    })

    it("Test access when logged in as annotator and then logging out", () => {
        cy.login(annotatorUsername, password)
        cy.visit("/")
        loggedInCheck(annotatorUsername, annotatorAccessLevel)
        cy.contains(annotatorUsername).click()
        cy.contains("Sign Out").click()
        loggedOutCheck()
    })

    it("Test access when logged in as manager", () => {
        cy.login(managerUsername, password)
        cy.visit("/")
        loggedInCheck(managerUsername, managerAccessLevel)
        cy.contains(managerUsername).click()
        cy.contains("Sign Out").click()
        loggedOutCheck()
    })

    it("Test access when logged in as admin", () => {
        cy.login(adminUsername, password)
        cy.visit("/")
        loggedInCheck(adminUsername, adminAccessLevel)
        cy.contains(adminUsername).click()
        cy.contains("Sign Out").click()
        loggedOutCheck()
    })

    describe("Test user account page", () => {

        beforeEach(()=>{
            cy.login(annotatorUsername, password)
            cy.visit("/")
            cy.contains(annotatorUsername).click()
            cy.contains("Account").click()

        })

        it("Check account page items", () => {

            cy.contains("Username").parent().contains(annotatorUsername)
            cy.contains("User Role").parent().contains("annotator")
            cy.contains("Email").parent().contains(annotatorEmail)
            cy.contains("Email").parent().within(() => {
                cy.get("a")
            })
            cy.contains("Joined")
            cy.contains("Password").parent().within(()=>{
                cy.get("a")
            })
        })

        it("Test changing email", ()=>{
            let changedEmail = "changed@test.com"
            cy.contains("Email").parent().within(() => {
                cy.get("a").click()
            })
            cy.contains("Change Email")
            cy.get("input[name='email_change'").clear().type(changedEmail)
            cy.contains("Submit").click()
            cy.contains(changedEmail)


        })

        it("Test changing user password", ()=>{
            let changedPassword = "newchangedpassword"
            cy.contains("Password").parent().within(()=>{
                cy.get("a").click()
            })

            cy.get("input[name='password']").clear().type(changedPassword)
            cy.get("input[name='password_confirm']").clear().type(changedPassword)
            cy.contains("Change Password").click()

            //Logout
            cy.contains(annotatorUsername).click()
            cy.contains("Sign Out").click()

            //Login with old password (should fail)
            cy.login(annotatorUsername, password, false)
            cy.reload()
            cy.contains(annotatorUsername).should("not.exist")

            // Login with new password
            cy.login(annotatorUsername, changedPassword)
            cy.reload()
            cy.contains(annotatorUsername)

        })

    })
})