# Síťově ovládaný e-ink IoT fotoaparát

Absolventská práce · **Tomáš Paul (23A)** · SPŠ sdělovací techniky Praha 1 – Panská, obor GST
Vedoucí práce: **Ing. Jakub Mikoláš** · školní rok 2026/27

Kompaktní digitální fotoaparát a zároveň fotorámeček s 6barevným e-ink displejem (Spectra 6).
Raspberry Pi Zero 2 WH, Camera Module 3, PiSugar 3 a vlastní THT deska plošných spojů. Ovládá se tlačítkem
nebo z mobilu přes Wi-Fi web (živý hledáček, galerie, stav baterie).

## 👉 Projektové centrum (web)
Interaktivní přehled stavu, plánu, deníku, schémat, DPS, 3D šasi a softwaru:
**https://slimaksmazeny.github.io/REPO/** (GitHub Pages ze souboru `index.html`)

## Obsah repozitáře
| Složka | Obsah |
|---|---|
| `index.html` | projektové centrum (otevře se i offline v prohlížeči) |
| `hardware/pcb/` | KiCad 8 projekt DPS v1.2 (schéma, layout, knihovna `reFrame_THT`), Gerbery, PDF výrobní dokumentace |
| `hardware/3d/` | STL díly šasi k tisku (otvor pro 16mm tlačítko), zkušební kupon, skript úpravy, návod k tisku |
| `software/` | kostra vlastního softwaru (FastAPI, Picamera2, dithering, e-ink, LED, PiSugar), systemd, síť |
| `prompts/`, `CLAUDE.md` | kontext a prompty pro AI asistenta |

## Stav (16. 11. 2026)
- ✅ DPS v1.2 navržena v KiCadu (DRC 0 chyb), Gerbery hotové – **zůstává beze změny**
- ✅ Šasi upraveno pro tlačítko 16 mm (otvor Ø16,2 mm) – čeká na zkušební tisk
- ⏳ Objednávka dílů (LaskaKit), výroba DPS, 3D tisk – prosinec
- 📋 Software – leden/únor · dokumentace a obhajoba – březen

Opravy zapojení z kontroly 16. 11.: LED tlačítka na **GPIO 13 (pin 33)** (GPIO 17 je RST displeje),
společný kontakt tlačítka na **PiSugar pad 2 (BAT)**.

## Zdroje a licence
- Projekt vychází z open-source fotoaparátu **reFrame** od Kaloyana Koleva – <https://github.com/kaloyaan/reframe>.
  3D modely v `hardware/3d/` jsou **upravené** soubory reFrame (licence **CC BY 4.0**), změna: otvor tlačítka 12,2 → 16,2 mm a vybrání pod matici.
  Tento projekt není oficiální součástí reFrame; název reFrame patří jeho autorovi.
- Vlastní DPS, software a dokumentace: Tomáš Paul. Při práci byli využiti AI asistenti (Google Gemini, Anthropic Claude).
