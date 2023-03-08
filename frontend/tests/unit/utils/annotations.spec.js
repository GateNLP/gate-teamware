import { generateBVOptions } from "@/utils/annotations.js"

describe("Annotation utilities", () => {
    it("Test generating bootstrapvue options from project config", () => {
        // Dictionary type options
        const dictOptions = {
            "val1": "Label 1",
            "val2": "Label 2",
            "val3": "Label 3",
        }

        let result = generateBVOptions(dictOptions)
        expect(Array.isArray(result)).toBeTruthy()
        expect(result.length).toEqual(3)
        for( let i in result){
            expect("value" in result[i]).toBeTruthy()
            expect("text" in result[i]).toBeTruthy()
        }

        // List type options
        const listOptions = [
            { "value": "val1", "label": "Label 1"},
            { "value": "val2", "label": "Label 2"},
            { "value": "val3", "label": "Label 3"}
        ]

        result = generateBVOptions(listOptions)
        expect(Array.isArray(result)).toBeTruthy()
        expect(result.length).toEqual(3)
        for( let i in result){
            expect("value" in result[i]).toBeTruthy()
            expect("text" in result[i]).toBeTruthy()
        }

    })

    it("Test generating dynamic options from document", () => {
        const optionsConfig = [
            { "value": "fixed1", "label": "Fixed value 1"},
            { "fromDocument": "options.simple"},
            { "fromDocument": "options.complex"},
            { "value": "fixed2", "label": "Fixed value 2"},
            { "fromDocument": "options.delimited", "separator": "###" }
        ]

        const document = {
            text: "This is an example document",
            options: {
                simple: ["Simple value 1", "Simple value 2"],
                complex: [
                    {value: "complex1", label: "Complex value 1"},
                    {value: "complex2", label: "Complex value 2"},
                ],
                // delimited options: test that
                // - whitespace is stripped around delimiters (both between options and between val=text)
                // - val=text only splits at the first "=", second =-sign is part of the label
                // - no "=" at all -> whole item is used as both value and text
                delimited: "delimited1 = Delimited value 1 ###delimited2=Delimited value=2### delimited3 ",
            }
        }

        let result = generateBVOptions(optionsConfig, document)
        expect(Array.isArray(result)).toBeTruthy()
        expect(result.length).toEqual(9)
        for( let i in result){
            expect("value" in result[i]).toBeTruthy()
            expect("text" in result[i]).toBeTruthy()
        }
        expect(result.map(v => v.value)).toEqual([
            "fixed1",
            "Simple value 1", "Simple value 2",
            "complex1", "complex2",
            "fixed2",
            "delimited1", "delimited2", "delimited3",
        ])
        expect(result.map(v => v.text)).toEqual([
            "Fixed value 1",
            "Simple value 1", "Simple value 2",
            "Complex value 1", "Complex value 2",
            "Fixed value 2",
            "Delimited value 1", "Delimited value=2", "delimited3",
        ])

    })
})
