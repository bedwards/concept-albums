# Cadaver Lab

Track 1 of 12. The thesis statement. Six minutes. E minor. 78 BPM.

The song opens with strings alone—violin, viola, cello—establishing weight before a single word arrives. No drums. No guitar. Just long tones breathing together through Em to C to Em to D. Like an orchestra tuning to a feeling instead of a note.

---

## How This Was Built

Everything you hear came from one file: `song.yaml`. That's the single source of truth—476 lines of YAML containing the complete song definition. Lyrics, chord changes, arrangement notes, and ABC notation for every instrument in every section.

The human wrote the concept and the words. The agent built the technical infrastructure that turns ideas into playable files.

### The Process

I described what I wanted: a slow song about knowing someone so deeply you'd recognize their skeleton. Strings-first intro. Verses that build. Drums entering gradually. A bridge that swells. An outro that fades instrument by instrument until only a final chord rings.

Claude Code took that description and generated the initial `song.yaml` structure—section definitions, bar counts, instrument placeholders. Then I wrote the lyrics into the YAML, line by line, attaching chord symbols to each phrase. The agent wrote the ABC notation for each instrument part, matching the harmonic rhythm I'd specified.

When the notation was complete, I ran:

```bash
python scripts/generate_song.py cadaver-lab/01-cadaver-lab/
```

The script produced:
- 10 MIDI files (one per instrument track)
- ABC notation files for each part
- Human-readable lyrics, chords, and arrangement documents
- All derived from that single YAML source

### What the Agent Does Well

ABC notation is picky. Every bar must add up exactly. In 4/4 time with an eighth-note default, each bar needs precisely 8 eighth-note units. Not 7. Not 9. The agent counts obsessively and catches errors I'd miss.

The agent also maintains consistency across files. If I change the verse from 16 bars to 12, everything downstream updates—drum patterns, bass lines, string parts. No manual synchronization.

When I describe an arrangement direction like "strings swell in the bridge," the agent translates that into specific notation: the violin moves from E4 to E5 over 12 bars, the viola follows a third below, the cello anchors on roots. I review, adjust, regenerate.

### What the Human Does

The concept. The words. The emotional arc. The judgment calls.

"I would know you in a lineup of the dead / Know you by the bones that hold your hands"—no agent wrote that. The image of a rib cage opening "like a cabinet, like a cart" came from thinking about medical students and the strange intimacy of anatomy class.

The arrangement decisions are human too. Strings alone in the intro because the song is about studying someone before you speak about them. Drums entering on brushes in verse 2, not verse 1, because patience matters here. The final chorus shifting from "you" to "we" because the knowing has become mutual by then.

The agent executes. The human directs and judges.

---

## Song Structure

| Section | Bars | Description |
|---------|------|-------------|
| Intro | 8 | Strings only. Establishing weight. |
| Verse | 16 | Guitar enters (fingerpicked), bass on whole notes. |
| Verse | 16 | Brushes enter. Same music, second set of lyrics. |
| Chorus | 8 | Piano enters. "Cadaver lab, cadaver lab." |
| Verse | 16 | Third iteration, dynamics building slightly. |
| Chorus | 8 | Fuller arrangement. |
| Bridge | 12 | Instrumental build. Strings ascending. |
| Verse | 16 | Final verse. "There's a drawer of your teeth somewhere." |
| Chorus Final | 8 | Full ensemble. "I would know you by your silence in the air." |
| Outro | 8 | Gradual fade. Instruments drop out one by one. |

Total: 116 bars. At 78 BPM, roughly 6 minutes.

---

## Instrumentation

**String Section:**
- Violin (MIDI program 40)
- Viola (MIDI program 41)
- Cello (MIDI program 42)

**Rhythm Section:**
- Acoustic guitar, steel-string (program 25)
- Acoustic bass (program 32)
- Drums: kick, snare, hi-hat (channel 10)

**Keys:**
- Piano (program 0)

