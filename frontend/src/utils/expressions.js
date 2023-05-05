import ExpressionEval from "jse-eval";

// set up jsep extensions
// hex and octal numeric literals
import jsepNumbers from "@jsep-plugin/numbers";
// object expressions
import jsepObject from "@jsep-plugin/object";
// regex literal support
import jsepRegex from "@jsep-plugin/regex";
// destructuring, useful in filtering functions etc.
import jsepSpread from "@jsep-plugin/spread";

ExpressionEval.registerPlugin(
    jsepNumbers,
    jsepObject,
    jsepRegex,
    jsepSpread,
)

// add "in" as a binary operator, partly to make it work in the syntax of all(x in xs, ...)
// expressions but also in its own right as a real binary operator.  "A in B" behaves like
// B.includes(A) if B is an array, otherwise it mean the same as the normal Javascript
// "A in B" checking whether B has a property named (the result of evaluating) A
function inOperator(a, b) {
    if(Array.isArray(b)) {
        return b.includes(a)
    } else {
        return a in b
    }
}
ExpressionEval.addBinaryOp("in", 6, inOperator)

// add =~ binary operator that tests a string against a regex
function testRegex(a, b) {
    if (!(b instanceof RegExp)) {
        throw new Error("Right hand argument of =~ must be a regular expression")
    }
    return b.test(a)
}
ExpressionEval.addBinaryOp("=~", 4, testRegex)

// Monkey-patch ExpressionEval to forbid access to the __ob__ property
// (which otherwise provides a route to reach the global "window" object)
// and any property whose name begins with "$", as well as the usual
// prototype and constructor properties that are forbidden by default.
//
// Within the body of the function, "this" refers to the
// ExpressionEval instance that is evaluating the expression, so it can
// access other instance methods of that class.
function evaluateMemberExcludeUnsafe(node) {
    return this.eval(node.object, (object) => this
        .evalSyncAsync(
            node.computed
                ? this.eval(node.property)
                : node.property.name,
            (key) => {
                if (typeof key === 'string' && /^\$|^(?:__proto__|prototype|constructor|__ob__)$/.test(key)) {
                    throw Error(`Access to member "${key}" disallowed.`);
                }
                return [object, (node.optional ? (object || {}) : object)[key], key];
            })
    );
}
ExpressionEval.prototype.evaluateMember = evaluateMemberExcludeUnsafe;

// similarly, replace the "Identifier" evaluator with one that checks the same block-list
function evalIdentifierExcludeUnsafe(node) {
    const key = node.name;
    if (typeof key === 'string' && /^\$|^(?:__proto__|prototype|constructor|__ob__)$/.test(key)) {
        throw Error(`Access to member "${key}" disallowed.`);
    }
    return this.context[key]
}
ExpressionEval.addEvaluator("Identifier", evalIdentifierExcludeUnsafe);

// limit function calls to specific utility functions that we provide

function preprocessQuantifier(type, args) {
    if(args.length > 2) {
        throw new Error(`At most two arguments expected for "${type}" quantifier`);
    }
    let bindingVar, arrayExpr, predicateExpr;
    if(args.length === 1) {
        // treat "all(xs)" as equivalent to all(x in xs, x), but use a unique Symbol
        // as the binding variable so it can't clash with any real variable names.
        bindingVar = Symbol('x')
        arrayExpr = args[0]
        predicateExpr = {
            type: 'Identifier',
            name: bindingVar,
        }
    } else {
        const binding = args[0]
        if(binding.type !== 'BinaryExpression' || binding.operator !== 'in' || binding.left.type !== 'Identifier') {
            throw new Error(`"${type}" quantifier binding must be of the form "identifier in expression"`);
        }
        bindingVar = binding.left.name
        arrayExpr = binding.right
        predicateExpr = args[1]
    }
    return [bindingVar, arrayExpr, predicateExpr]
}

/**
 * Universal quantifier:
 *
 * all(x in expr, predicate)
 *
 * expr should evaluate to an array, we then evaluate predicate for each item in
 * the array in turn, stopping if one of them returns a falsy value.
 * @param exprEval ExpressionEval instance
 * @param args array of nodes representing the arguments - there should be either
 * one argument (evaluating to a list) or two arguments the first of which is
 * "varName in expr" and the second an expression that can refer to the varName.
 */
function evalAllQuantifier(exprEval, args) {
    let [bindingVar, arrayExpr, predicateExpr] = preprocessQuantifier("all", args)

    const newContext = { ...exprEval.context }
    return exprEval.eval(arrayExpr, (arr) => {
        if(arr.length === 0) {
            // trivially true if no items in the array
            return true;
        }
        if (exprEval.isAsync) {
            const evalOnce = (item, i) => {
                newContext[bindingVar] = item
                return ExpressionEval.evalAsync(predicateExpr, newContext).then((result) => {
                    if(result) {
                        i++;
                        if (i >= arr.length) {
                            return true
                        } else {
                            return evalOnce(arr[i], i)
                        }
                    } else {
                        return false;
                    }
                })
            }
            return evalOnce(arr[0], 0)
        } else {
            return arr.every((item) => {
                newContext[bindingVar] = item;
                return ExpressionEval.eval(predicateExpr, newContext)
            })
        }
    })
}

/**
 * Existential quantifier:
 *
 * any(x in expr, predicate)
 *
 * expr should evaluate to an array, we then evaluate predicate for each item in
 * the array in turn, stopping if one of them returns a truthy value.
 * @param exprEval ExpressionEval instance
 * @param args array of nodes representing the arguments - there should be either
 * one argument (evaluating to a list) or two arguments the first of which is
 * "varName in expr" and the second an expression that can refer to the varName.
 */
function evalAnyQuantifier(exprEval, args) {
    let [bindingVar, arrayExpr, predicateExpr] = preprocessQuantifier("any", args)

    const newContext = { ...exprEval.context }
    return exprEval.eval(arrayExpr, (arr) => {
        if (arr.length === 0) {
            // trivially false if no items in the array
            return false;
        }
        if (exprEval.isAsync) {
            const evalOnce = (item, i) => {
                newContext[bindingVar] = item
                return ExpressionEval.evalAsync(predicateExpr, newContext).then((result) => {
                    if (result) {
                        return true;
                    } else {
                        i++;
                        if (i >= arr.length) {
                            return false
                        } else {
                            return evalOnce(arr[i], i)
                        }
                    }
                })
            }
            return evalOnce(arr[0], 0)
        } else {
            return arr.some((item) => {
                newContext[bindingVar] = item;
                return ExpressionEval.eval(predicateExpr, newContext)
            })
        }
    })
}

// Evaluator function - "this" within here refers to the ExpressionEval instance
function evalFunctionCall(node) {
    if(node.callee.type !== "Identifier") {
        throw new Error("Illegal function call");
    }
    switch(node.callee.name) {
        case "all":
            return evalAllQuantifier(this, node.arguments)
        case "any":
            return evalAnyQuantifier(this, node.arguments)
        default:
            throw new Error(`Unsupported function "${node.callee.name}"`)
    }
}
ExpressionEval.addEvaluator("CallExpression", evalFunctionCall);

export { compile } from "jse-eval"