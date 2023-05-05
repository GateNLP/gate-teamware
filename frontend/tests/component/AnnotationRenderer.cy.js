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

    describe('Test checkboxes', () => {
        it('simple checkboxes', () => {

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

        it('not optional', () => {

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

        it('optional', () => {

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

        it('minSelected=2', () => {
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

    describe("Conditional widgets", () => {
        it('Test condition based only on annotation', () => {
            cy.fixture("project_config_conditional").then((conf) => {
                cy.mount(AnnotationRenderer, {
                    propsData: {
                        config: conf,
                        document: {
                            "text": "I couldn't care either way about the thing."
                        },
                    }
                })

                cy.get("input[name='sentiment']").first().check({force: true})

                // initially the confidence reason field should not be shown
                cy.get("input[name='confidence_reason']").should("not.exist")

                cy.get("input[name='confidence'][value='3']").check({force: true})
                // now confidence is set to 3, reason field should appear
                cy.get("input[name='confidence_reason']").should("exist")

                // Submit should fail as confidence_reason not filled in
                cy.contains(submitButtonStr).click()
                cy.get("div.invalid-feedback").should("be.visible")

                cy.get("input[name='confidence'][value='5']").check({force: true})
                // now confidence is set to 5, reason field should vanish
                cy.get("input[name='confidence_reason']").should("not.exist")

                // Submit should now succeed even though reason not filled in, since only
                // visible fields are validated
                cy.contains(submitButtonStr).click()
                // not.be.visible means at least one matching item is not visible, we instead
                // need to check that *all* the items are not visible, so filter for the visible
                // ones and assert that there are none of them
                cy.get("div.invalid-feedback:visible").should("not.exist")
            })
        })

        it('Test document condition', () => {
            cy.fixture("project_config_conditional").then((conf) => {
                cy.mount(AnnotationRenderer, {
                    propsData: {
                        config: conf,
                        document: {
                            "text": "I <i>love</i> this thing!",
                            "preanno": {
                                "sentiment": "positive"
                            }
                        },
                        doc_preannotation_field: "preanno",
                    }
                })

                // initially the "why do you disagree" field should not be shown
                cy.get("input[name='reason']").should("not.exist")
                // and positive sentiment should be selected
                cy.get("input[name='sentiment'][value='positive']").should("be.checked")

                // select a different value
                cy.get("input[name='sentiment'][value='neutral']").check({force: true})
                // "why do you disagree" field should appear
                cy.get("input[name='reason']").should("exist")
            })
        })

        it('Test condition with error', () => {
            cy.fixture("project_config_conditional").then((conf) => {
                cy.mount(AnnotationRenderer, {
                    propsData: {
                        config: conf,
                        document: {
                            "text": "I <i>loathe</i> this thing!",
                        },
                        doc_preannotation_field: "preanno",
                    }
                })

                // initially the "why do you disagree" field should not be shown
                cy.get("input[name='reason']").should("not.exist")
                // and no sentiment should be selected (as the if expression throws an error with preanno missing)
                cy.get("input[name='sentiment']").should("not.be.checked")

                // select a value
                cy.get("input[name='sentiment'][value='neutral']").check({force: true})
                // "why do you disagree" field should still be absent, as the if expression still throws an error
                cy.get("input[name='reason']").should("not.exist")
            })
        })

        it('Test quantifier and regex', () => {
            cy.mount(AnnotationRenderer, {
                propsData: {
                    config: [
                        {
                            name: "fruits",
                            type: "checkbox",
                            title: "Which fruits do you like?",
                            options: [
                                {"value": "apple", "label": "Apple"},
                                {"value": "orange", "label": "Orange"},
                                {"value": "kiwi", "label": "Kiwi fruit"}
                            ]
                        },
                        {
                            name: "has_a",
                            if: "any(val in annotation.fruits, val =~ /a/)",
                            type: "html",
                            text: "You like fruit with an 'a' in its name"
                        }
                    ],
                }
            })

            // html label should not be visible
            cy.contains('in its name').should('not.exist')

            // check kiwi, label should still not be visible
            cy.get("input[name='fruits'][value='kiwi']").check({force: true})
            cy.contains('in its name').should('not.exist')

            // check apple as well, label should now appear
            cy.get("input[name='fruits'][value='apple']").check({force: true})
            cy.contains('in its name').should('exist')
        })
    })
})
