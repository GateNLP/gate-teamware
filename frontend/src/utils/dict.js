export function getValueFromKeyPath(objDict, keyPath, delimiter = ".") {
    if (objDict == null || keyPath == null || typeof keyPath !== "string" || keyPath.trim().length < 1) {
        return null
    }

    const keyPathSplit = keyPath.trim().split(delimiter)
    let currentValue = objDict
    for (let i in keyPathSplit) {
        if (keyPathSplit[i] in currentValue) {
            currentValue = currentValue[keyPathSplit[i]]
        } else {
            return null
        }
    }

    return currentValue

}
