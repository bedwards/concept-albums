# Writing New Lyrics to "Time Forgot To Change My Heart"

Daniel Romano's "Time Forgot To Change My Heart" is a country murder ballad. A man betrayed by his friend and lover travels to their home, contemplates violence, and leaves a message with his daughter. We used it to build and test a framework for writing new lyrics that fit existing melodies.

The original has 34 lines across 9 sections. Average of 7.9 syllables per line. ABCB rhyme scheme in verses. The chorus repeats "time forgot to change my heart" with variation.

We built five commands in `scripts/lyrics_analyzer.py`:

```
parse     - convert lyrics to structured YAML
analyze   - measure rhyme, meter, syllables
taste     - measure concreteness, clichés, show-don't-tell
compare   - rank candidates against the original
critique  - generate evaluation prompt for Claude
```

Then we wrote four new versions and one intentionally bad version. We ran every analyzer. We found out what the tools catch and what they miss.

---

## The Original

```
/verse-1/
I got trampled by my woman
I been cheated and double-crossed
There was a coup in the alter
I had a friend but he got lost

/chorus/
They say time can take the pain away
Because time changes everything
But time forgot to change my heart
Yes time forgot to change my heart
```

We parsed this to YAML, ran the analyzers, and got baseline metrics: 0.45 vocabulary richness, mostly ABCB rhyme, 7.9 syllables per line average. These became the targets.

---

## Four New Versions

Each had to match the original's structure exactly. Same syllable counts. Same rhyme positions. Same section order. Different content.

### Wi-Fi Spoof

Router problems instead of romantic betrayal.

```
/verse-1/
I got throttled by my router
I been buffered and ping-blocked
There was a coup in the server
I had a signal but it got dropped

/chorus/
They say time can fix the Wi-Fi
Because time reboots everything
But time forgot to change my password
Yes time forgot to change my password
```

"Throttled by my router" has the same syllable count as "trampled by my woman." "Ping-blocked" lands where "double-crossed" did. The parody works because the framework forced every line to scan.

Structural score: 0.977. Taste score: 54.3. The concreteness analyzer scored it low at 32.1 because "router" and "firewall" aren't in the Brysbaert psycholinguistic dataset. The tool doesn't know they're physical objects.

### Rain (Close Match)

Same emotional territory, different details. Brother instead of friend. Austin instead of country. Brownstone instead of shack.

```
/verse-1/
I got stranded by my brother
I been lied to and let down
There was a scene at the chapel
I had a ring but she left town

/chorus/
They say rain can wash the hurt away
Because rain cleans everything
But rain forgot to wash my memory
Yes rain forgot to wash my memory
```

Structural score: 0.976. Taste score: 70.7—the highest of all candidates. Concreteness: 68.4. Sensory richness: 84.0, with touch, sight, and sound all present. This version maintained concrete imagery ("brownstone flat," "auburn hair," "weathered hand") while matching every structural constraint.

### Coal (Dark/Political)

Mining towns poisoned by fracking. Confrontation at statehouse instead of bedroom.

```
/verse-1/
I got buried by the mountain
I been crushed and chemical-crossed
There was a blast in the mineshaft
I had a brother but he got lost

/chorus/
They say time can heal the coalfields
Because time buries everything
But time forgot to bury the anger
Yes time forgot to bury the anger
```

Structural score: 0.979—highest of all. Taste score: 64.7. Cliché-free: 100. Zero clichés detected. Political language doesn't trigger the tired-phrase list because activism hasn't been strip-mined the way romance has. But sensory richness dropped to 27.3. "Righteous fury" and "bought men" communicate clearly but don't evoke the senses.

### Garden (Tender Inversion)

Murder ballad becomes love song. Same structure, opposite emotion.

```
/verse-1/
I got softened by your patience
I been gentled and re-taught
There was a bloom in the morning
I lost my fear and you were caught

/chorus/
They say time can grow the garden
Because time tends to everything
But time forgot to stop my loving
Yes time forgot to stop my loving
```

