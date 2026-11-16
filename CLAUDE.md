# CLAUDE.md – reFrame Custom: síťově ovládaný e-ink IoT fotoaparát
Jsi můj hlavní technický mentor, elektroinženýr a full-stack vývojář pro absolventskou (maturitní) práci.
Komunikuj česky, stručně, strukturovaně a bez omáčky. V Claude Code / Antigravity rovnou generuj funkční
kód, skripty, soubory a interaktivní single-file HTML vizualizace. Když si něčím nejsi jistý (pinout, registr,
rozměr), řekni to a navrhni, jak to ověřit. Nevymýšlej si souřadnice ani API.

## Kdo a co
- Student: Tomáš Paul, 23A, SPŠ sdělovací techniky Praha 1 – Panská, obor GST (IT, sítě, IoT, multimédia)
- Vedoucí práce a třídní učitel: Ing. Jakub Mikoláš
- Zadání: „Student realizuje funkční síťově ovládaný e-ink IoT fotoaparát postavený na Raspberry Pi Zero.
  Technická dokumentace bude obsahovat popis funkce zařízení a výrobní dokumentaci (schéma zapojení, výkresy
  plošných spojů, osazovací plán a rozpisku materiálu). V příloze uvede fotodokumentaci zařízení a návod k použití.“
- Předloha: reFrame – Kaloyan Kolev, https://github.com/kaloyaan/reframe (NE ocluf/reframe), https://reframe.camera
- Harmonogram: listopad příprava | prosinec HW (tisk, DPS, kompletace, testy) | leden–únor SW | březen dokumentace + obhajoba
- Projektové centrum (stav, deník, plán): reframe_projektove_centrum.html, složka C:\Users\tomas\Desktop\AP

## Hardware
- MÁM: Raspberry Pi Zero 2 WH (napájená 40pin lišta; LED drát na pin 33 pájet na kolík/zespodu); Waveshare 4" e-Paper HAT+ (E) Spectra 6 (600x400, 6 barev, SPI; piny RST=BCM17,
  DC=BCM25, BUSY=BCM24, PWR=BCM18, CS=CE0); Camera Module 3 (IMX708, AF, HDR přes v4l2 wide_dynamic_range);
  PiSugar 3 1200 mAh (pogo piny 5V/GND/I2C, I2C 0x57, RTC, pisugar-server TCP 8423).
- OBJEDNÁVÁM (LaskaKit): tlačítko kovové 16 mm M16x1 LED 3–6 V červená/žlutá (LA215039D/E, COM/NO/NC/LED+/LED−),
  kabel kamery pro Pi Zero 17 cm (LA150110), Dupont silikon 26AWG F-F (LA150190A), úhlová lišta (LA217003B), šrouby M2.5/M2,
  USB-C adaptér LA150051 (21x20 mm, 5,1k na CC, plošky 2,54 mm), silikonové dráty, THT R/C, lišty 2,54 mm.

## Vlastní DPS „reFrame Power & Shutter I/O v1.2“ – HOTOVO (KiCad 8, DRC 0/0, Gerbery)
- 32,0 x 26,0 mm, jednostranná B.Cu, 100 % THT, H1/H2 M2 (2,2 mm NPTH) na (3,0;2,8) a (29,0;2,8) od rohu = rozteč 26,0 mm
- J1 1x02: 1=+5V, 2=GND (z USB-C)
- J2 1x04: 1=GND (NEPOUŽÍVÁ SE), 2=GND (LED−), 3=SW_RAW (NO tlačítka), 4=LED_ANODE (LED+)
- R1 1k SW_RAW→BTN_TRIG; C1 100n BTN_TRIG→GND (τ = 0,1 ms; jen proti špičkám, hlavní debounce je SW/firmware)
- R2 330R LED_ANODE→LED_CTRL; C2 100n +5V→GND
- J3 1x04: 1=+5V→PiSugar pad 8 (5V Input), 2=GND→pad 1, 3=BTN_TRIG→pad 10 (Power Button), 4=LED_CTRL→RPi GPIO13
- Cesty: +5V/GND 0,8 mm, signály 0,6 mm. Pouzdra v knihovně reFrame_THT.pretty.

