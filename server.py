from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/upload_test")
async def upload_test(request: Request):
    await request.body()  # actually read the uploaded blob
    return {"status": "ok"}

@app.post("/client_result")
async def receive_client_result(request: Request):
    data = await request.json()
    latency = data.get("latency")
    download = data.get("download")
    upload = data.get("upload")

    # Just print or log the results
    print(f"📊 Client Test Result:")
    print(f"Latency: {latency} ms")
    print(f"Download: {download} Mbps")
    print(f"Upload: {upload} Mbps\n")

    return {"status": "success", "message": "Results logged successfully"}
