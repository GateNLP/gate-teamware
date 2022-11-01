import {getValueFromKeyPath} from "@/utils";

describe("Test getting value from key path", () => {
    it("Test getting value from key path", () =>{
        let targetValue = "Test value"

        let testDict = {
            "direct_path": targetValue,
            "path1": {
                "path2": {
                    "path3": targetValue
                }
            },
            "path_array1": [
                {
                    "path2": targetValue
                }
            ]
        }

        // Get for normal path, should exist
        expect(getValueFromKeyPath(testDict, "direct_path", ".")).toEqual(targetValue)
        expect(getValueFromKeyPath(testDict, "path1.path2.path3", ".")).toEqual(targetValue)
        // Get for nonexistant path
        expect(getValueFromKeyPath(testDict, "path1.dontexist", ".")).toEqual(null)
        // Get for path with array
        expect(getValueFromKeyPath(testDict, "path_array1.0.path2", ".")).toEqual(targetValue)


    })
})
