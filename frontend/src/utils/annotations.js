import {getValueFromKeyPath} from "@/utils/dict";

export function generateBVOptions(options, document) {
    let optionsList = []
    if (Array.isArray(options)) {
        for (let option of options){
            if (document && option && typeof option === "object"
                && typeof option.fromDocument === "string") {
                // one or more options taken from the document data
                const propertyPath = option.fromDocument
                // fromDocument is supposed to be a dot-separated path, but if
                // the whole path is found as a top-level property name then use
                // it, i.e. try opt['foo.bar.baz'] first, then opt.foo.bar.baz
                // second
                let propertyValue = (propertyPath in document) ?
                    document[propertyPath] : getValueFromKeyPath(document, propertyPath);
                optionsList.push(...generateBVOptions(propertyValue));
            } else if (option !== null && typeof option !== "undefined") {
                // single option
                if (typeof option === 'string') {
                    optionsList.push({
                        value: option,
                        text: option,
                    })
                } else if ("value" in option) {
                    optionsList.push({
                        value: option.value,
                        text: ("label" in option ? option.label : option.value),
                    })
                } // else invalid option, so ignore
            }
        }
    } else {
        // a dictionary mapping value to label
        for (let optionKey in options) {
            optionsList.push({
                value: optionKey,
                text: options[optionKey]
            })
        }
    }


    return optionsList
}
