import React from 'react'

export default class SelectionView extends React.Component {
    constructor(props) {
        super(props);


        this.state = {
            player: document.getElementById('player'),
            canvas: document.getElementById('canvas'),
            constraints: {
                audio: false,
                video: true
            }
        }

        this.startRecording()
    }

    startRecording() {
        navigator.mediaDevices.getUserMedia(this.state.constraints).then((stream) => {
            this.state.player.srcObject = stream;
        });
    }

    stopRecording() {
        this.state.player.srcObject.getVideoTracks().forEach(track => track.stop());
    }

    capture() {
        let jpegDataUri = null  //holds the captured frame after its converted to a data URI
        let context = this.state.canvas.getContext('2d')

        context.drawImage(this.state.player, 0, 0, this.state.canvas.width, this.state.canvas.height);
        jpegDataUri = this.state.canvas.toDataURL('image/jpeg');

        this.stopRecording()
        this.props.updatePhoto('main', jpegDataUri)
    }


    render() {
        return (
            <div>
                <video id="player" controls muted autoplay></video>
                <canvas id="canvas" width="300" height="300"></canvas>
            </div>
        )
    }
}