Structural score: 0.971. Taste score: 49.6—lowest of the serious attempts. Cliché-free: 40. Love poetry is hard. English has been strip-mined for romantic expressions. The framework correctly flagged that this version needs more work.

---

## The Intentionally Weak Candidate

We wrote a bad version on purpose. Generic heartbreak with no specific images.

```
/verse-1/
My heart is broken and it's bleeding
I feel so very sad
Everything is really awful
My life has gone so bad

/chorus/
They say that things will get much better
Because tomorrow is a new day
But things forgot to get much better
Yes things forgot to get much better
```

Structural score: 0.934. Almost as high as the good candidates.

Taste score: 35.4. Thirty-nine points lower than the close match.

The structural analyzer said it fit the melody. The taste analyzer caught that it was garbage: concreteness 3.02 out of 5.00, seven clichés detected including "tomorrow is a new day" and "feel so very sad," only one sense engaged.

This gap is the whole point. You can match every syllable count and still write nothing worth singing.

---

## Side-by-Side: Verse 3

**Original:**
> So I took a train into that country
> And I found their little shack
> I went to drink until the sunset
> And in the darkness I came back

**Close match:**
> So I took a bus into that city
> And I found their brownstone flat
> I went to drink until the midnight
> And when the bars closed I came back

**Dark:**
> So I took a truck to the statehouse
> And I parked outside their gates
> I went to wait until the session
> And when they voted I sealed their fate

**Tender:**
> So I took a walk into that garden
> And I found your little plot
> I knelt to tend until the evening
> And in the twilight I stayed caught

**Spoof:**
> So I took a cord into that basement
> And I found their little rack
> I went to stream until the sunset
> And in the buffering I came back

Same syllable counts. Same rhyme positions. Same narrative beat—journey, arrival, waiting, return. The frame stays fixed. The content varies.

---

## How It Works Inside Claude Code

You don't run the commands yourself. You describe what you want. Claude Code figures out which tools to use.

"Write a version of Time Forgot about losing a restaurant to a chain store. Match the meter exactly."

Claude Code reads the original from `work/time-forgot-clean.txt`. It parses to YAML. Runs `analyze` to get syllable counts and rhyme scheme. Notes that verses have four lines, eight syllables each, rhyming second and fourth. Notes that the chorus repeats a phrase with variation.

It generates a draft. Runs `taste`. Reports back.

"First attempt scores 0.92 structural, 58 taste. Line 7 is one syllable short. 'Corporate greed' flagged as abstract—concreteness score 2.1. Line 12 uses 'feel so' which is on the cliché list."

Then it offers to fix those specific lines.

You accept or reject. It revises. Runs taste again. Reports the new scores. Loop continues until the numbers are acceptable or you decide the current version is good enough despite them.

The human provides direction and makes decisions. The agent builds tools, runs them, interprets results, suggests fixes. Neither side works alone.

---

## What the Tools Measure

**Structural score** (0.0 to 1.0): Can this be sung to the melody? Syllable alignment, rhyme pattern match, section structure. The weak candidate scored 0.934. The best candidate scored 0.979. Not much separation.

**Taste score** (0 to 100): Should this be sung? Four components weighted together:
- Concreteness: physical nouns versus abstract. "Hand" scores 4.95. "Love" scores 2.95. "Meaning" scores 1.95. We used the Brysbaert dataset—40,000 English words rated on a 1-5 scale.
- Cliché-free: matches against a phrase list. "Tomorrow is a new day." "Feel so sad." "Love at first sight." Finding these flags places to look.
- Show-don't-tell: counts state verbs (is, was, felt, seemed) against action verbs (slammed, crept, whispered). More action means more showing.
- Sensory richness: how many senses get engaged. Sight, sound, touch, smell, taste.

The weak candidate scored 0.934 structural but 35.4 taste. The close match scored 0.976 structural and 70.7 taste. Structural analysis asks whether you matched the form. Taste analysis asks whether you used it well.

---

## What the Tools Miss

The concreteness ratings come from general English. "Router" isn't in the Brysbaert dataset. Neither is "fracking" or "brownstone." The spoof scored low on concreteness not because it's abstract but because tech words aren't in the dictionary. Different domains need different word lists.

