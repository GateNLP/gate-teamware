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
})
