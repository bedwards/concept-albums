# Midwest Meridian - Bitwig Production Plan

## Rick Rubin Production Philosophy
- Strip it down to the essence
- Let the song breathe
- The room is an instrument
- Dynamics over loudness
- Honesty over polish

## Tempo & Key
- **Tempo**: 95 BPM
- **Key**: G Major
- **Time**: 4/4

---

## Quick Start

### Automated Setup (via OSC)
```bash
# Ensure Bitwig is running with 8 empty instrument tracks
cd ~/find-all-bitwig
python scripts/midwest_meridian_production.py
```

This script will:
- Set up all 8 tracks with instruments and effects
- Set volumes and pans
- Configure master track

### What You Need to Do Manually

After running the script, complete these steps:

---

## MANUAL STEP 1: Create Group Tracks

**OSC cannot set group track volumes. You must do this manually.**

### Instruments Bus (Tracks 1-4)
1. Select Tracks 1-4 (Acoustic Guitar, Pedal Steel, Fiddle, Electric Guitar)
2. Right-click → "Group Selected Tracks"
3. Rename to "Instruments Bus"
4. Set Volume: **-3dB**
5. Add FX: Compressor (Soft Compression preset) - gentle glue

### Rhythm Bus (Tracks 5-7)
1. Select Tracks 5-7 (Upright Bass, Kick, Snare)
2. Right-click → "Group Selected Tracks"
3. Rename to "Rhythm Bus"
4. Set Volume: **-4dB**
5. Add FX: Compressor + EQ-5

---

## MANUAL STEP 2: Import MIDI Files

From `~/concept-albums/midwest-meridian/01-midwest-meridian/midi/`:

| File | Track |
|------|-------|
| acoustic-guitar.mid | Track 1 |
| pedal-steel.mid | Track 2 |
| fiddle.mid | Track 3 |
| electric-guitar.mid | Track 4 |
| upright-bass.mid | Track 5 |
| drum-kick.mid | Track 6 |
| drum-snare.mid | Track 7 |
| vocal.mid | Track 8 |

---

## Track Layout

| # | Track Name | Instrument Preset | Effects Chain | Pan | Volume |
|---|------------|-------------------|---------------|-----|--------|
| 1 | Acoustic Guitar | Poly Grid - Old Nylon | Room One | 15% L | -6dB |
| 2 | Pedal Steel | Phase-4 - Ambient Strings | Mono K-Chorus → Room Two → Low Cut EQ | 25% R | -10dB |
| 3 | Fiddle | FM-4 - FM Violin | Room One | 20% L | -10dB |
| 4 | Electric Guitar | Poly Grid - Jazz Guitar | Clean Guitar Amp → Room Two | 20% R | -8dB |
| 5 | Upright Bass | Poly Grid - Acoustic Bass | Soft Compression | Center | -6dB |
| 6 | Kick | E-Kick - BOB Kick | (none) | Center | -8dB |
| 7 | Snare | E-Snare - Dark Snare | Room One | Center | -10dB |
| 8 | Vocal | (Audio track) | Low Cut EQ → Soft Compression → Room One | Center | -3dB |

---

## Detailed Track Specifications

### Track 1: Acoustic Guitar
- **Device**: Poly Grid
- **Preset**: Old Nylon
- **FX Chain**: Reverb (Room One)
- **Notes**: Fingerpicking in intro/bridge, light strumming in verses

### Track 2: Pedal Steel
- **Device**: Phase-4
- **Preset**: Ambient Strings
- **FX Chain**: Mono K-Chorus → Room Two → Low Cut EQ
- **Notes**: Enters bar 5 of intro. Volume swells, no attack. This IS the longing.

### Track 3: Fiddle
- **Device**: FM-4
- **Preset**: FM Violin
- **FX Chain**: Reverb (Room One)
- **Notes**: Enters at first chorus with counter-melody. Don't compete with vocal.

### Track 4: Electric Guitar
- **Device**: Poly Grid
- **Preset**: Jazz Guitar
- **FX Chain**: Clean Guitar Amp → Room Two
- **Notes**: Clean arpeggios in chorus. No distortion, no pedals. Pure.

### Track 5: Upright Bass
- **Device**: Poly Grid
- **Preset**: Acoustic Bass
- **FX Chain**: Soft Compression
- **Notes**: Root notes, half notes. The heartbeat. Don't rush.

### Track 6: Kick
- **Device**: E-Kick
- **Preset**: BOB Kick
- **FX Chain**: None
- **Notes**: Beats 1 and 3. Soft, jazz feel. Almost felt more than heard.

### Track 7: Snare
- **Device**: E-Snare
- **Preset**: Dark Snare
- **FX Chain**: Reverb (Room One)
- **Notes**: Brushes on 2 and 4. Whisper, don't hit. Silent during bridge.

### Track 8: Vocal
- **Type**: Audio track (placeholder for recording)
- **FX Chain**: Low Cut EQ → Soft Compression → Room One
- **Notes**: Conversational delivery. Don't oversing. Let the words carry.

