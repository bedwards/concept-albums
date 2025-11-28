#!/usr/bin/env python3
"""
ABC Notation Tools for Song Construction and Validation

Provides utilities to:
- Count bars in ABC files
- Validate ABC files with abc2midi
- Combine section ABC files into complete songs
- Verify all instruments have matching bar counts
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any


class ABCSection:
    """Represents a section of a song (intro, verse, chorus, etc.)"""
    
    def __init__(self, name: str, bars: int, has_vocals: bool = True):
        self.name = name
        self.bars = bars
        self.has_vocals = has_vocals
        self.instruments = {}  # instrument_name -> abc_content
    
    def add_instrument(self, instrument: str, content: str):
        """Add ABC content for an instrument in this section"""
        self.instruments[instrument] = content
    
    def validate_bars(self) -> Dict[str, int]:
        """Count bars in each instrument part"""
        bar_counts = {}
        for instrument, content in self.instruments.items():
            bar_counts[instrument] = count_bars(content)
        return bar_counts


def count_bars(abc_content: str) -> int:
    """
    Count the number of bars in ABC notation content.
    Handles multi-bar lines correctly.
    For multi-voice files (e.g. drums), counts only the first voice.
    """
    lines = abc_content.split('\n')
    music_lines = []
    in_first_voice = True
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip headers, lyrics, comments
        if line.startswith(('X:', 'T:', 'C:', 'M:', 'L:', 'Q:', 'K:', 'w:', '%')):
            if not line.startswith('%%'):  # Keep %%MIDI lines for context
                continue
        
        # Detect voice changes - only count first voice
        if line.startswith('V:'):
            if line.startswith('V:1'):
                in_first_voice = True
            else:
                in_first_voice = False
            continue
        
        if line.startswith('%%MIDI'):
            continue
        
        # Only add lines from first voice (or single-voice files)
        if in_first_voice:
            music_lines.append(line)
    
    music_content = '\n'.join(music_lines)
    
    # Count pipe symbols
    bar_count = 0
    bar_count += music_content.count('|')
    
    # Subtract special markers that aren't bar lines
    bar_count -= music_content.count('|:')
    bar_count -= music_content.count(':|')
    bar_count -= music_content.count('|]')
    
    # The final bar before |] counts as 1 bar
    if '|]' in music_content:
        bar_count += 1
    
    return bar_count


def validate_abc_file(filepath: Path) -> Tuple[bool, str]:
    """
    Validate an ABC file using abc2midi.
    Returns (success, message)
    """
    try:
        result = subprocess.run(
            ['abc2midi', str(filepath), '-o', '/tmp/test.mid'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Check for errors (not warnings)
        if 'Error' in result.stderr:
            return False, result.stderr
        
        # Check for timing errors (bar length mismatches)
        if 'Bar' in result.stderr and 'time units' in result.stderr:
            return False, result.stderr
        
        return True, "Valid ABC file"
        
    except subprocess.TimeoutExpired:
        return False, "abc2midi timed out"
    except FileNotFoundError:
        return False, "abc2midi not found - please install abcmidi package"
    except Exception as e:
        return False, f"Error: {str(e)}"


def read_section_file(filepath: Path) -> str:
    """Read a section ABC file and return just the music content"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract just the music lines (after K: header, before any w: lyrics if present)
    lines = content.split('\n')
    music_lines = []
    in_music = False
    
    for line in lines:
        if line.startswith('K:'):
            in_music = True
            continue
        if in_music and line.strip():
            if not line.startswith(('X:', 'T:', 'C:', 'M:', 'L:', 'Q:', 'V:', '%%')):
                music_lines.append(line)
    
    return '\n'.join(music_lines)


