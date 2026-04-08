#!/usr/bin/env python3
"""Test Gemini 3.1 Pro on the 40 sample conflicted names."""
from google import genai
from google.genai import types
import os, json, time

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
MODEL = "gemini-2.5-flash"

SYSTEM = """You are an expert on caste demographics in the Krishna-Guntur region of Andhra Pradesh, India. You have deep knowledge of Telugu naming conventions and which surnames and name patterns belong to which caste communities.

You will be given a set of full names of land beneficiaries from official APCRDA (Amaravati Capital Region) land records. These are real people who own land in villages around Vijayawada and Guntur.

For each person, determine their most likely caste community. Use EVERYTHING in the name — surname, given names, caste suffixes, honorifics, all of it.

Key facts you know:
- Telugu names typically have surname FIRST: "ALURI VENKATA RAO" = surname ALURI
- Caste suffixes: Reddy/Reddi = Reddy caste. Chowdary/Choudary/Chodary = Kamma. Setty/Setti/Shetty = Vysya.
- Naidu can be Kamma OR Kapu (context-dependent). Raju can be Kshatriya or just a name.
- Some surnames are shared across castes. In that case, look at the full name for additional signals.
- If a surname is genuinely used by multiple castes and there are no other signals, pick the MOST COMMON one in the Krishna-Guntur region.
- Christian given names (Israel, John, Mary, David, Glory, Jerusalem) suggest the person is Christian regardless of surname caste.
- Muslim given names (Mohammad, Noor, Ahmed) suggest Muslim regardless of surname caste.
- Deity names in given names can be signals: Vasavi = Vysya community deity.
- These are landowners in rural villages near Amaravati. Think about which communities historically owned agricultural land in this specific region.

Be decisive. Do not hedge with "Unknown" unless you truly have no basis for even a guess.

Return ONLY valid JSON: {"results": [{"name": "...", "caste": "...", "confidence": "high/medium/low", "reasoning": "..."}]}

Categories: Kamma, Kapu, Reddy, Brahmin, Vysya, Muslim, SC, ST, Velama, Kshatriya, Yadava, Christian, Other"""

test_cases = [
    ("CHAGANTI", [("CHAGANTI VENKATRAO","Nowlur"),("CHAGANTI RAMAKOTESWARA RAO","Kuragallu"),("CHAGANTI APARNA","Nekkallu"),("CHAGANTI LAKSHMI NAIDU","Velagapudi")]),
    ("SUNKARA", [("Sunkara Lakshmi","Gannavaram"),("SUNKARA SAMBASIVARAO","Nowlur"),("SUNKARA VENKATA SRINIVASA RAO","Nidamarru"),("SUNKARA GRUHA LAKSHMI","Venkatapalem")]),
    ("GADE", [("Gade Sudhakar Reddy","Nidamarru"),("GADE BAPAMMA","Nidamarru"),("GADE SAMBIREDDY","Nidamarru"),("GADE UMAMAHESWAR REDDY","Nidamarru")]),
    ("CHALASANI", [("CHALASANI ANIL KUMAR","Kuragallu"),("CHALASANI RATNA MANIKYAM","Venkatapalem"),("Chalasani Aswinidutt","Gannavaram"),("CHALASANI RAMAKRISHNA","Krishnayapalem")]),
    ("DASARI", [("Dasari Durga Prasad","Thullur"),("DASARI VENKATESWARARAO","Nekkallu"),("DASARI KISHORE KUMAR","Ananthavaram"),("DASARI JERUSALEM KUMARI","Nowlur")]),
    ("MADALA", [("MADALA RAMESH BABU","Kuragallu"),("Madala Venkateswara Rao","Kuragallu"),("MADALA TIRUMALA","Nelapadu"),("MADALA VASUDEVARAO","Kuragallu")]),
    ("GADDAM", [("Gaddam Vasavi Sowjanya","Mandadam"),("GADDAM PRANAV REDDY","Mandadam"),("GADDAM THIRUPATHI RAO","Ananthavaram"),("GADDAM GLORY RAMBABU","Mandadam")]),
    ("MALLELA", [("MALLELA MANIKYA GOPALA KRISHNA","Kondamarajupalem"),("MALLELA VENKATA RAYUDU","Rayapudi"),("MALLELA SRINADH CHODARY","Rayapudi"),("MALLELA SRIDHAR","Rayapudi")]),
    ("KADIYALA", [("KADIYALA RAVI","Gannavaram"),("KADIYALA LAVANYA","Ananthavaram"),("KADIYALA PRAMELA RANI","Mandadam"),("KADIYALA SAMBASIVARAO","Venkatapalem")]),
    ("KOLLA", [("KOLLA SRINIVASA RAO","Thullur"),("KOLLA YUGANDHAR","Lingayapalem"),("KOLLA SARATH BABU","Mandadam"),("KOLLA KRISHNAVENI","Thullur")]),
]

total_time = 0
for surname, names in test_cases:
    names_text = "\n".join(f"- {n} (village: {v})" for n, v in names)
    prompt = f"These are landowners in the Amaravati Capital Region with surname {surname}. Classify each:\n\n{names_text}"

    start = time.time()
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            temperature=0.1,
            response_mime_type="application/json",
        ),
    )
    elapsed = time.time() - start
    total_time += elapsed

    content = response.text
    # Parse JSON
    try:
        result = json.loads(content)
        items = result.get("results", result) if isinstance(result, dict) else result
    except:
        print(f"\n{surname}: ({elapsed:.1f}s) PARSE ERROR")
        print(f"  Raw: {content[:200]}")
        continue

    print(f"\n{surname}: ({elapsed:.1f}s)")
    for item in items:
        name = item.get("name", "?")
        caste = item.get("caste", "?")
        conf = item.get("confidence", "?")
        reasoning = item.get("reasoning", "")
        print(f"  {name:<45} -> {caste:<12} ({conf})")
        print(f"     {reasoning[:80]}")

    time.sleep(1)  # Rate limit

print(f"\n{'=' * 80}")
print(f"Model: {MODEL}")
print(f"Total time: {total_time:.0f}s ({total_time/40:.1f}s per name)")
print(f"Projected for 30,444 names (batches of 4): {total_time/10 * (30444/4) / 3600:.1f} hours")
print(f"Cost: Free tier / very cheap")
