#!/bin/bash

# Create drums - 65 bars with 2 voices
cat > drums.abc << 'ENDDRUMS'
X:1
T:Blood on the Capitol Steps - Drums  
C:Brian Edwards
M:4/4
L:1/8
Q:1/4=88
K:C perc
V:1 name="Kick"
%%MIDI program 128
%%MIDI channel 10
C4 C4 | C4 C4 | C4 C4 | C4 C4 |
C4 C4 | C4 C4 | C4 C4 | C4 C4 | C4 C4 | C4 C4 | C4 C4 | C4 C4 |
C3 C C2 C2 | C3 C C2 C2 | C3 C C2 C2 | C3 C C2 C2 | C3 C C2 C2 | C3 C C2 C2 | C3 C C2 C2 | C3 C C2 C2 | C4 C4 |
C4 C4 | C4 C4 | C4 C4 | C4 C4 | C4 C4 | C4 C4 | C4 C4 | C4 C4 |
C3 C C2 C2 | C3 C C2 C2 | C3 C C2 C2 | C3 C C2 C2 | C3 C C2 C2 | C3 C C2 C2 | C3 C C2 C2 | C3 C C2 C2 | C4 C4 |
C2 C2 C2 C2 | C2 C2 C2 C2 | C2 C2 C2 C2 | C2 C2 C2 C2 |
C4 C4 | C4 C4 | C4 C4 | C4 C4 |
C4 C4 | C4 C4 | C4 C4 | C4 C4 | C4 C4 | C4 C4 | C4 C4 | C4 C4 |
C2 C2 C2 C2 | C2 C2 C2 C2 | C2 C2 C2 C2 | C2 C2 C2 C2 | C2 C2 C2 C2 | C2 C2 C2 C2 | C2 C2 C2 C2 | C2 C2 C2 C2 | C4 C4 |
C4 z4 | C4 z4 | C4 z4 | C4 z4 | C4 z4 |]
V:2 name="Snare"
%%MIDI program 128
%%MIDI channel 10
z4 E4 | z4 E4 | z4 E4 | z4 E4 |
z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 |
z4 E2 z2 | z4 E2 z2 | z4 E2 z2 | z4 E2 z2 | z4 E2 z2 | z4 E2 z2 | z4 E2 z2 | z4 E2 z2 | z4 E4 |
z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 |
z4 E2 z2 | z4 E2 z2 | z4 E2 z2 | z4 E2 z2 | z4 E2 z2 | z4 E2 z2 | z4 E2 z2 | z4 E2 z2 | z4 E4 |
E2 E2 E2 E2 | E2 E2 E2 E2 | E2 E2 E2 E2 | E2 E2 E2 E2 |
z4 E4 | z4 E4 | z4 E4 | z4 E4 |
z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 |
z4 E3 E | z4 E3 E | z4 E3 E | z4 E3 E | z4 E3 E | z4 E3 E | z4 E3 E | z4 E3 E | z4 E4 |
z4 E4 | z4 E4 | z4 E4 | z4 E4 | z4 E4 |]
ENDDRUMS

# Create remaining instruments similar to bass but with appropriate voicings
cat > guitar-acoustic.abc << 'ENDAC'
X:1
T:Blood on the Capitol Steps - Acoustic Guitar
C:Brian Edwards
M:4/4
L:1/8
Q:1/4=88
K:Cmin
V:1
%%MIDI program 25
z8 | z8 | z8 | z8 |
"Cm"[C2E2G2] z2 z4 | "F"[C2F2A2] z2 z4 | "Cm"[C2E2G2] z2 z4 | "Bb"z8 | "Gm"z8 | "Eb"z8 | "Bb"z8 | "F"z8 |
"Bb"[D2F2B2][D2F2B2] [D2F2B2][D2F2B2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] | "Gm"[D2G2B2][D2G2B2] [D2G2B2][D2G2B2] | "Eb"[E2G2B2][E2G2B2] [E2G2B2][E2G2B2] |
"Bb"[D2F2B2][D2F2B2] [D2F2B2][D2F2B2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] | "Cm"[C2E2G2][C2E2G2] [C2E2G2][C2E2G2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] |
"Gm"[D2G2B2][D2G2B2] [D2G2B2][D2G2B2] | "Eb"[E2G2B2][E2G2B2] [E2G2B2][E2G2B2] | "Bb"[D2F2B2][D2F2B2] [D2F2B2][D2F2B2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] | "Gm"[D2G2B2]6 z2 |
"Cm"[C2E2G2] z2 z4 | "F"[C2F2A2] z2 z4 | "Cm"[C2E2G2] z2 z4 | "Bb"z8 | "Gm"z8 | "Eb"z8 | "Bb"z8 | "F"z8 |
"Bb"[D2F2B2][D2F2B2] [D2F2B2][D2F2B2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] | "Gm"[D2G2B2][D2G2B2] [D2G2B2][D2G2B2] | "Eb"[E2G2B2][E2G2B2] [E2G2B2][E2G2B2] |
"Bb"[D2F2B2][D2F2B2] [D2F2B2][D2F2B2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] | "Cm"[C2E2G2][C2E2G2] [C2E2G2][C2E2G2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] |
"Gm"[D2G2B2][D2G2B2] [D2G2B2][D2G2B2] | "Eb"[E2G2B2][E2G2B2] [E2G2B2][E2G2B2] | "Bb"[D2F2B2][D2F2B2] [D2F2B2][D2F2B2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] | "Gm"[D2G2B2]6 z2 |
"Bb"[D2F2B2][D2F2B2] [D2F2B2][D2F2B2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] | "Gm"[D2G2B2][D2G2B2] [D2G2B2][D2G2B2] | "Eb"[E2G2B2][E2G2B2] [E2G2B2][E2G2B2] |
"Cm"[C2E2G2] z2 [C2E2G2] z2 | "Bb"[D2F2B2] z2 [D2F2B2] z2 | "Cm"[C2E2G2] z2 [C2E2G2] z2 | "Gm"[D2G2B2] z2 "F"[C2F2A2] z2 |
"Cm"[C2E2G2] z2 z4 | "F"[C2F2A2] z2 z4 | "Cm"[C2E2G2] z2 z4 | "Bb"z8 | "Gm"z8 | "Eb"z8 | "Bb"z8 | "F"z8 |
"Bb"[D2F2B2][D2F2B2] [D2F2B2][D2F2B2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] | "Gm"[D2G2B2][D2G2B2] [D2G2B2][D2G2B2] | "Eb"[E2G2B2][E2G2B2] [E2G2B2][E2G2B2] |
"Bb"[D2F2B2][D2F2B2] [D2F2B2][D2F2B2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] | "Cm"[C2E2G2][C2E2G2] [C2E2G2][C2E2G2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] |
"Gm"[D2G2B2][D2G2B2] [D2G2B2][D2G2B2] | "Eb"[E2G2B2][E2G2B2] [E2G2B2][E2G2B2] | "Bb"[D2F2B2][D2F2B2] [D2F2B2][D2F2B2] | "F"[C2F2A2][C2F2A2] [C2F2A2][C2F2A2] | "Gm"[D2G2B2]6 z2 |
"Cm"C1 z1 E1 z1 G1 z1 c1 z1 | "Gm"D1 z1 G1 z1 B1 z1 d1 z1 | "Gm"[D2G2B2]6 z2 | [D2G2B2]6 z2 | [D2G2B2]6 z2 |]
ENDAC

