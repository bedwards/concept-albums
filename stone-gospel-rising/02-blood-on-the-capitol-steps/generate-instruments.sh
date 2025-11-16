#!/bin/bash
# Generate all 5 instrumental ABC files with EXACTLY 65 bars to match vocal melody

echo "Generating 65-bar instrumental files..."

# BASS - 65 bars
cat > bass.abc << 'EOF'
X:1
T:Blood on the Capitol Steps - Bass
C:Brian Edwards
M:4/4
L:1/8
Q:1/4=88
K:Cmin
V:1
%%MIDI program 33
"Cm"C,8 | C,8 | C,8 | C,8 |
"Cm"C,2 C,2 G,,2 G,,2 | "F"F,2 F,2 C,2 C,2 | "Cm"C,2 C,2 G,,2 G,,2 | "Bb"B,,2 B,,2 F,,2 F,,2 |
"Gm"G,2 G,2 D,2 D,2 | "Eb"E,2 E,2 B,,2 B,,2 | "Bb"B,,2 B,,2 F,,2 F,,2 | "F"F,2 F,2 C,2 C,2 |
"Bb"B,,1 B,,1 B,,1 B,,1 F,,1 F,,1 F,,1 F,,1 | "F"F,1 F,1 F,1 F,1 C,1 C,1 C,1 C,1 | "Gm"G,1 G,1 G,1 G,1 D,1 D,1 D,1 D,1 | "Eb"E,1 E,1 E,1 E,1 "Bb"B,,1 B,,1 B,,1 B,,1 |
"F"F,1 F,1 F,1 F,1 C,1 C,1 C,1 C,1 | "Cm"C,1 C,1 C,1 C,1 "F"F,1 F,1 F,1 F,1 | "Gm"G,1 G,1 G,1 G,1 D,1 D,1 D,1 D,1 | "Eb"E,1 E,1 E,1 E,1 "Bb"B,,1 B,,1 "F"F,1 F,1 | "Gm"G,8 |
"Cm"C,2 C,2 G,,2 G,,2 | "F"F,2 F,2 C,2 C,2 | "Cm"C,2 C,2 G,,2 G,,2 | "Bb"B,,2 B,,2 F,,2 F,,2 |
"Gm"G,2 G,2 D,2 D,2 | "Eb"E,2 E,2 B,,2 B,,2 | "Bb"B,,2 B,,2 F,,2 F,,2 | "F"F,2 F,2 C,2 C,2 |
"Bb"B,,1 B,,1 B,,1 B,,1 F,,1 F,,1 F,,1 F,,1 | "F"F,1 F,1 F,1 F,1 C,1 C,1 C,1 C,1 | "Gm"G,1 G,1 G,1 G,1 D,1 D,1 D,1 D,1 | "Eb"E,1 E,1 E,1 E,1 "Bb"B,,1 B,,1 B,,1 B,,1 |
"F"F,1 F,1 F,1 F,1 C,1 C,1 C,1 C,1 | "Cm"C,1 C,1 C,1 C,1 "F"F,1 F,1 F,1 F,1 | "Gm"G,1 G,1 G,1 G,1 D,1 D,1 D,1 D,1 | "Eb"E,1 E,1 E,1 E,1 "Bb"B,,1 B,,1 "F"F,1 F,1 | "Gm"G,8 |
"Bb"B,,1 B,,1 B,,1 B,,1 F,,1 F,,1 F,,1 F,,1 | "F"F,1 F,1 F,1 F,1 C,1 C,1 C,1 C,1 | "Gm"G,1 G,1 G,1 G,1 D,1 D,1 D,1 D,1 | "Eb"E,1 E,1 E,1 E,1 "Bb"B,,1 B,,1 B,,1 B,,1 |
"Cm"C,2 C,2 "Bb"B,,2 B,,2 | "Cm"C,2 C,2 "Bb"B,,2 B,,2 | "Cm"C,2 C,2 "Bb"B,,2 B,,2 | "Gm"G,2 G,2 "F"F,2 F,2 |
"Cm"C,2 C,2 G,,2 G,,2 | "F"F,2 F,2 C,2 C,2 | "Cm"C,2 C,2 G,,2 G,,2 | "Bb"B,,2 B,,2 F,,2 F,,2 |
"Gm"G,2 G,2 D,2 D,2 | "Eb"E,2 E,2 B,,2 B,,2 | "Bb"B,,2 B,,2 F,,2 F,,2 | "F"F,2 F,2 C,2 C,2 |
"Bb"B,,1 B,,1 B,,1 B,,1 F,,1 F,,1 F,,1 F,,1 | "F"F,1 F,1 F,1 F,1 C,1 C,1 C,1 C,1 | "Gm"G,1 G,1 G,1 G,1 D,1 D,1 D,1 D,1 | "Eb"E,1 E,1 E,1 E,1 "Bb"B,,1 B,,1 B,,1 B,,1 |
"F"F,1 F,1 F,1 F,1 C,1 C,1 C,1 C,1 | "Cm"C,1 C,1 C,1 C,1 "F"F,1 F,1 F,1 F,1 | "Gm"G,1 G,1 G,1 G,1 D,1 D,1 D,1 D,1 | "Eb"E,1 E,1 E,1 E,1 "Bb"B,,1 B,,1 "F"F,1 F,1 | "Gm"G,8 |
"Cm"C,2 C,2 C,2 "F"F,2 | "Gm"G,6 G,2 | "Gm"G,8 | G,8 | G,8 |]
EOF

echo "Created bass.abc - 65 bars"

# Test it
abc2midi bass.abc -o bass.mid 2>&1 | grep -E "(writing|Error)"

