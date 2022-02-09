describe('Site serve test', () => {

    let projectsPageStr = "Projects"
    let annotatePageStr = "Annotate"
    let manageUsersPageStr = "Manage Users"
    let documentationPageStr = "Documentation"
    let aboutPageStr = "About"
    let signInPageStr = "Sign In"
    let registerPageStr = "Register"
    let annotatorAccessLevel = 1
    let managerAccessLevel = 2
    let adminAccessLevel = 3

    let annotatorUsername = "annotator"
    let annotatorEmail = "annotator@test.com"

    let managerUsername = "manager"
    let managerEmail = "manager@test.com"

    let adminUsername = "admin"
    let adminEmail = "admin@test.com"
    let password = "testpassword"

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

    describe("Test user profile page", () => {

        beforeEach(()=>{
            cy.login(annotatorUsername, password)
            cy.visit("/")
            cy.contains(annotatorUsername).click()
            cy.contains("Profile").click()

        })

        it("Check profile page items", () => {

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

        it("Test changign email", ()=>{
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


    /**
     * Tests the entire annotation cycle including logging in, creating a project, configuring a project, upload
     * documents, add self as annotator and annotating something.
     */
    it.only('Test app annotation cycle', () => {
        // Login through JSON request
        cy.login("admin", "testpassword")

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
        cy.get("h2").contains("Annotators Management").parent().contains("admin").click()

        cy.contains("Improperly configured project").should("not.exist")

        //Check project name changed in project list
        cy.contains(projectsPageStr).click()
        cy.contains("New project name")


        //Check can annotate
        cy.contains(annotatePageStr).click()
        cy.contains("New project name")
        cy.contains("Negative").click()
        cy.contains("Submit").click()

        //Check annotation exists in documents list
        cy.contains(projectsPageStr).click()
        cy.contains("New project name").click()
        cy.contains("Documents & Annotations").click()
        cy.wait(500)
        cy.get("[data-role='annotation-display-container']").first().contains(adminUsername)

        //Check annotation exists in user profile
        cy.get("a").contains(adminUsername).click()
        cy.contains("Profile").click()
        cy.contains(newProjectName)
        cy.get("[data-role='annotation-display-container']").first().contains(adminUsername)
    })

    describe("Test admin user management", () => {

        let newAnnotatorName = "ChangedAnnotatorName"
        let newAnnotatorEmail = "changedemail@test.com"
        let newPassword = "newpassword"
        let wrongPassword = "wrongPassword"

        beforeEach(() => {
            // Login through JSON request
            cy.login("admin", "testpassword")


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


})
