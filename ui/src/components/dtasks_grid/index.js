import { h } from 'preact'
import { useState, useEffect } from 'preact/hooks'
import { fetchTasks } from '../../services/ddownloader_service';
import DTask from "../dtask";

const Loading = () => (
    <div className="container">
        <div className="columns column">
            <h4>Loading</h4>
        </div>
    </div>
)

const makeTasksItems = (tasksPage) => {
    if (!tasksPage.dtasks) {
        return []
    }

    return tasksPage.dtasks.map((dtask) => 
        <div className="column is-4">
            <DTask
                targetPath={ dtask.target_path }
                downloadedSize={ dtask.downloaded_size }
                totalSize={ dtask.total_size }
                status={ dtask.status }
            />
        </div>
    )
}

const DTasksGrid = () => {
    const [loading, setLoading] = useState(false)
    const [tasksPage, setTasksPage] = useState([])

    useEffect(() => {
        setLoading(true)
        fetchTasks()
            .then(tasksPage => {
                setLoading(false)
                setTasksPage(tasksPage)
            })
            .catch(e => {
                setLoading(false)
                console.error('Unable to fetch queued tasks')
            })
    }, [])

    if (loading) {
        return <Loading/>
    }

    return <div className="container">
        <div className="columns is-multiline">
            { makeTasksItems(tasksPage) }
        </div>
    </div>
}

export default DTasksGrid
