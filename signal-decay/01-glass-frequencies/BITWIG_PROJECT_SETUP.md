# Glass Frequencies - Bitwig Project Setup

## Professional Production Template

**Tempo:** 108 BPM
**Key:** D minor
**Genre:** Synthwave / Post-Punk

---

## Track Layout (8 Tracks)

| # | Track Name | Device | Preset (Verified) | MIDI File |
|---|------------|--------|-------------------|-----------|
| 1 | 01-Vocal | Polymer | **Glam Pad** | vocal-melody.mid |
| 2 | 02-Synth-Pad | Phase-4 | **DX-80s** ✓ | synth-pad.mid |
| 3 | 03-Synth-Arp | Polymer | **Lead The Way** ✓ | synth-arp.mid |
| 4 | 04-Guitar | Phase-4 | **Dirty Guitar** | guitar-electric.mid |
| 5 | 05-Bass | Polymer | **Bite Back Bass** | bass.mid |
| 6 | 06-Kick | E-Kick | **Sub Kick** | drum-kick.mid |
| 7 | 07-Snare | E-Snare | **Dark Snare** ✓ | drum-snare.mid |
| 8 | 08-HiHat | E-Hat | **Crushed Hat 1** | drum-hihat.mid |

> ✓ = Exact match from original plan. All presets verified in Bitwig database.
> Track 4 updated: Changed from Amp "Clean Guitar" to Phase-4 "Dirty Guitar" for better post-punk FM character.

---

## Detailed Track Configuration

### Track 1: Vocal Melody
**Device Chain:**
1. Polymer (Instrument)
   - Preset: **Glam Pad** ✓

2. EQ-5 (Post-EQ)
   - Preset: **Low Cut EQ** ✓
   - Cuts below 200Hz for clarity

3. Reverb
   - Preset: **Dark Spring** ✓
   - Mix: 25-35%

4. Delay-2
   - Preset: **Stereo Dub 2** ✓
   - 1/8 note stereo ping-pong feel

---

### Track 2: Synth Pad (Cold, Distant)
**Device Chain:**
1. Phase-4 (Instrument)
   - Preset: **DX-80s** ✓ (perfect for synthwave)

2. Chorus
   - Preset: **Phasey Chorus** ✓
   - Creates slight detuning for that cold 80s feel

3. Reverb
   - Preset: **Space Hall** ✓
   - Large hall, long decay, spacious

4. EQ-5
   - Preset: **Brighter EQ** ✓
   - Boost 8-10kHz for shimmer

---

### Track 3: Synth Arp (Crystalline, 16th notes)
**Device Chain:**
1. Polymer (Instrument)
   - Preset: **Lead The Way** ✓
   - Sawtooth-based, bright but not harsh

2. Delay-4
   - Preset: **One 8th Long Delay** ✓
   - Creates rhythmic interest

3. Reverb (Convolution)
   - Preset: **UK780 - Plate 1 (1.3s)** ✓
   - Short plate for clarity

4. Compressor
   - Preset: **Soft Compression** ✓
   - Light compression to even out levels

---

### Track 4: Electric Guitar (Angular, Post-Punk)
**Device Chain:**
1. Phase-4 (Instrument)
   - Preset: **Dirty Guitar** ✓
   - FM synthesis for authentic 80s character

2. Chorus
   - Preset: **Phasey Chorus** ✓
   - Classic post-punk shimmer

3. Delay-2
   - Preset: **Stereo Dub 2** ✓
   - Creates angular post-punk rhythm

4. Reverb
   - Preset: **TreeVerb** ✓
   - Small room ambience

5. EQ-5
   - Preset: **Mid Cut EQ** ✓
   - Cut at 3kHz to avoid harshness

---

### Track 5: Synth Bass
**Device Chain:**
1. Polymer (Instrument)
   - Preset: **Bite Back Bass** ✓
   - Sub-heavy with slight growl

2. EQ-5
   - Preset: **Low Cut EQ** ✓
   - High-pass to remove sub-rumble

3. Compressor
   - Preset: **Bass Compressor** ✓
   - Heavy compression for consistent level

