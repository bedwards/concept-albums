#!/usr/bin/env python3
"""
Lyrics Analyzer - Parse, analyze, and compare song lyrics

This script provides five main functions:
1. parse: Convert dirty lyrics to structured YAML
2. analyze: Quantitative analysis of lyrics (phonetics, meter, rhyme, etc.)
3. taste: Compute "taste" metrics (concreteness, cliché, show-don't-tell, sensory)
4. compare: Compare candidate lyrics against a model song and rank them
5. critique: Generate structured critique prompt for AI evaluation

Usage:
    python lyrics_analyzer.py parse --input raw_lyrics.txt --output structured.yaml
    python lyrics_analyzer.py analyze --input structured.yaml --output analysis.json
    python lyrics_analyzer.py taste --input structured.yaml --output taste.json
    python lyrics_analyzer.py compare --model model.txt --candidates song1.txt song2.txt --output report.json
    python lyrics_analyzer.py critique --input structured.yaml --model model.yaml --output critique_prompt.md

Dependencies (install via: pip install -r requirements-lyrics.txt):
    - pronouncing (CMU dictionary for phonemes/rhymes)
    - spacy (NLP for POS tagging)
    - pyphen (syllable counting fallback)
    - pyyaml (YAML processing)
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import yaml

# Lazy imports for optional dependencies
_pronouncing = None
_spacy = None
_nlp = None
_pyphen = None
_pyphen_dic = None


def _get_pronouncing():
    """Lazy load pronouncing library."""
    global _pronouncing
    if _pronouncing is None:
        try:
            import pronouncing
            _pronouncing = pronouncing
        except ImportError:
            print("Error: 'pronouncing' not installed. Run: pip install pronouncing")
            sys.exit(1)
    return _pronouncing


def _get_spacy():
    """Lazy load spacy and model."""
    global _spacy, _nlp
    if _spacy is None:
        try:
            import spacy
            _spacy = spacy
            try:
                _nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("Downloading spaCy model...")
                import subprocess
                subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
                _nlp = spacy.load("en_core_web_sm")
        except ImportError:
            print("Error: 'spacy' not installed. Run: pip install spacy")
            sys.exit(1)
    return _spacy, _nlp


def _get_pyphen():
    """Lazy load pyphen library."""
    global _pyphen, _pyphen_dic
    if _pyphen is None:
        try:
            import pyphen
            _pyphen = pyphen
            _pyphen_dic = pyphen.Pyphen(lang='en_US')
        except ImportError:
            _pyphen = False  # Mark as unavailable
            _pyphen_dic = None
    return _pyphen, _pyphen_dic


# =============================================================================
# FUNCTION 1: Parse dirty lyrics to structured YAML
# =============================================================================

def clean_line(line: str) -> str:
    """Remove chord annotations and clean up a lyric line."""
    # Remove chord annotations like [Am], [G], (Am), (G), Am:, G7, etc.
    # Common chord patterns: [Chord], (Chord), Chord:, standalone chords
    chord_pattern = r'\[[\w#b/]+\]|\([\w#b/]+\)|^[A-G][#b]?(?:m|maj|min|dim|aug|sus|add|7|9|11|13)*[/\w]*\s*:?\s*'
    line = re.sub(chord_pattern, '', line, flags=re.IGNORECASE)

    # Remove tab/chord line indicators
    if re.match(r'^[\s\-|x0-9]+$', line):  # Tab lines
        return ''

    # Remove lines that are mostly chord names
    words = line.split()
    chord_like = sum(1 for w in words if re.match(r'^[A-G][#b]?(?:m|maj|min|dim|aug|sus|add|7|9|11|13)*$', w, re.I))
    if len(words) > 0 and chord_like / len(words) > 0.5:
        return ''

    # Clean whitespace
    line = ' '.join(line.split())
    return line.strip()


def detect_section_marker(line: str) -> Optional[str]:
    """Detect if line is a section marker (verse, chorus, etc.)."""
    line_lower = line.lower().strip()

    # Remove brackets and parentheses
    line_clean = re.sub(r'[\[\](){}]', '', line_lower).strip()

    # Common section patterns
    section_patterns = [
        (r'^verse\s*(\d+)?', 'verse'),
        (r'^v\s*(\d+)', 'verse'),
        (r'^chorus\s*(\d+)?', 'chorus'),
        (r'^c\s*(\d+)', 'chorus'),
        (r'^pre-?chorus\s*(\d+)?', 'prechorus'),
        (r'^bridge\s*(\d+)?', 'bridge'),
        (r'^outro\s*(\d+)?', 'outro'),
        (r'^intro\s*(\d+)?', 'intro'),
        (r'^hook\s*(\d+)?', 'hook'),
        (r'^refrain\s*(\d+)?', 'refrain'),
        (r'^interlude\s*(\d+)?', 'interlude'),
        (r'^solo\s*(\d+)?', 'solo'),
        (r'^coda\s*(\d+)?', 'coda'),
        (r'^tag\s*(\d+)?', 'tag'),
    ]

    for pattern, section_type in section_patterns:
        match = re.match(pattern, line_clean)
        if match:
            num = match.group(1) if match.lastindex and match.group(1) else ''
            return f"{section_type}{num}" if num else section_type

    # Check for "/" delimiter indicating section
    if line_clean.startswith('/') or line_clean.endswith('/'):
        section_name = line_clean.strip('/').strip()
        if section_name:
            return section_name.replace(' ', '-')

    return None


def parse_lyrics_to_structure(input_text: str) -> Dict:
    """
    Parse raw/dirty lyrics text into structured format.

    Expected input: Claude-cleaned lyrics with section markers like:
    /verse-1/
    Line one of verse
    Line two of verse

    /chorus/
    Chorus line one
    ...
    """
    lines = input_text.strip().split('\n')

    structure = {
        'sections': [],
        'section_order': []
    }

    current_section = None
    current_lines = []
    section_counts = defaultdict(int)

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Check for section marker
        section = detect_section_marker(line)
        if section:
            # Save previous section
            if current_section and current_lines:
                structure['sections'].append({
                    'name': current_section,
                    'lines': current_lines
                })
                structure['section_order'].append(current_section)

            # Handle section numbering
            base_section = re.sub(r'\d+$', '', section)
            section_counts[base_section] += 1
            if not re.search(r'\d+$', section):
                section = f"{section}{section_counts[base_section]}"

            current_section = section
            current_lines = []
            continue

        # Clean the line
        cleaned = clean_line(line)
        if cleaned:
            current_lines.append(cleaned)

    # Save final section
    if current_section and current_lines:
        structure['sections'].append({
            'name': current_section,
            'lines': current_lines
        })
        structure['section_order'].append(current_section)

    # If no sections detected, treat as single section
    if not structure['sections']:
        all_lines = [clean_line(l) for l in lines if clean_line(l)]
        if all_lines:
            structure['sections'].append({
                'name': 'verse1',
                'lines': all_lines
            })
            structure['section_order'].append('verse1')

    return structure


# =============================================================================
# FUNCTION 2: Quantitative Analysis
# =============================================================================

def count_syllables(word: str) -> int:
    """Count syllables in a word using CMU dictionary with fallback."""
    pronouncing = _get_pronouncing()

    # Try CMU dictionary first
    phones = pronouncing.phones_for_word(word.lower())
    if phones:
        return pronouncing.syllable_count(phones[0])

    # Fallback to pyphen
    _, pyphen_dic = _get_pyphen()
    if pyphen_dic:
        hyphenated = pyphen_dic.inserted(word)
        return len(hyphenated.split('-'))

    # Simple fallback: count vowel groups
    word = word.lower()
    count = len(re.findall(r'[aeiouy]+', word))
    if word.endswith('e') and count > 1:
        count -= 1
    return max(1, count)


def get_phonemes(word: str) -> List[str]:
    """Get phonemes for a word from CMU dictionary."""
    pronouncing = _get_pronouncing()
    phones = pronouncing.phones_for_word(word.lower())
    if phones:
        return phones[0].split()
    return []


def get_stressed_syllables(word: str) -> List[int]:
    """Get positions of stressed syllables (1 = primary, 2 = secondary)."""
    pronouncing = _get_pronouncing()
    phones = pronouncing.phones_for_word(word.lower())
    if phones:
        stresses = pronouncing.stresses(phones[0])
        return [i for i, s in enumerate(stresses) if s in '12']
    return []


def analyze_rhyme_scheme(lines: List[str]) -> Dict:
    """Analyze rhyme scheme of a set of lines."""
    pronouncing = _get_pronouncing()

    def get_rhyme_part(word: str) -> str:
        """Get the rhyming part of a word."""
        phones = pronouncing.phones_for_word(word.lower())
        if phones:
            return pronouncing.rhyming_part(phones[0])
        return word[-3:].lower()  # Fallback to last 3 chars

    # Extract last word of each line
    last_words = []
    for line in lines:
        words = re.findall(r'\b\w+\b', line)
        if words:
            last_words.append(words[-1])
        else:
            last_words.append('')

    # Build rhyme scheme
    rhyme_parts = [get_rhyme_part(w) if w else '' for w in last_words]

    scheme = []
    rhyme_dict = {}
    current_letter = 'A'

    for rp in rhyme_parts:
        if not rp:
            scheme.append('X')
        elif rp in rhyme_dict:
            scheme.append(rhyme_dict[rp])
        else:
            rhyme_dict[rp] = current_letter
            scheme.append(current_letter)
            current_letter = chr(ord(current_letter) + 1)
            if current_letter > 'Z':
                current_letter = 'A'

    # Identify rhyme types
    scheme_str = ''.join(scheme)
    rhyme_types = {
        'couplet': bool(re.search(r'AA|BB|CC|DD', scheme_str)),
        'alternate': bool(re.search(r'ABAB|CDCD', scheme_str)),
        'enclosed': bool(re.search(r'ABBA|CDDC', scheme_str)),
        'terza_rima': bool(re.search(r'ABA.BCB', scheme_str)),
    }

    return {
        'scheme': scheme,
        'scheme_string': scheme_str,
        'unique_rhymes': len(set(scheme) - {'X'}),
        'rhyme_types': rhyme_types,
        'rhyme_density': 1 - (scheme.count('X') / len(scheme)) if scheme else 0
    }


def analyze_meter(lines: List[str]) -> Dict:
    """Analyze metrical patterns in lines."""
    pronouncing = _get_pronouncing()

    patterns = []
    syllable_counts = []

    for line in lines:
        words = re.findall(r'\b\w+\b', line)
        line_pattern = []
        line_syllables = 0

        for word in words:
            phones = pronouncing.phones_for_word(word.lower())
            if phones:
                stresses = pronouncing.stresses(phones[0])
                line_pattern.extend(stresses)
                line_syllables += len(stresses)
            else:
                # Fallback
                syl_count = count_syllables(word)
                line_pattern.extend(['0'] * syl_count)
                line_syllables += syl_count

        patterns.append(''.join(line_pattern))
        syllable_counts.append(line_syllables)

    # Detect common meters
    def detect_meter(pattern: str) -> str:
        if not pattern:
            return 'unknown'
        # Simplify pattern (0=unstressed, 1/2=stressed)
        simple = ''.join('1' if c in '12' else '0' for c in pattern)

        # Check for iambic (01)
        iambic = sum(1 for i in range(0, len(simple)-1, 2) if simple[i:i+2] == '01')
        trochaic = sum(1 for i in range(0, len(simple)-1, 2) if simple[i:i+2] == '10')
        dactylic = sum(1 for i in range(0, len(simple)-2, 3) if simple[i:i+3] == '100')
        anapestic = sum(1 for i in range(0, len(simple)-2, 3) if simple[i:i+3] == '001')

        max_meter = max(iambic, trochaic, dactylic, anapestic)
        if max_meter < 2:
            return 'free'
        if iambic == max_meter:
            return 'iambic'
        if trochaic == max_meter:
            return 'trochaic'
        if dactylic == max_meter:
            return 'dactylic'
        if anapestic == max_meter:
            return 'anapestic'
        return 'mixed'

    meters = [detect_meter(p) for p in patterns]
    meter_counts = Counter(meters)
    dominant_meter = meter_counts.most_common(1)[0][0] if meter_counts else 'unknown'

    return {
        'patterns': patterns,
        'syllable_counts': syllable_counts,
        'avg_syllables_per_line': sum(syllable_counts) / len(syllable_counts) if syllable_counts else 0,
        'syllable_variance': _variance(syllable_counts),
        'dominant_meter': dominant_meter,
        'meter_distribution': dict(meter_counts),
        'regularity': meter_counts[dominant_meter] / len(meters) if meters else 0
    }


def _variance(values: List[float]) -> float:
    """Calculate variance of a list of values."""
    if not values:
        return 0
    mean = sum(values) / len(values)
    return sum((x - mean) ** 2 for x in values) / len(values)


def analyze_pos(lines: List[str]) -> Dict:
    """Analyze parts of speech in lines."""
    _, nlp = _get_spacy()

    all_text = ' '.join(lines)
    doc = nlp(all_text)

    pos_counts = Counter(token.pos_ for token in doc if not token.is_punct)

    # Extract specific word types
    nouns = [token.text for token in doc if token.pos_ == 'NOUN']
    verbs = [token.text for token in doc if token.pos_ == 'VERB']
    adjectives = [token.text for token in doc if token.pos_ == 'ADJ']
    adverbs = [token.text for token in doc if token.pos_ == 'ADV']

    # Sentence structure analysis
    sentences = list(doc.sents)
    sentence_lengths = [len([t for t in sent if not t.is_punct]) for sent in sentences]

    return {
        'pos_distribution': dict(pos_counts),
        'noun_count': len(nouns),
        'verb_count': len(verbs),
        'adjective_count': len(adjectives),
        'adverb_count': len(adverbs),
        'noun_verb_ratio': len(nouns) / len(verbs) if verbs else 0,
        'unique_nouns': len(set(n.lower() for n in nouns)),
        'unique_verbs': len(set(v.lower() for v in verbs)),
        'sentence_count': len(sentences),
        'avg_sentence_length': sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0,
        'top_nouns': Counter(n.lower() for n in nouns).most_common(10),
        'top_verbs': Counter(v.lower() for v in verbs).most_common(10)
    }


def analyze_phonetics(lines: List[str]) -> Dict:
    """Analyze phonetic features of lyrics."""
    pronouncing = _get_pronouncing()

    all_words = []
    for line in lines:
        all_words.extend(re.findall(r'\b\w+\b', line))

    # Get all phonemes
    all_phonemes = []
    for word in all_words:
        phonemes = get_phonemes(word)
        all_phonemes.extend(phonemes)

    # Phoneme distribution
    phoneme_counts = Counter(re.sub(r'\d', '', p) for p in all_phonemes)

    # Consonant clusters
    consonants = [p for p in all_phonemes if not any(c.isdigit() for c in p) and p not in ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW']]
    vowels = [p for p in all_phonemes if p not in consonants]

    # Alliteration detection (repeated initial consonants)
    initial_sounds = []
    for line in lines:
        words = re.findall(r'\b\w+\b', line)
        line_initials = []
        for word in words:
            phones = pronouncing.phones_for_word(word.lower())
            if phones:
                first_phone = phones[0].split()[0] if phones[0] else ''
                line_initials.append(re.sub(r'\d', '', first_phone))
        initial_sounds.append(line_initials)

    alliteration_count = 0
    for line_initials in initial_sounds:
        if len(line_initials) >= 2:
            for i in range(len(line_initials) - 1):
                if line_initials[i] and line_initials[i] == line_initials[i+1]:
                    alliteration_count += 1

    return {
        'total_phonemes': len(all_phonemes),
        'unique_phonemes': len(set(re.sub(r'\d', '', p) for p in all_phonemes)),
        'consonant_count': len(consonants),
        'vowel_count': len(vowels),
        'consonant_vowel_ratio': len(consonants) / len(vowels) if vowels else 0,
        'top_phonemes': phoneme_counts.most_common(10),
        'alliteration_count': alliteration_count
    }


def analyze_vocabulary(lines: List[str]) -> Dict:
    """Analyze vocabulary richness and complexity."""
    _, nlp = _get_spacy()

    all_text = ' '.join(lines)
    doc = nlp(all_text)

    words = [token.text.lower() for token in doc if token.is_alpha]
    lemmas = [token.lemma_.lower() for token in doc if token.is_alpha]

    # Type-token ratio (vocabulary richness)
    ttr = len(set(words)) / len(words) if words else 0

    # Word length statistics
    word_lengths = [len(w) for w in words]

    # Syllable statistics
    syllable_counts = [count_syllables(w) for w in words]

    return {
        'total_words': len(words),
        'unique_words': len(set(words)),
        'unique_lemmas': len(set(lemmas)),
        'type_token_ratio': ttr,
        'avg_word_length': sum(word_lengths) / len(word_lengths) if word_lengths else 0,
        'avg_syllables_per_word': sum(syllable_counts) / len(syllable_counts) if syllable_counts else 0,
        'long_words': sum(1 for w in words if len(w) > 8),
        'polysyllabic_words': sum(1 for s in syllable_counts if s >= 3)
    }


# =============================================================================
# TASTE METRICS - Computable proxies for lyrical quality
# =============================================================================

# Concreteness ratings from Brysbaert et al. (2014) - abbreviated version
# Full dataset: https://link.springer.com/article/10.3758/s13428-013-0403-5
# Scale: 1 (abstract) to 5 (concrete)
# This is a curated subset of ~500 common words for demonstration
# For production, load the full 40k word dataset from CSV

CONCRETENESS_RATINGS = {
    # Very concrete (4.5-5.0) - physical objects you can touch/see
    'hand': 4.95, 'table': 4.97, 'dog': 4.98, 'chair': 4.97, 'tree': 4.93,
    'house': 4.92, 'car': 4.95, 'door': 4.94, 'window': 4.91, 'road': 4.85,
    'rain': 4.72, 'sun': 4.83, 'moon': 4.87, 'fire': 4.82, 'water': 4.78,
    'blood': 4.81, 'stone': 4.89, 'knife': 4.93, 'gun': 4.91, 'bottle': 4.92,
    'train': 4.88, 'truck': 4.91, 'barn': 4.85, 'farm': 4.62, 'field': 4.51,
    'river': 4.79, 'mountain': 4.78, 'valley': 4.45, 'desert': 4.52, 'ocean': 4.73,
    'face': 4.77, 'eye': 4.89, 'tear': 4.42, 'smile': 4.35, 'frown': 4.21,
    'bed': 4.93, 'pillow': 4.89, 'blanket': 4.87, 'sheet': 4.71, 'floor': 4.85,
    'wall': 4.91, 'roof': 4.83, 'fence': 4.82, 'gate': 4.78, 'bridge': 4.81,
    'letter': 4.63, 'ink': 4.67, 'paper': 4.88, 'book': 4.91, 'page': 4.72,
    'whiskey': 4.73, 'beer': 4.82, 'wine': 4.78, 'coffee': 4.81, 'tea': 4.76,
    'cigarette': 4.87, 'smoke': 4.45, 'ash': 4.52, 'flame': 4.61, 'match': 4.73,
    'temple': 4.42, 'church': 4.78, 'altar': 4.51, 'cross': 4.63, 'grave': 4.67,
    'baby': 4.85, 'child': 4.62, 'woman': 4.73, 'man': 4.71, 'girl': 4.68,
    'boy': 4.72, 'mother': 4.51, 'father': 4.48, 'daughter': 4.45, 'son': 4.43,
    'shack': 4.65, 'cabin': 4.72, 'cottage': 4.68, 'mansion': 4.71, 'castle': 4.78,

    # Moderately concrete (3.5-4.5) - sensory/perceptual
    'darkness': 3.89, 'shadow': 4.12, 'light': 4.21, 'color': 4.15, 'sound': 3.95,
    'voice': 4.18, 'song': 4.05, 'music': 3.92, 'noise': 3.88, 'silence': 3.21,
    'heat': 3.92, 'cold': 3.85, 'wind': 4.23, 'storm': 4.35, 'thunder': 4.42,
    'pain': 3.72, 'ache': 3.65, 'hurt': 3.51, 'wound': 4.21, 'scar': 4.35,
    'sleep': 3.85, 'dream': 3.42, 'nightmare': 3.35, 'wake': 3.21, 'rest': 3.15,
    'sunset': 4.45, 'sunrise': 4.42, 'dawn': 3.92, 'dusk': 3.85, 'midnight': 3.72,
    'memory': 2.95, 'moment': 2.85, 'time': 2.72, 'day': 3.52, 'night': 3.65,
    'country': 3.82, 'city': 4.35, 'town': 4.28, 'village': 4.21, 'street': 4.52,

    # Abstract (2.0-3.5) - concepts, emotions, states
    'love': 2.95, 'hate': 2.82, 'anger': 2.78, 'fear': 2.85, 'hope': 2.42,
    'joy': 2.65, 'sorrow': 2.45, 'grief': 2.38, 'regret': 2.21, 'shame': 2.35,
    'pride': 2.45, 'guilt': 2.28, 'peace': 2.52, 'war': 3.35, 'fight': 3.42,
    'truth': 2.12, 'lie': 2.35, 'faith': 2.18, 'doubt': 2.15, 'belief': 2.08,
    'soul': 2.25, 'spirit': 2.18, 'heart': 3.95, 'mind': 2.85, 'thought': 2.42,
    'feeling': 2.55, 'emotion': 2.35, 'mood': 2.42, 'desire': 2.52, 'want': 2.21,
    'need': 2.18, 'wish': 2.25, 'dream': 3.42, 'goal': 2.35, 'purpose': 2.15,
    'meaning': 1.95, 'reason': 2.12, 'cause': 2.18, 'effect': 2.21, 'result': 2.25,
    'change': 2.35, 'growth': 2.72, 'loss': 2.45, 'gain': 2.38, 'success': 2.28,
    'failure': 2.22, 'mistake': 2.35, 'lesson': 2.42, 'experience': 2.38, 'knowledge': 2.15,
    'thing': 2.85, 'stuff': 2.72, 'something': 2.15, 'nothing': 1.85, 'everything': 1.92,

    # Very abstract (1.0-2.0)
    'idea': 1.95, 'concept': 1.72, 'notion': 1.65, 'theory': 1.78, 'principle': 1.82,
    'essence': 1.55, 'nature': 2.35, 'reality': 1.92, 'existence': 1.78, 'being': 1.85,
    'possibility': 1.72, 'probability': 1.65, 'chance': 2.18, 'fate': 1.95, 'destiny': 1.88,
}

# Common clichés in songwriting - phrases that signal lazy writing
CLICHE_PHRASES = {
    # Time/change clichés
    "time heals all wounds", "time will tell", "only time will tell",
    "times have changed", "ahead of its time", "stood the test of time",
    "tomorrow is a new day", "tomorrow is another day", "new day dawning",

    # Love clichés
    "love at first sight", "head over heels", "meant to be",
    "love conquers all", "written in the stars", "made for each other",
    "two hearts beating as one", "you complete me", "other half",
    "heart of gold", "heart on my sleeve", "broken heart",

    # Emotional clichés
    "feel so sad", "feel so bad", "feel so good", "feel so alone",
    "really awful", "really terrible", "really wonderful",
    "very sad", "very happy", "very angry", "so very",
    "i feel like", "makes me feel", "how i feel",

    # Journey/road clichés
    "end of the road", "long road ahead", "road less traveled",
    "journey of a lifetime", "life is a journey", "path in life",

    # Nature clichés
    "calm before the storm", "weather the storm", "ray of sunshine",
    "light at the end of the tunnel", "darkest before the dawn",

    # Rhyme-forced clichés
    "above", "of", "love",  # The tired of/love/above triplet
    "fire", "desire", "higher",
    "heart", "apart", "start",

    # Filler phrases
    "you know what i mean", "if you know what i mean",
    "at the end of the day", "when all is said and done",
    "it is what it is", "everything happens for a reason",
    "learn from the past", "live for today", "hope for tomorrow",
}

# State verbs (telling) vs action verbs (showing)
STATE_VERBS = {
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'feel', 'felt', 'seem', 'seemed', 'appear', 'appeared',
    'look', 'looked', 'sound', 'sounded', 'taste', 'tasted',
    'smell', 'smelled', 'become', 'became', 'remain', 'remained',
    'stay', 'stayed', 'keep', 'kept', 'prove', 'proved',
    'think', 'thought', 'believe', 'believed', 'know', 'knew',
    'want', 'wanted', 'need', 'needed', 'like', 'liked',
    'love', 'loved', 'hate', 'hated', 'prefer', 'preferred',
}

# Strong action verbs (showing)
STRONG_VERBS = {
    'slam', 'slammed', 'crash', 'crashed', 'smash', 'smashed',
    'grab', 'grabbed', 'seize', 'seized', 'clutch', 'clutched',
    'whisper', 'whispered', 'shout', 'shouted', 'scream', 'screamed',
    'crawl', 'crawled', 'sprint', 'sprinted', 'leap', 'leaped',
    'stagger', 'staggered', 'stumble', 'stumbled', 'lurch', 'lurched',
    'pierce', 'pierced', 'stab', 'stabbed', 'slash', 'slashed',
    'burn', 'burned', 'blaze', 'blazed', 'smolder', 'smoldered',
    'shatter', 'shattered', 'crumble', 'crumbled', 'collapse', 'collapsed',
    'tremble', 'trembled', 'shiver', 'shivered', 'shake', 'shook',
    'creep', 'crept', 'sneak', 'snuck', 'prowl', 'prowled',
    'thunder', 'thundered', 'roar', 'roared', 'howl', 'howled',
    'drove', 'drive', 'walked', 'walk', 'ran', 'run',
}

# Sensory words by sense
SENSORY_WORDS = {
    'sight': {
        'see', 'saw', 'seen', 'watch', 'watched', 'gaze', 'gazed',
        'stare', 'stared', 'glance', 'glanced', 'glimpse', 'glimpsed',
        'bright', 'dim', 'dark', 'light', 'glow', 'glowed', 'shine', 'shone',
        'flash', 'flashed', 'sparkle', 'sparkled', 'gleam', 'gleamed',
        'shadow', 'silhouette', 'color', 'red', 'blue', 'green', 'black', 'white',
        'golden', 'silver', 'pale', 'vivid', 'faded', 'blurred',
    },
    'sound': {
        'hear', 'heard', 'listen', 'listened', 'sound', 'sounded',
        'ring', 'rang', 'rung', 'echo', 'echoed', 'resound', 'resounded',
        'whisper', 'whispered', 'murmur', 'murmured', 'hum', 'hummed',
        'roar', 'roared', 'thunder', 'thundered', 'crash', 'crashed',
        'crack', 'cracked', 'snap', 'snapped', 'click', 'clicked',
        'silent', 'quiet', 'loud', 'soft', 'harsh', 'gentle',
    },
    'touch': {
        'touch', 'touched', 'feel', 'felt', 'hold', 'held',
        'grab', 'grabbed', 'grasp', 'grasped', 'grip', 'gripped',
        'stroke', 'stroked', 'caress', 'caressed', 'brush', 'brushed',
        'rough', 'smooth', 'soft', 'hard', 'cold', 'warm', 'hot',
        'wet', 'dry', 'damp', 'sticky', 'slippery', 'sharp', 'dull',
    },
    'smell': {
        'smell', 'smelled', 'sniff', 'sniffed', 'scent', 'scented',
        'stink', 'stunk', 'reek', 'reeked', 'fragrant', 'pungent',
        'musty', 'fresh', 'stale', 'rotten', 'sweet', 'sour',
    },
    'taste': {
        'taste', 'tasted', 'savor', 'savored', 'sip', 'sipped',
        'swallow', 'swallowed', 'bite', 'bit', 'chew', 'chewed',
        'sweet', 'sour', 'bitter', 'salty', 'savory', 'bland',
    },
}


def analyze_concreteness(lines: List[str]) -> Dict:
    """Analyze concreteness of vocabulary using Brysbaert ratings."""
    _, nlp = _get_spacy()

    all_text = ' '.join(lines)
    doc = nlp(all_text)

    words = [token.lemma_.lower() for token in doc if token.is_alpha]

    # Get concreteness scores
    rated_words = []
    unrated_words = []
    concrete_examples = []
    abstract_examples = []

    for word in words:
        if word in CONCRETENESS_RATINGS:
            score = CONCRETENESS_RATINGS[word]
            rated_words.append((word, score))
            if score >= 4.5:
                concrete_examples.append(word)
            elif score <= 2.5:
                abstract_examples.append(word)
        else:
            unrated_words.append(word)

    if not rated_words:
        return {
            'avg_concreteness': 0,
            'rated_word_count': 0,
            'unrated_word_count': len(unrated_words),
            'coverage': 0,
            'concrete_words': [],
            'abstract_words': [],
            'concreteness_distribution': {}
        }

    scores = [s for _, s in rated_words]
    avg_score = sum(scores) / len(scores)

    # Distribution by range
    distribution = {
        'very_concrete_4.5+': sum(1 for s in scores if s >= 4.5),
        'concrete_3.5-4.5': sum(1 for s in scores if 3.5 <= s < 4.5),
        'moderate_2.5-3.5': sum(1 for s in scores if 2.5 <= s < 3.5),
        'abstract_1.5-2.5': sum(1 for s in scores if 1.5 <= s < 2.5),
        'very_abstract_<1.5': sum(1 for s in scores if s < 1.5),
    }

    return {
        'avg_concreteness': avg_score,
        'rated_word_count': len(rated_words),
        'unrated_word_count': len(unrated_words),
        'coverage': len(rated_words) / (len(rated_words) + len(unrated_words)),
        'concrete_words': list(set(concrete_examples))[:15],
        'abstract_words': list(set(abstract_examples))[:15],
        'concreteness_distribution': distribution
    }


def detect_cliches(lines: List[str]) -> Dict:
    """Detect cliché phrases in lyrics."""
    all_text = ' '.join(lines).lower()

    found_cliches = []
    for cliche in CLICHE_PHRASES:
        if cliche in all_text:
            # Count occurrences
            count = all_text.count(cliche)
            found_cliches.append({
                'phrase': cliche,
                'count': count
            })

    # Sort by severity (longer clichés are worse)
    found_cliches.sort(key=lambda x: len(x['phrase']), reverse=True)

    total_cliche_words = sum(
        len(c['phrase'].split()) * c['count']
        for c in found_cliches
    )

    total_words = len(all_text.split())
    cliche_density = total_cliche_words / total_words if total_words > 0 else 0

    return {
        'cliches_found': found_cliches,
        'cliche_count': len(found_cliches),
        'total_cliche_instances': sum(c['count'] for c in found_cliches),
        'cliche_word_density': cliche_density,
        'cliche_free': len(found_cliches) == 0
    }


def analyze_show_dont_tell(lines: List[str]) -> Dict:
    """Analyze ratio of action verbs (showing) vs state verbs (telling)."""
    _, nlp = _get_spacy()

    all_text = ' '.join(lines)
    doc = nlp(all_text)

    verbs = [token.lemma_.lower() for token in doc if token.pos_ == 'VERB']

    state_count = sum(1 for v in verbs if v in STATE_VERBS)
    strong_count = sum(1 for v in verbs if v in STRONG_VERBS)
    other_verbs = len(verbs) - state_count - strong_count

    # Find specific examples
    telling_examples = [v for v in verbs if v in STATE_VERBS][:10]
    showing_examples = [v for v in verbs if v in STRONG_VERBS][:10]

    total_verbs = len(verbs)
    if total_verbs == 0:
        show_tell_ratio = 0
    else:
        # Higher is better (more showing, less telling)
        show_tell_ratio = (strong_count + other_verbs * 0.5) / total_verbs

    return {
        'total_verbs': total_verbs,
        'state_verb_count': state_count,
        'strong_verb_count': strong_count,
        'other_verb_count': other_verbs,
        'show_tell_ratio': show_tell_ratio,
        'telling_examples': list(set(telling_examples)),
        'showing_examples': list(set(showing_examples)),
        'verdict': 'strong_showing' if show_tell_ratio > 0.6 else
                   'balanced' if show_tell_ratio > 0.4 else 'too_much_telling'
    }


def analyze_sensory_language(lines: List[str]) -> Dict:
    """Analyze use of sensory language by sense type."""
    _, nlp = _get_spacy()

    all_text = ' '.join(lines)
    doc = nlp(all_text)

    words = [token.lemma_.lower() for token in doc if token.is_alpha]
    word_set = set(words)

    sense_hits = {}
    sense_examples = {}

    for sense, sense_words in SENSORY_WORDS.items():
        hits = word_set & sense_words
        sense_hits[sense] = len(hits)
        sense_examples[sense] = list(hits)[:5]

    total_sensory = sum(sense_hits.values())
    total_words = len(words)

    return {
        'sensory_word_count': total_sensory,
        'sensory_density': total_sensory / total_words if total_words > 0 else 0,
        'by_sense': sense_hits,
        'examples_by_sense': sense_examples,
        'dominant_sense': max(sense_hits, key=sense_hits.get) if sense_hits else None,
        'sense_variety': sum(1 for v in sense_hits.values() if v > 0)
    }


def full_taste_analysis(structure: Dict) -> Dict:
    """Perform full taste/quality analysis of lyrics."""
    all_lines = []
    for section in structure.get('sections', []):
        all_lines.extend(section.get('lines', []))

    if not all_lines:
        return {'error': 'No lyrics found'}

    concreteness = analyze_concreteness(all_lines)
    cliches = detect_cliches(all_lines)
    show_tell = analyze_show_dont_tell(all_lines)
    sensory = analyze_sensory_language(all_lines)

    # Compute overall taste score (0-100)
    # Higher concreteness is better (target: 3.5+)
    concreteness_score = min(100, max(0, (concreteness['avg_concreteness'] - 2.0) / 2.5 * 100))

    # No clichés is better
    cliche_score = max(0, 100 - cliches['total_cliche_instances'] * 20)

    # Higher show/tell ratio is better
    show_tell_score = min(100, show_tell['show_tell_ratio'] * 150)

    # More sensory variety is better
    sensory_score = min(100, sensory['sense_variety'] * 25 + sensory['sensory_density'] * 500)

    overall_taste = (
        concreteness_score * 0.30 +
        cliche_score * 0.25 +
        show_tell_score * 0.25 +
        sensory_score * 0.20
    )

    return {
        'overall_taste_score': overall_taste,
        'component_scores': {
            'concreteness': concreteness_score,
            'cliche_free': cliche_score,
            'show_dont_tell': show_tell_score,
            'sensory_richness': sensory_score
        },
        'concreteness': concreteness,
        'cliches': cliches,
        'show_dont_tell': show_tell,
        'sensory': sensory,
        'recommendations': _generate_taste_recommendations(
            concreteness, cliches, show_tell, sensory
        )
    }


def _generate_taste_recommendations(concreteness, cliches, show_tell, sensory) -> List[str]:
    """Generate actionable recommendations based on taste analysis."""
    recs = []

    if concreteness['avg_concreteness'] < 3.5:
        recs.append(
            f"CONCRETENESS: Score {concreteness['avg_concreteness']:.2f}/5.00 is low. "
            f"Replace abstract words like [{', '.join(concreteness['abstract_words'][:5])}] "
            f"with physical, tangible nouns."
        )

    if cliches['cliche_count'] > 0:
        cliche_list = [c['phrase'] for c in cliches['cliches_found'][:3]]
        recs.append(
            f"CLICHÉS: Found {cliches['cliche_count']} cliché(s): [{', '.join(cliche_list)}]. "
            f"Replace with original imagery."
        )

    if show_tell['show_tell_ratio'] < 0.4:
        recs.append(
            f"SHOW DON'T TELL: Too many state verbs like [{', '.join(show_tell['telling_examples'][:5])}]. "
            f"Replace with action verbs that demonstrate emotion through behavior."
        )

    if sensory['sense_variety'] < 3:
        missing = [s for s, c in sensory['by_sense'].items() if c == 0]
        recs.append(
            f"SENSORY: Only {sensory['sense_variety']} senses engaged. "
            f"Add {', '.join(missing[:2])} imagery."
        )

    if not recs:
        recs.append("Strong taste metrics across all dimensions. Minor polish only.")

    return recs


def analyze_structure(structure: Dict) -> Dict:
    """Analyze song structure."""
    sections = structure.get('sections', [])
    section_order = structure.get('section_order', [])

    # Section statistics
    section_types = [re.sub(r'\d+$', '', s['name']) for s in sections]
    section_lengths = [len(s['lines']) for s in sections]

    return {
        'total_sections': len(sections),
        'section_types': list(set(section_types)),
        'section_order': section_order,
        'section_lengths': section_lengths,
        'avg_section_length': sum(section_lengths) / len(section_lengths) if section_lengths else 0,
        'has_chorus': 'chorus' in section_types,
        'has_bridge': 'bridge' in section_types,
        'chorus_count': section_types.count('chorus'),
        'verse_count': section_types.count('verse')
    }


def full_analysis(structure: Dict) -> Dict:
    """Perform full quantitative analysis of lyrics structure."""
    # Flatten all lines
    all_lines = []
    for section in structure.get('sections', []):
        all_lines.extend(section.get('lines', []))

    if not all_lines:
        return {'error': 'No lyrics found'}

    # Per-section analysis
    section_analyses = []
    for section in structure.get('sections', []):
        lines = section.get('lines', [])
        if lines:
            section_analyses.append({
                'name': section['name'],
                'line_count': len(lines),
                'rhyme': analyze_rhyme_scheme(lines),
                'meter': analyze_meter(lines)
            })

    return {
        'overall': {
            'total_lines': len(all_lines),
            'rhyme': analyze_rhyme_scheme(all_lines),
            'meter': analyze_meter(all_lines),
            'pos': analyze_pos(all_lines),
            'phonetics': analyze_phonetics(all_lines),
            'vocabulary': analyze_vocabulary(all_lines),
            'structure': analyze_structure(structure)
        },
        'sections': section_analyses
    }


# =============================================================================
# FUNCTION 3: Compare and rank against model
# =============================================================================

def compute_similarity_score(model_analysis: Dict, candidate_analysis: Dict) -> Dict:
    """Compute similarity score between model and candidate."""
    scores = {}

    model_overall = model_analysis.get('overall', {})
    cand_overall = candidate_analysis.get('overall', {})

    # Meter similarity
    if 'meter' in model_overall and 'meter' in cand_overall:
        model_meter = model_overall['meter']
        cand_meter = cand_overall['meter']

        # Same dominant meter
        meter_match = 1.0 if model_meter.get('dominant_meter') == cand_meter.get('dominant_meter') else 0.0

        # Syllable count similarity
        model_avg_syl = model_meter.get('avg_syllables_per_line', 0)
        cand_avg_syl = cand_meter.get('avg_syllables_per_line', 0)
        if model_avg_syl > 0:
            syl_diff = abs(model_avg_syl - cand_avg_syl) / model_avg_syl
            syl_score = max(0, 1 - syl_diff)
        else:
            syl_score = 0

        scores['meter_match'] = meter_match
        scores['syllable_similarity'] = syl_score

    # Rhyme similarity
    if 'rhyme' in model_overall and 'rhyme' in cand_overall:
        model_rhyme = model_overall['rhyme']
        cand_rhyme = cand_overall['rhyme']

        model_density = model_rhyme.get('rhyme_density', 0)
        cand_density = cand_rhyme.get('rhyme_density', 0)

        if model_density > 0:
            density_diff = abs(model_density - cand_density) / model_density
            scores['rhyme_density_similarity'] = max(0, 1 - density_diff)
        else:
            scores['rhyme_density_similarity'] = 1.0 if cand_density == 0 else 0.0

    # Vocabulary similarity
    if 'vocabulary' in model_overall and 'vocabulary' in cand_overall:
        model_vocab = model_overall['vocabulary']
        cand_vocab = cand_overall['vocabulary']

        model_ttr = model_vocab.get('type_token_ratio', 0)
        cand_ttr = cand_vocab.get('type_token_ratio', 0)

        if model_ttr > 0:
            ttr_diff = abs(model_ttr - cand_ttr) / model_ttr
            scores['vocabulary_similarity'] = max(0, 1 - ttr_diff)
        else:
            scores['vocabulary_similarity'] = 0

    # Structure similarity
    if 'structure' in model_overall and 'structure' in cand_overall:
        model_struct = model_overall['structure']
        cand_struct = cand_overall['structure']

        model_sections = set(model_struct.get('section_types', []))
        cand_sections = set(cand_struct.get('section_types', []))

        if model_sections:
            intersection = model_sections & cand_sections
            scores['structure_similarity'] = len(intersection) / len(model_sections)
        else:
            scores['structure_similarity'] = 0

    # POS distribution similarity
    if 'pos' in model_overall and 'pos' in cand_overall:
        model_pos = model_overall['pos']
        cand_pos = cand_overall['pos']

        model_nv = model_pos.get('noun_verb_ratio', 0)
        cand_nv = cand_pos.get('noun_verb_ratio', 0)

        if model_nv > 0:
            nv_diff = abs(model_nv - cand_nv) / model_nv
            scores['pos_similarity'] = max(0, 1 - min(nv_diff, 1))
        else:
            scores['pos_similarity'] = 0

    # Phonetics similarity
    if 'phonetics' in model_overall and 'phonetics' in cand_overall:
        model_phon = model_overall['phonetics']
        cand_phon = cand_overall['phonetics']

        model_cv = model_phon.get('consonant_vowel_ratio', 0)
        cand_cv = cand_phon.get('consonant_vowel_ratio', 0)

        if model_cv > 0:
            cv_diff = abs(model_cv - cand_cv) / model_cv
            scores['phonetic_similarity'] = max(0, 1 - min(cv_diff, 1))
        else:
            scores['phonetic_similarity'] = 0

    # Calculate weighted total score
    weights = {
        'meter_match': 0.20,
        'syllable_similarity': 0.15,
        'rhyme_density_similarity': 0.15,
        'vocabulary_similarity': 0.10,
        'structure_similarity': 0.15,
        'pos_similarity': 0.10,
        'phonetic_similarity': 0.15
    }

    total_score = sum(scores.get(k, 0) * w for k, w in weights.items())

    return {
        'component_scores': scores,
        'total_score': total_score,
        'max_possible': 1.0
    }


# =============================================================================
# AI CRITIQUE - Structured prompt for LLM-as-judge evaluation
# =============================================================================

def generate_critique_prompt(structure: Dict, model_structure: Optional[Dict] = None,
                             taste_analysis: Optional[Dict] = None) -> str:
    """
    Generate a structured critique prompt for AI evaluation.

    This follows LLM-as-judge best practices:
    - Binary or low-precision scores (1-5 scale)
    - Separate evaluators for each criterion
    - Chain-of-thought reasoning required
    - Structured JSON output

    The AI should complete this prompt and return structured JSON.
    """
    # Flatten lyrics for context
    all_lines = []
    for section in structure.get('sections', []):
        all_lines.extend(section.get('lines', []))

    lyrics_text = '\n'.join(all_lines)

    # Build model context if provided
    model_context = ""
    if model_structure:
        model_lines = []
        for section in model_structure.get('sections', []):
            model_lines.extend(section.get('lines', []))
        model_context = f"""
