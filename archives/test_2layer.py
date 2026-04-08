#!/usr/bin/env python3
"""Test 2-layer agent system on 40 sample names."""
from openai import OpenAI
import os, json, time

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

SYSTEM_PRIMARY = """You are the primary classifier for Telugu names from the Krishna-Guntur region of Andhra Pradesh. You classify land beneficiary names from APCRDA (Amaravati Capital Region) records.

For each name, determine:
- name_type: "person" or "non_person"
- caste: Kamma, Kapu, Reddy, Brahmin, Vysya, Muslim, SC, ST, Velama, Kshatriya, Yadava, Christian, Other, Unknown
- confidence: "high", "medium", or "low"
- needs_escalation: true/false
- reasoning: brief explanation

WHEN TO ESCALATE (needs_escalation = true):
- Your confidence is "low" on a person
- You are about to assign "Other" or "Unknown" — ALWAYS escalate these instead
- The surname is known to be shared across multiple castes (e.g., Dasari, Gaddam, Mallela, Chaganti, Kadiyala, Madala, Kolla, Gade)
- The given name has unusual or subtle signals you are not 100% sure about (deity names, uncommon patterns)
- You would classify it differently depending on interpretation
- The surname could be Brahmin OR Kamma (many coastal AP surnames overlap)

WHEN NOT TO ESCALATE:
- Clear caste suffix: Reddy, Chowdary/Chodary -> Kamma, Setty/Setti -> Vysya
- Clear Christian name (Israel, John, Mary, Glory, Jerusalem, David)
- Clear Muslim name (Mohammad, Noor, Ahmed, Basha)
- Well-known unambiguous surname with high confidence

IMPORTANT: Do NOT use "Other" as a dump category. If you are unsure, ESCALATE. "Other" means you positively know the person belongs to a community outside the listed categories (e.g., Marwari, Jain, Parsi). It does NOT mean "I don't know".

Telugu convention: surname comes FIRST. These are landowners in rural villages near Amaravati.

Return JSON: {"results": [{"name": "...", "name_type": "person", "caste": "...", "confidence": "...", "needs_escalation": true/false, "reasoning": "..."}]}"""

SYSTEM_SECONDARY = """You are the senior expert reviewer for Telugu caste classification in the Krishna-Guntur region of Andhra Pradesh. The primary classifier was unsure about these names and escalated them to you.

You have deeper knowledge of:
- Subtle given-name signals (deity names like Vasavi = Vysya community deity, naming patterns)
- Historical surname-caste associations: e.g., Chaganti is primarily Brahmin in coastal Andhra, Chalasani is Kamma (derived from a Kamma ruler), Dasari is predominantly SC/Mala in Krishna-Guntur
- Surnames shared across castes: when no suffix helps, use the MOST COMMON association in the specific Krishna-Guntur agricultural belt
- Christian and Muslim given name patterns in Telugu families
- Regional landholding patterns in the Amaravati Capital Region villages

You MUST make a decision. The primary already tried and failed — you are the last stop. Pick the most likely caste even if confidence is medium. Only use "Unknown" if the name is truly unclassifiable (single initials, gibberish, etc.).

Return JSON: {"results": [{"name": "...", "caste": "...", "confidence": "...", "reasoning": "..."}]}

Categories: Kamma, Kapu, Reddy, Brahmin, Vysya, Muslim, SC, ST, Velama, Kshatriya, Yadava, Christian, Other"""

