# Karen Jimena Hernández Ortega – 21199
# Diana Lucía Fernández Villatoro – 21747
# Daniel Esteban Morales Urízar – 21785
# --- Adventure — 98 BPM, 16 compases (~39 s) ---


from music import *
from random import *

# ---------- Fallbacks de programas GM  ----------
GM_PROG_FALLBACK = {
    "STRING_ENSEMBLE_1": 48,
    "HARP": 46,
    "PIANO": 0,
    "FLUTE": 73,
    "FRENCH_HORN": 60,
    "CHOIR_AAHS": 52,
    "VOICE_OOHS": 53
}
for name, val in GM_PROG_FALLBACK.items():
    if name not in globals():
        globals()[name] = val
        

CHOIR = VOICE_OOHS if 'VOICE_OOHS' in globals() else CHOIR_AAHS

# ---------- Parámetros ----------
tempoBPM = 98.0                 # tempo medio (90–120 según)
measures = 16                   # A (8) + A' (8)  → ~39 s a 98 BPM
score = Score("Adventure Loop", tempoBPM)

# Canales (0–15). Usa 0–8 para instrumentos melódicos; 9 (10 en 1-based) es drums.
ch_strings = 0
ch_arp     = 1
ch_melody  = 2
ch_horns   = 3
ch_choir   = 4

# Partes (programa GM, canal)
strings = Part("Strings", STRING_ENSEMBLE_1, ch_strings)
arp     = Part("Arp",     HARP,               ch_arp)
melody  = Part("Melody",  FLUTE,              ch_melody)
horns   = Part("Horns",   FRENCH_HORN,        ch_horns)
choir   = Part("Choir",   CHOIR,              ch_choir)


C3, D3, E3, F3, G3, A3, B3 = 48, 50, 52, 53, 55, 57, 59
C4, D4, E4, F4, G4, A4, B4 = 60, 62, 64, 65, 67, 69, 71
C5, D5, E5, F5, G5        = 72, 74, 76, 77, 79

PROG = [
    ("Cadd9", [C3, G3, C4, E4, D4]),   
    ("Am",    [A3, E4, A4, C4]),
    ("Fadd9", [F3, C4, F4, A4, G4]),   
    ("G",     [G3, D4, G4, B4]),
    ("Cadd9", [C3, G3, C4, E4, D4]),
    ("Fadd9", [F3, C4, F4, A4, G4]),
    ("Dm7",   [D3, A3, D4, F4, C4]),
    ("G",     [G3, D4, G4, B4]),
    ("Cadd9", [C3, G3, C4, E4, D4]),
    ("Am",    [A3, E4, A4, C4]),
    ("Fadd9", [F3, C4, F4, A4, G4]),
    ("G",     [G3, D4, G4, B4]),
    ("Cadd9", [C3, G3, C4, E4, D4]),
    ("Fadd9", [F3, C4, F4, A4, G4]),
    ("Dm7",   [D3, A3, D4, F4, C4]),
    ("Gsus4", [G3, D4, G4, C4])        
]


def add_strings_bar(chord_pitches, bar_idx, dyn=72):
    """Pad de cuerdas: acorde redonda (WN) en el compás bar_idx."""
    cp = CPhrase(bar_idx * WN)
    cp.addChord(chord_pitches, WN)
    for p in chord_pitches:
        pass  
    strings.addCPhrase(cp)

def add_arp_bar(chord_pitches, bar_idx, dyn=66, triplet=False):
    """Arpegio 1 compás (movimiento sutil con leve síncopa)."""
    ph = Phrase(bar_idx * WN)
    pat_idx = [0, 1, 2, 3, 0, 1, 4 if len(chord_pitches) > 4 else 2, 1]
    dur = EN if not triplet else (QN/3.0)  # (sensación 6/8)
    for i in range(8):
        idx = pat_idx[i] % len(chord_pitches)
        n = Note(chord_pitches[idx], dur)
        n.setDynamic(dyn)
        ph.addNote(n)
    
    ph.setDuration(WN)
    arp.addPhrase(ph)

def phrase_from_pairs(pairs, start_bar, dyn=84):
    """Crea una Phrase desde (pitch, dur), colocada desde start_bar."""
    ph = Phrase(start_bar * WN)
    for p, d in pairs:
        n = Note(p, d) if p != REST else Note(REST, d)
        n.setDynamic(dyn)
        ph.addNote(n)
    return ph

# ---------- Construcción ----------

# 1) STRINGS
for i, (_, chord) in enumerate(PROG):
    d = 70 if i < 8 else 78
    add_strings_bar(chord, i, dyn=d)

# 2) ARPEGIO
for i, (_, chord) in enumerate(PROG):
    d = 64 if i < 8 else 72
    add_arp_bar(chord, i, dyn=d, triplet=False)

# 3) MELODÍA 
melA = [
    (G4, QN), (C5, QN), (B4, EN), (A4, EN), (G4, HN),
    (E4, QN), (G4, EN), (A4, EN), (G4, QN+EN), (E4, EN),
    (F4, HN), (E4, QN), (D4, QN),
    (G4, HN), (REST, QN), (G4, QN)
]
melA_var = [
    (G4, QN), (C5, QN), (B4, EN), (A4, EN), (G4, HN),
    (E4, QN), (G4, EN), (A4, EN), (G4, QN+EN), (E4, EN),
    (F4, HN), (E4, QN), (D4, QN),
    (A4, QN), (G4, EN), (E4, EN), (D4, QN), (C4, QN)  
]
melA_ph  = phrase_from_pairs(melA,     start_bar=2, dyn=84)   # compases 3–6 aprox.
melA2_ph = phrase_from_pairs(melA_var, start_bar=10, dyn=90)  # compases 11–14
melody.addPhrase(melA_ph)
melody.addPhrase(melA2_ph)

# 4) HORNS 
for i in range(10, 14):  # compases 11–14
    root = PROG[i][1][0]
    ph = Phrase(i * WN)
    n = Note(root, WN); n.setDynamic(78)
    ph.addNote(n)
    horns.addPhrase(ph)

# 5) CHOIR (
for i in (8, 12, 15):  # compases 9, 13 y 16
    cp = CPhrase(i * WN)
    cp.addChord(PROG[i][1], WN)  # acorde entero
    choir.addCPhrase(cp)


score.addPart(strings)
score.addPart(arp)
score.addPart(melody)
score.addPart(horns)
score.addPart(choir)

# Reproducción
Play.midi(score)
Write.midi(score, "adventure_loop_major.mid")
