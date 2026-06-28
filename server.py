from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import pyautogui
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET = "nikita2004"

def check_secret(s: str):
    if s != SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/shutdown")
def shutdown(secret: str):
    check_secret(secret)
    subprocess.Popen("shutdown /s /t 5", shell=True)
    return {"status": "shutting down in 5 seconds"}

@app.get("/sleep")
def sleep(secret: str):
    check_secret(secret)
    subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
    return {"status": "sleeping"}

@app.get("/pause")
def pause(secret: str):
    check_secret(secret)
    pyautogui.press("playpause")
    return {"status": "toggled play/pause"}

@app.get("/mute")
def mute(secret: str):
    check_secret(secret)
    pyautogui.press("volumemute")
    return {"status": "toggled mute"}

@app.get("/launch")
def launch(secret: str, path: str):
    check_secret(secret)
    subprocess.Popen(f'start "" "{path}"', shell=True)
    return {"status": f"launched {path}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765)