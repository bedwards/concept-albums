#!/usr/bin/env python3
"""
Lyrics validation and consistency checking tools.

Ensures lyrics are consistent across:
- lyrics.yaml (structured lyrics only)
- chords.yaml (chords + lyrics)
- vocal ABC files (ABC notation with w: lyrics lines)
"""

import sys
import yaml
import re
from pathlib import Path
from typing import List, Dict, Tuple


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison.
    - Lowercase
    - Remove extra whitespace
    - Remove punctuation
    - Remove hyphens (used for syllable breaks in ABC)
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)     # Normalize whitespace
    return text.strip()


def extract_lyrics_from_yaml(yaml_file: Path) -> Dict[str, List[str]]:
    """
    Extract lyrics from lyrics.yaml or chords.yaml.
    
    Returns: dict of section_name -> list of lyric lines
    """
    with open(yaml_file) as f:
        data = yaml.safe_load(f)
    
    sections = {}
    
    if 'sections' in data:
        for section_name, content in data['sections'].items():
            if isinstance(content, list) and len(content) > 0:
                # Check first item type
                if isinstance(content[0], dict) and 'lyrics' in content[0]:
                    # chords.yaml format: list of {chords, lyrics} dicts
                    sections[section_name] = [line['lyrics'] for line in content]
                elif isinstance(content[0], str):
                    # lyrics.yaml format: list of strings
                    sections[section_name] = content
    
    return sections


def extract_lyrics_from_abc(abc_file: Path) -> List[str]:
    """
    Extract lyrics from ABC vocal file (lines starting with w:).
    
    Returns: list of lyric lines (joined from syllables)
    """
    lyrics_lines = []
    
    with open(abc_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith('w:'):
                # Remove 'w:' prefix and syllable hyphens
                lyric = line[2:].strip()
                # Join syllables (remove spaces between hyphens)
                lyric = re.sub(r'-\s+', '', lyric)
                lyrics_lines.append(lyric)
    
    return lyrics_lines


def compare_lyrics(
    source1: Dict[str, List[str]],
    source2: Dict[str, List[str]],
    source1_name: str,
    source2_name: str
) -> Tuple[bool, List[str]]:
    """
    Compare lyrics from two sources.
    
    Returns: (all_match, list_of_differences)
    """
    all_match = True
    differences = []
    
    # Check all sections in source1
    for section, lines1 in source1.items():
        if section not in source2:
            all_match = False
            differences.append(f"Section '{section}' in {source1_name} but not in {source2_name}")
            continue
        
        lines2 = source2[section]
        
        if len(lines1) != len(lines2):
            all_match = False
            differences.append(
                f"Section '{section}': {source1_name} has {len(lines1)} lines, "
                f"{source2_name} has {len(lines2)} lines"
            )
            continue
        
        for i, (line1, line2) in enumerate(zip(lines1, lines2), 1):
            norm1 = normalize_text(line1)
            norm2 = normalize_text(line2)
            
            if norm1 != norm2:
                all_match = False
                differences.append(
                    f"Section '{section}', line {i}:\n"
                    f"  {source1_name}: {line1}\n"
                    f"  {source2_name}: {line2}"
                )
    
    # Check for sections in source2 but not in source1
    for section in source2:
        if section not in source1:
            all_match = False
            differences.append(f"Section '{section}' in {source2_name} but not in {source1_name}")
    
    return all_match, differences


def validate_song_lyrics(song_dir: Path) -> Dict:
    """
    Validate lyrics consistency across all files in a song directory.
    
    Checks:
    - lyrics.yaml exists and is valid
    - chords.yaml exists and lyrics match lyrics.yaml
    - vocal ABC files have lyrics matching lyrics.yaml
    
    Returns validation results.
    """
    results = {
        'song_dir': song_dir.name,
        'all_valid': True,
        'files_checked': [],
        'errors': []
    }
    
    lyrics_yaml = song_dir / 'lyrics.yaml'
    chords_yaml = song_dir / 'chords.yaml'
    
    # Load lyrics.yaml (primary source of truth)
    if not lyrics_yaml.exists():
        results['all_valid'] = False
        results['errors'].append(f"lyrics.yaml not found in {song_dir}")
        return results
    
    try:
        lyrics_data = extract_lyrics_from_yaml(lyrics_yaml)
        results['files_checked'].append('lyrics.yaml')
    except Exception as e:
        results['all_valid'] = False
        results['errors'].append(f"Error reading lyrics.yaml: {e}")
        return results
    
    # Check chords.yaml if it exists
    if chords_yaml.exists():
        try:
            chords_data = extract_lyrics_from_yaml(chords_yaml)
            results['files_checked'].append('chords.yaml')
            
            all_match, differences = compare_lyrics(
                lyrics_data, chords_data,
                'lyrics.yaml', 'chords.yaml'
            )
            
            if not all_match:
                results['all_valid'] = False
                results['errors'].extend(differences)
        except Exception as e:
            results['all_valid'] = False
            results['errors'].append(f"Error reading chords.yaml: {e}")
    
    return results


def print_validation_results(results: Dict):
    """Print formatted validation results"""
    print(f"\n{'='*70}")
    print(f"Lyrics Validation: {results['song_dir']}")
    print(f"{'='*70}")
    
    print(f"Files checked: {', '.join(results['files_checked'])}")
    
    if results['errors']:
        print(f"\n{'='*70}")
        print(f"ERRORS ({len(results['errors'])}):")
        print(f"{'='*70}")
        for error in results['errors']:
            print(f"\n{error}")
    
    print(f"\n{'='*70}")
    if results['all_valid']:
        print("✅ All lyrics are consistent!")
    else:
        print(f"❌ Found {len(results['errors'])} inconsistencies")
    print(f"{'='*70}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Lyrics Validation Tools')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Validate lyrics command
    validate_parser = subparsers.add_parser('validate', help='Validate song lyrics')
    validate_parser.add_argument('song_dir', type=Path, help='Song directory')
    
    args = parser.parse_args()
    
    if args.command == 'validate':
        results = validate_song_lyrics(args.song_dir)
        print_validation_results(results)
        sys.exit(0 if results['all_valid'] else 1)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
