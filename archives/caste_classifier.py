#!/usr/bin/env python3
"""
Agentic Caste Classifier v3
============================
Processes ALL unique names from APCRDA data through GPT-5.4-mini.
- Step 1: Local directory lookup (5,856 surnames)
- Step 2: LLM classification for all names (with existing knowledge as context)
- Step 3: Flag conflicts between LLM and directory
- Step 4: Update directory with new findings

Usage: OPENAI_API_KEY=sk-... python caste_classifier.py
"""

import csv
import json
import os
import time
from collections import Counter, defaultdict
from datetime import datetime

from openai import OpenAI

# ─── Config ──────────────────────────────────────────────────────────────────
MODEL = "gpt-5.4-mini"
BATCH_SIZE = 20
DATA_DIR = "data"
MAPPING_FILE = f"{DATA_DIR}/caste_surname_map.json"
CSV_FILE = f"{DATA_DIR}/surname_caste_directory.csv"
OUTPUT_DIR = "data"
RESULTS_FILE = f"{OUTPUT_DIR}/llm_classification_results.json"
CONFLICTS_FILE = f"{OUTPUT_DIR}/llm_conflicts.csv"

SYSTEM_PROMPT = """You classify names from official land records in the Amaravati Capital Region (Krishna-Guntur districts, Andhra Pradesh, India). These are Telugu-speaking people from the Vijayawada-Guntur region.

For each name, determine:

1. name_type: "person" or "non_person"
   - "person": a human name (even if you can't identify the caste)
   - "non_person": business name, institution, government label, data artifact, place name

2. extracted_surname: The surname/family name you identified
   - Telugu convention: surname usually comes FIRST (e.g., "ALURI VENKATA RAO" → surname is ALURI)
   - Sometimes the order is reversed (Western style): "VENKATA RAO ALURI" → surname is still ALURI
   - If only an initial (A., K.), set to null — can't determine surname from an initial
   - If the name is a single word that's clearly a first name (RAMESH, LAKSHMI), set to null
   - Set to null for non_person entries

3. caste: The caste community this surname is most commonly associated with in the Krishna-Guntur region
   - Categories: Kamma, Kapu, Reddy, Brahmin, Vysya, Muslim, SC, ST, Velama, Kshatriya, Yadava, Christian, Other, Unknown
   - Use caste indicators in the name: "Reddy" suffix → Reddy, "Naidu"/"Chowdary" → Kamma, "Setty"/"Setti" → Vysya
   - If you genuinely cannot determine, use "Unknown"
   - Set to null for non_person entries

4. confidence: "high", "medium", or "low"
   - high: you are certain (well-known surname-caste association, or clear caste suffix)
   - medium: likely but not 100% certain
   - low: educated guess
   - Set to null for non_person entries

5. reasoning: Brief explanation (1-2 sentences max)

Return a JSON object: {"results": [...]}"""


def get_all_unique_names():
    """Extract all unique full names from processed data."""
    from build_report import process_data
    plots = process_data()

    names = {}  # name -> {caste from pipeline, count}
    for p in plots:
        for ind in p['individuals']:
            name = ind['name'].strip()
            if name not in names:
                names[name] = {
                    'pipeline_caste': ind['caste'],
                    'pipeline_confidence': ind['confidence'],
                    'count': 0,
                }
            names[name]['count'] += 1

    return names


