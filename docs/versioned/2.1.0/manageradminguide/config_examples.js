export default {
    config1: [
        {
            "name": "htmldisplay",
            "type": "html",
            "text": "{{{text}}}"
        },
        {
            "name": "sentiment",
            "type": "radio",
            "title": "Sentiment",
            "description": "Please select a sentiment of the text above.",
            "options": [
                {"value": "negative", "label": "Negative"},
                {"value": "neutral", "label": "Neutral"},
                {"value": "positive", "label": "Positive"}
            ]
        }
    ],
    config2: [
        {
            "name": "htmldisplay",
            "type": "html",
            "text": "{{{text}}}"
        },
        {
            "name": "sentiment",
            "type": "radio",
            "title": "Sentiment",
            "description": "Please select a sentiment of the text above.",
            "options": [
                {"value": "negative", "label": "Negative"},
                {"value": "neutral", "label": "Neutral"},
                {"value": "positive", "label": "Positive"}
            ]
        },
        {
            "name": "opinion",
            "type": "text",
            "title": "What's your opinion of the above text?",
            "optional": true
        }
    ],
    configDisplay: [
        {
            "name": "htmldisplay",
            "type": "html",
            "text": "{{{text}}}"
        }
    ],
    configDisplayHtmlNoHtml: [
        {
            "name": "htmldisplay",
            "type": "html",
            "text": "No HTML: {{text}} <br/> HTML: {{{text}}}"
        }
    ],
    configDisplayCustomFieldnames: [
        {
            "name": "htmldisplay",
            "type": "html",
            "text": "Custom field: {{customField}} <br/> Another custom field: {{{anotherCustomField}}} <br/> Subfield: {{{subfield.subfieldContent}}}"
        }
    ],
    configDisplayPreserveNewlines: [
        {
            "name": "htmldisplay",
            "type": "html",
            "text": "<div style='white-space: pre-line'>{{text}}</div>"
        }
    ],
    configTextInput: [
        {
            "name": "mylabel",
            "type": "text",
            "optional": true, //Optional - Set if validation is not required
            "regex": "regex string", //Optional - When specified, the regex pattern will used to validate the text
            "title": "Title string", //Optional
            "description": "Description string", //Optional
            "valSuccess": "Success message then field is validated", //Optional
            "valError": "Error message when field fails is validation" //Optional
        }
    ],
    configTextarea: [
        {
            "name": "mylabel",
            "type": "textarea",
            "optional": true, //Optional - Set if validation is not required
            "regex": "regex string", //Optional - When specified, the regex pattern will used to validate the text
            "title": "Title string", //Optional
            "description": "Description string", //Optional
            "valSuccess": "Success message then field is validated", //Optional
            "valError": "Error message when field fails is validation" //Optional
        }
    ],
    configRadio: [
        {
            "name": "mylabel",
            "type": "radio",
            "optional": true, //Optional - Set if validation is not required
            "orientation": "vertical", //Optional - default is "horizontal"
            "options": [ // The options that the user is able to select from
                {"value": "value1", "label": "Text to show user 1"},
                {"value": "value2", "label": "Text to show user 2"},
                {"value": "value3", "label": "Text to show user 3"}
            ],
            "title": "Title string", //Optional
            "description": "Description string", //Optional
            "valSuccess": "Success message then field is validated", //Optional
            "valError": "Error message when field fails is validation" //Optional
        }
    ],
    configRadioHelpText: [
        {
            "name": "mylabel",
            "type": "radio",
            "optional": true, //Optional - Set if validation is not required
            "orientation": "vertical", //Optional - default is "horizontal"
            "options": [ // The options that the user is able to select from
                    {"value": "value1", "label": "Text to show user 1", "helptext": "Additional help text for option 1"},
                    {"value": "value2", "label": "Text to show user 2", "helptext": "Additional help text for option 2"},
                    {"value": "value3", "label": "Text to show user 3"}
                ],
            "title": "Title string", //Optional
            "description": "Description string", //Optional
            "valSuccess": "Success message when the field is validated", //Optional
            "valError": "Error message when the field fails validation" //Optional
        }
    ],
    configCheckbox: [
        {
            "name": "mylabel",
            "type": "checkbox",
            "optional": true, //Optional - Set if validation is not required
            "orientation": "horizontal", //Optional - "horizontal" (default) or "vertical"
            "options": [ // The options that the user is able to select from
                {"value": "value1", "label": "Text to show user 1"},
                {"value": "value2", "label": "Text to show user 2"},
                {"value": "value3", "label": "Text to show user 3"}
            ],
            "minSelected": 1, //Optional - Specify the minimum number of options that must be selected
            "title": "Title string", //Optional
            "description": "Description string", //Optional
            "valSuccess": "Success message then field is validated", //Optional
            "valError": "Error message when field fails is validation" //Optional
        }
    ],
    configSelector: [
        {
            "name": "mylabel",
            "type": "selector",
            "optional": true, //Optional - Set if validation is not required
            "options": [ // The options that the user is able to select from
                {"value": "value1", "label": "Text to show user 1"},
                {"value": "value2", "label": "Text to show user 2"},
                {"value": "value3", "label": "Text to show user 3"}
            ],
            "title": "Title string", //Optional
            "description": "Description string", //Optional
            "valSuccess": "Success message then field is validated", //Optional
            "valError": "Error message when field fails is validation" //Optional
        }
    ],
    configRadioDict: [
        {
            "name": "mylabel",
            "type": "radio",
            "optional": true, //Optional - Set if validation is not required
            "options": { // The options can be specified as a dictionary, ordering is not guaranteed
                "value1": "Text to show user 1",
                "value2": "Text to show user 2",
                "value3": "Text to show user 3",
            },
            "title": "Title string", //Optional
            "description": "Description string", //Optional
            "valSuccess": "Success message then field is validated", //Optional
            "valError": "Error message when field fails is validation" //Optional
        }
    ],

    configDbpediaExample: [
        {
            "name": "uri",
            "type": "radio",
            "title": "Select the most appropriate URI",
            "options":[
                {"fromDocument": "candidates"},
                {"value": "none", "label": "None of the above"},
                {"value": "unknown", "label": "Cannot be determined without more context"}
            ]
        }
    ],
    docDbpediaExample: {
        "text": "President Bush visited the air base yesterday...",
        "candidates": [
            {
                "value": "http://dbpedia.org/resource/George_W._Bush",
                "label": "George W. Bush (Jnr)"
            },
            {
                "value": "http://dbpedia.org/resource/George_H._W._Bush",
                "label": "George H. W. Bush (Snr)"
            }
        ]
    },


    doc1: {text: "Sometext with <strong>html</strong>"},
    doc2: {
        customField: "Content of custom field.",
        anotherCustomField: "Content of another custom field.",
        subfield: {
            subfieldContent: "Content of a subfield."
        }
    },
    docPlainText: {
        "text": "This is some text\n\nIt has line breaks that we want to preserve."
    },
    configPreAnnotation: [
        {
            "name": "htmldisplay",
            "type": "html",
            "text": "{{{text}}}"
        },
        {
            "name": "radio",
            "type": "radio",
            "title": "Test radio input",
            "options": [
                {"value": "val1", "label": "Value 1"},
                {"value": "val2", "label": "Value 2"},
                {"value": "val3", "label": "Value 4"},
                {"value": "val4", "label": "Value 5"}
            ],
            "description": "Test radio description"
        },
        {
            "name": "checkbox",
            "type": "checkbox",
            "title": "Test checkbox input",
            "options": [
                {"value": "val1", "label": "Value 1"},
                {"value": "val2", "label": "Value 2"},
                {"value": "val3", "label": "Value 4"},
                {"value": "val4", "label": "Value 5"}
            ],
            "description": "Test checkbox description"
        },
        {
            "name": "text",
            "type": "text",
            "title": "Test text input",
            "description": "Test text description"
        }

    ],
    docPreAnnotation: {
        "id": 12345,
        "text": "Example document text",
        "preannotation": {
            "radio": "val1",
            "checkbox": ["val1", "val3"],
            "text": "Pre-annotation text value"
        }
    }


}
