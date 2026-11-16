#!/usr/bin/env python3
"""
reFrame enclosure – úprava otvoru spouště 12 mm -> 16,2 mm (LaskaKit LA215039A, závit M16x1)
Autor: Claude (pro Tomáše Paula, 23A) | 2026-11-16
Použití:  pip install trimesh manifold3d numpy
          python reframe_button_16mm.py enclosure.stl
Výstup:   enclosure_btn16.stl  (celé šasi)
          button_test_coupon.stl (jen roh stěny s otvorem – rychlý zkušební tisk ~15 min)

Geometrie zjištěná z originálu (github.com/kaloyaan/reframe, hardware/enclosure.stl):
  - původní otvor: Ø12,2 mm, osa rovnoběžná s Y, střed X=14,0  Z=17,0
  - vnější zahloubení Ø14,5 mm hloubka 2 mm (Y 69,5..71,5)
  - stěna: vnitřní líc Y=68,0, vnější líc Y=71,5 (tloušťka 3,5 mm)
  - vnitřní dutina za displejem: Z 8,8 .. 28,0 (= 19,2 mm), nad ní víko
"""
import sys, numpy as np, trimesh

# ---------- PARAMETRY (uprav po změření tlačítka posuvkou) ----------
HOLE_D      = 16.2   # průměr otvoru pro závit M16
CENTER_X    = 14.0   # střed otvoru (originál 14,0)
CENTER_Z    = 17.0   # střed otvoru (originál 17,0)
WALL_IN_Y   = 68.0
WALL_OUT_Y  = 71.5
NUT_D       = 22.0   # PŘEDPOKLAD: vnější průměr matice + vůle -> ZMĚŘIT!
NUT_RELIEF  = True   # vybrání v desce pod maticí (deska displeje končí na Z=8,8)
NUT_DEPTH   = 4.0    # jak hluboko od vnitřní stěny je matice + podložka
CB_D, CB_DEPTH = 0.0, 0.0   # volitelné vnější zahloubení pro hlavu (např. 19.0 a 1.5); 0 = vypnuto
# --------------------------------------------------------------------

def cyl_y(d, y0, y1, x=CENTER_X, z=CENTER_Z):
    c = trimesh.creation.cylinder(radius=d/2, height=y1-y0, sections=128)
    c.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1,0,0]))
    c.apply_translation([x, (y0+y1)/2, z])
    return c

def main(src):
    m = trimesh.load(src)
    assert m.is_watertight, "Vstupní STL není vodotěsné"
    cutters = [cyl_y(HOLE_D, WALL_IN_Y-1.0, WALL_OUT_Y+1.0)]
    if CB_D > 0:
        cutters.append(cyl_y(CB_D, WALL_OUT_Y-CB_DEPTH, WALL_OUT_Y+1.0))
    if NUT_RELIEF:
        relief = cyl_y(NUT_D, WALL_IN_Y-NUT_DEPTH, WALL_IN_Y+0.01)
        # jen část pod Z=8,8 (deska), nesmí zasáhnout do přední kapsy displeje (Z<4,8)
        box = trimesh.creation.box(extents=[60, 20, 8.8-6.8])
        box.apply_translation([CENTER_X, WALL_IN_Y-NUT_DEPTH/2, (8.8+6.8)/2])
        cutters.append(trimesh.boolean.intersection([relief, box], engine='manifold'))
    out = trimesh.boolean.difference([m] + cutters, engine='manifold')
    out.export('enclosure_btn16.stl')
    # zkušební kupon
    cbox = trimesh.creation.box(extents=[36, 14, 30])
    cbox.apply_translation([CENTER_X+3, 66.0, 15])
    coupon = trimesh.boolean.intersection([out, cbox], engine='manifold')
    coupon.export('button_test_coupon.stl')
    # kontrola vůlí
    lo, hi = CENTER_Z-HOLE_D/2, CENTER_Z+HOLE_D/2
    print(f"Otvor Ø{HOLE_D}: Z {lo:.1f}..{hi:.1f} (deska končí Z=8.8, víko začíná Z=28.0)")
    print(f"Matice Ø{NUT_D}: Z {CENTER_Z-NUT_D/2:.1f}..{CENTER_Z+NUT_D/2:.1f}  X {CENTER_X-NUT_D/2:.1f}..{CENTER_X+NUT_D/2:.1f}")
    if CENTER_Z+NUT_D/2 > 28.0: print("  !! matice přesahuje pod víko (Z>28) -> zmenšit NUT_D/posunout CENTER_Z nebo vybrat i víko")
    print("Objem originál / nový [cm3]:", round(m.volume/1000,2), round(out.volume/1000,2),
          "| watertight:", out.is_watertight)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'enclosure.stl')
