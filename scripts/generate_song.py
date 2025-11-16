#!/usr/bin/env python3
"""
Song Generator - Generate ALL song files from single source YAML

This script reads .source/song.yaml and generates:
- Complete ABC files for all instruments
- Lyrics files (YAML, TXT)
- Chords file (YAML, TXT)
- Arrangement file (TXT)
- Section ABC files
- Structure YAML
- MIDI files (via abc2midi)

Usage:
    python generate_song.py song-directory/
    
Directory structure:
    song-directory/
        .source/
            song.yaml          # HAND-WRITTEN: Single source of truth
        .generated/
            *.abc              # GENERATED: Complete ABC files
            *.mid              # GENERATED: MIDI files
            lyrics.yaml        # GENERATED
            chords.yaml        # GENERATED
            structure.yaml     # GENERATED
            sections/          # GENERATED: Individual section ABC files
        arrangement.txt        # GENERATED (human-readable)
        lyrics.txt             # GENERATED (human-readable)
        chords.txt             # GENERATED (human-readable)
"""

import sys
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List


def load_song_config(config_file: Path) -> Dict:
    """Load and validate song.yaml"""
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    # Validate required fields
    required = ['song', 'sections', 'instruments']
    for field in required:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
    
    return config


def generate_structure_yaml(config: Dict, output_file: Path):
    """Generate structure.yaml from config"""
    song = config['song']
    sections = config['sections']
    
    structure = {
        'title': song['title'],
        'composer': song['composer'],
        'tempo': song['tempo'],
        'time': song['time'],
        'key': song['key'],
        'sections': [
            {'name': name, 'bars': sections[name]['bars']}
            for name in set(song['structure'])  # Unique section names
        ],
        'structure': song['structure'],
        'instruments': config['instruments']
    }
    
    with open(output_file, 'w') as f:
        yaml.dump(structure, f, default_flow_style=False, sort_keys=False)
    
    print(f"Generated: {output_file.name}")


def generate_lyrics_yaml(config: Dict, output_file: Path):
    """Generate lyrics.yaml from config"""
    song_meta = config['song']
    sections = config['sections']
    
    lyrics = {
        'song': {
            'title': song_meta['title'],
            'composer': song_meta['composer']
        },
        'sections': {}
    }
    
    # Extract lyrics from each section
    for section_name, section_data in sections.items():
        if 'lyrics' in section_data:
            for lyric_section_name, lyric_lines in section_data['lyrics'].items():
                lyrics['sections'][lyric_section_name] = [
                    line['line'] for line in lyric_lines
                ]
    
    with open(output_file, 'w') as f:
        yaml.dump(lyrics, f, default_flow_style=False, sort_keys=False)
    
    print(f"Generated: {output_file.name}")


def generate_chords_yaml(config: Dict, output_file: Path):
    """Generate chords.yaml from config"""
    song_meta = config['song']
    sections = config['sections']
    
    chords = {
        'song': {
            'title': song_meta['title'],
            'composer': song_meta['composer'],
            'key': song_meta['key'],
            'tempo': song_meta['tempo'],
            'time': song_meta['time']
        },
        'sections': {}
    }
    
    # Extract chords and lyrics from each section
    for section_name, section_data in sections.items():
        if 'lyrics' in section_data:
            for lyric_section_name, lyric_lines in section_data['lyrics'].items():
                chords['sections'][lyric_section_name] = [
                    {'chords': line['chords'], 'lyrics': line['line']}
                    for line in lyric_lines
                ]
    
    with open(output_file, 'w') as f:
        yaml.dump(chords, f, default_flow_style=False, sort_keys=False)
    
    print(f"Generated: {output_file.name}")