def classify_batch(client, batch_names):
    """Send a batch of names to the LLM."""
    names_text = "\n".join(f"- {n}" for n in batch_names)

    prompt = (
        'Classify each name below. Return a JSON object with a "results" key '
        'containing an array. Each item: '
        '{"name": "...", "name_type": "person|non_person", "extracted_surname": "...|null", '
        '"caste": "...|null", "confidence": "high|medium|low|null", "reasoning": "..."}\n\n'
        'Names:\n' + names_text
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        result = json.loads(content)

        # Extract array from response
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            for v in result.values():
                if isinstance(v, list):
                    return v
        return []
    except Exception as e:
        print(f"  API error: {e}")
        return []


def main():
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Error: Set OPENAI_API_KEY environment variable")
        return

    client = OpenAI(api_key=api_key)
    start_time = time.time()

    # Load existing directory
    with open(MAPPING_FILE) as f:
        mapping = json.load(f)
    existing_surnames = mapping['surnames']

    # Get all unique names
    print("Loading all unique names from processed data...")
    all_names = get_all_unique_names()
    name_list = sorted(all_names.keys())
    print(f"Total unique names: {len(name_list):,}", flush=True)

    # Process in batches
    all_results = []
    total_batches = (len(name_list) + BATCH_SIZE - 1) // BATCH_SIZE
    errors = 0

    print(f"\nProcessing {len(name_list):,} names in {total_batches} batches of {BATCH_SIZE}...")
    print(f"Model: {MODEL}")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}\n")

    for i in range(0, len(name_list), BATCH_SIZE):
        batch = name_list[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1

        results = classify_batch(client, batch)
        all_results.extend(results)

        if batch_num % 10 == 0 or batch_num == total_batches:
            elapsed = time.time() - start_time
            rate = batch_num / elapsed * 60
            eta = (total_batches - batch_num) / rate if rate > 0 else 0
            print(f"  Batch {batch_num}/{total_batches}  |  {len(all_results):,} results  |  {rate:.0f} batches/min  |  ETA: {eta:.0f} min", flush=True)

        if not results:
            errors += 1
            if errors > 10:
                print("Too many consecutive errors, stopping.")
                break
        else:
            errors = 0

        time.sleep(0.3)  # Rate limiting

    elapsed = time.time() - start_time
    print(f"\nDone in {elapsed/60:.1f} minutes. Got {len(all_results):,} results.")

    # ─── Analyze Results ─────────────────────────────────────────────────
    # Normalize caste names
    CASTE_NORMALIZE = {
        'kamma': 'Kamma', 'kapu': 'Kapu', 'reddy': 'Reddy',
        'brahmin': 'Brahmin', 'vysya': 'Vysya', 'muslim': 'Muslim',
        'sc': 'SC', 'st': 'ST', 'velama': 'Velama',
        'kshatriya': 'Kshatriya', 'yadava': 'Yadava',
        'christian': 'Christian', 'other': 'Other', 'unknown': 'Unknown',
        'balija': 'Kapu', 'telaga': 'Kapu', 'naidu': 'Kamma',
        'komati': 'Vysya', 'kamsali': 'Other', 'mala': 'SC', 'madiga': 'SC',
        'scheduled caste': 'SC', 'scheduled tribe': 'ST',
    }

    new_surnames = 0
    new_not_surnames = 0
    conflicts = []
    non_persons = 0
    unknown_after_llm = 0
    caste_counts = Counter()

    for item in all_results:
        name = item.get('name', '').strip()
        name_type = item.get('name_type', 'person')
        surname = item.get('extracted_surname')
        caste_raw = item.get('caste')
        confidence = item.get('confidence', 'low')
        reasoning = item.get('reasoning', '')

        if confidence not in ('high', 'medium', 'low'):
            confidence = 'low'

        # Normalize caste
        caste = None
        if caste_raw and str(caste_raw).lower() not in ('null', 'none', ''):
            caste = CASTE_NORMALIZE.get(str(caste_raw).lower().strip(), str(caste_raw).strip())

        if name_type == 'non_person':
            non_persons += 1
            # Add to not_surnames if it has a surname-like token
            if surname and surname.upper() not in mapping['not_surnames']:
                mapping['not_surnames'].append(surname.upper())
                new_not_surnames += 1
            continue

        if not surname:
            unknown_after_llm += 1
            continue

        surname_upper = surname.upper()

        # Check for conflict with existing directory
        if surname_upper in existing_surnames:
            existing_caste = existing_surnames[surname_upper]['caste']
            if caste and caste != 'Unknown' and caste != existing_caste:
                conflicts.append({
                    'name': name,
                    'surname': surname_upper,
                    'directory_caste': existing_caste,
                    'llm_caste': caste,
                    'llm_confidence': confidence,
                    'reasoning': reasoning,
                })
        elif caste and caste != 'Unknown':
            # New surname not in directory
            mapping['surnames'][surname_upper] = {
                'caste': caste,
                'confidence': confidence,
            }
            new_surnames += 1
            caste_counts[caste] += 1
        else:
            unknown_after_llm += 1

    # ─── Save Results ────────────────────────────────────────────────────
    # Save full LLM results
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    # Save conflicts
    with open(CONFLICTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'surname', 'directory_caste', 'llm_caste', 'llm_confidence', 'reasoning'])
        for c in conflicts:
            writer.writerow([c['name'], c['surname'], c['directory_caste'],
                           c['llm_caste'], c['llm_confidence'], c['reasoning']])

    # Update mapping JSON
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    # Regenerate CSV directory
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['surname', 'caste', 'confidence'])
        for surname, info in sorted(mapping['surnames'].items()):
            writer.writerow([surname, info['caste'], info['confidence']])

    # ─── Summary ─────────────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print(f"  CASTE CLASSIFIER RESULTS")
    print(f"{'='*55}")
    print(f"  Names processed:        {len(all_results):,}")
    print(f"  Persons identified:     {len(all_results) - non_persons:,}")
    print(f"  Non-persons flagged:    {non_persons:,}")
    print(f"  New surnames added:     {new_surnames:,}")
    print(f"  New not-surnames:       {new_not_surnames:,}")
    print(f"  Conflicts found:        {len(conflicts):,}")
    print(f"  Still unknown:          {unknown_after_llm:,}")
    print(f"  Total surnames now:     {len(mapping['surnames']):,}")
    print(f"{'='*55}")

    if caste_counts:
        print(f"\n  New surnames by caste:")
        for caste, count in caste_counts.most_common():
            print(f"    {caste:<15} {count:,}")

    if conflicts:
        print(f"\n  Conflicts (directory vs LLM):")
        print(f"  Saved to: {CONFLICTS_FILE}")
        for c in conflicts[:10]:
            print(f"    {c['surname']}: directory={c['directory_caste']}, LLM={c['llm_caste']} ({c['llm_confidence']})")
        if len(conflicts) > 10:
            print(f"    ... and {len(conflicts) - 10} more")

    print(f"\n  Files updated:")
    print(f"    {MAPPING_FILE}")
    print(f"    {CSV_FILE}")
    print(f"    {RESULTS_FILE}")
    print(f"    {CONFLICTS_FILE}")
    print(f"\n  Time: {elapsed/60:.1f} minutes")


if __name__ == '__main__':
    main()
