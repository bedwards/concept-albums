# ABC Notation Build Tools

**Robust, test-driven tools for creating error-free ABC notation songs.**

This toolset ensures bar count accuracy and consistency across all song files through:
- Template generation with enforced bar counts
- Section-by-section validation before assembly
- Lyrics consistency checking across formats
- Complete test suite (14 tests) run in CI/CD
- Scripts that prevent manual errors

## Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Ensure abc2midi is installed (from abcmidi package)
# macOS: brew install abcmidi
# Ubuntu/Debian: apt-get install abcmidi
```

## Philosophy: Scripts Over Manual Editing

**DO NOT** manually create complete ABC files. Instead:
1. Define structure in YAML (sections, bar counts)
2. Generate section templates (guaranteed correct bar counts)
3. Fill in musical content in small, validatable sections
4. Let scripts assemble complete files

This approach makes bar count errors **impossible**.

## Tools

### section_tools.py

**NEW**: Section management with automatic bar count validation.

**Generate all section templates for a song:**
```bash
python section_tools.py generate-all stone-gospel-rising/02-blood-on-the-capitol-steps
```

**Validate a single section file:**
```bash
python section_tools.py validate structure.yaml intro bass sections/intro-bass.abc
```

**Validate all sections in a song:**
```bash
python section_tools.py validate-all stone-gospel-rising/02-blood-on-the-capitol-steps
```

This tool ensures every section file has exactly the right number of bars as defined in `structure.yaml`, preventing bar count errors before they happen.

### lyrics_tools.py

Lyrics validation and consistency checking.

**Validate lyrics consistency:**
```bash
python lyrics_tools.py validate song-directory/
```

Checks:
- lyrics.yaml exists and is valid YAML
- chords.yaml exists and lyrics match lyrics.yaml exactly
- Ignores punctuation/capitalization differences
- Reports specific line-level mismatches

Ensures your lyrics are consistent across all documentation formats.

### test_abc_tools.py

Comprehensive test suite (14 tests) that validates:
- Bar counting logic (single/multi-voice, headers, lyrics)
- Section template generation
- Section validation against expected bar counts
- File combining/assembly
- abc2midi validation

Run with: `python test_abc_tools.py`

All tests must pass for CI/CD to succeed.

### abc_tools.py

Core utilities for ABC file manipulation and validation.

**Count bars in a file:**
```bash
python abc_tools.py count song/vocal-melody.abc
```

**Validate ABC file:**
```bash
python abc_tools.py validate song/bass.abc
```

**Verify all instruments in a song match:**
```bash
python abc_tools.py verify stone-gospel-rising/02-blood-on-the-capitol-steps
```

### build_song.py

Build complete song files from modular section files.

**Workflow:**

1. Create a `sections/` directory in your song folder
2. Create individual ABC section files (e.g., `intro-vocal.abc`, `verse-bass.abc`)
3. Create a `structure.yaml` defining the song structure
4. Run the builder to combine sections into complete files

**Example structure.yaml:**
```yaml
title: "Blood on the Capitol Steps"
composer: "Brian Edwards"  
tempo: 88
time: "4/4"
key: "Cmin"

sections:
  - name: intro
    bars: 4
    vocals: false
  - name: verse
    bars: 8
    vocals: true
  - name: chorus
    bars: 8
    vocals: true

structure:
  - intro
  - verse
  - chorus
  - verse
  - chorus
  - outro

instruments:
  vocal:
    program: 53
  bass:
    program: 33
  drums:
    program: 128
  guitar-acoustic:
    program: 25
  guitar-electric:
    program: 29
  organ:
    program: 16
