# Prompt: oprava dokumentace DPS / případná v1.3

Navazuješ na projekt reFrame Custom (CLAUDE.md). Přikládám 23APaulT_kicad.zip a PDF „Výrobní dokumentace DPS v1.2“.
1. Oprav text dokumentace podle auditu: rozteč montážních děr 26,0 mm; šířky cest 0,8/0,6 mm; rozteč C 5,00 mm;
   zákmity tlačítka jsou v řádu ms (τ = 0,1 ms jen proti špičkám, hlavní debounce SW); LED_CTRL → GPIO 13 (pin 33);
   COM tlačítka → PiSugar pad 2 (BAT); J2.1 nezapojen; výpočet proudu LED pro skutečnou barvu LED; repo kaloyaan/reframe.
2. Vytvoř aktualizovanou propojovací tabulku vodičů a blokové schéma celého zařízení.
3. (Jen pokud řeknu „dělej v1.3“) Uprav .kicad_sch a .kicad_pcb: J2.1 → síť BAT_SW, J3 na 1x05 (5 = BAT),
   [volitelně Q1 BC547 TO-92 + R3 4k7 pro LED z +5V], zachovej 100 % THT, jednu vrstvu B.Cu, rozměr 32x26 mm
   a díry M2 na stejných místech. Spusť/zdůvodni DRC a vygeneruj Gerbery.