**Voice:**
- Vocal melody (program 53, "Voice Oohs" as placeholder)

---

## Chord Progression

The song lives in E minor with excursions to the relative major region.

**Verses:** Em - C - G - D - Em - C - G - Em

The G and D create lift before settling back to Em. The C adds warmth—it's the VI chord, the nostalgia position.

**Chorus:** Em - G - C - D (repeated)

Standard minor key progression but the melody emphasizes different tones on each pass, keeping it from feeling circular.

**Bridge:** Same chords, longer sustains, strings climbing through inversions.

---

## Lyrics

The thesis appears in the first line: "I would know you in a lineup of the dead."

Not morbid. Sacred. The way a doctor knows anatomy. The way years of attention leave you certain.

Each verse develops the metaphor:
1. The body itself—bones, vertebrae, skull
2. Where this knowledge comes from—the cadaver lab
3. What it means in daily life—footsteps, weight, air
4. What persists beyond presence—teeth in a drawer, identity without life

The chorus is incantation. Repetition that builds rather than deadens. "Cadaver lab, cadaver lab" becomes a mantra.

The final chorus shifts one word: "I would know you by your silence in the air." Now the knowing includes absence. The shape someone leaves when they're gone.

---

## Production Notes (for whoever records this)

**Dynamics:** The song should breathe. Verse 1 barely there. Verse 4 present. Final chorus full but controlled—never screaming, always PRESENT.

**Vocals:** Dry, close-mic'd, speaking-rhythm on the verses. The phrasing is conversational. "The vertebrae that curve just so"—let "just so" hang.

**Strings:** Not orchestral bombast. Chamber music intimacy. Three players who know each other.

**Drums:** Brushes until the bridge. Even in the final chorus, restraint. The emotional weight comes from the words and the melody, not from the backbeat.

**Outro:** Crucial. Drums stop first. Then bass. Then piano. Guitar and strings thin. Finally just guitar, then the final Em chord ringing. Let it decay naturally. 3-4 seconds of silence before the track ends. This sets the tone for the entire album.

---

## Files

```
01-cadaver-lab/
├── song.yaml           # Single source of truth (you edit this)
├── lyrics.txt          # Generated: lyrics only
├── chords.txt          # Generated: lyrics with chord symbols
├── arrangement.txt     # Generated: production notes per section
├── midi/               # Generated: one file per instrument
│   ├── vocal-melody.mid
│   ├── guitar-acoustic.mid
│   ├── bass.mid
│   ├── piano.mid
│   ├── violin.mid
│   ├── viola.mid
│   ├── cello.mid
│   ├── drum-kick.mid
│   ├── drum-snare.mid
│   └── drum-hihat.mid
└── .generated/         # Intermediate files (ABC notation, etc.)
```

To regenerate everything after editing `song.yaml`:

```bash
python scripts/generate_song.py cadaver-lab/01-cadaver-lab/
```

---

## The Workflow in Practice

I don't type commands. I describe intentions to Claude Code.

"Make the intro longer. Eight bars feels rushed."

The agent reads the current structure, modifies the intro section from 4 to 8 bars, extends the string parts accordingly, and regenerates all files. I listen to the MIDI. If it works, I move on. If not, I describe what's wrong.

"The violin is too busy in the verses. Long tones only."

The agent rewrites the violin ABC notation, replacing sixteenth-note movement with whole notes and half notes. Regenerates. I listen again.

This loop—describe, generate, listen, adjust—continues until the song feels right. The agent handles the notation math and file management. I handle the aesthetic judgment.

Neither of us works alone. The song emerges from the collaboration.

---

## What This Proves

You can build complete musical arrangements through conversation with an AI agent. The agent is excellent at maintaining consistency, counting bars, translating intentions into notation. It's not good at originating the emotional concept or making taste judgments.

The division of labor is clear: human direction, machine execution. Human judgment, machine precision. The song is mine. The infrastructure is shared.

---

*Brian Edwards*
*Waco, Texas*
*December 2025*
