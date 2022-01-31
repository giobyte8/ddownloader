import { h } from 'preact'

const Navbar = () => (
    <nav className="navbar is-light">
        <div className="container">
            <div className="navbar-menu">
                <div className="navbar-start">
                    <a href="#" className="navbar-item">Play</a>
                    <a href="#" className="navbar-item">Add</a>
                </div>
            </div>
        </div>
    </nav>
);

export default Navbar;
