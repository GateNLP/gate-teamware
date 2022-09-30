import {flatten} from "@/utils";

describe("Test flatten function", () => {
    it("Test flatten function", () => {
        const myObj = {
            contact: {
                firstname: "firstnametest",
                lastname: "surnametest"
            },
            company: {
                name: "testname",
                address: {
                    line1: "123 Fake St",
                    line2: "Apt 1",
                },
                listings: ["one", "two", {oname: "three", o2name: "four"}, ["ins1", "ins2", "ins3"]]
            },
            username: "testusername",
            fruitsILike: ["apples", "bananas", "pineapple"]
        };

        const outObj = flatten(myObj)
        console.log(outObj)

        expect(outObj).toEqual({
            "contact.firstname": "firstnametest",
            "contact.lastname": "surnametest",
            "company.name": "testname",
            "company.address.line1": "123 Fake St",
            "company.address.line2": "Apt 1",
            "username": "testusername",
            "fruitsILike": "apples,bananas,pineapple"
        })

    })
})