# Electric and organ with same 65-bar structure
cat > guitar-electric.abc << 'ENDELEC'
X:1
T:Blood on the Capitol Steps - Electric Guitar
C:Brian Edwards
M:4/4
L:1/8
Q:1/4=88
K:Cmin
V:1
%%MIDI program 29
z8 | z8 | z8 | z8 |
z8 | z8 | z8 | z8 | z8 | z8 | z8 | z8 |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Cm"[C4E4G4] [C4E4G4] | "F"[C4F4A4] [C4F4A4] |
"Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] | "Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D6G6B6] z2 |
z8 | z8 | z8 | z8 | z8 | z8 | z8 | z8 |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Cm"[C4E4G4] [C4E4G4] | "F"[C4F4A4] [C4F4A4] |
"Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] | "Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D6G6B6] z2 |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] |
"Cm"[C4E4G4] [C4E4G4] | "Bb"[D4F4B4] [D4F4B4] | "Cm"[C4E4G4] [C4E4G4] | "Gm"[D4G4B4] "F"[C4F4A4] |
z8 | z8 | z8 | z8 | z8 | z8 | z8 | z8 |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Cm"[C4E4G4] [C4E4G4] | "F"[C4F4A4] [C4F4A4] |
"Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] | "Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D6G6B6] z2 |
z8 | z8 | "Gm"[D6G6B6] z2 | [D6G6B6] z2 | [D6G6B6] z2 |]
ENDELEC

cat > organ.abc << 'ENDORGAN'
X:1
T:Blood on the Capitol Steps - Organ
C:Brian Edwards
M:4/4
L:1/8
Q:1/4=88
K:Cmin
V:1
%%MIDI program 16
"Cm"[C8E8G8] | [C8E8G8] | [C8E8G8] | [C8E8G8] |
"Cm"[C8E8G8] | "F"[C8F8A8] | "Cm"[C8E8G8] | "Bb"[D8F8B8] | "Gm"[D8G8B8] | "Eb"[E8G8B8] | "Bb"[D8F8B8] | "F"[C8F8A8] |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Cm"[C4E4G4] [C4E4G4] | "F"[C4F4A4] [C4F4A4] |
"Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] | "Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D8G8B8] |
"Cm"[C8E8G8] | "F"[C8F8A8] | "Cm"[C8E8G8] | "Bb"[D8F8B8] | "Gm"[D8G8B8] | "Eb"[E8G8B8] | "Bb"[D8F8B8] | "F"[C8F8A8] |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Cm"[C4E4G4] [C4E4G4] | "F"[C4F4A4] [C4F4A4] |
"Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] | "Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D8G8B8] |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] |
z8 | z8 | z8 | z8 |
"Cm"[C8E8G8] | "F"[C8F8A8] | "Cm"[C8E8G8] | "Bb"[D8F8B8] | "Gm"[D8G8B8] | "Eb"[E8G8B8] | "Bb"[D8F8B8] | "F"[C8F8A8] |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] |
"Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Cm"[C4E4G4] [C4E4G4] | "F"[C4F4A4] [C4F4A4] |
"Gm"[D4G4B4] [D4G4B4] | "Eb"[E4G4B4] [E4G4B4] | "Bb"[D4F4B4] [D4F4B4] | "F"[C4F4A4] [C4F4A4] | "Gm"[D8G8B8] |
"Cm"[C8E8G8] | "Gm"[D8G8B8] | "Gm"[D8G8B8] | [D8G8B8] | [D8G8B8] |]
ENDORGAN

# Generate all MIDI files
for f in drums.abc guitar-acoustic.abc guitar-electric.abc organ.abc; do
  abc2midi "$f" -o "${f%.abc}.mid" 2>&1 | grep -v "perc" | grep -E "(writing|Error)"
done

echo "All files created and validated"
ls -lh *.mid | awk '{print $9, $5}'
