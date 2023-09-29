import React from 'react';

export default class VideoRecorder extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            player: null,
            canvas: null,
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

            this.stopRecording();
            this.props.updatePhoto('main', jpegDataUri);
        }
    }

    render() {
        return (
            <div>
                <video id="player" muted autoPlay></video>
                <canvas id="canvas" width="300" height="300"></canvas>
            </div>
        );
    }
}