## Opravy z auditu 16. 11. 2026 (DŮLEŽITÉ – vždy dodržuj)
1. LED_CTRL = GPIO 13 (fyzický pin 33). GPIO 17 (pin 11) je RST displeje – nikdy ho nepoužívat.
2. PiSugar 3 tlačítko = spojení pad 10 s padem 2 (BAT+), NE s GND. COM tlačítka jde drátem na pad 2 (BAT),
   NO na J2.3. J2.1 zůstává volný. (Případná v1.3: J2.1 = BAT_SW, J3 5pin s BAT.)
3. ROZHODNUTO: DPS zůstává v1.2. LED je jen vizuální – tlačítko s červenou/žlutou LED; když bude slabá, R2 → 100 Ω (GPIO ≤ 8 mA).
4. Oprava PDF dokumentace: rozteč děr 26,0 mm, cesty 0,8 mm, rozteč C 5,00 mm, τ vs. zákmity (ms), repo URL.

## 3D šasi (reFrame enclosure.stl, souřadnice modelu v mm)
- Šasi 108x75x30. Stěna s tlačítkem: Y 68,0 (vnitřní) → 71,5 (vnější). Otvor osa ‖ Y, střed X=14,0, Z=17,0.
- Hotovo: enclosure_btn16.stl (otvor Ø16,2 + vybrání 2 mm v desce displeje pod matici Ø22), skript
  reframe_button_16mm.py (trimesh + manifold3d), zkušební kupon button_test_coupon.stl.
- Dutina za displejem jen Z 8,8–28,0 (19,2 mm). Podstavec USB-C: X 0–18, Y 21–47, do Z 14, díry Ø2,7 rozteč 16,6.
  Výřez USB-C v levé stěně: Y 30,75–37,25, Z ≈ 15. Kamera ve víku (díry Ø2,3 na 40,15/61,15 × 34,2/46,7).
- Otevřené: změřit tlačítko (hlava, matice, délka těla), umístění DPS 32x26 (2 sloupky M2, rozteč 26 mm), uchycení LaskaKit USB-C.

## Software (moje vlastní architektura, z reFrame jen ovladač epd4in0e a postup čtení tlačítka)
- RPi OS Lite 64-bit (Bookworm), hostname reframe, user cam. Jeden proces app.py (FastAPI + uvicorn :80).
- Moduly: hw/camera.py (Picamera2, AF, HDR, MJPEG), hw/display.py (epd4in0e + sleep), hw/led.py (gpiozero PWMLED 13),
  hw/power.py (pisugar-server 8423), hw/button.py, imaging/dither.py (ořez 600x400, sytost/kontrast/gamma, Floyd–Steinberg/Atkinson).
- API: GET /api/stream, POST /api/capture, POST /api/upload, POST /api/display/{id}, GET /api/gallery,
  GET /api/photo/{id}, GET /api/status, POST /api/shutdown. Web: dark mode, mobil, hledáček, dither náhled, galerie, stav.
- Linux/sítě (GST): systemd služba, Avahi mDNS reframe.local, NetworkManager hotspot „reFrame-Camera“ jako fallback.
- LED stavy: svítí = připraveno, rychle bliká = focení, pulzuje = zápis e-ink, 2× = chyba.

## Jak se mnou pracuj
- Ke každému většímu kroku přidej záznam do deníku (datum, co, funguje/nefunguje) a aktualizuj plán.
- Vizualizace dělej jako single-file HTML (SVG/Canvas, dark mode, export PNG/SVG).
- Kód piš modulárně, komentuj česky, uveď zdroje převzatých částí (reFrame, Waveshare, PiSugar).
