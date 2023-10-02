import VideoRecorder from './components/videoRecorder';
import Background from './components/background'
import empty from './default.jpg';
import React from 'react';
import axios from 'axios';
import './style/App.css';


export default class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      fileInputRef: React.createRef(),
      recordingPerms: true,
      main: empty,
      left: empty,
      right: empty,
      name: ''
    };
  }

  disableRecording = () => {
    this.setState({ recordingPerms: false });
  };

  fetchClosest = () => {
    let data = null;

    axios
      .post('http://localhost:5000/', { img: this.state.main })
      .then((response) => {
        data = response.data;
        this.setState({ left: this.loadPythonJSONImg(data.meanFace) });
        this.setState({ right: this.loadPythonJSONImg(data.photo) });
        this.setState({ name: data.name });
      })
      .catch((error) => {
        console.error(error);
      });
  };

  loadPythonJSONImg(base64JSONImg) {
    base64JSONImg = base64JSONImg.replace('\'', '');
    base64JSONImg = base64JSONImg.replace('\"', '');
    base64JSONImg = base64JSONImg.substring(1, base64JSONImg.length - 1);
    base64JSONImg = 'data:image/jpeg;base64,' + base64JSONImg;

    return base64JSONImg;
  }

  updatePhoto = (posi, photo) => {
    switch (posi) {
      case 'main':
        this.setState({ main: photo });
        break;

      case 'left':
        this.setState({ left: photo });
        break;

      case 'right':
        this.setState({ right: photo });
        break;
    }
  };

  upload = () => {
    this.state.fileInputRef.current.click();
  };

  handleFileChange = (event) => {
    let selectedFile = event.target.files[0];

    if(selectedFile) {
      let reader = new FileReader();

      reader.onload = (event) => {
        let fileContent = event.target.result;
        this.setState({ main: fileContent });
      };

      reader.readAsDataURL(selectedFile);
    }
  };

  render() {
    return (
      <div>
        <Background/>
        <h1 class='title'>M.O.B</h1>
        <h3 class='desc'>Authentication using MapReduce and the Eigenface algorithm</h3>

        <div class='app'>
          {this.state.recordingPerms 
            ? ( <VideoRecorder updatePhoto={this.updatePhoto} fetchClosest={this.fetchClosest} disable={this.disableRecording}/> ) 
            : (
            <div class='cameraArea'>
              <img src={this.state.main} class='pictureFill shadow'></img>

              <div class='btnArea'>
                <input
                  type='file'
                  ref={this.state.fileInputRef}
                  style={{ display: 'none' }}
                  onChange={this.handleFileChange}
                />
                <button class='captureBtn' onClick={this.upload}>Upload</button>
                <button class='captureBtn' onClick={this.fetchClosest}>Submit</button>
              </div>
            </div>
          )}
          <div class='pictureHolder'>
            <img src={this.state.left} class='shadow'></img>
            <div class='welcomeMsg'>
            <h1>Welcome!</h1>
            <h1>{this.state.name}</h1>
            </div>
            <img src={this.state.right} class='shadow'></img>
          </div>
        </div>
      </div>
    );
  }
}
