#!/usr/bin/env python3
"""
Song Generator - Generate ALL song files from single source YAML

This script reads song.yaml and generates:
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
        song.yaml              # HAND-WRITTEN: Single source of truth
        lyrics.txt             # GENERATED (human-readable)
        chords.txt             # GENERATED (human-readable)
        arrangement.txt        # GENERATED (human-readable)
        README.md              # GENERATED documentation
        midi/                  # GENERATED: MIDI files for DAW import
            *.mid
        .generated/            # GENERATED: Intermediate build files
            *.abc              # Complete ABC files
            *.mid              # MIDI files
            lyrics.yaml        # Structured lyrics
            chords.yaml        # Structured chords
            structure.yaml     # Structure definition
            sections/          # Individual section ABC files
"""

import sys
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

# Optional: mido for MIDI post-processing (articulations, automation)
try:
    import mido
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False


def load_plugin_controls(plugins_dir: Path) -> Dict:
    """Load plugin control database"""
    controls_file = plugins_dir / 'controls.yaml'
    if controls_file.exists():
        with open(controls_file) as f:
            return yaml.safe_load(f)
    return {}


def get_keyswitch_note(plugin_controls: Dict, plugin_name: str, articulation: str) -> Optional[int]:
    """Get MIDI note number for a keyswitch articulation"""
    if plugin_name not in plugin_controls:
        return None
    plugin = plugin_controls[plugin_name]
    if 'keyswitches' not in plugin:
        return None
    keyswitches = plugin['keyswitches']
    if articulation in keyswitches:
        return keyswitches[articulation].get('note')
    return None


def inject_midi_controls(midi_file: Path, plugin_controls: Dict, instrument_config: Dict,
                         section_config: Optional[Dict] = None) -> bool:
    """Inject keyswitches and CC automation into MIDI file

    Args:
        midi_file: Path to MIDI file to modify
        plugin_controls: Loaded plugin control database
        instrument_config: Instrument config from song.yaml (has 'plugin', 'articulation')
        section_config: Optional section-specific config (can override articulation)

    Returns:
        True if modifications were made
    """
    if not MIDO_AVAILABLE:
        return False

    plugin_name = instrument_config.get('plugin')
    if not plugin_name:
        return False

    # Determine articulation (section overrides instrument default)
    articulation = None
    if section_config:
        articulation = section_config.get('articulation')
    if not articulation:
        articulation = instrument_config.get('articulation')

    # Get automation config (from instrument or section level)
    automation = instrument_config.get('automation', [])
    if section_config and 'automation' in section_config:
        automation = automation + section_config['automation']

    # Nothing to do?
    if not articulation and not automation:
        return False

    try:
        mid = mido.MidiFile(str(midi_file))
    except Exception as e:
        print(f"Warning: Could not read {midi_file}: {e}")
        return False

    modified = False
    ticks_per_beat = mid.ticks_per_beat

    # Find the main track (usually track 0 or 1)
    track_idx = 0 if len(mid.tracks) == 1 else 1
    track = mid.tracks[track_idx]

    # Collect existing messages with absolute times
    abs_messages = []
    abs_time = 0
    for msg in track:
        abs_time += msg.time
        abs_messages.append((abs_time, msg))

    new_messages = []

    # 1. Inject keyswitch at the start
    if articulation:
        keyswitch_note = get_keyswitch_note(plugin_controls, plugin_name, articulation)
        if keyswitch_note:
            # Add keyswitch note at time 0 (very short duration)
            new_messages.append((0, mido.Message('note_on', note=keyswitch_note, velocity=100, time=0)))
            new_messages.append((10, mido.Message('note_off', note=keyswitch_note, velocity=0, time=0)))
            modified = True
            print(f"  Injected keyswitch: {articulation} (note {keyswitch_note})")

    # 2. Inject CC automation
    for auto in automation:
        cc_num = auto.get('cc')
        values = auto.get('values', [])  # List of [beat, value] pairs

        if cc_num is None or not values:
            continue

        for beat, value in values:
            tick = int(beat * ticks_per_beat)
            new_messages.append((tick, mido.Message('control_change', control=cc_num, value=value, time=0)))
            modified = True

        print(f"  Injected CC{cc_num} automation: {len(values)} points")

    if not modified:
        return False

    # Merge new messages with existing
    all_messages = abs_messages + new_messages
    all_messages.sort(key=lambda x: (x[0], 0 if x[1].type.startswith('note') else 1))

    # Convert back to delta time
    new_track = mido.MidiTrack()
    prev_time = 0
    for abs_t, msg in all_messages:
        delta = abs_t - prev_time
        new_track.append(msg.copy(time=delta))
        prev_time = abs_t

    mid.tracks[track_idx] = new_track
    mid.save(str(midi_file))

    return True


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
%%MIDI program {inst_config['program']}
%%MIDI chordprog -1
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
                                # Remove chord symbols (e.g., "Cm", "F") from the line
                                import re
                                line_no_chords = re.sub(r'"[A-G][#b]?[^"]*"', '', line)
                                music.append(line_no_chords)
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


