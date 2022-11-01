const fs = require('fs')
import {render, fireEvent} from "@testing-library/vue";
import '@testing-library/jest-dom';

import '../globalVue'
import AnnotationRenderer from "@/components/AnnotationRenderer";

function elementHasTagWithName(elem, tag, name) {
    const queryStr = `${tag}[name='${name}']`
    const result = elem.querySelector(queryStr)
    return result
}

function elementHasTagWithValue(elem, tag, val) {
    const queryStr = `${tag}[value='${val}']`
    const result = elem.querySelector(queryStr)
    return result
}

describe("AnnotationRenderer", () => {

    it('Test rendering valid annotation components', async () => {

        const annotationComps = JSON.parse(fs.readFileSync("../examples/project_config.json", "utf-8"))

        const ar = render(AnnotationRenderer, {
            props: {
                config: annotationComps
            }
        })

        for (let comp of annotationComps) {
            //Check title's rendered
            if (comp.title)
                ar.getByText(comp.title)

            //Check description's rendered
            if (comp.description)
                ar.getByText(comp.description)

            //Check that the correct component is rendered
            switch (comp.type) {
                case "text":
                    expect(elementHasTagWithName(ar.container, "input", comp.name)).toBeTruthy()
                    break
                case "textarea":
                    expect(elementHasTagWithName(ar.container, "textarea", comp.name)).toBeTruthy()
                    break
                case "radio":
                    expect(elementHasTagWithName(ar.container, "input", comp.name)).toBeTruthy()
                    break
                case "checkbox":
                    expect(elementHasTagWithName(ar.container, "input", comp.name)).toBeTruthy()
                    break
                case "selector":
                    expect(elementHasTagWithName(ar.container, "select", comp.name)).toBeTruthy()
                    break
                case "html":
                    ar.getByText(comp.text)

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

        const ar = render(AnnotationRenderer, {
            props: {
                config: annotationComps
            }
        })

        for (let comp of annotationComps) {
            //Check title's rendered
            if (comp.title)
                ar.getByText(comp.title)

            //Check description's rendered
            if (comp.description)
                ar.getByText(comp.description)

            //Outputs warning that component's invalid
            ar.getByText("Component invalid")

        }

    })

    it('Test text regex', async () => {

        const annotationComps = [
            {
                name: "text",
                type: "text",
                regex: "^foo$",

            }]

        const ar = render(AnnotationRenderer, {
            props: {
                config: annotationComps
            }
        })

        const textElem = elementHasTagWithName(ar.container, "input", "text")
        const submitBtn = ar.getByText("Submit")

        await fireEvent.update(textElem, "sadfsdfds")
        await fireEvent.click(submitBtn)

        expect(ar.emitted().submit).not.toBeTruthy()

        await fireEvent.update(textElem, "foo")
        await fireEvent.click(submitBtn)

        expect(ar.emitted().submit).toHaveLength(1)


    })

    async function clickCheckboxInAnnotationRenderer(annotationRenderer, val) {
        let checkboxElem = elementHasTagWithValue(annotationRenderer.container, "input", val)
        await fireEvent.click(checkboxElem)
    }

    it('Test checkbox', async () => {

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

        const ar = render(AnnotationRenderer, {
            props: {
                config: annotationComps
            }
        })

        const submitBtn = ar.getByText("Submit")

        // Empty - Fail
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).not.toBeTruthy()

        await clickCheckboxInAnnotationRenderer(ar, "val1")

        // Single selection - Pass
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).toBeTruthy()

        await clickCheckboxInAnnotationRenderer(ar, "val2")


        // Two selection - Pass
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).toBeTruthy()


    })

    it('Test checkbox not optional', async () => {

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

        const ar = render(AnnotationRenderer, {
            props: {
                config: annotationComps
            }
        })

        const submitBtn = ar.getByText("Submit")

        // Empty - Fail
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).not.toBeTruthy()

        await clickCheckboxInAnnotationRenderer(ar, "val1")

        // Single selection - Pass
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).toBeTruthy()

        await clickCheckboxInAnnotationRenderer(ar, "val2")


        // Two selection - Pass
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).toBeTruthy()


    })

    it('Test checkbox optional', async () => {

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

        const ar = render(AnnotationRenderer, {
            props: {
                config: annotationComps
            }
        })

        const submitBtn = ar.getByText("Submit")

        // Empty - Pass
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).toBeTruthy()

        await clickCheckboxInAnnotationRenderer(ar, "val1")

        // Single selection - Pass
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).toBeTruthy()

        await clickCheckboxInAnnotationRenderer(ar, "val2")


        // Two selection - Pass
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).toBeTruthy()


    })

    it('Test checkbox minSelected=2', async () => {
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

        const ar = render(AnnotationRenderer, {
            props: {
                config: annotationComps
            }
        })

        const submitBtn = ar.getByText("Submit")

        // Empty - Fail
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).not.toBeTruthy()

        await clickCheckboxInAnnotationRenderer(ar, "val1")

        // Single selection - Fail
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).not.toBeTruthy()

        await clickCheckboxInAnnotationRenderer(ar, "val2")


        // Two selection - Pass
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).toBeTruthy()


    })

    it('Test checkbox minSelected=2 and optional, minSelected should have priority', async () => {
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

        const ar = render(AnnotationRenderer, {
            props: {
                config: annotationComps
            }
        })

        const submitBtn = ar.getByText("Submit")

        // Empty - Fail
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).not.toBeTruthy()

        await clickCheckboxInAnnotationRenderer(ar, "val1")

        // Single selection - Fail
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).not.toBeTruthy()

        await clickCheckboxInAnnotationRenderer(ar, "val2")


        // Two selection - Pass
        await fireEvent.click(submitBtn)
        expect(ar.emitted().submit).toBeTruthy()


    })

    it('Test function of reject document button', async () => {

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
        const ar = render(AnnotationRenderer, {
            props: {
                config: annotationComps,
                allow_document_reject: true
            }
        })

        const rejectBtn = ar.getByText("Reject document")
        await fireEvent.click(rejectBtn)
        expect(ar.emitted().reject).toBeTruthy()

    })


    it('Test function of allow_document_reject config option', async () => {

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
        const ar = render(AnnotationRenderer, {
            props: {
                config: annotationComps,
                allow_document_reject: false
            }
        })

        const rejectBtn = ar.queryByText("Reject document")
        expect(rejectBtn).toBeNull()

    })

    it('Test pre-annotation', async () => {

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

        const document = {
            "text": "<p>Some html text <strong>in bold</strong>.</p><p>Paragraph 2.</p>",
            "preanno": {
                "sentiment": "neutral"
            }
        }

        // Test disabling reject button
        const ar = render(AnnotationRenderer, {
            props: {
                config: annotationComps,
                document: document,
                doc_preannotation_field: "preanno",
            }
        })


    })


})
