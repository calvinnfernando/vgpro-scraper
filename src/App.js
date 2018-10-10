import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Result from './result';
import HomePage from './HomePage';
import './App.css';

class App extends Component {

	render() {
		return (
			<Router>
				<Switch>
					<Route path='/result' render={() => {<Result link="http://localhost:5000/sortFunc?name=calvinfernando&numGames=10&hero=Vox&hero=Lyra"/>}} />
					<Route path='/' component={HomePage} />
				</Switch>
			</Router>
		);
	}
}

export default App;