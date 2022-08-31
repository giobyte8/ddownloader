import { useState, useEffect } from 'preact/hooks'
import { getUrlMetadata } from '../../services/ddownloader_service'
import { bytesToHuman } from '../../utils'

import Loading from '../loading/index'


const fileNameError = 'Enter a valid file name'

const isFileNameValid = (fileName) => {
    return false
}

const filePreview = (urlMeta) => {

    // Do not render preview for files greater than 10MB
    if (urlMeta.content_length > 10 * 1024 * 1024) {
        return ''
    }

    const supportedContentTypes = [
        'image/jpeg',
        'image/jpg',
        'image/jpege',
        'image/png'
    ]

    if (!supportedContentTypes.includes(urlMeta.content_type)) {
        return ''
    }

    return <div className="column is-12 has-text-centered">
        <img
            src={ urlMeta.url }
            alt="Image preview"
            style="
                height: 100%;
                max-height: 200px;
                width: 150px;
                object-fit: contain;
            "
        />
    </div>
}

const LoadingWrapper = () => <div className="card-content">
    <Loading/>
</div>

const DTaskFileNameForm = ({ url, fileName, setFileName, setFormStep }) => {
    const [isLoading, setLoading] = useState(true)
    const [urlMeta, setUrlMeta] = useState(null)

    const [fileNameValid, setFileNameValid] = useState(true)

    const onBackClicked = () => setFormStep(1)
    const onNextClicked = () => {
        console.log('Doing magic')
    }

    useEffect(() => {
        getUrlMetadata(url)
            .then(meta => {
                setUrlMeta(meta)
                setFileName(meta.proposed_file_name)
                setLoading(false)
            })
            .catch(err => {
                console.error(err)
            })
    }, [url])

    if (isLoading) return <LoadingWrapper />
    if (!urlMeta) return <div className="pt-3">Something went wrong :(</div>

    return <>
        <div className="card-content">
            <div className="columns is-multiline">
                { filePreview(urlMeta) }

                <div className="column is-6">
                    <span className="subtitle is-6">File size</span>
                    <br />
                    <span className="has-text-weight-bold">
                        { bytesToHuman(urlMeta.content_length) }
                    </span>
                </div>

                <div className="column is-6">
                    <span className="subtitle is-6">Content type</span>
                    <br />
                    <span className="has-text-weight-bold">
                        { urlMeta.content_type }
                    </span>
                </div>
            </div>

            <hr />

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
