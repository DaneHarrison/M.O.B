import VideoRecorder from './components/videoRecorder'
import logo from './100_10.jpg';
import React from 'react'
import './style/App.css'
import axios from 'axios';

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            recordingPerms: true,
            main: logo, // default image to show incase recording permissions are not granted
            left: null,
            middle: null,
            right: null
        }
    }


    disableRecording = () => {
        this.setState({ recordingPerms: false })
    }

    fetchClosest = () => {
        axios.post('http://localhost:5000/', { img: this.state.main })
            .then(response => {
                console.log(response.data); // Handle the server response
                //     //unzip res
                //     //updatePhoto
                //     //updatePhoto
            })
            .catch(error => {
                console.error(error);
            }
        );
    }

    updatePhoto = (posi, photo) => {
        switch (posi) {
            case 'main':
                this.setState({ main: photo })
                //
                //
                break;

            case 'left':
                break;

            case 'middle':
                break;

            case 'right':
                break;
        }
    }

    upload() {

    }

    render() {
        return (
            <div class='background'>
                <h1 class='title'>M.O.B</h1>
                <h3 class='desc'>Authentication using MapReduce and the Eigenface algorithm</h3>
                <div class='app'>
                    {this.state.recordingPerms
                        ? <VideoRecorder updatePhoto={this.updatePhoto} upload={this.upload} fetchClosest={this.fetchClosest} disable={this.disableRecording} />
                        : <div class='cameraArea'>
                            <img src={this.state.main} class='pictureFill shadow'></img>

                            <div class='btnArea'>
                                <button class='captureBtn'>Upload</button>
                                <button class='captureBtn' onClick={this.fetchClosest}>Submit</button>
                            </div>
                        </div>}
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