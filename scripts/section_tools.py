#!/usr/bin/env python3
"""
Section Management Tools for ABC Song Construction

This tool helps create and validate section ABC files, ensuring they have
exactly the correct number of bars as defined in the structure.yaml file.

Usage:
    # Create a template for a section
    python section_tools.py template structure.yaml intro bass
    
    # Validate a section file has correct bar count
    python section_tools.py validate structure.yaml intro bass sections/intro-bass.abc
    
    # Validate all sections for a song
    python section_tools.py validate-all song-dir
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from abc_tools import count_bars


class SectionSpec:
    """Specification for a song section from structure.yaml"""
    
    def __init__(self, name: str, bars: int):
        self.name = name
        self.bars = bars
    
    def __repr__(self):
        return f"Section({self.name}, {self.bars} bars)"


class SongStructure:
    """Parse and manage song structure from YAML"""
    
    def __init__(self, structure_file: Path):
        with open(structure_file) as f:
            self.config = yaml.safe_load(f)
        
        self.title = self.config['title']
        self.composer = self.config.get('composer', 'Brian Edwards')
        self.tempo = self.config['tempo']
        self.time_sig = self.config['time']
        self.key = self.config['key']
        self.instruments = self.config.get('instruments', {})
        
        # Parse structure - count bars for each unique section type
        self.section_specs = self._parse_sections()
        self.structure_order = self.config['structure']
    
    def _parse_sections(self) -> Dict[str, SectionSpec]:
        """
        Parse the structure to determine bar counts for each section type.
        
        For now, we use a default mapping. In the future, this could be
        specified explicitly in the YAML.
        """
        # Default bar counts for common section types
        defaults = {
            'intro': 4,
            'verse': 8,
            'chorus': 8,
            'bridge': 4,
            'break': 4,
            'outro': 5,
            'instrumental': 4,
            'solo': 8,
        }
        
        # Check if sections are explicitly defined in YAML
        if 'sections' in self.config:
            specs = {}
            for section in self.config['sections']:
                name = section['name']
                bars = section['bars']
                specs[name] = SectionSpec(name, bars)
            return specs
        
        # Otherwise use defaults
        section_names = set(self.config['structure'])
        return {name: SectionSpec(name, defaults.get(name, 8)) 
                for name in section_names}
    
    def get_section_bars(self, section_name: str) -> int:
        """Get expected bar count for a section"""
        if section_name in self.section_specs:
            return self.section_specs[section_name].bars
        raise ValueError(f"Unknown section: {section_name}")
    
    def get_instruments(self) -> List[str]:
        """Get list of instrument names"""
        return list(self.instruments.keys())
    
    def is_percussion(self, instrument: str) -> bool:
        """Check if an instrument is percussion (multi-voice)"""
        return self.instruments.get(instrument, {}).get('percussion', False)


def create_section_template(
    song_structure: SongStructure,
    section_name: str,
    instrument: str,
    output_file: Optional[Path] = None
) -> str:
    """
    Create a template ABC file for a section with the correct number of bars.
    
    Returns the template content.
    """
    expected_bars = song_structure.get_section_bars(section_name)
    is_perc = song_structure.is_percussion(instrument)
    
    # Build header
    header = f"""X:1
T:{song_structure.title} - {section_name.title()} - {instrument.title()}
M:{song_structure.time_sig}
L:1/8
K:{song_structure.key if not is_perc else 'C perc'}
"""
    
    # Generate bar templates
    if is_perc:
        # Drums: two voices
        header += """V:1 name="Kick"
