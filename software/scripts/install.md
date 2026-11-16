# Instalace na Raspberry Pi (prosinec – první test)

```bash
sudo apt update && sudo apt install -y git python3-venv python3-picamera2 python3-spidev \
     python3-gpiozero v4l-utils i2c-tools netcat-openbsd
sudo raspi-config nonint do_i2c 0 && sudo raspi-config nonint do_spi 0
sudo usermod -a -G video,i2c,spi,gpio cam

# PiSugar Power Manager (vyber PiSugar 3)
wget https://cdn.pisugar.com/release/pisugar-power-manager.sh && bash pisugar-power-manager.sh -c release
echo "set_anti_mistouch false" | nc -q 0 127.0.0.1 8423      # zapínání jedním stiskem

git clone <tvůj repozitář> reframe-custom && cd reframe-custom
python3 -m venv --system-site-packages .venv
.venv/bin/pip install fastapi "uvicorn[standard]" pillow numpy python-multipart

# rychlé testy HW
i2cdetect -y 1                       # PiSugar 3 na 0x57
rpicam-still -o test.jpg             # kamera
v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0   # HDR
python3 -c "from gpiozero import LED; import time; l=LED(13); l.on(); time.sleep(2)"   # LED kroužek
```
