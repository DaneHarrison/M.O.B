import logo from './100_10.jpg';
import React from 'react'
import './style/App.css'

export default class App extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
		}
	}


	render() {		
		return (
      <div class='background'>
        <h1 class='title'>M.O.B</h1>
        <h3 class='desc'>Authentication using MapReduce and the Eigenface algorithm</h3>
			<div class='app'>
        <div class='cameraArea'>
          <img src={logo} class='pictureFill shadow'></img>
          <div class='btnArea'>
            <button class='captureBtn'>lol</button>
          </div>
        </div>
				<div class='pictureHolder'>
          <img src={logo} class='shadow'></img>
          <img src={logo} class='middle shadow'></img>
          <img src={logo} class='shadow'></img>
        </div>
			</div>
      </div>
		);
	}
}