import asyncio, subprocess, threading, time
from pathlib import Path
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from hw.camera import Camera
from hw.display import Display
from hw.led import StatusLed
from hw.power import battery_status, cpu_temp, disk_free_gb
from hw.button import button_events
from imaging.dither import prepare, dither_fast

PHOTOS = Path("/home/cam/photos"); PHOTOS.mkdir(parents=True, exist_ok=True)
app = FastAPI(title="reFrame Custom API")
cam, disp, led = Camera(), Display(), StatusLed()
lock = asyncio.Lock()                      # kamera + displej: jedna úloha najednou
loop = None

def mjpeg():
    while True:
        with cam.stream.cond:
            cam.stream.cond.wait()
            frame = cam.stream.frame
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"

@app.get("/api/stream")
def stream():
    return StreamingResponse(mjpeg(), media_type="multipart/x-mixed-replace; boundary=frame")

async def shoot_and_show(img=None):
    async with lock:
        led.busy()
        pid = time.strftime("%Y%m%d_%H%M%S")
        if img is None:
            img = await asyncio.to_thread(cam.capture, PHOTOS / f"{pid}.jpg")
        else:
            img.convert("RGB").save(PHOTOS / f"{pid}.jpg", quality=92)
        d = await asyncio.to_thread(lambda: dither_fast(prepare(img)))
        d.save(PHOTOS / f"{pid}_dither.png")
        led.writing()
        await asyncio.to_thread(disp.show, d)
        led.ready()
        return {"id": pid}

@app.post("/api/capture")
async def capture():
    return await shoot_and_show()

@app.post("/api/upload")
async def upload(file: UploadFile):
    return await shoot_and_show(Image.open(file.file))

@app.post("/api/display/{pid}")
async def redisplay(pid: str):
    p = PHOTOS / f"{pid}_dither.png"
    if p.parent != PHOTOS or not p.exists():
        raise HTTPException(404)
    async with lock:
        led.writing(); await asyncio.to_thread(disp.show, Image.open(p).convert("RGB")); led.ready()
    return {"ok": True}

@app.get("/api/gallery")
def gallery():
    return sorted((p.stem for p in PHOTOS.glob("*.jpg")), reverse=True)

@app.get("/api/photo/{pid}")
def photo(pid: str, dithered: bool = False):
    p = PHOTOS / (f"{pid}_dither.png" if dithered else f"{pid}.jpg")
    if p.parent != PHOTOS or not p.exists():
        raise HTTPException(404)
    return FileResponse(p)

@app.get("/api/status")
def status():
    return {**battery_status(), "cpu_temp": cpu_temp(), "free_gb": disk_free_gb(),
            "photos": len(list(PHOTOS.glob("*.jpg")))}

@app.post("/api/shutdown")
def shutdown():
    subprocess.Popen(["sudo", "shutdown", "-h", "now"])     # sudoers: cam smí shutdown
    return {"ok": True}

def button_loop():
    for ev in button_events():
        if ev == "single":
            asyncio.run_coroutine_threadsafe(shoot_and_show(), loop)

@app.on_event("startup")
async def startup():
    global loop
    loop = asyncio.get_running_loop()
    threading.Thread(target=button_loop, daemon=True).start()
    led.ready()

app.mount("/", StaticFiles(directory="web", html=True), name="web")
