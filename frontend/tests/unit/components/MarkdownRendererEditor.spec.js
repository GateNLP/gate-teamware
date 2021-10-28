const fs = require('fs')

import {render, fireEvent, waitFor} from "@testing-library/vue";
import '@testing-library/jest-dom';

import '../globalVue'
import MarkdownRenderer from "@/components/MarkdownRenderer";
import MarkdownEditor from "@/components/MarkdownEditor";

// Markdown doc with a few test components
let pageContent = `
# Header 1
## Header 2
[Test link](https://test.com)
<a href="https://test.com">Test link HTML</a>
`

/**
 * Call after firing an input event for a v-model bound component
 * to update the component's value prop with the input event emitted.
 */
function updateVModel(elem){

    let inputEvents = elem.emitted()["input"]
    expect(inputEvents).toHaveLength(1)

    elem.updateProps({
        value: inputEvents[0][0]
    })

}

describe("Test markdown renderer and editor", () => {

    it('Test MarkdownRenderer', async () => {


        const mdRenderer = render(MarkdownRenderer, {
            props: {
                content: pageContent
            }
        })

        // Check that correct tags are generated
        let h1 = await mdRenderer.findByText("Header 1")
        expect(h1.tagName === "H1").toBeTruthy()
        let h2 =  await mdRenderer.findByText("Header 2")
        expect(h2.tagName === "H2").toBeTruthy()
        let testLink =  await mdRenderer.findByText("Test link")
        expect(testLink.tagName === "A").toBeTruthy()
        let testLinkHTML =  await mdRenderer.findByText("Test link HTML")
        expect(testLinkHTML.tagName === "A").toBeTruthy()

    })

    it('Test MarkdownEditor', async () =>{
        // Mount editor
        const mdEditor = render(MarkdownEditor, {
            props: {
                value: ""
            }
        })

        // Update textarea in editor with page content
        const textArea = mdEditor.container.querySelector("textarea")
        await fireEvent.update(textArea, pageContent)
        
        updateVModel(mdEditor)

        mdEditor.getByText("Editor")
        await mdEditor.getByText("Preview").click()
        // Check that correct tags are generated
        let h1 = await mdEditor.findByText("Header 1")
        expect(h1.tagName === "H1").toBeTruthy()
        let h2 =  await mdEditor.findByText("Header 2")
        expect(h2.tagName === "H2").toBeTruthy()
        let testLink =  await mdEditor.findByText("Test link")
        expect(testLink.tagName === "A").toBeTruthy()
        let testLinkHTML =  await mdEditor.findByText("Test link HTML")
        expect(testLinkHTML.tagName === "A").toBeTruthy()

    })

})
