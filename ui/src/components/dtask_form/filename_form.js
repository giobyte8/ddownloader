import { useState } from 'preact/hooks'


const fileNameError = 'Enter a valid file name'

const isFileNameValid = (fileName) => {
    return false
}

const DTaskFileNameForm = ({ url, fileName, setFileName, setFormStep }) => {
    const [fileNameValid, setFileNameValid] = useState(true)
    
    const onBackClicked = () => setFormStep(1)
    const onNextClicked = () => {
        console.log('Doing magic')
    }

    return <>
        <div className="card-content">
            <span>{ url }</span>
            <br />
            <span>Loading url details</span>

            <div className="field">
                <label htmlFor="inp-file-name" className="label">
                    File name
                </label>
                <div className="control">
                    <input
                        id="inp-file-name"
                        className={`input ${ fileNameValid ? '' : 'is-danger' }`}
                        name="filename"
                        type="text"
                        value={ fileName }
                        onInput={ (e) => setFileName(e.target.value) }
                    />
                </div>

                { fileNameValid || <span className="help is-danger">
                    { fileNameError }
                </span> }
            </div>
        </div>
    
        <div className="card-footer">
            <a className="card-footer-item has-text-grey"
                onClick={ onBackClicked }
            >
                Back
            </a>
            <a className="card-footer-item has-text-primary-dark"
                onClick={ onNextClicked }
            >
                Queue
            </a>
        </div>
    </>
}

export default DTaskFileNameForm
