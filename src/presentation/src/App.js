import VideoRecorder from './components/videoRecorder';
import logo from './100_10.jpg';
import React from 'react';
import axios from 'axios';
import './style/App.css'

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            recordingPerms: true,
            main: logo,
            left: logo,
            right: logo
        }
    }


    disableRecording = () => {
        this.setState({ recordingPerms: false })
    }

    fetchClosest = () => {
        let data = null;

        axios.post('http://localhost:5000/', { img: this.state.main })
            .then(response => {
                data = response.data
                this.setState({ left: this.loadPythonJSONImg(data.meanFace) })
                this.setState({ right: this.loadPythonJSONImg(data.bestMapping) })
            })
            .catch(error => {
                console.error(error);
            }
        );
    }

    loadPythonJSONImg(base64JSONImg) {
        base64JSONImg = base64JSONImg.replace('\"', '')
        base64JSONImg = base64JSONImg.replace('\'', '')
        base64JSONImg = base64JSONImg.substring(1, base64JSONImg.length - 1);
        base64JSONImg = 'data:image/jpeg;base64,' + base64JSONImg

        return base64JSONImg
    }

    updatePhoto = (posi, photo) => {
        switch (posi) {
            case 'main':
                this.setState({ main: photo })
                break;

            case 'left':
                this.setState({ main: photo })
                break;

            case 'right':
                this.setState({ main: photo })
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
                        <img src={this.state.left} class='shadow'></img>
                        <img class='middle shadow invisible'></img>
                        <img src={this.state.right} class='shadow'></img>
                    </div>
                </div>
            </div>
        );
    }
}