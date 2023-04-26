import AnnotationRenderer from '../../src/components/AnnotationRenderer.vue'

describe("AnnotationRenderer", () => {

    it('Test rendering valid annotation components', () => {

        cy.fixture("project_config").then(annotationComps => {

            // see: https://on.cypress.io/mounting-vue
            cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})

            for (let comp of annotationComps) {
                //Check title's rendered
                if (comp.title)
                    cy.contains(comp.title)

                //Check description's rendered
                if (comp.description)
                    cy.contains(comp.description)

                //Check that the correct component is rendered
                switch (comp.type) {
                    case "text":
                        cy.get(`input[name="${comp.name}"]`).should("exist")
                        break
                    case "textarea":
                        cy.get(`textarea[name="${comp.name}"]`).should("exist")
                        break
                    case "radio":
                        cy.get(`input[name="${comp.name}"]`).should("exist")
                        break
                    case "checkbox":
                        cy.get(`input[name="${comp.name}"]`).should("exist")
                        break
                    case "selector":
                        cy.get(`select[name="${comp.name}"]`).should("exist")
                        break
                    case "html":
                        cy.contains(comp.text)

                }

            }

        })


    })

    it('Test rendering invalid annotation components', () => {

        const annotationComps = [
            {
                name: "failcomp",
                type: "doesnotexist",
                title: "failtitle",
                description: "faildescription"
            }]

        cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})

        for (let comp of annotationComps) {
            //Check title's rendered
            if (comp.title)
                cy.contains(comp.title)

            //Check description's rendered
            if (comp.description)
                cy.contains(comp.description)

            //Outputs warning that component's invalid
            cy.contains("Component invalid")

        }

    })

    const annotationErrorStr = "Annotation required"
    const submitButtonStr = "Submit"

    it('Test text regex', () => {

        const annotationComps = [
            {
                name: "text",
                type: "text",
                regex: "^foo$",

            }]

        cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})

        cy.get("input[name='text']").type("sadfsdfds")
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("be.visible")


        cy.get("input[name='text']").clear().type("foo")
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("not.be.visible")

    })

    it('Test checkbox', () => {

        const annotationComps = [
            {
                name: "text",
                type: "checkbox",
                options: {
                    "val1": "Val 1",
                    "val2": "Val 2",
                    "val3": "Val 3",
                    "val4": "Val 4",
                }

            }]

        cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})

        // Empty - Fail
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("be.visible")

        // Single selection - Pass
        cy.get("[name='text'][value='val1']").check({force: true})
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("not.be.visible")

        // Two selection - Pass
        cy.get("[name='text'][value='val1']").check({force: true})
        cy.get("[name='text'][value='val2']").check({force: true})
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("not.be.visible")

    })

    it('Test checkbox not optional', () => {

        const annotationComps = [
            {
                name: "text",
                type: "checkbox",
                optional: false,
                options: {
                    "val1": "Val 1",
                    "val2": "Val 2",
                    "val3": "Val 3",
                    "val4": "Val 4",
                }

            }]

        cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})

        // Empty - Fail
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("be.visible")

        // Single selection - Pass
        cy.get("[name='text'][value='val1']").check({force: true})
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("not.be.visible")

        // Two selection - Pass
        cy.get("[name='text'][value='val1']").check({force: true})
        cy.get("[name='text'][value='val2']").check({force: true})
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("not.be.visible")


    })

    it('Test checkbox optional', () => {

        const annotationComps = [
            {
                name: "text",
                type: "checkbox",
                optional: true,
                options: {
                    "val1": "Val 1",
                    "val2": "Val 2",
                    "val3": "Val 3",
                    "val4": "Val 4",
                }

            }]

        cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})


        // Empty - Pass
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("not.be.visible")

        // Single selection - Pass
        cy.get("[name='text'][value='val1']").check({force: true})
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("not.be.visible")

        // Two selection - Pass
        cy.get("[name='text'][value='val1']").check({force: true})
        cy.get("[name='text'][value='val2']").check({force: true})
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("not.be.visible")


    })

    it('Test checkbox minSelected=2', () => {
        const annotationComps = [
            {
                name: "text",
                type: "checkbox",
                minSelected: 2,
                options: {
                    "val1": "Val 1",
                    "val2": "Val 2",
                    "val3": "Val 3",
                    "val4": "Val 4",
                }

            }]

        cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})

        // Empty - Fail
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("be.visible")

        // Single selection - Fail
        cy.get("[name='text'][value='val1']").check({force: true})
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("be.visible")

        // Two selection - Pass
        cy.get("[name='text'][value='val1']").check({force: true})
        cy.get("[name='text'][value='val2']").check({force: true})
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("not.be.visible")


    })


    it('Test dynamic options fromDocument', () => {
        cy.fixture("test_from_document_fixture").then(fixture => {
            const annotationComps = fixture.config
            const documents = fixture.documents

            for (let doc of documents) {
                // const submitSpy = cy.spy().as("submitSpy")
                cy.mount(AnnotationRenderer, {
                    propsData: {config: annotationComps, document: doc},
                })
                // all example documents have three choices, plus the one static
                // option from the config should be four radio buttons in total
                cy.get("input[type='radio']").should("have.length", 4)


                // This is a radio button, so submit before selecting should fail
                cy.contains(submitButtonStr).click()
                cy.contains(annotationErrorStr).should("be.visible")


                // but after selecting should succeed
                // and the selected item ("answer" property of the first argument to the
                // first emitted "submit" event) should be one of the dynamic ones, not
                // the static "none"
                cy.get("input[type='radio']").first().check({force: true})
                cy.contains(submitButtonStr).click().vue().then((wrapper) => {
                    expect(wrapper.emitted("submit")[0][0].answer).to.not.equal("none")
                })
                cy.contains(annotationErrorStr).should("not.be.visible")


            }

        })
    })

    it('Test checkbox minSelected=2 and optional, minSelected should have priority', () => {
        const annotationComps = [
            {
                name: "text",
                type: "checkbox",
                optional: true,
                minSelected: 2,
                options: {
                    "val1": "Val 1",
                    "val2": "Val 2",
                    "val3": "Val 3",
                    "val4": "Val 4",
                }

            }]

        cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})


        // Empty - Fail
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("be.visible")

        // Single selection - Fail
        cy.get("[name='text'][value='val1']").check({force: true})
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("be.visible")

        // Two selection - Pass
        cy.get("[name='text'][value='val1']").check({force: true})
        cy.get("[name='text'][value='val2']").check({force: true})
        cy.contains(submitButtonStr).click()
        cy.contains(annotationErrorStr).should("not.be.visible")


    })

    it('Test function of reject document button', () => {

        const annotationComps = [
            {
                name: "text",
                type: "checkbox",
                optional: true,
                minSelected: 2,
                options: {
                    "val1": "Val 1",
                    "val2": "Val 2",
                    "val3": "Val 3",
                    "val4": "Val 4",
                }

            }]

        // Test reject button functions when enabled
        cy.mount(AnnotationRenderer, {propsData: {config: annotationComps, allow_document_reject: true}})

        cy.contains("Reject").should("exist")
        cy.contains("Reject").click().vue().then((wrapper) => {
            expect(wrapper.emitted("reject").length).to.equal(1)
        })

    })

    it('Test function of allow_document_reject config option', () => {

        const annotationComps = [
            {
                name: "text",
                type: "checkbox",
                optional: true,
                minSelected: 2,
                options: {
                    "val1": "Val 1",
                    "val2": "Val 2",
                    "val3": "Val 3",
                    "val4": "Val 4",
                }

            }]

        // Test disabling reject button
        cy.mount(AnnotationRenderer, {propsData: {config: annotationComps, allow_document_reject: false}})
        cy.contains("Reject").should("not.exist")


    })

    it('Test pre-annotation', () => {

        cy.fixture("project_config").then(annotationComps => {

            const document = {
                "text": "<p>Some html text <strong>in bold</strong>.</p><p>Paragraph 2.</p>",
                "preanno": {
                    "radio": "val1",
                    "checkbox": [
                        "val1",
                        "val3"
                    ],
                    "selector": "val2",
                    "textarea": "Test textarea",
                    "text": "Test text"
                }
            }

            cy.mount(AnnotationRenderer,
                {
                    propsData: {config: annotationComps, document: document, doc_preannotation_field: "preanno"}
                })


            // Test radio
            cy.get("[name='radio'][value='val1']").should("be.checked")
            cy.get("[name='radio'][value='val2']").should("not.be.checked")
            cy.get("[name='radio'][value='val3']").should("not.be.checked")
            cy.get("[name='radio'][value='val4']").should("not.be.checked")

            // Test checkbox
            cy.get("[name='checkbox'][value='val1']").should("be.checked")
            cy.get("[name='checkbox'][value='val2']").should("not.be.checked")
            cy.get("[name='checkbox'][value='val3']").should("be.checked")
            cy.get("[name='checkbox'][value='val4']").should("not.be.checked")

            //Test selector
            cy.get("[name='selector'] option:selected").should("have.text", "Value 2")

            // Test text area
            cy.get("textarea[name='textarea']").should("have.value", "Test textarea")

            //Test text box
            cy.get("input[name='text']").should("have.value", "Test text")

        })


    })
})
