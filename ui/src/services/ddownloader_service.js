import { isValidHttpUrl } from "./validator.service"

const baseUrl = 'http://192.168.1.106:5000'


export async function fetchTasks() {
    const url = `${baseUrl}/tasks`

    const response = await fetch(url, {
        method: 'GET',
        mode: 'cors'
    })

    if (!response.ok) {
        throw new Error(`Unable to retrieve tasks: ${response.statusText}`)
    }

    return response.json();
}

export async function getUrlMetadata(targetUrl) {
    if (!isValidHttpUrl(targetUrl)) {
        throw new Error(`Invalid http url: ${ targetUrl }`)
    }

    const url = `${ baseUrl }/url/metadata?url=${ targetUrl }`
    const res = await fetch(url, {
        method: 'GET',
        mode: 'cors'
    })

    if (!res.ok) {
        throw new Error(`Unable to get url metadata: ${ res.statusText }`)
    }

    return res.json()
}
