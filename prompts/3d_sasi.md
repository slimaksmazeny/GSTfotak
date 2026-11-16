# Prompt: úprava 3D šasi (pokračování / úprava po změření)

Navazuješ na projekt reFrame Custom (kontext v CLAUDE.md). Úkol: dokončit úpravu 3D šasi pro 16mm tlačítko
a přidat držák mé DPS. Pracuj v Pythonu (trimesh + manifold3d, `pip install trimesh manifold3d numpy`), NE v OpenSCADu
s vymyšlenými souřadnicemi. Každou souřadnici si nejdřív ověř na modelu (ray-casting / řezy) a vypiš ji.

PŘILOŽENÉ SOUBORY: enclosure.stl (originál reFrame), enclosure_btn16.stl (moje současná verze), lid.stl,
reframe_button_16mm.py (současný skript), fotky/rozměry níže.

ZNÁMÁ GEOMETRIE (souřadnice modelu, mm): šasi 108x75x30; stěna s tlačítkem Y 68,0→71,5; původní otvor Ø12,2
(+ zahloubení Ø14,5 × 2 mm), osa ‖ Y, střed X=14,0 Z=17,0. Deska displeje Z 4,8–8,8, dutina Z 8,8–28,0, víko Z 28–30.
Podstavec USB-C X 0–18, Y 21–47, do Z 14. Výřez USB-C v levé stěně Y 30,75–37,25, Z≈15.

ZMĚŘENÉ ROZMĚRY TLAČÍTKA LA215039 (doplním):
- průměr hlavy: ___ mm, výška hlavy nad panelem: ___ mm
- matice: průměr/rozměr přes rohy ___ mm, tloušťka ___ mm
- délka těla za panelem včetně vývodů: ___ mm, max. průměr těla: ___ mm
- výsledek zkušebního kuponu: ___

ÚKOLY:
1. Podle rozměrů zkontroluj kolize (matice × deska displeje/víko, tělo × podstavec USB-C/Pi). Když je třeba,
   posuň osu otvoru (CENTER_X/CENTER_Z), uprav vybrání a vypiš vůle v mm.
2. Volitelně zahloubení pro hlavu tlačítka (jen pokud chci zarovnání do roviny).
3. Přidej 2 sloupky pro DPS 32x26 mm (díry M2, rozteč 26,0 mm, otvory 3,0 mm od kratší a 2,8 mm od horní hrany),
   výška ___ mm, otvor Ø1,7 pro samořezný M2 nebo Ø2,2 + matice. Umístění: ___ (zvolím po suché montáži).
4. Případně uprav podstavec pro LaskaKit USB-C (21x20 mm, rozteč děr ___ mm, výška konektoru ___ mm).
5. Výstup: upravené STL (vodotěsné, ověř is_watertight), aktualizovaný parametrický skript, PNG řezy před/po,
   zkušební kupon a krátký záznam do deníku.
