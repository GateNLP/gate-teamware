# Project configuration

## Project annotation configuration

Annotation projects takes a `json` string for configuring how the document is displayed to the user and types of 
annotation will be collected. Here's an example configuration:

```js
[
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
        "options": {
            "negative": "Negative",
            "neutrual": "Neutrual",
            "positive": "Positive"
            
        }
    }
]
```

The above configuration displays the value from the `text` field from the document to be annotated. It then shows
a set of 3 radio inputs that allows the user to select a Negative, Neutrual, or Positive sentiment with the label
name `sentiment`. 

All fields **require** the properties **name** and **type**, it is used to name our label and determine the type 
of input/display to be shown to the user respectively.

Another field can be added to collect more information, e.g. a text field for opinions:

```js
[
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
        "options": {
            "negative": "Negative",
            "neutrual": "Neutrual",
            "positive": "Positive"
            
        }
    },
    {
        "name": "opinion",
        "type": "text",
        "title": "What's your opinion of the above text?",
        "optional": true
    }
    
]
```

Note that for the above case, the `optional` field is added ensure that allows user to not have to input any value. 
This `optional` field can be used on all components.

Some fields are available to configure which are specific to components, e.g. the `options` field are only available
for the `radio`, `checkbox` and `selector` components. See details below on the usage of each specific component.

### Displaying text

```js
[
    {
        "name": "htmldisplay",
        "type": "html",
        "text": "{{{text}}}"
    }
]
```

### Text input

```js
[
    {
        "name": "mylabel",
        "type": "text",
        "optional": true, //Optional - Set if validation is not required
        "title": "Title string", //Optional
        "description": "Descrption string" //Optional
    }
]
```

### Textarea input

```js
[
    {
        "name": "mylabel",
        "type": "textarea",
        "optional": true, //Optional - Set if validation is not required
        "title": "Title string", //Optional
        "description": "Descrption string" //Optional
    }
]
```

### Radio input

```js
[
    {
        "name": "mylabel",
        "type": "radio",
        "optional": true, //Optional - Set if validation is not required
        "options": { // The options that the user is able to select from
            "value1": "Text to show user 1", 
            "value2": "Text to show user 2",
            "value2": "Text to show user 3",
        },
        "title": "Title string", //Optional
        "description": "Descrption string" //Optional
    }
]
```

### Checkbox input

```js
[
    {
        "name": "mylabel",
        "type": "checkbox",
        "optional": true, //Optional - Set if validation is not required
        "options": { // The options that the user is able to select from
            "value1": "Text to show user 1", 
            "value2": "Text to show user 2",
            "value2": "Text to show user 3",
        },
        "title": "Title string", //Optional
        "description": "Descrption string" //Optional
    }
]
```

### Selector input

```js
[
    {
        "name": "mylabel",
        "type": "selector",
        "optional": true, //Optional - Set if validation is not required
        "options": { // The options that the user is able to select from
            "value1": "Text to show user 1", 
            "value2": "Text to show user 2",
            "value2": "Text to show user 3",
        },
        "title": "Title string", //Optional
        "description": "Descrption string" //Optional
    }
]
```
