import AnnotationRenderer from '../../src/components/AnnotationRenderer.vue'

describe("AnnotationRenderer", () => {
    it('Test rendering valid annotation components', () => {
        const annotationComps = [
            {
                "name": "html",
                "title": "Test html display",
                "description": "Test html display description",
                "type": "html",
                "text": "Some text to display"
            },
            {
                "name": "radio",
                "title": "Test radio input",
                "description": "Test radio description",
                "type": "radio",
                "options": {
                    "val1": "Value 1",
                    "val2": "Value 2",
                    "val3": "Value 4",
                    "val4": "Value 5"
                }
            },
            {
                "name": "checkbox",
                "title": "Test checkbox input",
                "description": "Test checkbox description",
                "type": "checkbox",
                "orientation": "vertical",
                "options": {
                    "val1": "Value 1",
                    "val2": "Value 2",
                    "val3": "Value 4",
                    "val4": "Value 5"
                }
            },
            {
                "name": "selector",
                "title": "Test selector input",
                "description": "Test selector description",
                "type": "selector",
                "options": {
                    "val1": "Value 1",
                    "val2": "Value 2",
                    "val3": "Value 4",
                    "val4": "Value 5"
                }
            },
            {
                "name": "textarea",
                "title": "Test textarea input",
                "description": "Test textarea description",
                "type": "textarea"
            },
            {
                "name": "text",
                "title": "Test text input",
                "description": "Test text description",
                "type": "text"
            }
        ]

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

    it('Test text regex', () => {

        const annotationComps = [
            {
                name: "text",
                type: "text",
                regex: "^foo$",

            }]

        cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})

        cy.get("input[name='text']").type("sadfsdfds")
        cy.contains("Submit").click()
        cy.contains("Annotation required").should("be.visible")


        cy.get("input[name='text']").clear().type("foo")
        cy.contains("Submit").click()
        cy.contains("Annotation required").should("not.be.visible")

    })

    // async function clickCheckboxInAnnotationRenderer(annotationRenderer, val) {
    //     let checkboxElem = elementHasTagWithValue(annotationRenderer.container, "input", val)
    //     await fireEvent.click(checkboxElem)
    // }
    //
    // it('Test checkbox', async () => {
    //
    //     const annotationComps = [
    //         {
    //             name: "text",
    //             type: "checkbox",
    //             options: {
    //                 "val1": "Val 1",
    //                 "val2": "Val 2",
    //                 "val3": "Val 3",
    //                 "val4": "Val 4",
    //             }
    //
    //         }]
    //
    //     cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})
    //
    //     const submitBtn = cy.contains("Submit")
    //
    //     // Empty - Fail
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).not.toBeTruthy()
    //
    //     await clickCheckboxInAnnotationRenderer(ar, "val1")
    //
    //     // Single selection - Pass
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).toBeTruthy()
    //
    //     await clickCheckboxInAnnotationRenderer(ar, "val2")
    //
    //
    //     // Two selection - Pass
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).toBeTruthy()
    //
    //
    // })
    //
    // it('Test checkbox not optional', async () => {
    //
    //     const annotationComps = [
    //         {
    //             name: "text",
    //             type: "checkbox",
    //             optional: false,
    //             options: {
    //                 "val1": "Val 1",
    //                 "val2": "Val 2",
    //                 "val3": "Val 3",
    //                 "val4": "Val 4",
    //             }
    //
    //         }]
    //
    //     cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})
    //
    //     const submitBtn = cy.contains("Submit")
    //
    //     // Empty - Fail
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).not.toBeTruthy()
    //
    //     await clickCheckboxInAnnotationRenderer(ar, "val1")
    //
    //     // Single selection - Pass
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).toBeTruthy()
    //
    //     await clickCheckboxInAnnotationRenderer(ar, "val2")
    //
    //
    //     // Two selection - Pass
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).toBeTruthy()
    //
    //
    // })
    //
    // it('Test checkbox optional', async () => {
    //
    //     const annotationComps = [
    //         {
    //             name: "text",
    //             type: "checkbox",
    //             optional: true,
    //             options: {
    //                 "val1": "Val 1",
    //                 "val2": "Val 2",
    //                 "val3": "Val 3",
    //                 "val4": "Val 4",
    //             }
    //
    //         }]
    //
    //     cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})
    //
    //     const submitBtn = cy.contains("Submit")
    //
    //     // Empty - Pass
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).toBeTruthy()
    //
    //     await clickCheckboxInAnnotationRenderer(ar, "val1")
    //
    //     // Single selection - Pass
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).toBeTruthy()
    //
    //     await clickCheckboxInAnnotationRenderer(ar, "val2")
    //
    //
    //     // Two selection - Pass
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).toBeTruthy()
    //
    //
    // })
    //
    // it('Test checkbox minSelected=2', async () => {
    //     const annotationComps = [
    //         {
    //             name: "text",
    //             type: "checkbox",
    //             minSelected: 2,
    //             options: {
    //                 "val1": "Val 1",
    //                 "val2": "Val 2",
    //                 "val3": "Val 3",
    //                 "val4": "Val 4",
    //             }
    //
    //         }]
    //
    //     cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})
    //
    //     const submitBtn = cy.contains("Submit")
    //
    //     // Empty - Fail
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).not.toBeTruthy()
    //
    //     await clickCheckboxInAnnotationRenderer(ar, "val1")
    //
    //     // Single selection - Fail
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).not.toBeTruthy()
    //
    //     await clickCheckboxInAnnotationRenderer(ar, "val2")
    //
    //
    //     // Two selection - Pass
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).toBeTruthy()
    //
    //
    // })

    // it('Test dynamic options fromDocument', async () => {
    //     const annotationComps = JSON.parse(fs.readFileSync("../examples/project_config_radio_fromDocument.json", "utf-8"))
    //
    //     const documents = JSON.parse(fs.readFileSync("../examples/documents_radio_fromDocument.json", "utf-8"))
    //
    //
    //     for(let doc of documents) {
    //         const ar = render(AnnotationRenderer, {
    //             props: {
    //                 config: annotationComps,
    //                 document: doc,
    //             }
    //         })
    //         // all example documents have three choices, plus the one static
    //         // option from the config should be four radio buttons in total
    //         const radios = ar.container.querySelectorAll('input[type=radio]')
    //         expect(radios.length).toEqual(4)
    //
    //         const submitBtn = cy.contains("Submit")
    //         // This is a radio button, so submit before selecting should fail
    //         await fireEvent.click(submitBtn)
    //         expect(ar.emitted().submit).not.toBeTruthy()
    //
    //         // but after selecting should succeed
    //         await fireEvent.click(radios[0])
    //         await fireEvent.click(submitBtn)
    //         const submitted = ar.emitted().submit
    //         expect(submitted).toBeTruthy()
    //
    //         // and the selected item ("answer" property of the first argument to the
    //         // first emitted "submit" event) should be one of the dynamic ones, not
    //         // the static "none"
    //         expect(submitted[0][0].answer).not.toEqual("none")
    //
    //         ar.unmount()
    //     }
    //
    //
    // })

    // it('Test checkbox minSelected=2 and optional, minSelected should have priority', async () => {
    //     const annotationComps = [
    //         {
    //             name: "text",
    //             type: "checkbox",
    //             optional: true,
    //             minSelected: 2,
    //             options: {
    //                 "val1": "Val 1",
    //                 "val2": "Val 2",
    //                 "val3": "Val 3",
    //                 "val4": "Val 4",
    //             }
    //
    //         }]
    //
    //     cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})
    //
    //     const submitBtn = cy.contains("Submit")
    //
    //     // Empty - Fail
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).not.toBeTruthy()
    //
    //     await clickCheckboxInAnnotationRenderer(ar, "val1")
    //
    //     // Single selection - Fail
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).not.toBeTruthy()
    //
    //     await clickCheckboxInAnnotationRenderer(ar, "val2")
    //
    //
    //     // Two selection - Pass
    //     await fireEvent.click(submitBtn)
    //     expect(ar.emitted().submit).toBeTruthy()
    //
    //
    // })
    //
    // it('Test function of reject document button', async () => {
    //
    //     const annotationComps = [
    //         {
    //             name: "text",
    //             type: "checkbox",
    //             optional: true,
    //             minSelected: 2,
    //             options: {
    //                 "val1": "Val 1",
    //                 "val2": "Val 2",
    //                 "val3": "Val 3",
    //                 "val4": "Val 4",
    //             }
    //
    //         }]
    //
    //     // Test reject button functions when enabled
    //     cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})
    //
    //     const rejectBtn = cy.contains("Reject document")
    //     await fireEvent.click(rejectBtn)
    //     expect(ar.emitted().reject).toBeTruthy()
    //
    // })
    //
    //
    // it('Test function of allow_document_reject config option', async () => {
    //
    //     const annotationComps = [
    //         {
    //             name: "text",
    //             type: "checkbox",
    //             optional: true,
    //             minSelected: 2,
    //             options: {
    //                 "val1": "Val 1",
    //                 "val2": "Val 2",
    //                 "val3": "Val 3",
    //                 "val4": "Val 4",
    //             }
    //
    //         }]
    //
    //     // Test disabling reject button
    //     cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})
    //
    //     const rejectBtn = ar.queryByText("Reject document")
    //     expect(rejectBtn).toBeNull()
    //
    // })
    //
    // it('Test pre-annotation', async () => {
    //
    //     const annotationComps = JSON.parse(fs.readFileSync("../examples/project_config.json", "utf-8"))
    //
    //     const document = {
    //         "text": "<p>Some html text <strong>in bold</strong>.</p><p>Paragraph 2.</p>",
    //         "preanno": {
    //             "radio": "val1",
    //             "checkbox": [
    //                 "val1",
    //                 "val3"
    //             ],
    //             "selector": "val2",
    //             "textarea": "Test textarea",
    //             "text": "Test text"
    //         }
    //     }
    //
    //     cy.mount(AnnotationRenderer, {propsData: {config: annotationComps}})
    //
    //     function getInputElemFromComponent(component, name, value) {
    //         return component.container.querySelector(`input[name='${name}'][value='${value}']`)
    //     }
    //
    //     // Test radio
    //     expect(getInputElemFromComponent(ar, "radio", "val1")).toBeChecked()
    //     expect(getInputElemFromComponent(ar, "radio", "val2")).not.toBeChecked()
    //     expect(getInputElemFromComponent(ar, "radio", "val3")).not.toBeChecked()
    //     expect(getInputElemFromComponent(ar, "radio", "val4")).not.toBeChecked()
    //
    //     // Test cheeckbox
    //     expect(getInputElemFromComponent(ar, "checkbox", "val1")).toBeChecked()
    //     expect(getInputElemFromComponent(ar, "checkbox", "val2")).not.toBeChecked()
    //     expect(getInputElemFromComponent(ar, "checkbox", "val3")).toBeChecked()
    //     expect(getInputElemFromComponent(ar, "checkbox", "val4")).not.toBeChecked()
    //
    //     //Test selector
    //     expect(ar.container.querySelector(`select[name='selector']`)).toHaveValue("val2")
    //
    //     //Test text box
    //     expect(ar.container.querySelector(`input[name='text']`)).toHaveValue("Test text")
    //
    //
    // })
})