def generate_section_abc_files(config: Dict, sections_dir: Path):
    """Generate individual section ABC files"""
    sections_dir.mkdir(exist_ok=True)
    
    sections = config['sections']
    song_meta = config['song']
    
    for section_name, section_data in sections.items():
        if 'instruments' not in section_data:
            continue
        
        for instrument, content in section_data['instruments'].items():
            # Handle regular instruments
            if instrument != 'drums':
                abc_content = f"""X:1
T:{song_meta['title']} - {section_name.title()} - {instrument.title()}
M:{song_meta['time']}
L:1/8
K:{song_meta['key']}
{content['abc']}
"""
                output_file = sections_dir / f"{section_name}-{instrument}.abc"
                output_file.write_text(abc_content)
            
            # Handle drums - create separate files for each drum instrument
            else:
                drums = content
                # All drum parts use middle C (c = MIDI note 60) for Bitwig single instrument
                drum_parts = {
                    'kick': {'note': 'c', 'midi_note': 60, 'name': 'Kick'},
                    'snare': {'note': 'c', 'midi_note': 60, 'name': 'Snare'},
                }
                
                # Add optional drum parts if they exist (all use c/C3/MIDI 60)
                if 'hihat' in drums:
                    drum_parts['hihat'] = {'note': 'c', 'midi_note': 60, 'name': 'Hi-Hat'}
                if 'crash' in drums:
                    drum_parts['crash'] = {'note': 'c', 'midi_note': 60, 'name': 'Crash'}
                if 'ride' in drums:
                    drum_parts['ride'] = {'note': 'c', 'midi_note': 60, 'name': 'Ride'}
                if 'tom1' in drums:
                    drum_parts['tom1'] = {'note': 'c', 'midi_note': 60, 'name': 'Tom 1'}
                if 'tom2' in drums:
                    drum_parts['tom2'] = {'note': 'c', 'midi_note': 60, 'name': 'Tom 2'}
                if 'tom3' in drums:
                    drum_parts['tom3'] = {'note': 'c', 'midi_note': 60, 'name': 'Tom 3'}
                
                for drum_key, drum_info in drum_parts.items():
                    if drum_key not in drums:
                        continue
                    
                    abc_content = f"""X:1
T:{song_meta['title']} - {section_name.title()} - {drum_info['name']}
M:{song_meta['time']}
L:1/8
K:C
%%MIDI channel 10
{drums[drum_key]}
"""
                    output_file = sections_dir / f"{section_name}-drum-{drum_key}.abc"
                    output_file.write_text(abc_content)
    
    print(f"Generated: {len(list(sections_dir.glob('*.abc')))} section files")


def generate_complete_abc_files(config: Dict, output_dir: Path, sections_dir: Path):
    """Generate complete ABC files from sections"""
    song_meta = config['song']
    structure = song_meta['structure']
    instruments_config = config['instruments']
    
    # For each instrument, combine sections
    for instrument, inst_config in instruments_config.items():
        is_percussion = inst_config.get('percussion', False)
        
        if is_percussion:
            # Generate separate files for each drum part
            drum_parts = ['kick', 'snare', 'hihat', 'crash', 'ride', 'tom1', 'tom2', 'tom3']
            drum_names = {
                'kick': 'Kick',
                'snare': 'Snare', 
                'hihat': 'Hi-Hat',
                'crash': 'Crash',
                'ride': 'Ride',
                'tom1': 'Tom 1',
                'tom2': 'Tom 2',
                'tom3': 'Tom 3'
            }
            
            for drum_part in drum_parts:
                music_parts = []
                has_content = False
                
                for section_name in structure:
                    section_file = sections_dir / f"{section_name}-drum-{drum_part}.abc"
                    
                    if section_file.exists():
                        has_content = True
                        content = section_file.read_text()
                        
                        # Extract just the music
                        lines = content.split('\n')
                        music = []
                        for line in lines:
                            if not line.startswith(('X:', 'T:', 'M:', 'L:', 'K:', '%%MIDI')):
                                if line.strip():
                                    music.append(line)
                        music_parts.append('\n'.join(music))
                
                # Only create file if we found content
                if has_content:
                    header = f"""X:1
T:{song_meta['title']} - {drum_names[drum_part]}
C:{song_meta['composer']}
M:{song_meta['time']}
L:1/8
Q:1/4={song_meta['tempo']}
K:C
%%MIDI channel 10
"""
                    full_content = header + '\n'.join(music_parts)
                    
                    output_file = output_dir / f"drum-{drum_part}.abc"
                    output_file.write_text(full_content)
                    print(f"Generated: {output_file.name}")
        else:
            # Regular instrument
            header = f"""X:1
T:{song_meta['title']}
C:{song_meta['composer']}
M:{song_meta['time']}
L:1/8
Q:1/4={song_meta['tempo']}
K:{song_meta['key']}
V:1
%%MIDI program {inst_config['program']}
"""
            
            # Collect sections
            music_parts = []
            
            for section_name in structure:
                section_file = sections_dir / f"{section_name}-{instrument}.abc"
                
                if section_file.exists():
                    content = section_file.read_text()
                    
                    # Extract just the music
                    lines = content.split('\n')
                    music = []
                    for line in lines:
                        if not line.startswith(('X:', 'T:', 'M:', 'L:', 'K:', 'V:')):
                            if line.strip():
                                music.append(line)
                    music_parts.append('\n'.join(music))
            
            # Write complete file
            full_content = header + '\n'.join(music_parts)
            
            output_file = output_dir / f"{instrument}.abc"
            output_file.write_text(full_content)
            print(f"Generated: {output_file.name}")