def generate_midi_files(output_dir: Path, song_dir: Path, config: Dict, plugin_controls: Dict):
    """Generate MIDI files from ABC files, inject plugin controls, and copy to midi/"""
    abc_files = list(output_dir.glob('*.abc'))

    # Create midi subdirectory in song root for easy import
    midi_dir = song_dir / 'midi'
    midi_dir.mkdir(exist_ok=True)

    instruments_config = config.get('instruments', {})
    sections_config = config.get('sections', {})

    # Merge section-level automation into instrument config
    for section_name, section_data in sections_config.items():
        if 'instruments' not in section_data:
            continue
        for inst_name, inst_section in section_data['instruments'].items():
            if inst_name in instruments_config:
                # Copy section-level articulation and automation to instrument
                if 'articulation' in inst_section and 'articulation' not in instruments_config[inst_name]:
                    instruments_config[inst_name]['articulation'] = inst_section['articulation']
                if 'automation' in inst_section:
                    if 'automation' not in instruments_config[inst_name]:
                        instruments_config[inst_name]['automation'] = []
                    instruments_config[inst_name]['automation'].extend(inst_section['automation'])

    for abc_file in abc_files:
        mid_file = abc_file.with_suffix('.mid')
        instrument_name = abc_file.stem  # e.g., 'guitar', 'bass', 'alto-sax'

        try:
            result = subprocess.run(
                ['abc2midi', str(abc_file), '-o', str(mid_file)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"Generated: {mid_file.name}")

                # Inject plugin controls (keyswitches, CC automation)
                if instrument_name in instruments_config:
                    inst_config = instruments_config[instrument_name]
                    if inject_midi_controls(mid_file, plugin_controls, inst_config):
                        print(f"  Applied plugin controls for {instrument_name}")

                # Copy to song root midi/ subdirectory for easy DAW import
                import shutil
                midi_copy = midi_dir / mid_file.name
                shutil.copy2(mid_file, midi_copy)
            else:
                print(f"Warning: Failed to generate {mid_file.name}")
                if result.stderr:
                    print(f"  {result.stderr[:200]}")
        except FileNotFoundError:
            print("Warning: abc2midi not found - skipping MIDI generation")
            return
        except Exception as e:
            print(f"Warning: Error generating {mid_file.name}: {e}")

    # Print summary
    midi_count = len(list(midi_dir.glob('*.mid')))
    if midi_count > 0:
        print(f"\n✓ {midi_count} MIDI files ready in midi/ for DAW import")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate song files from source YAML')
    parser.add_argument('song_dir', type=Path, help='Song directory')
    parser.add_argument('--skip-midi', action='store_true', help='Skip MIDI generation')

    args = parser.parse_args()

    song_dir = args.song_dir
    generated_dir = song_dir / '.generated'

    # Check for source file (new location: song root)
    config_file = song_dir / 'song.yaml'
    if not config_file.exists():
        print(f"Error: {config_file} not found")
        print(f"Expected hand-written source file at: {config_file}")
        return 1

    # Load config
    print(f"\nLoading configuration from {config_file}...")
    config = load_song_config(config_file)

    # Load plugin controls database (from concept-albums root)
    scripts_dir = Path(__file__).parent
    plugins_dir = scripts_dir.parent / 'plugins'
    plugin_controls = load_plugin_controls(plugins_dir)
    if plugin_controls:
        print(f"Loaded plugin controls: {', '.join(plugin_controls.keys())}")

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
        generate_midi_files(generated_dir, song_dir, config, plugin_controls)

    print(f"\n{'='*70}")
    print("✅ Generation complete!")
    print(f"{'='*70}")
    print(f"\nSource (hand-written):   {song_dir}/song.yaml")
    print(f"Generated (do not edit): {generated_dir}/")
    print(f"Human-readable:          {song_dir}/*.txt")
    print(f"MIDI files for DAW:      {song_dir}/midi/")
    

if __name__ == '__main__':
    sys.exit(main() or 0)
