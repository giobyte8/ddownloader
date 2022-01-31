import { useState } from 'preact/hooks'
import DTaskFileNameForm from '../../components/dtask_form/filename_form'
import DTaskUrlForm from '../../components/dtask_form/url_form'


const AddTaskForm = () => {
    const [formStep, setFormStep] = useState(1)
    const [url, setUrl] = useState('')
    const [fileName, setFileName] = useState('')

    let form = ''
    if (formStep === 1) {
        form = <DTaskUrlForm
            url={ url }
            setUrl={ setUrl }
            setFormStep={ setFormStep }
        />
    } else if (formStep === 2) {
        form = <DTaskFileNameForm
            url={ url }
            fileName={ fileName }
            setFileName={ setFileName }
            setFormStep={ setFormStep }
        />
    }

    return <div className="container">
        <div className="columns">
            <div className="column is-4 is-offset-4">
                <div className="card">
                    <header className="card-header">
                        <h1 className="card-header-title">
                            Add download task
                        </h1>
                    </header>

                    { form }
                </div>
            </div>
        </div>
    </div>
}

export default AddTaskForm
