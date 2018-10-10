import React, { Component } from 'react';
import './App.css';

class HeroesDropDown extends React.Component {
	constructor(props){
		super(props);
	}

	removeHeroes() {
		//
	}

	render() {
		return (
			<div className="heroesSelection">
				Select Heroes:
					<select name="hero">
						<option>Adagio</option>
						<option>Alpha</option>
						<option>Anka</option>
						<option>Ardan</option>
						<option>Baptiste</option>
						<option>Baron</option>
						<option>Blackfeather</option>
						<option>Catherine</option>
						<option>Celeste</option>
						<option>Churnwalker</option>
						<option>Flicker</option>
						<option>Fortress</option>
						<option>Glaive</option>
						<option>Grace</option>
						<option>Grumpjaw</option>
						<option>Gwen</option>
						<option>Idris</option>
						<option>Joule</option>
						<option>Kensei</option>
						<option>Kestrel</option>
						<option>Kinetic</option>
						<option>Koshka</option>
						<option>Krul</option>
						<option>Lance</option>
						<option>Lorelai</option>
						<option>Lyra</option>
						<option>Malene</option>
						<option>Ozo</option>
						<option>Petal</option>
						<option>Phinn</option>
						<option>Reim</option>
						<option>Reza</option>
						<option>Ringo</option>
						<option>Rona</option>
						<option>Samuel</option>
						<option>SAW</option>
						<option>Silvernail</option>
						<option>Skaarf</option>
						<option>Skye</option>
						<option>Taka</option>
						<option>Tony</option>
						<option>Varya</option>
						<option>Vox</option>
						<option>Yates</option>
					</select>
				<button type="Button" onClick={() => this.removeHeroes()}>Remove</button>
				<br />
			</div>
		);
	}
}

class App extends Component {
	constructor(props){
		super(props);

		this.state = { 
			submitForm: false,
			heroes: [HeroesDropDown]
		};
	}

	addHeroes() {
		const heroes = this.state.heroes.concat(HeroesDropDown);
		this.setState({heroes: heroes});
	}

	handleSubmit() {
		this.setState({submitForm: true});
	}

	render() {
		if (this.state.submitForm === true){
			return <Redirect to='/result' />
		}

		return (
			<div className="form">
				<form>
					VainGlory Player Name: <input type="text" name="name" required/> CASE SENSITIVE!
					<br />
					Display How Many Games:
						<select name="numGames">
							<option>10</option>
							<option>20</option>
							<option>30</option>
							<option>40</option>
							<option>50</option>
							<option>60</option>
							<option>70</option>
							<option>80</option>
							<option>90</option>
							<option>100</option>
							<option>110</option>
							<option>120</option>
							<option>130</option>
							<option>140</option>
							<option>150</option>
							<option>160</option>
							<option>170</option>
							<option>180</option>
							<option>190</option>
							<option>200</option>
						</select>
					<br />
					{this.state.heroes.map((Element, index) => {return <Element key={index} index={index}/>})}
					<button type="Button" value="Add More Heroes" onClick={() => this.addHeroes()} />
					<button type="submit" value="Submit" onClick={() => this.handleSubmit()} />
				</form>
			</div>
		);
	}
}

export default App;