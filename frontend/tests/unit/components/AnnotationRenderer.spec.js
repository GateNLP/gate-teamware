const fs = require('fs')
import {render, fireEvent} from "@testing-library/vue";

import '../globalVue'
import AnnotationRenderer from "@/components/AnnotationRenderer";

function elementHasTagWithName(elem, tag, name){
    const queryStr = `${tag}[name='${name}']`
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
            switch (comp.type){
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


})
