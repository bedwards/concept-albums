# Concept Albums

This is where songs get made. Not the quick kind, the ones you toss off on a Tuesday afternoon. The other kind. The ones that sit with you for a while.

We're building concept albums here. Full records. Each one's got a theme that runs through it like a river, connecting every verse to the next one, every chorus to the story it's telling. Political records. Story records. The kind where you can't just shuffle the tracks because they belong in order, each one leading to the next.

**[Teaching AI to Have Taste](lyrics/time-forgot/REPORT.md)** — An experiment in human-AI collaboration for songwriting. We built a framework that measures lyric quality: concreteness, clichés, show-don't-tell ratios, sensory language. Then we used it to write new lyrics that fit existing melodies. The report shows what worked, what didn't, and what the measurements reveal about writing.

## What Lives Here

Right now there's one album sitting in these folders. Stone Gospel Rising by Precious Jim Stone. Eight tracks about Texas and uprising and the people who build roads and then have to march on them. It's got oil fields and border crossings and state capitol confrontations. Liberation theology set to stripped-down rock and roll in the key of Bb.

But there'll be more. That's the whole point of this place. Each concept gets its own folder. Each folder becomes a complete record you could actually play if you had the band and the conviction.

## How We Build These Things

It starts with an idea. Not just "let's write some songs" but something bigger. A story that needs eight or ten tracks to tell it right. A theme that can hold weight across a whole album side.

Then comes the structure. We don't just write lyrics and call it done. Every song in here gets the full treatment:

**Nine files per song.** That's the baseline. Could be eleven if you need a banjo or some other particular instrument to make the sound work.

First there's `lyrics.txt`. Just the words. Verse, chorus, bridge. Labeled clean so you know what's what. No chords cluttering it up.

Then `chords.txt`. Same lyrics but now with the chord changes sitting right above the syllables where they land. Monospace format. You can read it and play it. Bb to Gm to Cm to F. Whatever the song needs.

Next is `arrangement.txt`. This one tells you how the whole thing actually sounds. Tempo and time signature at the top. Then section by section it lays out what each instrument does. Kick drum on 1 and 3, snare on the backbeat, bass walking root-fifth, acoustic fingerpicking, electric staying quiet until the chorus. Specific and actionable. A real arranger could take this and make the record happen.

After that come the ABC notation files. That's where it gets technical but in a good way. ABC is old-school computer music notation. Text files that describe exactly what notes to play. We write one for each part: `vocal-melody.abc`, `guitar-acoustic.abc`, `guitar-electric.abc`, `bass.abc`, `drums.abc`, `organ.abc`. Sometimes `banjo.abc` if the song calls for it.

The beautiful thing about ABC is you can turn it into MIDI. There's a tool called abc2midi that reads those .abc files and spits out .mid files. Actual playback. You can hear the bass line or the vocal melody or all of it together. Not perfect but real enough to know if you wrote something that works.

## The Iteration Part

Here's what we learned making the first album.

ABC notation is picky. Real picky. You can write something that looks right and abc2midi will throw warnings at you. Bar 12 has five time units when it should have four. Track three is missing lyrics. The annotation syntax is wrong.

So you fix it. You count eighth notes. You make sure every bar adds up to exactly what the time signature promises. You remove the repeat markers and write out the full structure because abc2midi doesn't like having multiple lyric lines for the same repeated music. It wants every sung note to have its words right there.

For drums we learned that percussion notation is its own strange beast. The tool complains about the key signature but generates the MIDI anyway. You live with the warnings that don't matter and fix the ones that do.

For guitars and bass we learned to count obsessively. A bar in 4/4 wants eight eighth notes or four quarter notes or some combination that adds to eight eighths total. Not nine. Not seven. Eight.

We stripped out performance annotations like "palm mute" and "let ring" because they confused the MIDI generator. The arrangement file is where that information lives anyway. ABC is for the notes themselves.

## The Process Flows Like This

**Concept first.** Know what the album is about before you write a single line.

**Track listing.** Eight to ten songs usually. Map out what each one covers. First song opens the door. Last song closes it with something that feels like resolution or at least like you've said what you came to say.

**Song by song, file by file.** Write the lyrics. Add the chords. Describe the arrangement. Then translate it all into ABC notation. Test with abc2midi. Fix the errors. Generate the MIDI. Listen. Adjust.

**Keep it playable.** These aren't progressive metal compositions with seventeen time signature changes. They're songs an actual band could learn and perform. Simple chord progressions. Repeatable rhythms. Earthy and direct.

**Check your work.** abc2midi is your quality control. If it complains, listen. Count your bars. Make sure notes fall on beats. Get it clean.

## What You'll Find in Each Album Folder

A README.md that introduces the concept and lists the tracks.

Numbered directories for each song: `01-song-title`, `02-next-song`, etc. Lowercase, hyphens, no spaces.

Inside each song folder: the nine or eleven files described above. Lyrics, chords, arrangement, and ABC notation for every instrument. Plus the generated MIDI files sitting right next to their source .abc files.

## Technical Notes

All the ABC files follow standard ABC notation version 2.1. They include tempo markings (Q:1/4=110), key signatures (K:Gmin), time signatures (M:4/4), and default note length (L:1/8).

MIDI generation uses abc2midi version 5.02 or later. Run it like this:

```bash
abc2midi vocal-melody.abc -o vocal-melody.mid
```

If you get warnings, read them. Fix the bars that don't add up. Remove annotations that break the parser. Test again until it runs clean.

## Why This Matters

Because songs mean something when they're connected. Because a concept album can tell a story an EP can't. Because taking the time to write out every part and make it playable means you're not just sketching ideas, you're building something complete.

And because sometimes you need the constraint. Eight songs in the same key family. A specific theme. Real notation you can validate and convert to sound. It makes you finish what you start.

That's what this repository is for. Concept albums from start to finish. Complete and documented. Ready to become real music if someone wants to make it real.

---

*Brian Edwards, Jalopy Music, Waco, Texas*
