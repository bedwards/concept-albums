#!/usr/bin/env python3
"""
Verify all MIDI files for a movement have the same duration.

Usage:
    python verify_midi_lengths.py axiom-digital-age/01-axiom/
"""

import sys
import mido
from pathlib import Path


def check_midi_lengths(movement_dir: str):
    """Check all MIDI files in a movement have the same length"""
    midi_dir = Path(movement_dir) / "midi"

    if not midi_dir.exists():
        print(f"Error: {midi_dir} does not exist")
        return False

    files_data = []

    for midi_file in sorted(midi_dir.glob("*.mid")):
        mid = mido.MidiFile(midi_file)

        # Get tempo
        tempo = 500000  # default (120 BPM)
        for track in mid.tracks:
            for msg in track:
                if msg.type == "set_tempo":
                    tempo = msg.tempo
                    break

        # Get total length in ticks
        total_ticks = 0
        for track in mid.tracks:
            track_ticks = sum(msg.time for msg in track)
            total_ticks = max(total_ticks, track_ticks)

        bpm = 60000000 / tempo
        tpb = mid.ticks_per_beat

        # Calculate bars in 4/4 time
        beats = total_ticks / tpb
        bars = beats / 4

        files_data.append((midi_file.name, tpb, bpm, total_ticks, bars))

    # Find min and max
    min_file = min(files_data, key=lambda x: x[3])
    max_file = max(files_data, key=lambda x: x[3])

    print(f"\nMovement: {movement_dir}")
    print(f"{'File':<20} {'Ticks/Beat':>12} {'BPM':>8} {'Total Ticks':>12} {'Bars':>8}")
    print("-" * 70)

    for name, tpb, bpm, ticks, bars in sorted(files_data, key=lambda x: x[3]):
        marker = ""
        if name == min_file[0]:
            marker = " ← SHORTEST"
        elif name == max_file[0]:
            marker = " ← LONGEST"
        print(f"{name:<20} {tpb:>12} {bpm:>8.1f} {ticks:>12} {bars:>8.1f}{marker}")

    print("\n" + "=" * 70)

    if min_file[3] == max_file[3]:
        print(f"✓ ALL FILES SAME LENGTH: {min_file[4]:.1f} bars")
        return True
    else:
        print(f"✗ LENGTH MISMATCH:")
        print(f"  Shortest: {min_file[0]} = {min_file[4]:.1f} bars")
        print(f"  Longest:  {max_file[0]} = {max_file[4]:.1f} bars")
        print(f"  Difference: {max_file[4] - min_file[4]:.1f} bars")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_midi_lengths.py <movement-directory>")
        sys.exit(1)

    success = check_midi_lengths(sys.argv[1])
    sys.exit(0 if success else 1)
