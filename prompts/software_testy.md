# Prompt: software – prosincové testy HW

Navazuješ na projekt reFrame Custom (CLAUDE.md). HW je složený. Napiš sadu malých testovacích skriptů
(tests/hw_*.py), každý samostatně spustitelný přes SSH, s jasným výpisem OK/CHYBA:
1. hw_camera.py – Picamera2: náhled 640x480 → JPEG, autofocus_cycle, foto 12 MPx, HDR zap/vyp (v4l2-ctl).
2. hw_display.py – epd4in0e: testovací obrazec 6 barev + text, změř dobu překreslení, sleep.
3. hw_led.py – GPIO13: on/blink/pulse, každý stav 3 s.
4. hw_button.py – vypisuj stisky tlačítka (krátký/dlouhý), převezmi postup z reFrame (I2C 0x57) a uveď zdroj.
5. hw_battery.py – pisugar-server 8423: %, napětí, nabíjení, RTC čas.
6. hw_all.py – spustí vše a vytvoří report (Markdown) do deníku.
Před psaním si přečti reframe.py z github.com/kaloyaan/reframe kvůli ověřeným detailům (HDR, tlačítko).
Uveď, co je nutné ověřit na skutečném HW.