---

## Bus Structure

### Instruments Bus (Tracks 1-4)
- **Tracks**: Acoustic Guitar, Pedal Steel, Fiddle, Electric Guitar
- **FX**: Soft Compression (gentle glue)
- **Volume**: -3dB

### Rhythm Bus (Tracks 5-7)
- **Tracks**: Upright Bass, Kick, Snare
- **FX**: Compressor + EQ-5
- **Volume**: -4dB

---

## Master Track
- **EQ-5**: Gentle high-shelf air at 10kHz
- **Peak Limiter**: -1dB ceiling, gentle ratio
- **Philosophy**: Warm, not loud. Preserve dynamics.

---

## Mix Reference

### Volumes (dB to Linear)
| Track | dB | Linear | OSC (0-128) |
|-------|-----|--------|-------------|
| Acoustic Guitar | -6 | 0.50 | 64 |
| Pedal Steel | -10 | 0.32 | 41 |
| Fiddle | -10 | 0.32 | 41 |
| Electric Guitar | -8 | 0.40 | 51 |
| Upright Bass | -6 | 0.50 | 64 |
| Kick | -8 | 0.40 | 51 |
| Snare | -10 | 0.32 | 41 |
| Vocal | -3 | 0.71 | 91 |

### Panning
| Track | Pan Value | Direction |
|-------|-----------|-----------|
| Acoustic Guitar | -0.15 | 15% Left |
| Pedal Steel | 0.25 | 25% Right |
| Fiddle | -0.20 | 20% Left |
| Electric Guitar | 0.20 | 20% Right |
| Upright Bass | 0.00 | Center |
| Kick | 0.00 | Center |
| Snare | 0.00 | Center |
| Vocal | 0.00 | Center |

---

## OSC Limitations
- Group track volumes cannot be set via OSC (manual adjustment required)
- Note devices add at end of chain (must be moved manually if needed)
- Touch events required for reliable parameter changes

---

## Kontakt 8 / M-Tron Pro IV Alternatives

Optional replacements for Bitwig built-in instruments. Load via Kontakt 8.

### Track 1: Acoustic Guitar
**Kontakt 8** (Session Guitarist):
```
/Users/Shared/Session Guitarist - Picked Acoustic Library/Instruments/Picked Acoustic.nki ★
/Users/Shared/Session Guitarist - Picked Acoustic Library/Instruments/Picked Acoustic (Melody).nki
/Users/Shared/Session Guitarist - Strummed Acoustic Library/Instruments/Strummed Acoustic.nki
```

**M-Tron Pro IV**: Nylon Guitar - Basic, Nylon Guitar - Wide

### Track 2: Pedal Steel
**M-Tron Pro IV**: ARP Country Guitar Basic ★, ARP Country Guitar Full, Basic Nashville Country

### Track 3: Fiddle
**M-Tron Pro IV**: Electric Violin - Basic ★, Electric Violin - Wide, M300B Lower Violin - Basic

### Track 4: Electric Guitar
**M-Tron Pro IV**: Adrian's Guitar - Basic ★, Adrian's Guitar - Wide, 24 String Guitar

### Track 5: Upright Bass
**Kontakt 8** (Spitfire Alternative Solo Strings):
```
/Volumes/External/kontakt_libraries/Spitfire/Spitfire Alternative Solo Strings library/Instruments/Bass.nki ★
/Volumes/External/kontakt_libraries/Spitfire/Spitfire Alternative Solo Strings library/Instruments/_Advanced_/Individual articulations/Bass/Bass - Long.nki
/Volumes/External/kontakt_libraries/Spitfire/Spitfire Alternative Solo Strings library/Instruments/_Advanced_/Individual articulations/Bass/Bass - Short Pizzicato.nki
```

**M-Tron Pro IV**: 70s Synth Bass

### Track 6: Kick
**Kontakt 8** (Spitfire Percussion):
```
/Volumes/External/kontakt_libraries/Spitfire/Spitfire Percussion Library/Instruments/_Individual Instruments_/Drums - Low/Bass Drum.nki ★
```

**M-Tron Pro IV**: Drum Synths - Basic

### Track 7: Snare (Brush)
**Kontakt 8** (Spitfire The Grange - Andy Kit Brushes):
```
/Volumes/External/kontakt_libraries/Spitfire/Spitfire The Grange library/Instruments/Instruments Mixes/Mapped kits/c - Andy kit (Brushes).nki ★
/Volumes/External/kontakt_libraries/Spitfire/Spitfire The Grange library/Instruments/Instruments Mixes/Loops/c - Andy/c - Andy - Brush.nki
```

### Track 8: Vocal (Synth Placeholder)
**M-Tron Pro IV**: DS Male Voice Dreamy Choir, 15 Choir Basic

---

## Remember

*"When in doubt, take it out."*

*"The song is the boss. Everything serves the song."*

*"If it doesn't make you feel something, it's not finished."*

— Rick Rubin
