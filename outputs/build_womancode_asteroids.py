#!/usr/bin/env python3
"""
Baut die eingebackene Asteroiden-Ephemeride fuer den Womancode-Reader.

Zieht fuer 15 Womancode-Asteroiden die geozentrische ekliptikale Laenge "of date"
(QUANTITIES=31, ObsEcLon) von der JPL Horizons API, ueber einen festen Zeitraum
mit festem Schritt. Codiert jede Laenge als 3-stelligen Base36-Wert (Zentigrad)
und schreibt eine kompakte JS-Datei womancode-asteroids-data.js.

Zur Laufzeit interpoliert der Reader linear zwischen den Stuetzstellen und nutzt
origin.julianDate der Engine, damit die Asteroiden auf exakt denselben Moment
fallen wie die Planeten.
"""
import json, re, sys, time, urllib.parse, urllib.request

# name -> JPL Kleinplaneten-Nummer (gleiche Nummern wie astro.com / Womancode-Guide)
ASTEROIDS = [
    ("Ceres", 1), ("Juno", 3), ("Psyche", 16), ("Fortuna", 19),
    ("Hera", 103), ("Medusa", 149), ("Abundantia", 151), ("Eva", 164),
    ("Eros", 433), ("Bella", 695), ("Nymphe", 875), ("Sirene", 1009),
    ("Aphrodite", 1388), ("Midas", 1981), ("Glo", 3267),
]

START = "1950-01-01"      # Abdeckung Geburtsjahrgaenge
STOP  = "2015-01-01"
STEP  = "4d"              # 4-Tage-Schritt: Interpolationsfehler < 0.1 Grad
HOST  = "https://ssd.jpl.nasa.gov/api/horizons.api"

def jd_ut(y, m, d):
    """Standard Julian Date fuer Kalenderdatum 00:00 UT (Gregorianisch)."""
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    jdn = d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045
    return jdn - 0.5  # 00:00 UT

def fetch(num):
    params = {
        "format": "text",
        "COMMAND": f"'{num};'",
        "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'OBSERVER'",
        "CENTER": "'500@399'",      # geozentrisch
        "START_TIME": f"'{START}'",
        "STOP_TIME": f"'{STOP}'",
        "STEP_SIZE": f"'{STEP}'",
        "QUANTITIES": "'31'",       # Observer ecliptic lon & lat, of date
    }
    url = HOST + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            sys.stderr.write(f"  retry {attempt+1} ({e})\n")
            time.sleep(5)
    raise RuntimeError(f"Horizons fetch failed for {num}")

def parse_lons(txt):
    block = re.search(r"\$\$SOE(.*?)\$\$EOE", txt, re.S)
    if not block:
        raise RuntimeError("kein $$SOE/$$EOE Block")
    lons = []
    for line in block.group(1).strip().splitlines():
        # letzte zwei Floats der Zeile = ObsEcLon, ObsEcLat
        m = re.search(r"(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$", line)
        if not m:
            continue
        lon = float(m.group(1)) % 360.0
        lons.append(lon)
    return lons

def b36(v):
    v = int(round(v)) % 36000
    s = ""
    for _ in range(3):
        v, r = divmod(v, 36)
        s = "0123456789abcdefghijklmnopqrstuvwxyz"[r] + s
    return s

def main():
    out = {"jd0": jd_ut(1950, 1, 1), "step": 4, "bodies": {}}
    expected = None
    for name, num in ASTEROIDS:
        sys.stderr.write(f"Hole {name} (#{num}) ...\n")
        lons = parse_lons(fetch(num))
        if expected is None:
            expected = len(lons)
        sys.stderr.write(f"  {len(lons)} Punkte, erste={lons[0]:.3f} letzte={lons[-1]:.3f}\n")
        out["bodies"][name] = {"num": num, "vals": "".join(b36(x * 100) for x in lons), "n": len(lons)}
        time.sleep(1)
    # Konsistenz: alle gleich lang?
    lens = {n: b["n"] for n, b in out["bodies"].items()}
    if len(set(lens.values())) != 1:
        sys.stderr.write(f"WARNUNG: ungleiche Laengen: {lens}\n")
    js = "/* Womancode Asteroiden-Ephemeride. Quelle: JPL Horizons (ObsEcLon, of date, geozentrisch). */\n"
    js += "window.WC_AST = " + json.dumps(out, separators=(",", ":")) + ";\n"
    with open("womancode-asteroids-data.js", "w") as f:
        f.write(js)
    sys.stderr.write(f"\nFertig. {len(out['bodies'])} Asteroiden, {expected} Stuetzstellen, "
                     f"Dateigroesse ~{len(js)//1024} KB\n")

if __name__ == "__main__":
    main()
