import React, { Component } from 'react';

class Result extends Component {
	constructor(props){
		super(props);
		this.state = {
			error: null,
			isLoaded: false,
			heroNamesArr: [],
			avgKDAArr: [],
			killArr: [],
			deathArr: [],
			assistArr: [],
			kdaArr: [],
			winLossArr: [],
			modesArr: [],
			itemsArr: []
		};
	}

	componentDidMount(){
		// generate complete url
		var url = "http://localhost:5000/sortFunc?";
		var name_str = "name=";
		var numGames_str = "numGames=";
		var hero_str = "hero=";
		var ampersand_str = "&"
		var completeURL = url + name_str + this.props.location.state.name + ampersand_str + numGames_str + this.props.location.state.numGames;
		for (var i = 0; i < this.props.location.state.hero.length; i++){
			completeURL = completeURL + ampersand_str + hero_str + this.props.location.state.hero[i];
		}

		fetch(completeURL)
			.then(res => res.json())
			.then(
				(result) => {
					this.setState({
						isLoaded: true,
						heroNamesArr: result.hero_names_arr,
						avgKDAArr: result.avg_kda_arr,
						killArr: result.kills_arr,
						deathArr: result.deaths_arr,
						assistArr: result.assist_arr,
						kdaArr: result.kda_arr,
						winLossArr: result.win_loss_arr,
						modesArr: result.modes_arr,
						itemsArr: result.items_arr
					});
				},
				(error) => {
					this.setState({
						isLoaded: true,
						error
					});
				}
			)
	}

	render(){
		const {error, isLoaded, heroNamesArr, avgKDAArr, killArr, deathArr, assistArr, kdaArr, winLossArr, modesArr, itemsArr} = this.state;
		if (error) {
			return <div>Error: {error.message}</div>;
		} else if (!isLoaded) {
			return <div>Loading... This may take some time.</div>;
		} else {
			return (
				<div className="sortResult">
					<ul>
						{heroNamesArr.map(heroName => (
							<li key={heroName}>
								{heroName}
							</li>
						))}
					</ul>
				</div>
			);
		}
	}
}

export default Result;