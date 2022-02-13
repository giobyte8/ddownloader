import { useState } from 'preact/hooks'
import { isValidHttpUrl } from '../../services/validator.service'


const urlError = 'Url seems to be invalid or unreachable'

const DTaskUrlForm = ({ url, setUrl, setFormStep }) => {
    const [urlValid, setUrlValid] = useState(true)
    
    const onBackClicked = () => console.log('Going back to main route')
    const onNextClicked = () => {
        if (isValidHttpUrl(url)) {
            setUrlValid(true)
            setFormStep(2)
        } else {
            setUrlValid(false)
        }
    }

    return <>
        <div className="card-content">
            <div className="field">
                <label htmlFor="inp-url" className="label">Url</label>
                <div className="control">
                    <input
                        id="inp-url"
                        className={`input ${ urlValid ? '' : 'is-danger' }`}
                        name="url"
                        type="url"
                        value={ url }
                        onInput={ (e) => setUrl(e.target.value) }
                    />
                </div>

                { urlValid || <span className="help is-danger">{ urlError }</span> }
            </div>
        </div>
    
        <div className="card-footer">
            <a className="card-footer-item has-text-grey"
                onClick={ onBackClicked }
            >
                Cancel
            </a>
            <a className="card-footer-item has-text-primary-dark"
                onClick={ onNextClicked }
            >
                Next
            </a>
        </div>
    </>
}

export default DTaskUrlForm
