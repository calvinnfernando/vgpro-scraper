import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Result from './result';
import HomePage from './HomePage';

class RouteFile extends Component {

	render() {
		return (
			<Router>
				<Switch>
					<Route path='/result' component={Result} />}} />
					<Route path='/' component={HomePage} />
				</Switch>
			</Router>
		);
	}
}

export default RouteFile;