## MODEL SONG (reference for style/quality)
```
{chr(10).join(model_lines)}
```
"""

    # Build taste metrics context if provided
    taste_context = ""
    if taste_analysis:
        taste_context = f"""
## AUTOMATED TASTE METRICS (already computed)

Overall Taste Score: {taste_analysis.get('overall_taste_score', 0):.1f}/100

Component Scores:
- Concreteness: {taste_analysis.get('component_scores', {}).get('concreteness', 0):.1f}/100
- Cliché-Free: {taste_analysis.get('component_scores', {}).get('cliche_free', 0):.1f}/100
- Show Don't Tell: {taste_analysis.get('component_scores', {}).get('show_dont_tell', 0):.1f}/100
- Sensory Richness: {taste_analysis.get('component_scores', {}).get('sensory_richness', 0):.1f}/100

Automated Recommendations:
{chr(10).join('- ' + r for r in taste_analysis.get('recommendations', []))}
"""

    prompt = f'''# LYRICS CRITIQUE REQUEST

You are an expert lyricist and editor. Evaluate the following lyrics using the structured criteria below. You must provide reasoning before each score.
{model_context}
## CANDIDATE LYRICS (to evaluate)
```
{lyrics_text}
```
{taste_context}

---

## EVALUATION CRITERIA

For each criterion, first explain your reasoning (2-3 sentences), then assign a score.

### 1. IMAGERY & CONCRETENESS (1-5)
Does the song use specific, tangible images? Or vague abstractions?
- 5 = Rich physical imagery throughout (rain on tin roof, calloused hands, smell of diesel)
- 3 = Mixed - some concrete images, some abstract
- 1 = Mostly abstract (love, pain, feelings, things)

### 2. ORIGINALITY (1-5)
Are the phrases fresh? Or are they clichés you've heard a thousand times?
- 5 = Surprising, memorable phrases I've never heard before
- 3 = Some original moments, some familiar territory
- 1 = Wall-to-wall clichés and stock phrases

### 3. EMOTIONAL AUTHENTICITY (1-5)
Does this feel like genuine human experience? Or greeting-card sentiment?
- 5 = Raw, specific, earned emotion
- 3 = Genuine feeling but somewhat generic expression
- 1 = Hollow, sentimental, or performative

### 4. NARRATIVE COHERENCE (1-5)
Does the story/emotion build? Is there an arc?
- 5 = Clear progression with earned resolution/revelation
- 3 = Some structure but meandering or unclear
- 1 = Disconnected ideas, no through-line

### 5. CRAFT (1-5)
Technical skill: meter, rhyme, line breaks, word choice
- 5 = Masterful control of form, every word earns its place
- 3 = Competent but some awkward moments
- 1 = Forced rhymes, broken meter, filler words

### 6. SINGABILITY (1-5)
Would these words feel natural in someone's mouth when sung?
- 5 = Natural phrasing, good vowels on stressed notes
- 3 = Mostly singable with a few awkward spots
- 1 = Tongue-twisters, harsh consonant clusters, unnatural stress

---

## REQUIRED OUTPUT FORMAT

You MUST respond with valid JSON in exactly this format:

```json
{{
  "imagery_concreteness": {{
    "reasoning": "Your 2-3 sentence explanation here",
    "score": 4,
    "examples": ["specific good/bad examples from the lyrics"]
  }},
  "originality": {{
    "reasoning": "Your 2-3 sentence explanation here",
    "score": 3,
    "cliches_found": ["any clichés you noticed"],
    "fresh_phrases": ["any notably original phrases"]
  }},
  "emotional_authenticity": {{
    "reasoning": "Your 2-3 sentence explanation here",
    "score": 4
  }},
  "narrative_coherence": {{
    "reasoning": "Your 2-3 sentence explanation here",
    "score": 3,
    "arc_description": "Brief description of the narrative arc"
  }},
  "craft": {{
    "reasoning": "Your 2-3 sentence explanation here",
    "score": 4,
    "weak_spots": ["any awkward lines or forced rhymes"]
  }},
  "singability": {{
    "reasoning": "Your 2-3 sentence explanation here",
    "score": 4
  }},
  "overall_score": 3.7,
  "verdict": "REVISE|POLISH|READY",
  "top_3_improvements": [
    "Most important revision needed",
    "Second priority",
    "Third priority"
  ],
  "strongest_lines": ["Quote 1-3 of the best lines"],
  "weakest_lines": ["Quote 1-3 lines that need the most work"]
}}
```

Verdict meanings:
- REVISE = Major issues, needs significant rewriting
- POLISH = Good bones, needs line-level improvements
- READY = Publication quality, only minor tweaks if any

Now evaluate the candidate lyrics above.
'''

    return prompt


def compare_against_model(model_file: Path, candidate_files: List[Path]) -> Dict:
    """Compare candidate lyrics against a model song."""

    # Load and analyze model
    print(f"Analyzing model: {model_file}")
    model_text = model_file.read_text()
    model_structure = parse_lyrics_to_structure(model_text)
    model_analysis = full_analysis(model_structure)

    # Analyze each candidate
    results = []
    for cand_file in candidate_files:
        print(f"Analyzing candidate: {cand_file}")
        cand_text = cand_file.read_text()
        cand_structure = parse_lyrics_to_structure(cand_text)
        cand_analysis = full_analysis(cand_structure)

        similarity = compute_similarity_score(model_analysis, cand_analysis)

        results.append({
            'file': str(cand_file),
            'similarity': similarity,
            'analysis': cand_analysis
        })

    # Rank by total score
    results.sort(key=lambda x: x['similarity']['total_score'], reverse=True)

    # Add rankings
    for i, result in enumerate(results):
        result['rank'] = i + 1

    return {
        'model': {
            'file': str(model_file),
            'analysis': model_analysis
        },
        'candidates': results,
        'ranking_summary': [
            {
                'rank': r['rank'],
                'file': r['file'],
                'score': r['similarity']['total_score']
            }
            for r in results
        ]
    }


# =============================================================================
# CLI
# =============================================================================

def cmd_parse(args):
    """Parse dirty lyrics to structured YAML."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1

    input_text = input_path.read_text()
    structure = parse_lyrics_to_structure(input_text)

    output_path = Path(args.output) if args.output else input_path.with_suffix('.yaml')

    with open(output_path, 'w') as f:
        yaml.dump(structure, f, default_flow_style=False, sort_keys=False)

    print(f"Parsed structure written to: {output_path}")
    print(f"  Sections: {len(structure['sections'])}")
    print(f"  Section order: {' -> '.join(structure['section_order'])}")

    return 0