def generate_text_files(config: Dict, song_dir: Path):
    """Generate human-readable text files"""
    
    # lyrics.txt
    lyrics_lines = ["# LYRICS\n"]
    sections = config['sections']
    for section_name in config['song']['structure']:
        if section_name in sections and 'lyrics' in sections[section_name]:
            for lyric_name, lyric_data in sections[section_name]['lyrics'].items():
                lyrics_lines.append(f"\n{lyric_name.upper()}")
                for line in lyric_data:
                    lyrics_lines.append(line['line'])
    
    (song_dir / 'lyrics.txt').write_text('\n'.join(lyrics_lines))
    print("Generated: lyrics.txt")
    
    # chords.txt
    chords_lines = ["# CHORDS\n"]
    for section_name in config['song']['structure']:
        if section_name in sections and 'lyrics' in sections[section_name]:
            for lyric_name, lyric_data in sections[section_name]['lyrics'].items():
                chords_lines.append(f"\n{lyric_name.upper()}")
                for line in lyric_data:
                    chords_str = "  ".join(line['chords'])
                    chords_lines.append(chords_str)
                    chords_lines.append(line['line'])
    
    (song_dir / 'chords.txt').write_text('\n'.join(chords_lines))
    print("Generated: chords.txt")
    
    # arrangement.txt
    if 'arrangement' in config:
        arr_lines = [
            f"TEMPO: {config['song']['tempo']} bpm",
            f"TIME: {config['song']['time']}",
            f"KEY: {config['song']['key']}\n"
        ]
        for section, notes in config['arrangement'].items():
            arr_lines.append(f"{section.upper()}")
            arr_lines.append(notes)
        
        (song_dir / 'arrangement.txt').write_text('\n'.join(arr_lines))
        print("Generated: arrangement.txt")


def generate_midi_files(output_dir: Path):
    """Generate MIDI files from ABC files"""
    abc_files = list(output_dir.glob('*.abc'))
    
    for abc_file in abc_files:
        mid_file = abc_file.with_suffix('.mid')
        try:
            result = subprocess.run(
                ['abc2midi', str(abc_file), '-o', str(mid_file)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"Generated: {mid_file.name}")
            else:
                print(f"Warning: Failed to generate {mid_file.name}")
                if result.stderr:
                    print(f"  {result.stderr[:200]}")
        except FileNotFoundError:
            print("Warning: abc2midi not found - skipping MIDI generation")
            return
        except Exception as e:
            print(f"Warning: Error generating {mid_file.name}: {e}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate song files from source YAML')
    parser.add_argument('song_dir', type=Path, help='Song directory')
    parser.add_argument('--skip-midi', action='store_true', help='Skip MIDI generation')
    
    args = parser.parse_args()
    
    song_dir = args.song_dir
    source_dir = song_dir / '.source'
    generated_dir = song_dir / '.generated'
    
    # Check for source file
    config_file = source_dir / 'song.yaml'
    if not config_file.exists():
        print(f"Error: {config_file} not found")
        print(f"Expected hand-written source file at: {config_file}")
        return 1
    
    # Load config
    print(f"\nLoading configuration from {config_file}...")
    config = load_song_config(config_file)
    
    # Create output directories
    generated_dir.mkdir(exist_ok=True)
    sections_dir = generated_dir / 'sections'
    sections_dir.mkdir(exist_ok=True)
    
    print(f"\n{'='*70}")
    print(f"Generating song: {config['song']['title']}")
    print(f"{'='*70}\n")
    
    # Generate all files
    generate_structure_yaml(config, generated_dir / 'structure.yaml')
    generate_lyrics_yaml(config, generated_dir / 'lyrics.yaml')
    generate_chords_yaml(config, generated_dir / 'chords.yaml')
    generate_section_abc_files(config, sections_dir)
    generate_complete_abc_files(config, generated_dir, sections_dir)
    generate_text_files(config, song_dir)
    
    if not args.skip_midi:
        print()
        generate_midi_files(generated_dir)
    
    print(f"\n{'='*70}")
    print("✅ Generation complete!")
    print(f"{'='*70}")
    print(f"\nSource (hand-written):  {source_dir}/")
    print(f"Generated (do not edit): {generated_dir}/")
    print(f"Human-readable:          {song_dir}/*.txt")
    

if __name__ == '__main__':
    sys.exit(main() or 0)
