import JRPCClient from "@/jrpc";

// Testing code that's not vue component
describe("Separate test", () =>{
    it("test item", async ()=>{
        const rpc = new JRPCClient("/something")
        try{
            await rpc.call("test")
        }catch(e){
            expect(e instanceof Error).toBeTruthy()

        }

        expect(true).toBe(true)
    })
})