```

**Build song:**
```bash
python build_song.py stone-gospel-rising/02-blood-on-the-capitol-steps structure.yaml
```

## Modular Section Files

Section files contain just the music notation for one section of one instrument.

**Example: `sections/intro-bass.abc`**
```abc
"Cm"C,8 | C,8 | C,8 | C,8 |
```

**Example: `sections/verse-bass.abc`**
```abc
"Cm"C,2 C,2 G,,2 G,,2 | "F"F,2 F,2 C,2 C,2 |
"Cm"C,2 C,2 G,,2 G,,2 | "Bb"B,,2 B,,2 F,,2 F,,2 |
"Gm"G,2 G,2 D,2 D,2 | "Eb"E,2 E,2 B,,2 B,,2 |
"Bb"B,,2 B,,2 F,,2 F,,2 | "F"F,2 F,2 C,2 C,2 |
```

No headers needed - just the music notation. The builder adds headers automatically.

## Benefits

1. **Easier to verify**: Each section file is small and easy to count
2. **Reusable**: Verse pattern repeats? Use the same file multiple times
3. **Consistency**: All instruments guaranteed to have same structure
4. **Debugging**: If bar counts don't match, you can see exactly which section is wrong

## Complete Workflow Example

### Step 1: Create Structure Definition

```bash
cd stone-gospel-rising/03-new-song
```

Create `structure.yaml`:
```yaml
title: "The Foreman's Son"
composer: "Brian Edwards"
tempo: 95
time: "4/4"
key: "Gmin"

sections:
  - name: intro
    bars: 4
  - name: verse
    bars: 8
  - name: chorus
    bars: 8
  - name: bridge
    bars: 4
  - name: outro
    bars: 4

structure:
  - intro
  - verse
  - chorus
  - verse
  - chorus
  - bridge
  - chorus
  - outro

instruments:
  vocal-melody:
    program: 53
  bass:
    program: 33
  guitar-acoustic:
    program: 25
  guitar-electric:
    program: 29
  organ:
    program: 16
  drums:
    percussion: true
```

### Step 2: Create Lyrics (YAML)

Create `lyrics.yaml`:
```yaml
song:
  title: "The Foreman's Son"
  composer: "Brian Edwards"

sections:
  verse1:
    - "First line of verse one"
    - "Second line of verse one"
  chorus:
    - "Chorus line one"
    - "Chorus line two"
  # etc...
```

### Step 3: Create Chords (YAML)

Create `chords.yaml`:
```yaml
song:
  title: "The Foreman's Son"
  key: "G minor"
  tempo: 95

sections:
  verse1:
    - chords: ["Gm", "Cm"]
      lyrics: "First line of verse one"
    - chords: ["Bb", "F"]
      lyrics: "Second line of verse one"
  # etc...
```

### Step 4: Validate Lyrics

```bash
python ../../scripts/lyrics_tools.py validate .
```

Output:
```
✅ All lyrics are consistent!
```

### Step 5: Generate Section Templates

```bash
python ../../scripts/section_tools.py generate-all .
```

Output:
```
Created template: sections/intro-vocal-melody.abc (4 bars)
Created template: sections/intro-bass.abc (4 bars)
...
Generated 36 section templates
```

### Step 6: Fill in Musical Content

Edit individual section files in `sections/`:
- Each file is small (4-8 bars)
- Easy to verify manually
- Templates start with rests - replace with actual notes

### Step 7: Validate Sections

```bash
python ../../scripts/section_tools.py validate-all .
```

Output:
```
✅ All sections valid!
```

### Step 8: Build Complete ABC Files

```bash
python ../../scripts/build_song.py . structure.yaml
```

Output:
```
Built vocal-melody.abc
Built bass.abc
...
✓ All files match: 28 bars
```

### Step 9: Verify and Generate MIDI

```bash
python ../../scripts/abc_tools.py verify .

for f in *.abc; do abc2midi "$f" -o "${f%.abc}.mid"; done
```

### Step 10: Run Full Validation

```bash
# All checks that run in CI/CD
python ../../scripts/test_abc_tools.py          # Test suite
python ../../scripts/lyrics_tools.py validate . # Lyrics consistency
python ../../scripts/section_tools.py validate-all . # Section bar counts
python ../../scripts/abc_tools.py verify .      # Complete file consistency
```

## Running Tests

```bash
cd scripts
python3 test_abc_tools.py
```

14 tests covering:
- Bar counting (single/multi-voice, with headers/lyrics)
- Section template generation
- Section validation
- File combining
- abc2midi validation
