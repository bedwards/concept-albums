#!/usr/bin/env python3
"""
Test ABC to MIDI timing consistency.

These tests use actual abc2midi to verify our understanding of ABC notation
and catch any issues with bar counting/timing.
"""

import subprocess
import tempfile
import unittest
from pathlib import Path

import mido


def create_abc(music: str, title: str = "Test") -> str:
    """Create a complete ABC file with standard header."""
    return f"""X:1
T:{title}
M:4/4
L:1/8
Q:1/4=60
K:C
{music}
"""


def abc_to_midi(abc_content: str) -> tuple[Path, list[str]]:
    """
    Convert ABC to MIDI using abc2midi.

    Returns:
        (midi_path, warnings)
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".abc", delete=False) as f:
        f.write(abc_content)
        abc_path = Path(f.name)

    midi_path = abc_path.with_suffix(".mid")

    result = subprocess.run(
        ["abc2midi", str(abc_path), "-o", str(midi_path)],
        capture_output=True,
        text=True,
    )

    warnings = []
    for line in (result.stdout + result.stderr).split("\n"):
        if "Warning" in line or "Error" in line:
            warnings.append(line.strip())

    return midi_path, warnings


def get_midi_bars(midi_path: Path) -> float:
    """Get the number of bars in a MIDI file."""
    mid = mido.MidiFile(midi_path)

    # Get total ticks across all tracks
    total_ticks = 0
    for track in mid.tracks:
        track_ticks = sum(msg.time for msg in track)
        total_ticks = max(total_ticks, track_ticks)

    # Calculate bars (4/4 time = 4 beats per bar)
    bars = total_ticks / mid.ticks_per_beat / 4
    return bars


class TestABCNotation(unittest.TestCase):
    """Test ABC notation produces correct MIDI timing."""

    def test_whole_note_c8(self):
        """C8 in L:1/8 = 8 eighth notes = 1 bar in 4/4."""
        abc = create_abc("C8 | C8 | C8 | C8 |")
        midi_path, warnings = abc_to_midi(abc)
        bars = get_midi_bars(midi_path)

        self.assertEqual(len(warnings), 0, f"Unexpected warnings: {warnings}")
        self.assertAlmostEqual(bars, 4.0, places=1, msg="C8 should be 1 bar each")

    def test_whole_rest_z8(self):
        """z8 in L:1/8 = 8 eighth rests = 1 bar in 4/4."""
        abc = create_abc("z8 | z8 | z8 | z8 |")
        midi_path, warnings = abc_to_midi(abc)
        bars = get_midi_bars(midi_path)

        self.assertEqual(len(warnings), 0, f"Unexpected warnings: {warnings}")
        self.assertAlmostEqual(bars, 4.0, places=1, msg="z8 should be 1 bar each")

    def test_half_notes_c4c4(self):
        """C4 C4 in L:1/8 = 4+4 eighth notes = 1 bar in 4/4."""
        abc = create_abc("C4 C4 | C4 C4 | C4 C4 | C4 C4 |")
        midi_path, warnings = abc_to_midi(abc)
        bars = get_midi_bars(midi_path)

        self.assertEqual(len(warnings), 0, f"Unexpected warnings: {warnings}")
        self.assertAlmostEqual(bars, 4.0, places=1, msg="C4 C4 should be 1 bar each")

    def test_quarter_notes_c2c2c2c2(self):
        """C2 C2 C2 C2 in L:1/8 = 2+2+2+2 eighth notes = 1 bar in 4/4."""
        abc = create_abc("C2 C2 C2 C2 | C2 C2 C2 C2 | C2 C2 C2 C2 | C2 C2 C2 C2 |")
        midi_path, warnings = abc_to_midi(abc)
        bars = get_midi_bars(midi_path)

        self.assertEqual(len(warnings), 0, f"Unexpected warnings: {warnings}")
        self.assertAlmostEqual(
            bars, 4.0, places=1, msg="C2 C2 C2 C2 should be 1 bar each"
        )

    def test_eighth_notes_cccccccc(self):
        """C C C C C C C C in L:1/8 = 8 eighth notes = 1 bar in 4/4."""
        abc = create_abc("C C C C C C C C | C C C C C C C C |")
        midi_path, warnings = abc_to_midi(abc)
        bars = get_midi_bars(midi_path)

        self.assertEqual(len(warnings), 0, f"Unexpected warnings: {warnings}")
        self.assertAlmostEqual(
            bars, 2.0, places=1, msg="8 eighth notes should be 1 bar"
        )

    def test_mixed_rhythm(self):
        """Mixed note values should sum correctly."""
        # D,4 A,4 = 4+4 = 8 eighths = 1 bar
        abc = create_abc("D,4 A,4 | D,4 A,4 | D,4 A,4 | D,4 A,4 |")
        midi_path, warnings = abc_to_midi(abc)
        bars = get_midi_bars(midi_path)

        self.assertEqual(len(warnings), 0, f"Unexpected warnings: {warnings}")
        self.assertAlmostEqual(bars, 4.0, places=1, msg="D,4 A,4 should be 1 bar each")

    def test_long_silence_single_line(self):
        """Many bars of silence on one line should count correctly."""
        abc = create_abc("C8 | z8 | z8 | z8 | z8 | z8 | z8 | z8 |")
        midi_path, warnings = abc_to_midi(abc)
        bars = get_midi_bars(midi_path)

        self.assertAlmostEqual(bars, 8.0, places=1, msg="8 bars should be 8 bars")

    def test_long_silence_multiple_lines(self):
        """Many bars of silence on multiple lines should count correctly."""
        abc = create_abc("""C8 |