all_names = [
    ("CHAGANTI VENKATRAO","Nowlur"),("CHAGANTI RAMAKOTESWARA RAO","Kuragallu"),
    ("CHAGANTI APARNA","Nekkallu"),("CHAGANTI LAKSHMI NAIDU","Velagapudi"),
    ("Sunkara Lakshmi","Gannavaram"),("SUNKARA SAMBASIVARAO","Nowlur"),
    ("SUNKARA VENKATA SRINIVASA RAO","Nidamarru"),("SUNKARA GRUHA LAKSHMI","Venkatapalem"),
    ("Gade Sudhakar Reddy","Nidamarru"),("GADE BAPAMMA","Nidamarru"),
    ("GADE SAMBIREDDY","Nidamarru"),("GADE UMAMAHESWAR REDDY","Nidamarru"),
    ("CHALASANI ANIL KUMAR","Kuragallu"),("CHALASANI RATNA MANIKYAM","Venkatapalem"),
    ("Chalasani Aswinidutt","Gannavaram"),("CHALASANI RAMAKRISHNA","Krishnayapalem"),
    ("Dasari Durga Prasad","Thullur"),("DASARI VENKATESWARARAO","Nekkallu"),
    ("DASARI KISHORE KUMAR","Ananthavaram"),("DASARI JERUSALEM KUMARI","Nowlur"),
    ("MADALA RAMESH BABU","Kuragallu"),("Madala Venkateswara Rao","Kuragallu"),
    ("MADALA TIRUMALA","Nelapadu"),("MADALA VASUDEVARAO","Kuragallu"),
    ("Gaddam Vasavi Sowjanya","Mandadam"),("GADDAM PRANAV REDDY","Mandadam"),
    ("GADDAM THIRUPATHI RAO","Ananthavaram"),("GADDAM GLORY RAMBABU","Mandadam"),
    ("MALLELA MANIKYA GOPALA KRISHNA","Kondamarajupalem"),("MALLELA VENKATA RAYUDU","Rayapudi"),
    ("MALLELA SRINADH CHODARY","Rayapudi"),("MALLELA SRIDHAR","Rayapudi"),
    ("KADIYALA RAVI","Gannavaram"),("KADIYALA LAVANYA","Ananthavaram"),
    ("KADIYALA PRAMELA RANI","Mandadam"),("KADIYALA SAMBASIVARAO","Venkatapalem"),
    ("KOLLA SRINIVASA RAO","Thullur"),("KOLLA YUGANDHAR","Lingayapalem"),
    ("KOLLA SARATH BABU","Mandadam"),("KOLLA KRISHNAVENI","Thullur"),
]

# STEP 1: Primary (5.4-mini)
print("STEP 1: Primary Agent (gpt-5.4-mini)")
print("=" * 80)

primary_results = []
for i in range(0, len(all_names), 20):
    batch = all_names[i:i+20]
    names_text = "\n".join(f"- {n} (village: {v})" for n, v in batch)
    resp = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PRIMARY},
            {"role": "user", "content": f"Classify these Amaravati land beneficiaries:\n\n{names_text}"},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    items = json.loads(resp.choices[0].message.content).get("results", [])
    primary_results.extend(items)
    time.sleep(0.3)

escalated = []
resolved = []
for item in primary_results:
    esc = item.get("needs_escalation", False)
    tag = "ESC" if esc else "OK "
    print(f'  [{tag}] {item["name"]:<45} -> {item["caste"]:<12} ({item["confidence"]})')
    if esc:
        escalated.append(item)
    else:
        resolved.append(item)

print(f"\nResolved: {len(resolved)}/40  |  Escalated: {len(escalated)}/40")

# STEP 2: Secondary (5.4)
if escalated:
    print(f"\nSTEP 2: Secondary Agent (gpt-5.4) - {len(escalated)} names")
    print("=" * 80)

    esc_text = "\n".join(
        f'- {item["name"]} (primary said: {item["caste"]}, confidence: {item["confidence"]}. Reason: {item["reasoning"]})'
        for item in escalated
    )

    resp2 = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {"role": "system", "content": SYSTEM_SECONDARY},
            {"role": "user", "content": f"The primary classifier escalated these {len(escalated)} names:\n\n{esc_text}"},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    secondary_results = json.loads(resp2.choices[0].message.content).get("results", [])

    for item in secondary_results:
        primary_caste = next((e["caste"] for e in escalated if e["name"] == item["name"]), "?")
        changed = "CHANGED" if item["caste"] != primary_caste else "AGREED "
        print(f'  [{changed}] {item["name"]:<45} {primary_caste:<8} -> {item["caste"]:<12} ({item["confidence"]})')
        print(f'           {item["reasoning"]}')

escalation_pct = 100 * len(escalated) / len(primary_results) if primary_results else 0
print(f"\n{'=' * 80}")
print(f"SUMMARY")
print(f"{'=' * 80}")
print(f"Total names:     {len(primary_results)}")
print(f"Resolved (mini): {len(resolved)} ({100-escalation_pct:.0f}%)")
print(f"Escalated (5.4): {len(escalated)} ({escalation_pct:.0f}%)")

# Cost projection for full 30K names
full_names = 30444
est_escalated = int(full_names * escalation_pct / 100)
est_resolved = full_names - est_escalated
mini_cost = est_resolved / 20 * (1100/1e6*0.4 + 3000/1e6*1.6)
big_cost = est_escalated / 20 * (1100/1e6*5.0 + 3000/1e6*15.0)
print(f"\nProjected cost for all {full_names:,} names:")
print(f"  Mini ({est_resolved:,} names): ${mini_cost:.2f}")
print(f"  5.4  ({est_escalated:,} names): ${big_cost:.2f}")
print(f"  TOTAL: ${mini_cost + big_cost:.2f}")
print(f"  (vs ${77:.2f} if all through 5.4)")
