#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Erzeugt die eingebettete Ephemeride des WAHREN Mondknotens fuer den
Eclipse Navigator (Bernadettes Vorgabe 25.07.2026: Berechnungsgrundlage
wahrer Knoten, nicht mittlerer — die Engine kann nur den mittleren).

Quelle: Swiss Ephemeris (pyswisseph, SE_TRUE_NODE, Moshier-Ephemeride,
Ekliptik des Datums) = dieselbe Basis wie professionelle Astro-Software.
Muster: build_womancode_asteroids.py (JPL-Ephemeride eingebacken,
Browser interpoliert linear ueber origin.julianDate).

Format: outputs/true-node-data.js
  TN_START_JD (JD UT des ersten Werts), TN_STEP (1 Tag),
  TN_DATA = Base36-String, 3 Zeichen je Wert (Zentigrad 0..35999).
Zeitraum: 1900-01-01 bis 2036-01-01 (deckt Geburtsjahrgaenge des Readers).
"""
import os
import swisseph as swe

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "true-node-data.js")

JD_START = swe.julday(1900, 1, 1, 0.0)
JD_END = swe.julday(2036, 1, 1, 0.0)
STEP = 1.0

def true_node(jd):
    pos, _ = swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_MOSEPH)
    return pos[0] % 360.0

vals = []
jd = JD_START
while jd <= JD_END:
    vals.append(true_node(jd))
    jd += STEP

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"
def b36(n):
    s = ""
    for _ in range(4):
        s = DIGITS[n % 36] + s
        n //= 36
    return s

data = "".join(b36(int(round(v * 1000)) % 360000) for v in vals)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("// Wahrer Mondknoten (Swiss Ephemeris SE_TRUE_NODE, Moshier, Ekliptik des Datums)\n")
    f.write("// 1900-01-01 bis 2036-01-01, 1-Tages-Schritt, Base36-Zentigrad (3 Zeichen/Wert)\n")
    f.write("const TN_START_JD = %.1f;\n" % JD_START)
    f.write("const TN_STEP = %.1f;\n" % STEP)
    f.write('const TN_DATA = "%s";\n' % data)

print("OK ->", OUT)
print("Werte:", len(vals), " Groesse:", len(data), "Zeichen")

# --- Genauigkeitspruefung: Interpolation zwischen den Stuetzstellen ---------
import random
random.seed(7)
def interp(jd):
    # quadratisch (3 Stuetzstellen), wie im Reader
    idx = (jd - JD_START) / STEP
    i = max(1, min(round(idx), len(vals) - 2))
    t = idx - i
    v = lambda k: int(data[k*4:k*4+4], 36) / 1000.0
    y1 = v(i)
    y0 = y1 + (((v(i-1) - y1 + 540) % 360) - 180)
    y2 = y1 + (((v(i+1) - y1 + 540) % 360) - 180)
    return (y1 + t*(y2 - y0)/2 + t*t*(y2 - 2*y1 + y0)/2) % 360.0

worst = 0.0
for _ in range(4000):
    jd = JD_START + random.random() * (JD_END - JD_START - 2)
    err = abs(((interp(jd) - true_node(jd) + 540) % 360) - 180)
    worst = max(worst, err)
print("Max. Interpolationsfehler (4000 Stichproben): %.4f Grad = %.1f Bogenminuten" % (worst, worst * 60))