def cmd_analyze(args):
    """Analyze lyrics from YAML or text file."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1

    # Load input
    if input_path.suffix in ['.yaml', '.yml']:
        with open(input_path) as f:
            structure = yaml.safe_load(f)
    else:
        # Assume text file
        input_text = input_path.read_text()
        structure = parse_lyrics_to_structure(input_text)

    # Perform analysis
    print(f"Analyzing: {input_path}")
    analysis = full_analysis(structure)

    # Output
    output_path = Path(args.output) if args.output else input_path.with_suffix('.analysis.json')

    with open(output_path, 'w') as f:
        json.dump(analysis, f, indent=2)

    # Print summary
    overall = analysis.get('overall', {})
    print(f"\nAnalysis written to: {output_path}")
    print(f"\nSummary:")
    print(f"  Total lines: {overall.get('total_lines', 0)}")

    if 'meter' in overall:
        meter = overall['meter']
        print(f"  Dominant meter: {meter.get('dominant_meter', 'unknown')}")
        print(f"  Avg syllables/line: {meter.get('avg_syllables_per_line', 0):.1f}")

    if 'rhyme' in overall:
        rhyme = overall['rhyme']
        print(f"  Rhyme scheme: {rhyme.get('scheme_string', '')[:20]}...")
        print(f"  Rhyme density: {rhyme.get('rhyme_density', 0):.2f}")

    if 'vocabulary' in overall:
        vocab = overall['vocabulary']
        print(f"  Vocabulary richness (TTR): {vocab.get('type_token_ratio', 0):.2f}")
        print(f"  Total words: {vocab.get('total_words', 0)}")

    return 0


def cmd_compare(args):
    """Compare candidate lyrics against a model."""
    model_path = Path(args.model)
    if not model_path.exists():
        print(f"Error: Model file not found: {model_path}")
        return 1

    candidate_paths = [Path(p) for p in args.candidates]
    missing = [p for p in candidate_paths if not p.exists()]
    if missing:
        print(f"Error: Candidate files not found: {missing}")
        return 1

    # Perform comparison
    results = compare_against_model(model_path, candidate_paths)

    # Output
    output_path = Path(args.output) if args.output else Path('comparison_report.json')

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nComparison report written to: {output_path}")
    print(f"\nRanking (best match to model):")
    print("-" * 50)
    for item in results['ranking_summary']:
        print(f"  #{item['rank']}: {Path(item['file']).name} (score: {item['score']:.3f})")

    return 0


def cmd_taste(args):
    """Compute taste metrics for lyrics."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1

    # Load input
    if input_path.suffix in ['.yaml', '.yml']:
        with open(input_path) as f:
            structure = yaml.safe_load(f)
    else:
        input_text = input_path.read_text()
        structure = parse_lyrics_to_structure(input_text)

    # Perform taste analysis
    print(f"Analyzing taste metrics: {input_path}")
    taste = full_taste_analysis(structure)

    # Output
    output_path = Path(args.output) if args.output else input_path.with_suffix('.taste.json')

    with open(output_path, 'w') as f:
        json.dump(taste, f, indent=2)

    # Print summary
    print(f"\nTaste analysis written to: {output_path}")
    print(f"\n{'='*50}")
    print(f"OVERALL TASTE SCORE: {taste.get('overall_taste_score', 0):.1f}/100")
    print(f"{'='*50}")

    scores = taste.get('component_scores', {})
    print(f"\nComponent Scores:")
    print(f"  Concreteness:    {scores.get('concreteness', 0):5.1f}/100")
    print(f"  Cliché-Free:     {scores.get('cliche_free', 0):5.1f}/100")
    print(f"  Show Don't Tell: {scores.get('show_dont_tell', 0):5.1f}/100")
    print(f"  Sensory Richness:{scores.get('sensory_richness', 0):5.1f}/100")

    print(f"\nRecommendations:")
    for rec in taste.get('recommendations', []):
        print(f"  • {rec}")

    return 0


