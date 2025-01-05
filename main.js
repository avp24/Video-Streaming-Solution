const ws = new WebSocket("ws://localhost:8089");
const buttons = {
    liveStream: document.getElementById("liveStream"),
    playback: document.getElementById("playback"),
    startRecording: document.getElementById("startRecording"),
    stopRecording: document.getElementById("stopRecording"),
    stopStream: document.getElementById("stopStream"),
};
const videoElement = document.getElementById("video");
const playbackVideo = document.getElementById("playbackVideo");

let stopStream = false;

// Utility to set button active and reset others
function setActiveButton(buttonId) {
    Object.keys(buttons).forEach((key) => {
        buttons[key].classList.remove("active");
    });
    if (buttonId) {
        buttons[buttonId].classList.add("active");
    }
}

ws.onmessage = (event) => {
    if (!stopStream) {
        const data = JSON.parse(event.data);
        if (data.frame) {
            videoElement.src = `data:image/png;base64,${data.frame}`;
            videoElement.style.display = "block";
            playbackVideo.style.display = "none";
        }
    }
};

buttons.liveStream.onclick = () => {
    stopStream = false;
    setActiveButton("liveStream");
};

buttons.playback.onclick = () => {
    stopStream = true;
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "video/mp4,video/avi";
    fileInput.onchange = () => {
        const file = fileInput.files[0];
        if (file) {
            playbackVideo.src = URL.createObjectURL(file);
            playbackVideo.style.display = "block";
            videoElement.style.display = "none";
            setActiveButton("playback");
        }
    };
    fileInput.click();
};

buttons.startRecording.onclick = () => {
    const path = prompt("Enter the path for saving recordings:", "./recordings");
    ws.send(JSON.stringify({ action: "start_recording", path }));
    setActiveButton("startRecording");
};

buttons.stopRecording.onclick = () => {
    ws.send(JSON.stringify({ action: "stop_recording" }));
    setActiveButton("stopRecording");
};

buttons.stopStream.onclick = () => {
    stopStream = true;
    videoElement.style.display = "none";
    setActiveButton("stopStream");
};

