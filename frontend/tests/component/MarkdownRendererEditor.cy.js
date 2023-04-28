import MarkdownRenderer from "../../src/components/MarkdownRenderer.vue"
import MarkdownEditor from "../../src/components/MarkdownEditor.vue"


// Markdown doc with a few test components
let pageContent = `
# Header 1
## Header 2
[Test link](https://test.com)
<a href="https://test.com">Test link HTML</a>
`

describe("Test markdown renderer and editor", () => {

    it('Test MarkdownRenderer', () => {
        cy.mount(MarkdownRenderer, {propsData: {content: pageContent}})
        cy.get("h1").contains("Header 1")
        cy.get("h2").contains("Header 2")
        cy.get("a").contains("Test link")
         cy.get("a").contains("Test link HTML")
    })

    it.only('Test MarkdownEditor', () =>{
        // Mount editor
        cy.mount(MarkdownEditor, {propsData: {
            value: pageContent
            }})

        //Checks editor window
        cy.contains("Editor").click()
        cy.get("textarea").should("have.value", pageContent)

        //Checks preview window
        cy.contains("Preview").click()
        cy.get("h1").contains("Header 1")
        cy.get("h2").contains("Header 2")
        cy.get("a").contains("Test link")
        cy.get("a").contains("Test link HTML")


    })
})
