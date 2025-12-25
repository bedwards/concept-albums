# Lyrics Iteration Workflow

A systematic approach to writing and refining song lyrics using deterministic tools + AI judgment.

## Philosophy

**AI is bad at:** Counting letters, syllables, precise measurement, consistent evaluation
**AI is good at:** Building tools that measure things, interpreting tool output, making qualitative judgments, suggesting revisions

**The workflow:** Build deterministic tools → AI interprets results → AI suggests revisions → Run tools again → Iterate

---

## Tools Overview

```bash
# 5 commands available:
python scripts/lyrics_analyzer.py parse     # Dirty lyrics → structured YAML
python scripts/lyrics_analyzer.py analyze   # Quantitative metrics (rhyme, meter, etc.)
python scripts/lyrics_analyzer.py taste     # Quality metrics (concreteness, clichés, etc.)
python scripts/lyrics_analyzer.py compare   # Rank candidates against model
python scripts/lyrics_analyzer.py critique  # Generate AI critique prompt
```

---

## The Complete Workflow

### Phase 1: Establish the Model

```bash
# 1. Get a reference song you want to match
# Clean it up with section markers: /verse-1/, /chorus/, etc.

# 2. Parse to YAML
python scripts/lyrics_analyzer.py parse \
  -i lyrics/time-forgot/work/time-forgot-clean.txt \
  -o lyrics/time-forgot/work/time-forgot.yaml

# 3. Analyze structure
python scripts/lyrics_analyzer.py analyze \
  -i lyrics/time-forgot/work/time-forgot.yaml \
  -o lyrics/time-forgot/work/time-forgot-analysis.json

# 4. Analyze taste (concreteness, clichés, etc.)
python scripts/lyrics_analyzer.py taste \
  -i lyrics/time-forgot/work/time-forgot.yaml \
  -o lyrics/time-forgot/work/time-forgot-taste.json
```

**You now have baseline metrics to compare against.**

---

### Phase 2: Generate Candidates

Write or generate multiple candidate lyrics. Put them in a directory:

```
lyrics/time-forgot/gen-songs/
├── candidate-01.txt
├── candidate-02.txt
└── candidate-03.txt
```

Parse each one:
```bash
for f in lyrics/time-forgot/gen-songs/*.txt; do
  python scripts/lyrics_analyzer.py parse -i "$f"
done
```

---

### Phase 3: Quantitative Filter

```bash
# Compare structure against model
python scripts/lyrics_analyzer.py compare \
  -m lyrics/time-forgot/work/time-forgot.yaml \
  -c lyrics/time-forgot/gen-songs/*.yaml \
  -o lyrics/time-forgot/work/comparison.json
```

**This eliminates candidates with wrong structure** (wrong bar counts, different section order, etc.)

---

### Phase 4: Taste Filter

```bash
# Run taste analysis on each candidate
for f in lyrics/time-forgot/gen-songs/*.yaml; do
  python scripts/lyrics_analyzer.py taste -i "$f"
done
```

**This eliminates candidates with:**
- Low concreteness (too abstract)
- High cliché density
- Too much "telling" vs "showing"
- Weak sensory language

---

### Phase 5: AI Critique

For your top candidates, generate AI critique prompts:

```bash
# Generate critique prompt with taste context
python scripts/lyrics_analyzer.py critique \
  -i lyrics/time-forgot/gen-songs/candidate-02.yaml \
  -m lyrics/time-forgot/work/time-forgot.yaml \
  --include-taste \
  -o lyrics/time-forgot/work/candidate-02-critique.md
```

**Then paste the prompt into Claude/ChatGPT.** The AI returns structured JSON:

```json
{
  "imagery_concreteness": { "reasoning": "...", "score": 4 },
  "originality": { "reasoning": "...", "score": 3 },
  "emotional_authenticity": { "reasoning": "...", "score": 4 },
  "narrative_coherence": { "reasoning": "...", "score": 3 },
  "craft": { "reasoning": "...", "score": 4 },
  "singability": { "reasoning": "...", "score": 4 },
  "overall_score": 3.7,
  "verdict": "POLISH",
  "top_3_improvements": [...],
  "strongest_lines": [...],
  "weakest_lines": [...]
}
```

