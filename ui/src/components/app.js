import { h } from 'preact';
import { Router } from 'preact-router';

import Header from './header';

// Code-splitting is automated for `routes` directory
import Home from '../routes/home';
import Profile from '../routes/profile';

import DTasksGrid from './dtasks_grid';
import Navbar from './navbar';
import AddTaskForm from '../routes/add_dtask';


const App = () => (
	<div id="app">
		<Navbar />
		<section className="section">
			<Router>
				<DTasksGrid path="/" />
				<AddTaskForm path="/add" />
				<Profile path="/profile/" user="me" />
				<Profile path="/profile/:user" />
			</Router>
		</section>
	</div>
);

export default App;
