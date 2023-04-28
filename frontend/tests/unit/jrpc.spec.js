import { afterEach, beforeEach, describe, it ,expect, vi } from 'vitest'
import axios from 'axios'
import JRPCClient from '@/jrpc'

vi.mock('axios')

describe("jrpc lib test", () => {
    it("Test normal response", async () => {

        const checkString = "Test call check string"
        const mockResponse = {
            data: {
                result: checkString
            }
        }

        axios.post.mockResolvedValue(mockResponse)

        const rpc = new JRPCClient("/")
        const result = await rpc.call("some param")
        expect(result).toEqual(checkString)
    })

    it("Test auth error", async () => {
        const mockResponse = {
            data: {
                error: {
                    code: JRPCClient.AUTHENTICATION_ERROR,
                    message: "Test error message"
                }
            }
        }

        const mockError = new Error("Test error")
        mockError.response = mockResponse

        axios.post.mockImplementation(async () => {
            throw mockError;
        })
        const rpc = new JRPCClient("/")

        await expect(rpc.call("some param")).rejects.toThrow()

        try {
            await rpc.call("some param")
        } catch (e) {
            expect(e.code).toEqual(JRPCClient.AUTHENTICATION_ERROR)
        }
    })

    it("Test permission error", async () => {
        const mockResponse = {
            data: {
                error: {
                    code: JRPCClient.UNAUTHORIZED_ERROR,
                    message: "Test error message"
                }
            }
        }

        const mockError = new Error("Test error")
        mockError.response = mockResponse

        axios.post.mockImplementation(async () => {
            throw mockError;
        })
        const rpc = new JRPCClient("/")

        await expect(rpc.call("some param")).rejects.toThrow()

        try {
            await rpc.call("some param")
        } catch (e) {
            expect(e.code).toEqual(JRPCClient.UNAUTHORIZED_ERROR)
        }
    })

    it("Test internal error", async () => {


        const mockError = new Error("Test error")

        axios.post.mockImplementation(async () => {
            throw mockError;
        })
        const rpc = new JRPCClient("/")

        await expect(rpc.call("some param")).rejects.toThrow()

        try {
            await rpc.call("some param")
        } catch (e) {
            expect(e.code).toEqual(JRPCClient.INTERNAL_ERROR)
        }


    })
})
