// Mocking jrpc/index.js

//Mocking the JRPCClient class
//Replacing the call function with a custom mockCall function
export const mockCall = jest.fn(()=> 30);
const mock = jest.fn().mockImplementation(() => {
  return {call: mockCall};
});

export default mock;
