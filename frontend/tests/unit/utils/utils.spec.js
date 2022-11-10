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
                listings: ["one", "two", {l2name1: "three", l2name2: "four"}],
                doublelist: ["one", "two", ["one", "two"], ["one", "two"]]
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
            "company.listings.0": "one",
            "company.listings.1": "two",
            "company.listings.2.l2name1": "three",
            "company.listings.2.l2name2": "four",
            "company.doublelist.0":"one",
            "company.doublelist.1":"two",
            "company.doublelist.2.0":"one",
            "company.doublelist.2.1":"two",
            "company.doublelist.3.0":"one",
            "company.doublelist.3.1":"two",
            "username": "testusername",
            "fruitsILike.0": "apples",
            "fruitsILike.1": "bananas",
            "fruitsILike.2": "pineapple",
        })

    })
})