def combine_sections(
    sections: List[Tuple[str, str]],
    output_file: Path,
    title: str,
    composer: str = "Brian Edwards",
    tempo: int = 88,
    time_sig: str = "4/4",
    key: str = "Cmin",
    instrument: str = "vocal",
    midi_program: int = 53,
    is_percussion: bool = False
) -> str:
    """
    Combine multiple section files into a complete ABC file.
    
    sections: List of (section_name, filepath) tuples
    is_percussion: True for drums (multi-voice with percussion key)
    Returns: complete ABC content
    """
    if is_percussion:
        # Drums need special multi-voice header
        header = f"""X:1
T:{title} - Drums  
C:{composer}
M:{time_sig}
L:1/8
Q:1/4={tempo}
K:C perc
V:1 name="Kick"
%%MIDI program 128
%%MIDI channel 10
"""
    else:
        header = f"""X:1
T:{title}
C:{composer}
M:{time_sig}
L:1/8
Q:1/4={tempo}
K:{key}
V:1
%%MIDI program {midi_program}
"""
    
    # Read all section files and organize by voice
    voice1_parts = []  # Kick drum or main voice
    voice2_parts = []  # Snare drum (if percussion)
    
    for section_name, section_file in sections:
        if Path(section_file).exists():
            content = Path(section_file).read_text()
            
            if is_percussion:
                # Parse multi-voice content
                lines = content.split('\n')
                v1_music = []
                v2_music = []
                current_voice = 1
                
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith(('X:', 'T:', 'C:', 'M:', 'L:', 'Q:', 'K:', '%')):
                        continue
                    if line.startswith('V:2'):
                        current_voice = 2
                        continue
                    if line.startswith('V:1'):
                        current_voice = 1
                        continue
                    if line.startswith('%%MIDI'):
                        continue
                        
                    if current_voice == 1:
                        v1_music.append(line)
                    elif current_voice == 2:
                        v2_music.append(line)
                
                if v1_music:
                    voice1_parts.append('\n'.join(v1_music))
                if v2_music:
                    voice2_parts.append('\n'.join(v2_music))
            else:
                # Single voice - extract music content
                music = read_section_file(Path(section_file))
                voice1_parts.append(music)
        else:
            print(f"Warning: Section file not found: {section_file}")
    
    # Combine all parts
    if is_percussion:
        # Build Voice 1 (Kick)
        full_content = header + '\n'.join(voice1_parts)
        
        # Add Voice 2 (Snare)
        if voice2_parts:
            full_content += '\nV:2 name="Snare"\n%%MIDI program 128\n%%MIDI channel 10\n'
            full_content += '\n'.join(voice2_parts)
    else:
        full_content = header + '\n'.join(voice1_parts)
    
    # Write output
    output_file.write_text(full_content)
    
    return full_content


def verify_song_consistency(song_dir: Path) -> Dict[str, Any]:
    """
    Verify all instrument ABC files in a song directory have the same bar count.
    Returns a dict with validation results.
    """
    abc_files = list(song_dir.glob('*.abc'))
    
    if not abc_files:
        return {'error': 'No ABC files found'}
    
    results = {
        'song_dir': song_dir.name,
        'files': {},
        'all_match': False,
        'bar_counts': {}
    }
    
    for abc_file in abc_files:
        content = abc_file.read_text()
        bar_count = count_bars(content)
        valid, msg = validate_abc_file(abc_file)
        
        results['files'][abc_file.name] = {
            'bars': bar_count,
            'valid': valid,
            'message': msg if not valid else 'OK'
        }
        results['bar_counts'][abc_file.name] = bar_count
    
    # Check if all bar counts match
    bar_counts = list(results['bar_counts'].values())
    results['all_match'] = len(set(bar_counts)) == 1
    results['expected_bars'] = bar_counts[0] if bar_counts else 0
    
    return results


def print_validation_report(results: Dict):
    """Print a formatted validation report"""
    print(f"\n{'='*60}")
    print(f"Song: {results['song_dir']}")
    print(f"{'='*60}")
    
    for filename, info in results['files'].items():
        status = '✓' if info['valid'] else '✗'
        bars = info['bars']
        msg = info['message']
        print(f"{status} {filename:30s} {bars:3d} bars  {msg}")
    
    print(f"{'-'*60}")
    
    if results['all_match']:
        print(f"✓ All files match: {results['expected_bars']} bars")
    else:
        bar_counts = results['bar_counts']
        unique_counts = set(bar_counts.values())
        print(f"✗ Bar count mismatch! Found: {unique_counts}")
        print(f"  Expected: all files should have the same bar count")
    
    print(f"{'='*60}\n")


if __name__ == '__main__':
    # CLI interface
    import argparse
    
    parser = argparse.ArgumentParser(description='ABC Notation Tools')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Count bars command
    count_parser = subparsers.add_parser('count', help='Count bars in ABC file')
    count_parser.add_argument('file', type=Path, help='ABC file to count')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate ABC file')
    validate_parser.add_argument('file', type=Path, help='ABC file to validate')
    
    # Verify song command
    verify_parser = subparsers.add_parser('verify', help='Verify all instruments in a song')
    verify_parser.add_argument('song_dir', type=Path, help='Song directory')
    
    args = parser.parse_args()
    
    if args.command == 'count':
        content = args.file.read_text()
        bars = count_bars(content)
        print(f"{args.file.name}: {bars} bars")
    
    elif args.command == 'validate':
        valid, msg = validate_abc_file(args.file)
        print(f"{args.file.name}: {'✓ VALID' if valid else '✗ INVALID'}")
        if not valid:
            print(msg)
    
    elif args.command == 'verify':
        results = verify_song_consistency(args.song_dir)
        print_validation_report(results)
    
    else:
        parser.print_help()
