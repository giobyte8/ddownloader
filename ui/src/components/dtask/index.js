import { h } from 'preact'

const formatBytes = (bytes, decimals = 2) => {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

const formatProgressText = (downloadedSize, totalSize) => {
    const fDownloaded = formatBytes(downloadedSize)
    const fTotal = formatBytes(totalSize)

    let percent = 0;
    if (totalSize > 0) {
        percent = ((downloadedSize/totalSize) * 100).toFixed(2)
    }

    return `${ fDownloaded } of ${ fTotal } (${ percent }%)`
}

const DTask = ({ targetPath, downloadedSize, totalSize, status }) => {
    return <div className="card">
        <div className="card-content">
            <div className="media">
                <div className="media-left">
                    <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image"/>
                </div>
                <div className="media-content">
                    <p className="title is-5">{ targetPath }</p>
                    <p className="subtitle is-6">
                        { formatProgressText(downloadedSize, totalSize) }
                    </p>
                </div>
            </div>

            <div className="content">
                <progress className="progress is-small" value={ downloadedSize } max={ totalSize }>15%</progress>
            </div>
        </div>

        <footer className="card-footer">
            <a href="#" className="card-footer-item has-text-danger">Abort</a>
            <a href="#" className="card-footer-item">Pause</a>
            <a href="#" className="card-footer-item">Details</a>
        </footer>
    </div>
}

export default DTask;