4. Saturator
   - Preset: **Light Saturation** ✓
   - Subtle harmonics

---

### Track 6: Kick (808-style electronic)
**Device Chain:**
1. E-Kick (Instrument)
   - Preset: **Sub Kick** ✓
   - Tune to D1 (root note of the song)

2. EQ-5
   - Preset: **Brighter EQ** ✓
   - Adds click at 3kHz for punch

3. Transient Control
   - Default settings (adjust attack for punch)

---

### Track 7: Snare
**Device Chain:**
1. E-Snare (Instrument)
   - Preset: **Dark Snare** ✓

2. EQ-5
   - Preset: **Brighter EQ** ✓
   - Boosts crack at 5kHz

3. Reverb (FX Chain)
   - Preset: **Gated Reverb** ✓
   - Classic 80s gated reverb sound!

---

### Track 8: Hi-Hat
**Device Chain:**
1. E-Hat (Instrument)
   - Preset: **Crushed Hat 1** ✓
   - Tight and electronic

2. EQ-5
   - Preset: **Hi Only** ✓
   - High-pass + boost 8-10kHz for sizzle

3. Transient Control
   - Default settings (reduce sustain for tighter feel)

---

## Bus Routing (Group Tracks)

### Drums Bus
- Group tracks 6-8
- Add: Glue Compressor (2-3dB gain reduction)
- Add: Saturator (subtle warmth)
- Add: EQ for overall drum tone

### Synths Bus
- Group tracks 2, 3, 5
- Add: Stereo widener (subtle)
- Add: Gentle compression

### Master Bus
- Limiter (ceiling at -1dB)
- EQ-5 (gentle high shelf boost at 10kHz)
- Optional: Tape saturation for warmth

---

## MIDI Import Instructions

### Automated Import (Clip Launcher)
```bash
# Insert MIDI files into clip launcher slots
bwctl clip insert "/path/to/midi/vocal-melody.mid" -t 1 -s 1
bwctl clip insert "/path/to/midi/synth-pad.mid" -t 2 -s 1
bwctl clip insert "/path/to/midi/synth-arp.mid" -t 3 -s 1
bwctl clip insert "/path/to/midi/guitar-electric.mid" -t 4 -s 1
bwctl clip insert "/path/to/midi/bass.mid" -t 5 -s 1
bwctl clip insert "/path/to/midi/drum-kick.mid" -t 6 -s 1
bwctl clip insert "/path/to/midi/drum-snare.mid" -t 7 -s 1
bwctl clip insert "/path/to/midi/drum-hihat.mid" -t 8 -s 1
```

### Manual Arranger Placement
1. MIDI clips are loaded in clip launcher (slot 1 of each track)
2. Select all clips in clip launcher
3. Right-click → "Copy to Arranger" or drag clips to arranger at position 0:00

### Track Mapping
| Track | MIDI File | Clip Launcher |
|-------|-----------|---------------|
| 1 | vocal-melody.mid | Slot 1 ✓ |
| 2 | synth-pad.mid | Slot 1 ✓ |
| 3 | synth-arp.mid | Slot 1 ✓ |
| 4 | guitar-electric.mid | Slot 1 ✓ |
| 5 | bass.mid | Slot 1 ✓ |
| 6 | drum-kick.mid | Slot 1 ✓ |
| 7 | drum-snare.mid | Slot 1 ✓ |
| 8 | drum-hihat.mid | Slot 1 ✓ |

**Note Mapping for Drums:**
- All drum MIDI files use C3 (MIDI note 60)
- E-Kick, E-Snare, E-Hat will trigger on any note

---

## Mix Notes

**Levels (starting points):**
- Kick: -6dB (anchor)
- Snare: -8dB
- HiHat: -12dB
- Bass: -8dB
- Synth Pad: -14dB (sits back)
- Synth Arp: -10dB
- Guitar: -12dB
- Vocal: -6dB (focus)

**Panning:**
- Kick, Snare, Bass, Vocal: Center
- HiHat: 20% Right
- Synth Pad: Wide (stereo)
- Synth Arp: 30% Left
- Guitar: 25% Right

