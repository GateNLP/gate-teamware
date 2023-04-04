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
                let optionsFromDocument = (propertyPath in document) ?
                    document[propertyPath] : getValueFromKeyPath(document, propertyPath);

                if(typeof optionsFromDocument === "string") {
                    // single string - treat it as a delimited list of options where
                    // each option may be a pair of value and label.  For example,
                    // with the default delimiters
                    //
                    // orange=Orange; kiwi=Kiwi fruit
                    //
                    // maps to
                    //
                    // [{"value":"orange", "label":"Orange"},
                    //  {"value":"kiwi", "label":"Kiwi fruit"}]
                    //
                    // Whitespace around the delimiters is ignored
                    const optionSeparator = (typeof option.separator === 'string' ? option.separator : ';');
                    if (optionSeparator) {
                        optionsFromDocument = optionsFromDocument.split(optionSeparator);
                    } else {
                        optionsFromDocument = [optionsFromDocument];
                    }
                    optionsFromDocument = optionsFromDocument.map(s => s.trim());

                    const valueLabelSeparator =
                        (typeof option.valueLabelSeparator === 'string' ? option.valueLabelSeparator : '=');
                    if(valueLabelSeparator) {
                        optionsFromDocument = optionsFromDocument.map(opt => {
                            // can't use String.prototype.split here as we want everything after the first
                            // occurrence of the separator to be used as the value, even when that includes
                            // more instances of the separator string
                            const sepIndex = opt.indexOf(valueLabelSeparator);
                            if(sepIndex >= 0) {
                                return {
                                    value: opt.substring(0, sepIndex).trim(),
                                    label: opt.substring(sepIndex + valueLabelSeparator.length).trim(),
                                };
                            } else {
                                // no separator - use whole item as both value and label
                                return opt;
                            }
                        });
                    }
                }
                optionsList.push(...generateBVOptions(optionsFromDocument));
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
                        helptext: ("helptext" in option ? option.helptext : null),
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
