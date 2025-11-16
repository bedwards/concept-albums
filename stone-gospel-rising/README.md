# Stone Gospel Rising

**Precious Jim Stone**

## The Vision

This album exists because James Talarico exists. A state representative who quotes scripture on the House floor like he's calling down judgment. A Christian who won't let the powerful hide behind the Bible while ignoring its demands.

This is prophetic rock. Not protest music with religious imagery, but actual theological confrontation. Every song asks the same question Talarico asks in the capitol: You read the same book I do - so why do our gods look so different?

The sound is stripped down, intense, uncomfortable. Think old wood creaking. Think revival tent meets political floor fight. Banjo and bass and raw vocals that won't let you look away. This isn't music to make you feel good. It's music to make you confront what you've been avoiding.

## The Theological Core

Talarico's Jesus is specific: the one who flipped tables, called religious leaders vipers, said the first will be last. That's the Jesus in these songs. Not abstract love and grace, but concrete demands for justice. 

Scripture here isn't decoration - it's weaponized. Isaiah's woe to lawmakers. Psalm 82's "how long will you defend the unjust?" Matthew's "you cannot serve God and money." These land in the middle of songs like accusations.

This album is for anyone who's watched people use Christianity to justify cruelty and thought: No. You don't get to do that. We're taking this back.

## Musical Approach

**Instrumentation:** Banjo-forward, menacing bass, reedy pump organ, sparse drums with uncomfortable silences. No prettiness. Add hurdy-gurdy or accordion on darker tracks for that folk noir edge.

**Tempo:** Mostly slow (85-95 bpm), trudging like an unavoidable march. When it's fast, it's urgent panic, not energy.

**Dynamics:** Extreme contrast. Whispered truth building to walls of sound. No fades - everything ends decisively, like slamming a book shut.

**Vocal delivery:** Raw, insistent, sometimes on the edge of shouting. Not singing pretty, but preaching. The sound of someone who knows they're right and won't shut up about it.

## The Narrative Arc

This album tells a complete story from awakening to resurrection:

**ACT I: CONFRONTATION (Songs 1-2)**
The prophetic voice awakens. Scripture is named. Lines are drawn.

**ACT II: SOLIDARITY (Songs 3-4)**  
Personal cost and ecological witness. The movement grows through sacrifice.

**ACT III: DIRECT CHALLENGE (Songs 5-7)**
Face-to-face confrontation with religious hypocrisy and border injustice.

**ACT IV: RESURRECTION (Song 8)**
Sunday morning. The stone rolls away. What they killed cannot stay dead. The uprising continues.

## Track Listing

1. **They Call It Trespassing** - Land rights, Psalm 24, Leviticus 25. The dispossessed quote scripture back at their oppressors.

2. **Blood on the Capitol Steps** - Isaiah 10, Matthew 25, Amos. Pink granite stained. Prophetic judgment on lawmakers.

3. **The Foreman's Son** - James 5, Luke 12:51, Deuteronomy. Working class solidarity breaks family loyalty for justice.

4. **Permian Prophecy** - Habakkuk, Romans 8:22, Psalm 24. Creation groans. Environmental reckoning in oil country.

5. **Rio Grande Testament** - Matthew 2, Exodus, Deuteronomy. Refugee theology. The stranger at the border is Christ himself.

6. **Same Book Different Gospel** - Direct confrontation with religious hypocrisy. Exposing false faith.

7. **Beatitudes for the Powerful** - Matthew 5 weaponized. Blessings become curses on those who hoard.

8. **Stone Rolled Away** - Mark 16, Matthew 28, Luke 20:18, Acts 4:11. Resurrection as revolution. Hope as inevitable.

## Key Signatures

Bb major and its modes throughout:
- Bb major (I) - hope, declaration
- G minor (vi) - sorrow, anger  
- D dorian (iii) - determination
- Eb lydian (IV) - transcendence
- F mixolydian (V) - driving force
- C minor (ii) - darkness, confrontation

## Recording Philosophy

**Live and raw.** If it sounds too clean, it's wrong. Drums should have room sound. Bass should rattle. Vocals should crack on the high notes because the singer means it.

**Banjo prominence.** Not bluegrass pretty - dissonant, driving, relentless. The banjo is the conscience that won't shut up.

**Space and silence.** Don't fill every bar. Let the uncomfortable pauses sit there. Make people squirm.

**Pump organ, not Hammond.** Reedy, old church, slightly out of tune. The sound of abandoned sanctuaries and broken promises.

**No effects.** Dry vocals. Minimal reverb. Present and accusing, not distant and atmospheric.

## The Talarico Framework

Every song should pass this test: Could this be something Talarico would say on the House floor if he could get away with it?

- **Scripturally grounded** - Quote chapter and verse
- **Politically specific** - Name what's wrong, don't dance around it
- **Theologically precise** - Know the difference between prosperity gospel and liberation theology
- **Uncomfortable** - If the listener feels attacked, that's working
- **Redemptive** - Even in judgment, the door is open for repentance

This isn't "Christian music" in the contemporary worship sense. This is music that takes Christianity seriously enough to demand it mean what it says.

## Implementation Notes

Songs should include:
- Direct scripture quotations as accusations
- Specific Texas geography (Permian Basin, Rio Grande, Travis County, etc.)
- Named hypocrisies (defending the rich while quoting Jesus, etc.)
- Character perspectives from both sides of power
- Beatitudes and prophetic books as structural frameworks
- No metaphor where directness will do

Some songs should be primarily banjo and vocal - no drums, minimal accompaniment. Just truth and strings.

At least one song in 3/4 time - waltz feel but unsettling, off-balance.

One song from the perspective of a legislator being confronted - sympathetic and damning at once.

## File Structure & Single-Source System

**All 8 songs now use a single-source-of-truth system** that guarantees consistency and eliminates manual errors.

### Per Song Directory

```
song-directory/
  .source/
    song.yaml           ← ONLY FILE YOU EDIT (hand-written source)
  .generated/
    *.abc               ← Generated ABC files (all instruments)
    *.mid               ← Generated MIDI files
    sections/*.abc      ← Individual section ABC files
    structure.yaml      ← Structure definition
    lyrics.yaml         ← Lyrics with chords
    chords.yaml         ← Chords reference
  lyrics.txt            ← Human-readable lyrics
  chords.txt            ← Human-readable chords
  arrangement.txt       ← Human-readable arrangement notes
  README.md             ← Song documentation
```

### Workflow

**To modify a song:**
1. Edit only `.source/song.yaml`
2. Run: `python3 scripts/generate_song.py song-directory/`
3. All other files regenerate automatically

**To create a new song:**
1. Copy `.source/song.yaml` from an existing song as template
2. Modify sections, lyrics, instruments, arrangement
3. Generate all files with the script

### Why This Matters

The single-source system makes errors **structurally impossible**:
- ✅ Bar counts can't mismatch (enforced by structure)
- ✅ Lyrics stay consistent across all files
- ✅ No copy-paste errors between sections
- ✅ All instruments guaranteed to match in length
- ✅ Changes propagate automatically to all formats

Everything is validated and generated from the one source file.

## ABC Playback

Use abc2midi, EasyABC, or abcjs for playback/conversion.

All generated MIDI files are tested with abc2midi to ensure valid ABC notation.

**Credits**: Brian Edwards, Jalopy Music, Waco, TX

---

*"The stones will cry out." - Luke 19:40*
