from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os, platform, re, speedtest, asyncio

app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def ping(host="8.8.8.8", count=3):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = f"ping {param} {count} {host}"
    response = os.popen(command).read()
    return response

def parse_latency(response):
    match_win = re.search(r'Average = (\d+)', response)
    if match_win:
        return int(match_win.group(1))
    match_unix = re.search(r' = [\d\.]+/([\d\.]+)/[\d\.]+/[\d\.]+ ms', response)
    if match_unix:
        return float(match_unix.group(1))
    return None

@app.get("/ping")
async def get_ping():
    response = ping()
    latency = parse_latency(response)
    return {"latency": latency or None}

@app.post("/client_result")
async def receive_client_result(request: Request):
    data = await request.json()
    print("Client:", data)
    return {"status": "ok"}