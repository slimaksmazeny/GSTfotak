import io, threading
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import controls

class StreamingOutput(io.BufferedIOBase):
    """Drží poslední JPEG snímek pro MJPEG stream."""
    def __init__(self):
        self.frame, self.cond = None, threading.Condition()
    def write(self, buf):
        with self.cond:
            self.frame = buf
            self.cond.notify_all()

class Camera:
    def __init__(self):
        self.cam = Picamera2()
        self.video_cfg = self.cam.create_video_configuration(main={"size": (640, 480)})
        self.still_cfg = self.cam.create_still_configuration()        # 4608 x 2592
        self.stream = StreamingOutput()
        self._start_preview()

    def _start_preview(self):
        self.cam.configure(self.video_cfg)
        self.cam.start_recording(JpegEncoder(), FileOutput(self.stream))
        self.cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})

    def capture(self, path):
        """Plné rozlišení: zastaví náhled, doostří, vyfotí, uloží JPG, obnoví náhled."""
        self.cam.stop_recording()                     # OVĚŘIT na HW (paměť 512 MB)
        self.cam.configure(self.still_cfg)
        self.cam.start()
        self.cam.autofocus_cycle()
        img = self.cam.capture_image("main")
        img.save(path, quality=92)
        self.cam.stop()
        self._start_preview()
        return img

    def set_focus(self, mode):                        # "auto" | "macro" | "inf"
        if mode == "auto":
            self.cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        else:
            self.cam.set_controls({"AfMode": controls.AfModeEnum.Manual,
                                   "LensPosition": 10.0 if mode == "macro" else 0.0})
