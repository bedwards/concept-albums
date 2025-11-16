#!/usr/bin/env python3
"""
Build complete song ABC files from modular section files.

Usage:
    python build_song.py song-dir structure.yaml
"""

import sys
import yaml
from pathlib import Path
from abc_tools import count_bars, combine_sections, verify_song_consistency, print_validation_report


def build_song_from_sections(song_dir: Path, structure_file: Path):
    """
    Build all instrument files for a song from section files.
    
    structure.yaml format:
    title: "Song Title"
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
      # ... etc
    
    structure:
      - intro
      - verse
      - chorus
      - verse
      - chorus
      - break
      - bridge
      - verse
      - chorus
      - outro
    
    instruments:
      vocal:
        program: 53
      bass:
        program: 33
      # ... etc
    """
    
    # Load structure
    with open(structure_file) as f:
        config = yaml.safe_load(f)
    
    title = config['title']
    composer = config.get('composer', 'Brian Edwards')
    tempo = config['tempo']
    time_sig = config['time']
    key = config['key']
    
    sections_dir = song_dir / 'sections'
    sections_dir.mkdir(exist_ok=True)
    
    # Build each instrument
    instruments = config.get('instruments', {})
    structure = config['structure']
    
    for instrument_name, instrument_config in instruments.items():
        midi_program = instrument_config.get('program', 0)
        is_percussion = instrument_config.get('percussion', False)
        
        # Collect section files in order
        section_files = []
        for section_name in structure:
            section_file = sections_dir / f"{section_name}-{instrument_name}.abc"
            if section_file.exists():
                section_files.append((section_name, str(section_file)))
            else:
                print(f"Warning: Missing {section_file}")
        
        # Combine into full file
        output_file = song_dir / f"{instrument_name}.abc"
        combine_sections(
            section_files,
            output_file,
            title,
            composer,
            tempo,
            time_sig,
            key,
            instrument_name,
            midi_program,
            is_percussion
        )
        
        print(f"Built {output_file.name}")
    
    # Verify consistency
    print("\nVerifying consistency...")
    results = verify_song_consistency(song_dir)
    print_validation_report(results)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python build_song.py <song-dir> <structure.yaml>")
        sys.exit(1)
    
    song_dir = Path(sys.argv[1])
    structure_file = Path(sys.argv[2])
    
    if not song_dir.exists():
        print(f"Error: Song directory not found: {song_dir}")
        sys.exit(1)
    
    if not structure_file.exists():
        print(f"Error: Structure file not found: {structure_file}")
        sys.exit(1)
    
    build_song_from_sections(song_dir, structure_file)
