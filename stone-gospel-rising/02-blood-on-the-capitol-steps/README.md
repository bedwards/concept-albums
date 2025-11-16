# Blood on the Capitol Steps

## File Structure

This song uses the **single-source configuration** approach:

### 📝 Source Files (Hand-Written)

```
.source/
    song.yaml           ← EDIT THIS: Single source of truth
```

**This is the ONLY file you should edit.** It contains:
- Song metadata (title, tempo, key, etc.)
- Complete song structure
- All lyrics with chords
- ABC notation snippets for each instrument/section
- Arrangement notes

### 🤖 Generated Files (Do Not Edit)

```
.generated/
    structure.yaml      ← Generated from song.yaml
    lyrics.yaml         ← Generated from song.yaml
    chords.yaml         ← Generated from song.yaml
    sections/           ← Generated section ABC files
        intro-bass.abc
        verse-vocal-melody.abc
        ...
    vocal-melody.abc    ← Generated complete ABC
    bass.abc            ← Generated complete ABC
    ...
    *.mid               ← Generated MIDI files
```

**Never edit these files directly.** They are regenerated from `.source/song.yaml`.

### 📖 Human-Readable Files (Generated)

```
lyrics.txt              ← Generated plain text lyrics
chords.txt              ← Generated chords with lyrics
arrangement.txt         ← Generated arrangement notes
```

These are for easy reading. Edit the source YAML instead.

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

### From Scratch

See `.source/song.yaml` for the complete format. Key sections:

- `song:` - Metadata and structure
- `sections:` - Each section with bars, lyrics, and ABC snippets
- `instruments:` - MIDI program numbers
- `arrangement:` - Human-readable notes

### Validation

The generator ensures:
- ✅ All instruments have identical bar counts
- ✅ Lyrics are consistent across formats
- ✅ Section bar counts match definitions
- ✅ ABC files are syntactically valid
- ✅ MIDI files generate successfully

## Philosophy: DRY (Don't Repeat Yourself)

- **One source file** instead of dozens of redundant files
- **Verse pattern** defined once, lyrics vary
- **Chorus** defined once, used multiple times
- **No manual bar counting** - enforced by structure
- **No copy-paste errors** - generated programmatically

## Song Information

- **Title:** Blood on the Capitol Steps
- **Composer:** Brian Edwards
- **Tempo:** 88 BPM
- **Key:** C minor
- **Total Bars:** 65
- **Structure:** intro, verse, chorus, verse, chorus, break, bridge, verse, chorus, outro

All content generated from: `.source/song.yaml`