---

### Phase 6: Revise and Iterate

Based on the AI critique, revise the lyrics. Then:

```bash
# Re-run taste analysis
python scripts/lyrics_analyzer.py taste -i candidate-02-v2.yaml

# Re-generate critique
python scripts/lyrics_analyzer.py critique -i candidate-02-v2.yaml -t
```

**Keep iterating until:**
- Taste score > 70
- AI verdict = "READY" or "POLISH"
- No major clichés detected
- Concreteness > 3.5/5.0

---

## Metric Targets

### Structural (from `analyze`)
- Match model's rhyme scheme (ABCB for ballads, ABAB for alt)
- Match model's syllable count (±1 per line)
- Same section structure

### Taste (from `taste`)
| Metric | Target | Why |
|--------|--------|-----|
| Overall Taste | > 70 | Composite quality score |
| Concreteness | > 70 | Physical vs abstract language |
| Cliché-Free | 100 | Zero clichés in final draft |
| Show Don't Tell | > 60 | Action verbs over state verbs |
| Sensory | > 50 | At least 3 senses engaged |

### AI Critique (from `critique`)
| Criterion | Target | Description |
|-----------|--------|-------------|
| Imagery | 4-5 | Specific, tangible images |
| Originality | 4-5 | Fresh phrases, no clichés |
| Authenticity | 4-5 | Genuine emotional truth |
| Narrative | 4-5 | Clear arc with resolution |
| Craft | 4-5 | Skilled meter and rhyme |
| Singability | 4-5 | Natural in the mouth |
| Verdict | READY | No major issues remaining |

---

## Example Session

```bash
# Start with a rough draft
echo "I feel so sad today
The rain is falling down
Everything is awful
In this lonely town" > draft-v1.txt

# Parse and taste-check
python scripts/lyrics_analyzer.py parse -i draft-v1.txt
python scripts/lyrics_analyzer.py taste -i draft-v1.yaml

# Output: OVERALL TASTE SCORE: 28.4/100
# - Clichés: "feel so sad", "rain falling down"
# - Concreteness: Low (sad, awful, lonely)
# - Show Don't Tell: Weak ("I feel")

# Revise based on feedback...
echo "The gutter water runs black with ash
Where the mill used to stand
I trace her name on the frosted glass
Cold coffee in my hand" > draft-v2.txt

# Re-check
python scripts/lyrics_analyzer.py taste -i draft-v2.yaml

# Output: OVERALL TASTE SCORE: 82.1/100
# - Clichés: None
# - Concreteness: High (gutter, ash, mill, glass, coffee)
# - Sensory: sight + touch + taste

# Generate AI critique for final polish
python scripts/lyrics_analyzer.py critique -i draft-v2.yaml -t
```

---

## Integration with Claude Code

When working with Claude Code, you can ask it to:

1. **Generate candidates:** "Write 3 variations of this verse in the style of Daniel Romano"
2. **Run the tools:** Claude will execute `taste` and `critique` commands
3. **Interpret results:** Claude reads the JSON output and explains what to fix
4. **Suggest revisions:** Claude proposes specific line changes
5. **Verify improvement:** Claude re-runs the tools to confirm scores improved

The key insight: **Claude builds and runs the measurement tools, then uses its judgment to interpret the measurements.** This combines the reliability of deterministic analysis with the contextual understanding of AI.

---

## References

- [Brysbaert Concreteness Ratings](https://link.springer.com/article/10.3758/s13428-013-0403-5) - 40k word dataset
- [LLM-as-a-Judge Guide](https://www.evidentlyai.com/llm-guide/llm-as-a-judge) - Best practices for AI evaluation
- [spaCy](https://spacy.io/) - NLP for POS tagging
- [CMU Pronouncing Dictionary](https://pronouncing.readthedocs.io/) - Phonemes and rhymes
