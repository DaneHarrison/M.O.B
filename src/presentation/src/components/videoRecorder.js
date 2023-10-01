import React from 'react';
import '../style/App.css'

export default class VideoRecorder extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            player: null,
            canvas: null,
            recording: true,
            constraints: {
                video: true,
            }
        };
    }

    componentDidMount() {
        // Get references to the video and canvas after creation then start recording
        this.setState({ player: document.getElementById('player')})
        this.setState({ canvas: document.getElementById('canvas')})

        this.startRecording();
    }

    async startRecording() {
        let stream = null

        try {
            stream = await navigator.mediaDevices.getUserMedia(this.state.constraints);
            this.state.player.srcObject = stream;
        } 
        catch(error) {
            console.error('[ERROR]: ', error);
            this.props.disable()
        }
    }

    stopRecording() {
        if(this.state.player && this.state.player.srcObject) {
            this.state.player.srcObject.getVideoTracks().forEach((track) => track.stop());
        }
    }

    capture() {
        let context = null;
        let jpegDataUri = null;

        if(this.state.player && this.state.canvas) {
            context = this.state.canvas.getContext('2d');
            context.drawImage(this.state.player, 0, 0, this.state.canvas.width, this.state.canvas.height);
            jpegDataUri = this.state.canvas.toDataURL('image/jpeg');
            this.props.updatePhoto('main', jpegDataUri);
        }
    }

    toggleRecording = () => {
        if(this.state.recording) {
            this.capture()
            this.stopRecording();

            this.state.player.classList.add('hidden')
            this.state.canvas.classList.remove('hidden')
        }
        else {
            this.startRecording()
            this.state.player.classList.remove('hidden')
            this.state.canvas.classList.add('hidden')    
        }

        this.setState({recording: !this.state.recording})
    }

    render() {
        return (
            <div class='cameraArea'>
                <video id="player" class='stream' muted autoPlay></video>
                <canvas id="canvas" class='stream keepTall shadow hidden'></canvas> 

                <div class='btnArea'>
                    <button class='captureBtn' onClick={this.props.upload}>Upload</button> 
                    <button class='captureBtn' onClick={this.toggleRecording}>Capture</button>
                    <button class='captureBtn' onClick={this.props.fetchClosest}>Submit</button>
                </div>
            </div>
        );
    }
}