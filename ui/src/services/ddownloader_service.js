
const baseUrl = 'http://192.168.1.105:5000'


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