**Automation ideas:**
- Synth pad: Automate filter cutoff in bridge
- Arp: Volume swells into choruses
- Reverb: Increase on vocal in chorus

---

## CLI Commands Used

```bash
# Create tracks
bwctl track add -t instrument -n "01-Vocal"
bwctl track add -t instrument -n "02-Synth-Pad"
bwctl track add -t instrument -n "03-Synth-Arp"
bwctl track add -t instrument -n "04-Guitar"
bwctl track add -t instrument -n "05-Bass"
bwctl track add -t instrument -n "06-Kick"
bwctl track add -t instrument -n "07-Snare"
bwctl track add -t instrument -n "08-HiHat"

# Load presets (includes device - no separate device add needed!)
bwctl device load "Glam Pad" -d Polymer -t 1
bwctl device load "DX-80s" -d Phase-4 -t 2
bwctl device load "Lead The Way" -d Polymer -t 3
bwctl device load "Dirty Guitar" -d Phase-4 -t 4
bwctl device load "Bite Back Bass" -d Polymer -t 5
bwctl device load "Sub Kick" -d E-Kick -t 6
bwctl device load "Dark Snare" -d E-Snare -t 7
bwctl device load "Crushed Hat 1" -d E-Hat -t 8

# Add FX chains with presets
# Track 1: Vocal FX
bwctl device load "Low Cut EQ" -d EQ-5 -t 1
bwctl device load "Dark Spring" -d Reverb -t 1
bwctl device load "Stereo Dub 2" -d Delay-2 -t 1

# Track 2: Synth Pad FX
bwctl device load "Phasey Chorus" -d Chorus -t 2
bwctl device load "Space Hall" -d Reverb -t 2
bwctl device load "Brighter EQ" -d EQ-5 -t 2

# Track 3: Synth Arp FX
bwctl device load "One 8th Long Delay" -d Delay-4 -t 3
bwctl device load "UK780 - Plate 1 (1.3s)" -d Convolution -t 3
bwctl device load "Soft Compression" -d Compressor -t 3

# Track 4: Guitar FX
bwctl device load "Phasey Chorus" -d Chorus -t 4
bwctl device load "Stereo Dub 2" -d Delay-2 -t 4
bwctl device load "TreeVerb" -d Reverb -t 4
bwctl device load "Mid Cut EQ" -d EQ-5 -t 4

# Track 5: Bass FX
bwctl device load "Low Cut EQ" -d EQ-5 -t 5
bwctl device load "Bass Compressor" -d Compressor -t 5
bwctl device load "Light Saturation" -d Saturator -t 5

# Track 6: Kick FX
bwctl device load "Brighter EQ" -d EQ-5 -t 6
bwctl device add "Transient Control" -t 6

# Track 7: Snare FX
bwctl device load "Brighter EQ" -d EQ-5 -t 7
bwctl device load "Gated Reverb" -t 7

# Track 8: HiHat FX
bwctl device load "Hi Only" -d EQ-5 -t 8
bwctl device add "Transient Control" -t 8

# Set mix levels
bwctl track volume 1 0.71  # Vocal: -6dB
bwctl track volume 2 0.40  # Synth Pad: -14dB (sits back)
bwctl track volume 3 0.50  # Synth Arp: -10dB
bwctl track volume 4 0.44  # Guitar: -12dB
bwctl track volume 5 0.56  # Bass: -8dB
bwctl track volume 6 0.63  # Kick: -6dB (anchor)
bwctl track volume 7 0.56  # Snare: -8dB
bwctl track volume 8 0.35  # HiHat: -12dB

# Transport
bwctl play
bwctl stop
```

---

## Reference Tracks
- The Cure - "A Forest" (angular guitar, cold pads)
- Depeche Mode - "Enjoy the Silence" (synth pad texture)
- Joy Division - "Love Will Tear Us Apart" (post-punk energy)
- Kavinsky - "Nightcall" (synthwave bass)
- John Carpenter - "Assault on Precinct 13" (arp patterns)
