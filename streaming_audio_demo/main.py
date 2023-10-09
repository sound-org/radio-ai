from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, WebSocket

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def serve_homepage():
    content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Music Streaming</title>
</head>
<body>
    <audio id="audioPlayer" controls>
        <source src="/stream/file1.wav" type="audio/wav">
        Your browser does not support the audio element.
    </audio>

    <script>
        const audioPlayer = document.getElementById('audioPlayer');
        const audioFiles = ["file1.wav", "file2.wav", "file3.wav"];  // Add your filenames here
        let currentFileIndex = 0;

        audioPlayer.addEventListener('ended', function() {
            currentFileIndex++;
            if (currentFileIndex < audioFiles.length) {
                audioPlayer.children[0].src = "/stream/" + audioFiles[currentFileIndex];
                audioPlayer.load();
                audioPlayer.play();
            }
        });
    </script>
</body>
</html>
    """
    return HTMLResponse(content=content)


@app.get("/stream/{filename}")
async def stream_audio(filename: str):
    file_location = f"./static/{filename}"
    return StreamingResponse(open(file_location, "rb"), media_type="audio/wav")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # data = await websocket.receive_text()
        await websocket.send_text(f"Message received: ")
