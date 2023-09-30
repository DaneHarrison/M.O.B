import VideoRecorder from "./components/videoRecorder";
import logo from "./100_10.jpg";
import React from "react";
import "./style/App.css";

export default class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      recording: true,
      main: null,
      left: null,
      middle: null,
      right: null,
    };
  }

  fetchClosest() {
    //load left, middle and right
    //which ever is closest change that ones outline to green
  }

  updatePhoto() {
    //main
    //if main set recording to false
    //const base64Image = jpegDataUri.split(',')[1];
    //const binaryImageData = atob(base64Image);
    //left
    //middle
    //right
  }

  render() {
    return (
      <div class="background">
        <h1 class="title">M.O.B</h1>
        <h3 class="desc">
          Authentication using MapReduce and the Eigenface algorithm
        </h3>
        <div class="app">
          <div class="cameraArea">
            <VideoRecorder />
            {/* <img src={logo} class='pictureFill shadow'></img> */}
            <div class="btnArea">
              <form method="post" action="/" enctype="multipart/form-data">
                <dl>
                  <p>
                    <input
                      type="file"
                      name="file"
                      class="form-control"
                      autocomplete="off"
                      required
                    ></input>
                  </p>
                </dl>
                <p>
                  <input type="submit" value="Submit"></input>
                </p>
              </form>

              <button class="captureBtn">Capture</button>
              <button class="captureBtn">Submit</button>
            </div>
          </div>
          <div class="pictureHolder">
            <img src={logo} class="shadow"></img>
            <img src={logo} class="middle shadow"></img>
            <img src={logo} class="shadow"></img>
          </div>
        </div>
      </div>
    );
  }
}
