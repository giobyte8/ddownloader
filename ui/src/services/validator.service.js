

/**
 * Checks if given string is a valid http|https url
 * 
 * @param {string} urlStr Url to validate
 * @returns true if url is valid
 */
export function isValidHttpUrl(urlStr) {
    let url;

    try {
        url = new URL(urlStr)
    } catch ( _ ) {
        return false
    }

    // Probably protocol should not be validated (?)
    return url.protocol === 'http:' || url.protocol === 'https:'
}
