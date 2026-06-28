from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import pyautogui
import uvicorn
import pyperclip
import ctypes

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

@app.get("/volume_up")
def volume_up(secret: str):
    check_secret(secret)
    for _ in range(4):
        pyautogui.press("volumeup")
    return {"status": "volume up"}

@app.get("/volume_down")
def volume_down(secret: str):
    check_secret(secret)
    for _ in range(4):
        pyautogui.press("volumedown")
    return {"status": "volume down"}

@app.get("/lock")
def lock(secret: str):
    check_secret(secret)
    subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True, capture_output=True, text=True)
    return {"status": "locked"}

@app.get("/type")
def type_text(secret: str, text: str):
    check_secret(secret)
    import pyperclip
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    return {"status": "typed"}

@app.get("/test_lock")
def test_lock(secret: str):
    check_secret(secret)
    result = subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True, capture_output=True, text=True)
    return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765)