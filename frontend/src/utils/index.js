export function generateBVOptions(options) {
    let optionsList = []
    for (let optionKey in options) {
        optionsList.push({
            value: optionKey,
            text: options[optionKey]
        })
    }

    return optionsList
}