z8 | z8 | z8 | z8 |
z8 | z8 | z8 |""")
        midi_path, warnings = abc_to_midi(abc)
        bars = get_midi_bars(midi_path)

        self.assertAlmostEqual(
            bars,
            8.0,
            places=1,
            msg="8 bars across multiple lines should still be 8 bars",
        )


class TestABCBarConsistency(unittest.TestCase):
    """Test that instruments with same notation produce same length MIDI."""

    def test_notes_vs_silence_same_length(self):
        """Bars with notes and bars with silence should have same duration."""
        # Both should be exactly 4 bars
        abc_notes = create_abc("C8 | C8 | C8 | C8 |", "Notes")
        abc_silence = create_abc("z8 | z8 | z8 | z8 |", "Silence")

        midi_notes, warn_notes = abc_to_midi(abc_notes)
        midi_silence, warn_silence = abc_to_midi(abc_silence)

        bars_notes = get_midi_bars(midi_notes)
        bars_silence = get_midi_bars(midi_silence)

        self.assertEqual(len(warn_notes), 0, f"Notes warnings: {warn_notes}")
        self.assertEqual(len(warn_silence), 0, f"Silence warnings: {warn_silence}")
        self.assertAlmostEqual(
            bars_notes,
            bars_silence,
            places=1,
            msg=f"Notes ({bars_notes}) and silence ({bars_silence}) should match",
        )

    def test_melodic_vs_sustained_same_length(self):
        """Melodic line and sustained note should have same bar count."""
        # Both should be 4 bars
        abc_melody = create_abc(
            "C2 D2 E2 F2 | G2 A2 B2 c2 | c2 B2 A2 G2 | F2 E2 D2 C2 |"
        )
        abc_sustain = create_abc("C8 | C8 | C8 | C8 |")

        midi_melody, _ = abc_to_midi(abc_melody)
        midi_sustain, _ = abc_to_midi(abc_sustain)

        bars_melody = get_midi_bars(midi_melody)
        bars_sustain = get_midi_bars(midi_sustain)

        self.assertAlmostEqual(
            bars_melody,
            bars_sustain,
            places=1,
            msg=f"Melody ({bars_melody}) and sustain ({bars_sustain}) should match",
        )


class TestProblemPatterns(unittest.TestCase):
    """Test specific patterns that caused issues in production."""

    def test_trailing_silence_no_extra_bar(self):
        """
        Instrument ending in silence should not have extra bars added.

        This is the actual bug we saw: bassoon had 137 bars while cello had 136.
        """
        # Cello-like: notes until the end
        abc_active = create_abc(
            """C8 | C8 | C8 | C8 |
C8 | C8 | C4 z4 | z8 |""",
            "Active",
        )

        # Bassoon-like: long trailing silence
        abc_silent = create_abc(
            """C8 | C8 | z8 | z8 |
z8 | z8 | z8 | z8 |""",
            "Silent",
        )

        midi_active, warn_active = abc_to_midi(abc_active)
        midi_silent, warn_silent = abc_to_midi(abc_silent)

        bars_active = get_midi_bars(midi_active)
        bars_silent = get_midi_bars(midi_silent)

        self.assertAlmostEqual(
            bars_active,
            8.0,
            places=1,
            msg=f"Active instrument should be 8 bars, got {bars_active}",
        )
        self.assertAlmostEqual(
            bars_silent,
            8.0,
            places=1,
            msg=f"Silent instrument should be 8 bars, got {bars_silent}",
        )
        self.assertAlmostEqual(
            bars_active,
            bars_silent,
            places=1,
            msg=f"Active ({bars_active}) and silent ({bars_silent}) should match",
        )

    def test_wrong_quarter_note_pattern_warns(self):
        """
        Pattern like 'e4 d4 c4 B,4' is WRONG in L:1/8.

        In L:1/8:
          - '4' means 4 eighth notes = half a bar
          - So 'e4 d4 c4 B,4' = 16 eighths = 2 bars, not 1

        abc2midi warns when it sees surrounding context that exposes the mismatch.
        """
        # Wrong pattern surrounded by correct bars - abc2midi will warn
        abc = create_abc("C8 | e4 d4 c4 B,4 | C8 |")
        midi_path, warnings = abc_to_midi(abc)

        # Should produce a warning about bar length mismatch
        self.assertTrue(
            len(warnings) > 0,
            "abc2midi should warn about 'e4 d4 c4 B,4' having wrong bar length",
        )

        # Total should be 4 bars (1 + 2 + 1) not 3
        bars = get_midi_bars(midi_path)
        self.assertAlmostEqual(
            bars,
            4.0,
            places=1,
            msg="C8 | e4 d4 c4 B,4 | C8 produces 4 bars (1+2+1) not 3",
        )

        # The bar should actually be 2 bars worth of content
        bars = get_midi_bars(midi_path)
        self.assertGreater(bars, 1.5, msg="e4 d4 c4 B,4 is actually 2 bars of content")

    def test_correct_quarter_note_pattern(self):
        """
        Correct quarter notes in L:1/8 use '2' not '4'.

        In L:1/8:
          - '2' means 2 eighth notes = quarter note
          - So 'e2 d2 c2 B,2' = 8 eighths = 1 bar
        """
        abc = create_abc("e2 d2 c2 B,2 | e2 d2 c2 B,2 |")
        midi_path, warnings = abc_to_midi(abc)
        bars = get_midi_bars(midi_path)

        self.assertEqual(len(warnings), 0, f"Should have no warnings: {warnings}")
        self.assertAlmostEqual(
            bars, 2.0, places=1, msg="e2 d2 c2 B,2 should be exactly 1 bar each"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
