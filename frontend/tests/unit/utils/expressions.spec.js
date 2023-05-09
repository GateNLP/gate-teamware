import { describe, it ,expect, vi } from 'vitest'
import { compile } from '@/utils/expressions'

describe("Expression parsing & evaluation", () => {
    it("Test simple expression", () => {
        const fn = compile('annotation.confidence >= 4');
        expect(fn({
            annotation: {
                confidence: "5"
            }
        })).toBeTruthy();
        expect(fn({
            annotation: {
                confidence: "3"
            }
        })).toBeFalsy();
    })

    it("Test universal quantifier with predicate", () => {
        const allFn = compile("all(v in annotation.values, v < 3)")
        expect(allFn({
            annotation: {
                values: []
            }
        })).toBeTruthy()
        expect(allFn({
            annotation: {
                values: ["1", "2"]
            }
        })).toBeTruthy()
        expect(allFn({
            annotation: {
                values: ["1", "2", "3"]
            }
        })).toBeFalsy()
    })

    it("Test universal quantifier without predicate", () => {
        const allFnNoPredicate = compile("all(annotation.values)")
        expect(allFnNoPredicate({
            annotation: {
                values: ["1", "2", "3"]
            }
        })).toBeTruthy()
        expect(allFnNoPredicate({
            annotation: {
                values: ["1", "", "3"]
            }
        })).toBeFalsy()
    })

    it("Test universal quantifier over object", () => {
        const allFn = compile("all(prop in document.labels, prop.value > 0.5)")
        expect(allFn({
            document: {
                labels: {
                    "a": 0.3,
                    "b": 0.8,
                    "c": 0.95
                }
            }
        })).toBeFalsy()
        expect(allFn({
            document: {
                labels: {
                    "a": 0.6,
                    "b": 0.8,
                    "c": 0.95
                }
            }
        })).toBeTruthy()
    })

    it("Test existential quantifier with predicate", () => {
        const anyFn = compile("any(v in annotation.values, v < 3)")
        expect(anyFn({
            annotation: {
                values: []
            }
        })).toBeFalsy()
        expect(anyFn({
            annotation: {
                values: ["1", "4"]
            }
        })).toBeTruthy()
        expect(anyFn({
            annotation: {
                values: ["3", "4"]
            }
        })).toBeFalsy()
    })

    it("Test existential quantifier without predicate", () => {
        const anyFnNoPredicate = compile("any(annotation.values)")
        expect(anyFnNoPredicate({
            annotation: {
                values: ["1", 0, ""]
            }
        })).toBeTruthy()
        expect(anyFnNoPredicate({
            annotation: {
                values: [null, "", 0]
            }
        })).toBeFalsy()
    })

    it("Test existential quantifier over object", () => {
        const anyFn = compile("any(prop in document.labels, prop.value < 0.5)")
        expect(anyFn({
            document: {
                labels: {
                    "a": 0.3,
                    "b": 0.8,
                    "c": 0.95
                }
            }
        })).toBeTruthy()
        expect(anyFn({
            document: {
                labels: {
                    "a": 0.6,
                    "b": 0.8,
                    "c": 0.95
                }
            }
        })).toBeFalsy()
    })

    it("Test compile error (invalid syntax)", () => {
        expect(() => compile("annotation.foo <")).toThrowError()
    })

    it("Test compile error (unsupported expression types)", () => {
        expect(() => compile("annotation.foo = 4")).toThrowError()
        expect(() => compile("annotation.bar += 3")).toThrowError()
    })

    it("Test access to 'prototype' is forbidden at runtime", () => {
        const fn = compile("annotation.prototype.foo")
        expect(() => fn({annotation: {}})).toThrowError(/Access to member .* disallowed/);
    })

    it("Test access to '__ob__' as a member is forbidden at runtime", () => {
        const fn = compile("annotation['__ob__'].dep.subs[0]")
        expect(() => fn({annotation: {}})).toThrowError(/Access to member .* disallowed/);
    })

    it("Test access to '__ob__' as a top-level identifier is forbidden at runtime", () => {
        const fn = compile("__ob__.dep.subs[0]")
        expect(() => fn({__ob__: {}})).toThrowError(/Access to member .* disallowed/);
    })

    it("Test other function calls are forbidden", () => {
        const fnCallMethod = compile("example.method()")
        expect(() => fnCallMethod({
            example: {
                method() {return true}
            }
        })).toThrowError(/function/);

        const fnCallTopLevel = compile("someFunc()")
        expect(() => fnCallTopLevel({
            someFunc() { return true }
        })).toThrowError(/function/);
    })

    it("Test Object.assign is unavailable at runtime", () => {
        const fn = compile("Object.assign(annotation, {foo: 'bar'})")
        const ctx = {annotation: {}};
        expect(() => fn(ctx)).toThrowError() // illegal function call
        expect(ctx.annotation.foo).toBeUndefined() // ctx is unchanged
    })

    it("Test regex operator", () => {
        const fn = compile("annotation.val =~ /^b/")
        expect(fn({annotation: {val: "foo"}})).toBeFalsy()
        expect(fn({annotation: {val: "bar"}})).toBeTruthy()
    })

    it("Test 'in' operator", () => {
        const fn = compile("'hello' in things")
        expect(fn({things: ['hello', 'world']})).toBeTruthy()
        expect(fn({things: ['goodbye', 'world']})).toBeFalsy()
        expect(fn({things: {'hello': 'world'}})).toBeTruthy()
        expect(fn({things: {'world': 'hello'}})).toBeFalsy()
    })
})