"""
        # Create empty bars for Voice 1 (Kick)
        kick_bars = []
        for i in range(expected_bars):
            kick_bars.append("C4 C4")  # Default kick pattern
        
        voice1 = " | ".join(kick_bars) + " |"
        
        # Create empty bars for Voice 2 (Snare)
        snare_bars = []
        for i in range(expected_bars):
            snare_bars.append("z4 E4")  # Default snare pattern
        
        voice2 = "\nV:2 name=\"Snare\"\n" + " | ".join(snare_bars) + " |"
        
        content = header + voice1 + voice2
    else:
        # Regular instrument: single voice
        bars = []
        for i in range(expected_bars):
            bars.append("z8")  # Default: rests (to be filled in)
        
        content = header + " | ".join(bars) + " |"
    
    # Add helpful comment
    content += f"\n% Expected: {expected_bars} bars\n"
    
    # Write to file if specified
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content)
        print(f"Created template: {output_file}")
        print(f"  Section: {section_name}")
        print(f"  Instrument: {instrument}")
        print(f"  Expected bars: {expected_bars}")
    
    return content


def validate_section_file(
    song_structure: SongStructure,
    section_name: str,
    instrument: str,
    section_file: Path
) -> Tuple[bool, str]:
    """
    Validate that a section file has the correct number of bars.
    
    Returns (is_valid, message)
    """
    if not section_file.exists():
        return False, f"File not found: {section_file}"
    
    expected_bars = song_structure.get_section_bars(section_name)
    content = section_file.read_text()
    actual_bars = count_bars(content)
    
    if actual_bars == expected_bars:
        return True, f"✓ {section_file.name}: {actual_bars} bars (correct)"
    else:
        return False, f"✗ {section_file.name}: {actual_bars} bars (expected {expected_bars})"


def validate_all_sections(song_dir: Path, structure_file: Path) -> Dict:
    """
    Validate all section files in a song directory.
    
    Returns validation results.
    """
    song_structure = SongStructure(structure_file)
    sections_dir = song_dir / 'sections'
    
    if not sections_dir.exists():
        return {'error': 'No sections directory found'}
    
    results = {
        'song': song_structure.title,
        'sections': {},
        'all_valid': True,
        'missing': [],
        'invalid': []
    }
    
    # Check each section/instrument combination
    for section_name in set(song_structure.structure_order):
        for instrument in song_structure.get_instruments():
            section_file = sections_dir / f"{section_name}-{instrument}.abc"
            
            if not section_file.exists():
                results['missing'].append(str(section_file.name))
                results['all_valid'] = False
                continue
            
            is_valid, message = validate_section_file(
                song_structure,
                section_name,
                instrument,
                section_file
            )
            
            key = f"{section_name}-{instrument}"
            results['sections'][key] = {
                'valid': is_valid,
                'message': message
            }
            
            if not is_valid:
                results['invalid'].append(section_file.name)
                results['all_valid'] = False
    
    return results


def print_validation_results(results: Dict):
    """Print formatted validation results"""
    print(f"\n{'='*70}")
    print(f"Section Validation: {results['song']}")
    print(f"{'='*70}")
    
    if 'error' in results:
        print(f"ERROR: {results['error']}")
        return
    
    # Print section results
    for key, info in sorted(results['sections'].items()):
        print(info['message'])
    
    # Print missing files
    if results['missing']:
        print(f"\n{'='*70}")
        print(f"Missing section files ({len(results['missing'])}):")
        for filename in results['missing']:
            print(f"  - {filename}")
    
    # Print summary
    print(f"\n{'='*70}")
    if results['all_valid'] and not results['missing']:
        print("✓ All sections valid!")
    else:
        if results['invalid']:
            print(f"✗ {len(results['invalid'])} invalid sections")
        if results['missing']:
            print(f"✗ {len(results['missing'])} missing sections")
    print(f"{'='*70}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Section Management Tools')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Template command
    template_parser = subparsers.add_parser('template', help='Create section template')
    template_parser.add_argument('structure_file', type=Path, help='structure.yaml file')
    template_parser.add_argument('section', help='Section name (intro, verse, chorus, etc.)')
    template_parser.add_argument('instrument', help='Instrument name')
    template_parser.add_argument('--output', '-o', type=Path, help='Output file path')
    
    # Validate single section
    validate_parser = subparsers.add_parser('validate', help='Validate a section file')
    validate_parser.add_argument('structure_file', type=Path, help='structure.yaml file')
    validate_parser.add_argument('section', help='Section name')
    validate_parser.add_argument('instrument', help='Instrument name')
    validate_parser.add_argument('file', type=Path, help='Section file to validate')
    
    # Validate all sections
    validate_all_parser = subparsers.add_parser('validate-all', help='Validate all sections')
    validate_all_parser.add_argument('song_dir', type=Path, help='Song directory')
    
    # Generate all templates
    generate_parser = subparsers.add_parser('generate-all', help='Generate all section templates')
    generate_parser.add_argument('song_dir', type=Path, help='Song directory')
    
    args = parser.parse_args()
    
    if args.command == 'template':
        song_structure = SongStructure(args.structure_file)
        
        # Determine output file
        if args.output:
            output_file = args.output
        else:
            # Default to sections/{section}-{instrument}.abc
            sections_dir = args.structure_file.parent / 'sections'
            output_file = sections_dir / f"{args.section}-{args.instrument}.abc"
        
        create_section_template(
            song_structure,
            args.section,
            args.instrument,
            output_file
        )
    
    elif args.command == 'validate':
        song_structure = SongStructure(args.structure_file)
        is_valid, message = validate_section_file(
            song_structure,
            args.section,
            args.instrument,
            args.file
        )
        print(message)
        sys.exit(0 if is_valid else 1)
    
    elif args.command == 'validate-all':
        structure_file = args.song_dir / 'structure.yaml'
        results = validate_all_sections(args.song_dir, structure_file)
        print_validation_results(results)
        sys.exit(0 if results['all_valid'] else 1)
    
    elif args.command == 'generate-all':
        structure_file = args.song_dir / 'structure.yaml'
        song_structure = SongStructure(structure_file)
        sections_dir = args.song_dir / 'sections'
        sections_dir.mkdir(exist_ok=True)
        
        count = 0
        for section_name in set(song_structure.structure_order):
            for instrument in song_structure.get_instruments():
                output_file = sections_dir / f"{section_name}-{instrument}.abc"
                if not output_file.exists():
                    create_section_template(
                        song_structure,
                        section_name,
                        instrument,
                        output_file
                    )
                    count += 1
        
        print(f"\nGenerated {count} section templates")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
