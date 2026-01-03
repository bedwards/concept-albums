# Stone Rolled Away

**Track 8** from *Stone Gospel Rising*

## The Song

A resurrection anthem that marries Americana instrumentation with gospel urgency. The stone that sealed the tomb becomes a symbol of unstoppable momentum - what empire buries, God raises.

- **Key**: G minor (resolves to G major on final chord)
- **Tempo**: 95 BPM
- **Time**: 4/4
- **Structure**: Intro → Verse → Verse → Build → Chorus → Chorus → Outro

## How It Was Made

This song was composed using a YAML-based workflow where all musical content lives in a single source file (`song.yaml`). ABC notation defines each instrument's part, section by section.

### The Process

1. **Write lyrics and chords** in the YAML file
2. **Compose ABC notation** for each instrument in each section
3. **Run the generator script** to produce MIDI files
4. **Load into DAW** for production

### Instrumentation

| Track | Role | Character |
|-------|------|-----------|
| vocal-melody | Lead line | Proclaimed, almost shouted in chorus |
| bass | Foundation | Root-fifth walk, aggressive eighth notes in chorus |
| guitar-acoustic | Rhythm | Fingerpicking in verse, full strums in chorus |
| guitar-electric | Power | Silent until chorus, then open power chords |
| organ | Atmosphere | Pump organ pads, hopeful not dark |
| banjo | Drive | Clawhammer pattern, celebratory rolls |
| drum-kick | Pulse | Quarter notes building to driving chorus |
| drum-snare | Backbeat | 2 & 4, fills on key lyrical moments |

### The ABC Notation

Each section contains inline ABC for every instrument:

```yaml
chorus:
  bars: 8
  instruments:
    bass:
      abc: |
        "Bb"B,,1 B,,1 B,,1 B,,1 F,,1 F,,1 F,,1 F,,1 |
        "C"F,1 F,1 F,1 F,1 C,1 C,1 C,1 C,1 |
        ...
```

The chord symbols (`"Bb"`, `"C"`) are annotations - the actual notes follow ABC standard notation where `,` drops an octave and `1` is a sixteenth note in this context.

### Arrangement Philosophy

From the `arrangement` section of song.yaml:

**Intro**: Building intensity, hopeful not dark. Kick quarters on 1 & 3, pump organ Gm pad sustained.

**Verse**: Forward momentum. Bass root-fifth walk, banjo clawhammer driving, electric silent.

**Chorus**: Full band, triumphant but not polished. Kick driving quarters with doubles on "rolled away". Vocal proclaimed.

**Build**: Rising intensity toward triumph. Every instrument louder, drums relentless.

**Outro**: "Stone keeps rolling" - all instruments drop to half, banjo prominent. Final line returns loud. End on Gm MAJOR (resolve minor to major). All instruments hit together, let ring 4 bars. Natural decay, no fade. Ends on hope, not darkness.

## Files

```
08-stone-rolled-away/
├── song.yaml           # Single source of truth (ABC, lyrics, arrangement)
├── lyrics.txt          # Extracted lyrics
├── chords.txt          # Chord chart
├── arrangement.txt     # Production notes
├── midi/               # Generated MIDI files
│   ├── vocal-melody.mid
│   ├── bass.mid
│   ├── guitar-acoustic.mid
│   ├── guitar-electric.mid
│   ├── organ.mid
│   ├── banjo.mid
│   ├── drum-kick.mid
│   └── drum-snare.mid
└── .generated/         # Other generated artifacts
```

## Regenerating

```bash
python scripts/generate_song.py stone-gospel-rising/08-stone-rolled-away/
```

This reads `song.yaml` and produces fresh MIDI files from the ABC notation.

## Musical Decisions

**Why G minor?** Traditional resurrection hymns often use major keys. G minor creates tension - the weight of the sealed tomb, the fear of the guards. The resolution to G major on the final chord is the surprise: death transformed.

**Why banjo?** Americana gospel. The rolling banjo pattern evokes both Appalachian tradition and the literal rolling of the stone.

**Why "pump organ"?** Not a Hammond B3 - a reed organ. Older, wheezier, more human. The sound of country churches where this theology lives.

**Why 95 BPM?** Slow enough to feel weighty, fast enough to feel inevitable. The stone is heavy but it's moving.

---

*"The stone the builders rejected has become the cornerstone."* — Psalm 118:22
