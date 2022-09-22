export function generateBVOptions(options) {
    let optionsList = []
    if (Array.isArray(options)) {
        for( let i in options){
            const option = options[i]
            optionsList.push({
                value: option.value,
                text: option.label
            })
        }
    } else {
        for (let optionKey in options) {
            optionsList.push({
                value: optionKey,
                text: options[optionKey]
            })
        }
    }


    return optionsList
}