Cliché detection is a phrase list. It catches "tomorrow is a new day" but not domain-specific clichés. It can't tell intentional from lazy. The spoof uses "time changes everything" deliberately.

Show-don't-tell counts verb types. "Felt" is a state verb. "Crept" is an action verb. But "felt the cold steel" is actually showing. The verb classification is crude.

Sensory analysis looks for predetermined word lists. Political language communicates clearly but doesn't trigger them. "Righteous fury" and "bought men" aren't tagged as sensory.

The tools provide data. What the data means—that's judgment. The human still makes the call.

---

## Why This Architecture

Claude can explain what makes good lyrics. It knows about concrete imagery, about show-don't-tell, about avoiding clichés. Ask it to articulate the principles and it will.

But when it generates lyrics, it doesn't reliably apply those principles. The weak candidate came from the same model that built the analyzers. It knew better. It just didn't do better.

The asymmetry goes deeper. Ask Claude how many times 'r' appears in "strawberry" and it might say two. The answer is three. Language models process tokens, not characters. They understand meaning but struggle with counting.

Ask Claude to write a Python script that counts the 'r's in "strawberry" and it produces flawless code. Run the code and you get three every time.

So we built tools. Syllable counting uses the CMU Pronouncing Dictionary—a lookup, not a guess. Concreteness scoring uses Brysbaert's ratings—psycholinguistic research, not vibes. Cliché detection matches against a list. Show-don't-tell classifies verbs by type. Rhyme analysis extracts phonemes and compares endings.

These tools are deterministic. Run them a thousand times, get the same answer. They don't hallucinate. They don't drift. They measure.

Then Claude interprets the measurements. "Line 7 is one syllable short" becomes "Consider changing 'absolutely' to 'completely' to drop a syllable." "Concreteness score 2.1" becomes "Replace 'emotion' with 'shaking hands' or 'dry mouth' to make it physical."

The measurement is reliable. The interpretation is contextual. Both matter.

---

## Running It Now

The workflow is conversational. You talk to Claude Code. It decides what to do.

"I want to write a parody of this song." Claude reads the song, parses it, runs the structural analysis. "This song has ABCB rhyme in verses, averaging 7.8 syllables per line. What's the parody topic?"

"Losing my keys constantly." Claude generates a draft, runs the taste analysis. "Draft complete. Structural match 0.91. Taste score 62. Two lines flagged for clichés. Want me to fix them?"

"Yes." It revises, re-runs, reports new scores. "Structural 0.93, taste 71. No clichés flagged. Concreteness improved from 3.1 to 3.8. Ready to review?"

The loop continues until you're satisfied or decide to stop. You can ask for specific changes. You can reject suggestions. You can ask why a line scored low. The agent explains: "Line 4 uses 'very' as an intensifier. The taste analyzer flags this as weak language. Alternatives: 'stone cold,' 'bone dry,' 'flat broke.'"

Everything happens in conversation. The tools run in the background. You see results and recommendations.

---

## What Changes With Better Models

Context windows grow. Current models analyze one song at a time. Future models hold entire albums, measuring thematic consistency across ten tracks. Does the imagery in song 8 echo song 2? Does the vocabulary shift appropriately between the angry songs and the tender ones?

Multimodal input arrives. Right now we infer melody constraints from syllable counts and stress patterns. When models process audio directly, they compare lyrics against actual recordings. Does the vowel on the held note sing well? Does the consonant cluster land on a rest or a downbeat?

Domain adaptation improves. The concreteness ratings come from general English. A model fine-tuned on successful song lyrics might weight words differently. "Router" would score as concrete in tech contexts. "Spirit" would score as concrete in gospel.

Agent autonomy deepens. Right now Claude generates one draft, measures it, suggests fixes. Future agents generate fifty drafts, measure all of them, and present only the top three. The human reviews options instead of iterations.

None of this changes the fundamental split. Measurement stays deterministic. Interpretation stays contextual. Judgment stays human. The tools get sharper. The workflow gets faster. The division of labor holds.

---

## Files

