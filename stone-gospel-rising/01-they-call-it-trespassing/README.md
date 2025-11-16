# They Call It Trespassing

## File Structure

This song uses the **single-source configuration** approach:

### 📝 Source Files (Hand-Written)

```
.source/
    song.yaml           ← EDIT THIS: Single source of truth
```

**This is the ONLY file you should edit.**

### 🤖 Generated Files (Do Not Edit)

```
.generated/
    structure.yaml      ← Generated from song.yaml
    lyrics.yaml         ← Generated from song.yaml
    chords.yaml         ← Generated from song.yaml
    sections/           ← Generated section ABC files
    *.abc               ← Generated complete ABC
    *.mid               ← Generated MIDI files
```

**Never edit these files directly.** They are regenerated from `.source/song.yaml`.

### 📖 Human-Readable Files (Generated)

```
lyrics.txt              ← Generated plain text lyrics
chords.txt              ← Generated chords with lyrics
arrangement.txt         ← Generated arrangement notes
```

## Workflow

### Making Changes

1. **Edit** `.source/song.yaml`
2. **Generate** everything:
   ```bash
   python scripts/generate_song.py .
   ```
3. **Verify** output:
   ```bash
   python scripts/abc_tools.py verify .generated/
   ```
4. **Listen** to MIDI files in `.generated/`

## Song Information

- **Title:** They Call It Trespassing
- **Composer:** Brian Edwards
- **Tempo:** 92 BPM
- **Key:** G minor
- **Total Bars:** 62
- **Structure:** intro (8), verse (8), chorus (6), verse (8), chorus (6), bridge (8), verse (8), chorus (6), outro (4)
- **Instruments:** Vocal, Bass, Acoustic Guitar, Electric Guitar, Organ, Banjo, Drums

All content generated from: `.source/song.yaml`
