import { h } from 'preact'
import style from './style.scss'

const Loading = () => <div className="p-3 pt-5">
    <div class={ style.loadingDots }></div>
</div>

export default Loading