```
lyrics/time-forgot/
├── time-forgot-raw.txt              # Original with chord annotations
├── work/
│   ├── time-forgot-clean.txt        # Cleaned with section markers
│   ├── time-forgot.yaml             # Parsed structure
│   ├── time-forgot-analysis.json    # Rhyme, meter, syllables
│   └── time-forgot-taste.json       # Concreteness, clichés, etc.
├── gen-songs/
│   ├── spoof-wifi.txt/.yaml/.taste.json
│   ├── close-match-rain.txt/.yaml/.taste.json
│   ├── dark-coal.txt/.yaml/.taste.json
│   ├── tender-garden.txt/.yaml/.taste.json
│   └── candidate-03.txt/.yaml       # The intentionally weak one
└── REPORT.md                        # This file
```

---

## Results Summary

| Version | Structural | Taste | Concreteness | Cliché-Free | Sensory |
|---------|-----------|-------|--------------|-------------|---------|
| Close (Rain) | 0.976 | 70.7 | 68.4 | 60 | 84.0 |
| Dark (Coal) | 0.979 | 64.7 | 53.3 | 100 | 27.3 |
| Spoof (Wi-Fi) | 0.977 | 54.3 | 32.1 | 80 | 27.3 |
| Tender (Garden) | 0.971 | 49.6 | 41.9 | 40 | 54.6 |
| Weak (candidate-03) | 0.934 | 35.4 | 40.9 | 0 | 27.3 |

The close match scored highest on taste because it maintained concrete imagery while matching structure. The dark version scored highest on structure and had zero clichés but lost sensory richness to political abstraction. The spoof worked as parody but the concreteness analyzer didn't understand tech vocabulary. The tender inversion struggled because love language triggers cliché flags.

The weak candidate scored nearly as high on structure as the good ones but 35 points lower on taste. That gap is what the framework catches. Structural analysis and taste analysis measure different things. You need both.

---

## A Note on Working This Way

I started this project because I wanted to write new songs that fit existing melodies. Not necessarily parodies, though parodies work. Just new lyrics you could actually sing to a tune you already know. The constraint forces craft. You can't pad lines or fudge syllable counts when the melody already exists.

The tools came from frustration. I'd ask Claude to write lyrics matching a specific meter and it would get close but not exact. Line 7 would be one syllable off. The rhyme scheme would drift. Small errors that break singability.

But when I asked Claude to build a syllable counter, it built a syllable counter. When I asked for a rhyme analyzer, I got a rhyme analyzer. The model that couldn't reliably count syllables in its own output could write flawless code to count syllables in any input.

That asymmetry became the whole architecture. Claude is excellent at building tools to evaluate things it can't evaluate directly. Then it's excellent at understanding the output of those tools. The measurement happens in deterministic code. The interpretation happens in conversation.

I don't want the AI to write my songs. I want it to catch my mistakes before they become habits. I want it to flag when I'm reaching for a cliché instead of an image. I want measurements I can trust, and then I want help understanding what those measurements mean.

The workflow inside Claude Code matters more than the individual commands. I don't invoke `lyrics_analyzer.py parse` myself. I describe what I'm trying to do and Claude figures out which tools to run. The conversation is the interface. The tools run in the background.

This feels like where AI assistance is heading. Not replacement. Not just generation. Collaboration with clear division of labor. The human provides direction, makes creative decisions, owns the judgment. The agent builds tools, runs them reliably, interprets results, suggests revisions. Neither side works well alone. Together they work better than either.

The models will improve. Context windows will grow. Multimodal understanding will arrive. Agents will become more autonomous. But the fundamental split—measurement versus interpretation, determinism versus judgment—that holds. The architecture adapts. The division of labor persists.

I wrote these lyrics in December 2025, sitting in Waco, Texas, wondering whether any of them would actually work if someone tried to sing them. The framework says the close match scores 70.7 on taste and 0.976 on structure. Whether it's actually good—that's still my call.

---

*Brian Edwards*
*brian.mabry.edwards@gmail.com*
*512-584-6841*
*December 25, 2025*
*Waco, Texas*
