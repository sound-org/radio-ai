from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

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
        <audio controls>
            <source src="/stream/test.wav" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
    </body>
    </html>
    """
    return HTMLResponse(content=content)


@app.get("/stream/{filename}")
async def stream_audio(filename: str):
    file_location = f"./static/{filename}"
    return StreamingResponse(open(file_location, "rb"), media_type="audio/wav")