def cmd_critique(args):
    """Generate AI critique prompt for lyrics."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1

    # Load input
    if input_path.suffix in ['.yaml', '.yml']:
        with open(input_path) as f:
            structure = yaml.safe_load(f)
    else:
        input_text = input_path.read_text()
        structure = parse_lyrics_to_structure(input_text)

    # Optionally load model
    model_structure = None
    if args.model:
        model_path = Path(args.model)
        if model_path.exists():
            if model_path.suffix in ['.yaml', '.yml']:
                with open(model_path) as f:
                    model_structure = yaml.safe_load(f)
            else:
                model_structure = parse_lyrics_to_structure(model_path.read_text())

    # Optionally include taste analysis
    taste_analysis = None
    if args.include_taste:
        print(f"Computing taste metrics...")
        taste_analysis = full_taste_analysis(structure)

    # Generate prompt
    prompt = generate_critique_prompt(structure, model_structure, taste_analysis)

    # Output
    output_path = Path(args.output) if args.output else input_path.with_suffix('.critique.md')

    with open(output_path, 'w') as f:
        f.write(prompt)

    print(f"\nCritique prompt written to: {output_path}")
    print(f"\nTo use this prompt:")
    print(f"  1. Copy the contents of {output_path}")
    print(f"  2. Paste into Claude, ChatGPT, or your preferred LLM")
    print(f"  3. The AI will return structured JSON evaluation")
    print(f"  4. Use the evaluation to guide revisions")

    if args.include_taste:
        print(f"\n  Taste metrics included in prompt context.")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Lyrics Analyzer - Parse, analyze, and compare song lyrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse dirty lyrics to structured YAML
  python lyrics_analyzer.py parse --input raw_lyrics.txt --output structured.yaml

  # Analyze lyrics quantitatively
  python lyrics_analyzer.py analyze --input lyrics.txt --output analysis.json

  # Compare candidates against a model song
  python lyrics_analyzer.py compare --model model.txt --candidates song1.txt song2.txt --output report.json
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse dirty lyrics to structured YAML')
    parse_parser.add_argument('--input', '-i', required=True, help='Input lyrics file (dirty)')
    parse_parser.add_argument('--output', '-o', help='Output YAML file')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze lyrics quantitatively')
    analyze_parser.add_argument('--input', '-i', required=True, help='Input lyrics file (YAML or text)')
    analyze_parser.add_argument('--output', '-o', help='Output analysis JSON file')

    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare candidates against model')
    compare_parser.add_argument('--model', '-m', required=True, help='Model lyrics file')
    compare_parser.add_argument('--candidates', '-c', nargs='+', required=True, help='Candidate lyrics files')
    compare_parser.add_argument('--output', '-o', help='Output report JSON file')
    compare_parser.add_argument('-n', type=int, help='(For documentation) Number of candidates expected')

    # Taste command
    taste_parser = subparsers.add_parser('taste', help='Compute taste/quality metrics')
    taste_parser.add_argument('--input', '-i', required=True, help='Input lyrics file (YAML or text)')
    taste_parser.add_argument('--output', '-o', help='Output taste analysis JSON file')

    # Critique command
    critique_parser = subparsers.add_parser('critique', help='Generate AI critique prompt')
    critique_parser.add_argument('--input', '-i', required=True, help='Input lyrics file to critique')
    critique_parser.add_argument('--model', '-m', help='Optional model lyrics for comparison')
    critique_parser.add_argument('--output', '-o', help='Output markdown file for prompt')
    critique_parser.add_argument('--include-taste', '-t', action='store_true',
                                 help='Include automated taste metrics in prompt')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    if args.command == 'parse':
        return cmd_parse(args)
    elif args.command == 'analyze':
        return cmd_analyze(args)
    elif args.command == 'compare':
        return cmd_compare(args)
    elif args.command == 'taste':
        return cmd_taste(args)
    elif args.command == 'critique':
        return cmd_critique(args)

    return 0


if __name__ == '__main__':
    sys.exit(main())
