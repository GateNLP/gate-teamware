import JRPCClient from "@/jrpc";
jest.mock('@/jrpc')

import store from '@/store'

/**

 Example on how to mock the jrpc call

describe("Vuex functions testing", () =>{

    beforeAll(() =>{

        //Re-implement custom mock call implementation if needed
        JRPCClient.mockImplementation(()=>{
            return {
                call(){
                    return 50
                }
            }
        })

    })

    it("testfunc", async () =>{

        const noutput = await store.dispatch("testnormal")
        expect(noutput).toBe("Hello world")

        const aoutput = await store.dispatch("testasync")
        expect(aoutput).toBe("Hello world")

        const rpc = new JRPCClient("/")
        const result = await rpc.call("some param")
        expect(result).toBe(50)

    })
})

**/
