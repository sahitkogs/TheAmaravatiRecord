# AP Scheduled Castes — Surname Data Enrichment Plan

## Objective

Enrich an existing spreadsheet of Andhra Pradesh Scheduled Caste sub-castes with **real-world surnames (intiperu / family names)** by scraping and extracting name + caste data from publicly available sources.

The existing file (`AP_Scheduled_Castes_Surnames.xlsx`) has 4 sheets organized by the 2025 SC sub-classification groups:
- **Group 1 — Most Backward** (12 sub-castes, 1% reservation)
- **Group 2 — Madiga Group** (18 sub-castes, 6.5% reservation)
- **Group 3 — Mala Group** (29 sub-castes, 7.5% reservation)
- **Summary**

Each sheet has columns: S.No, Sub-Caste, Variants, Population, Surnames/Family Names, Lineages/Clans, Region, Traditional Occupation, Notes.

**Goal**: Populate the "Surnames/Family Names" column with real surnames extracted from public data, and optionally add a new sheet with raw extracted records (Full Name, Surname, Caste, Sub-Caste, Source, Constituency/Context).

---

## Background: How Telugu SC Surnames Work

In Telugu naming, a person's full name follows: **Intiperu (family name) + Given Name + [Caste suffix (optional)]**

- The **intiperu** (house name) is the surname — typically place-based or lineage-based (e.g., Gollapalli, Audimulapu, Mannepakula).
- Some people use the **caste name itself** as a surname (e.g., Madiga, Mala).
- Many SC individuals use **caste-neutral surnames** like Kumar, Babu, Prasad, Rao.
- The intiperu almost always comes **first** in Telugu names displayed in official records.

**Extraction rule**: In a name like "GOLLAPALLI SURYA RAO", the surname is **GOLLAPALLI** (first word). In "DR DASARI SUDHA", the surname is **DASARI** (skip honorifics like Dr/Sri/Smt).

---

## Data Sources (Ranked by Value)

### Source 1: Party Candidate Lists with Caste (HIGHEST VALUE)

**Why**: These PDFs explicitly list `Candidate Name | Caste Category | Specific Caste` (e.g., "Mala" or "Madiga").

**Known URLs**:
- YSRCP 2024: `https://images.assettype.com/thenewsminute/2024-03/46e8ac51-2b26-4364-b51a-a9c660b98dfa/YSRCP_Assembly_election_candidates_2024.pdf`
- Search for TDP, JSP, BJP, Congress candidate lists for AP 2024 with caste details.
- Search for 2019 AP election candidate lists with caste.

**What to extract**: For each SC-category candidate:
- Full Name
- Surname (first word of name, skipping honorifics)
- Specific caste (Mala, Madiga, etc.)
- Constituency
- Party
- Year

**Already extracted from YSRCP 2024** (29 SC candidates):

| Surname | Caste | Constituency |
|---------|-------|-------------|
| Tale | Mala | Rajam |
| Kambala | Mala | Payakaraopet |
| Alajangi | Madiga | Parvathipuram |
| Gollapalli | Mala | Razole |
| Pinipe | Mala | Amalapuram |
| Vipparthi | Mala | P Gannavaram |
| Taneti | Madiga | Gopalapuram |
| Talari | Mala | Kovvur |
| Kambham | Mala | Chintalapudi |
| Kaile | Mala | Pamarru |
| Monditoka | Madiga | Nandigama |
| Nallagatla | Madiga | Tiruvuru |
| Mekathoti | Mala | Tadikonda |
| Balasani | Madiga | Prathipadu |
| Varikuti | Mala | Vemuru |
| Merugu | Mala | Santhanuthalapadu |
| Tatiparthi | Madiga | Yerragondapalem |
| Audimulapu | Madiga | Kondapi |
| Meriga | Mala | Gudur |
| Kiliveti | Mala | Sullurpeta |
| Nukathoti | Mala | Satyaveedu |
| Kalathur | Mala | G.D.Nellore |
| Mudirevula | Mala | Puthalapattu |
| Koramutla | Mala | Kodur |
| Dasari | Mala | Badvel |
| Audimulapu | Madiga | Kodumur |
| Dara | Mala | Nandikotkur |
| Eera | Madiga | Madakasira |
| Mannepakula | Madiga | Singanamala |

---

### Source 2: MyNeta.info — SC Reserved Constituencies (HIGH VALUE)

**Why**: All candidates in SC-reserved constituencies must be SC. Candidate names are publicly listed with structured HTML.

**Base URL**: `https://www.myneta.info/AndhraPradesh2024/`

**AP SC-Reserved Assembly Constituencies (29 total)**:

| Constituency | District | URL Param (constituency_id) |
|---|---|---|
| Madakasira (SC) | Anantapur | Find from site |
| Singanamala (SC) | Anantapur | 162 |
| Gangadhara Nellore (SC) | Chittoor | Find from site |
| Puthalapattu (SC) | Chittoor | Find from site |
| Satyavedu (SC) | Chittoor | Find from site |
| Amalapuram (SC) | East Godavari | Find from site |
| Gannavaram (SC) | East Godavari | Find from site |
| Razole (SC) | East Godavari | Find from site |
| Prathipadu (SC) | Guntur | Find from site |
| Tadikonda (SC) | Guntur | Find from site |
| Vemuru (SC) | Guntur | Find from site |
| Badvel (SC) | Kadapa | Find from site |
| Kodur (SC) | Kadapa | Find from site |
| Nandigama (SC) | Krishna | Find from site |
| Pamarru (SC) | Krishna | Find from site |
| Tiruvuru (SC) | Krishna | Find from site |
| Kodumur (SC) | Kurnool | Find from site |
| Nandikotkur (SC) | Kurnool | Find from site |
| Gudur (SC) | Nellore | Find from site |
| Sullurpeta (SC) | Nellore | Find from site |
| Kondapi (SC) | Prakasam | Find from site |
| Santhanuthalapadu (SC) | Prakasam | Find from site |
| Yerragondapalem (SC) | Prakasam | Find from site |
| Rajam (SC) | Srikakulam | Find from site |
| Payakaraopet (SC) | Visakhapatnam | 34 |
| Parvathipuram (SC) | Vizianagaram | Find from site |
| Chintalapudi (SC) | West Godavari | Find from site |
| Gopalapuram (SC) | West Godavari | Find from site |
| Kovvur (SC) | West Godavari | Find from site |

**SC-Reserved Lok Sabha Constituencies (4)**:
- Amalapuram (SC)
- Bapatla (SC)
- Chittoor (SC)
- Tirupati (SC)

**Method**:
1. For each constituency, fetch `https://www.myneta.info/AndhraPradesh2024/index.php?action=show_candidates&constituency_id={ID}`
2. Parse the HTML table for candidate names
3. Extract surname (first word, skip Dr/Sri/Smt)
4. All candidates are SC (constituency is reserved), but specific sub-caste is NOT available here — only the surname

**Also scrape 2019 election**: `https://www.myneta.info/AndhraPradesh2019/` — same structure, doubles the data.

**Limitation**: MyNeta does NOT provide specific sub-caste (Mala vs Madiga). These surnames can only be tagged as "SC" generically. Cross-reference with Source 1 data or other sources to classify.

---

### Source 3: AP Panchayat / MPTC / ZPTC Election Results (HIGH VOLUME)

**Why**: Local body elections have SC-reserved wards. Thousands of winner names available.

**Where to search**:
- AP State Election Commission: `https://www.apsec.gov.in/`
- Search for "AP MPTC ZPTC results 2021 SC reserved" or "AP sarpanch election results SC"
- Results are often published as district-wise PDFs with winner name + ward + category

**Method**: Download result PDFs, extract names from SC-reserved wards/mandals.

---

### Source 4: APPSC Selection Lists (MEDIUM VALUE)

**Why**: Government recruitment selection lists show candidate name + category (SC). Some newer lists post-2025 may show SC sub-group (Group 1/2/3).

**Where to search**:
- `https://psc.ap.gov.in/` — look for "Selection Lists" or "Results"
- Search for "APPSC group 1 2 selection list SC candidates PDF"
- AP DSC (teacher recruitment) results also have category-wise lists

**Method**: Download PDFs, extract SC-category candidate names.

---

### Source 5: SC Scholarship / Welfare Beneficiary Lists (MEDIUM VALUE)

**Why**: AP Social Welfare Department publishes SC scholarship recipient lists.

**Where to search**:
- AP Social Welfare Department: `https://sw.ap.gov.in/`
- Search for "AP post matric scholarship SC beneficiary list"
- Jnanabhumi portal: `https://jnanabhumi.ap.gov.in/`
- Search for "AP SC scholarship recipients list PDF"

**Method**: These lists typically have student name + caste + college. Extract surnames.

---

### Source 6: News Articles with MLA/MP Caste Details (SUPPLEMENTARY)

**Why**: Political news articles often mention elected representatives' caste.

**Where to search**:
- Search for "AP SC MLA list 2024 caste wise"
- Search for "AP SC reserved constituency winners 2024 2019 caste"
- TheNewsMinute, The Hindu, Sakshi, Eenadu archives

---

## Implementation Steps for Claude Code

### Step 1: Setup
```
- Read existing spreadsheet (AP_Scheduled_Castes_Surnames.xlsx)
- Create a new sheet called "Raw Extracted Data" with columns:
  Full_Name, Surname, Caste_Category, Specific_Caste, Source, 
  Constituency, Party, Year, District, Notes
- Pre-populate with the 29 YSRCP records already extracted (listed above)
```

### Step 2: Scrape Party Candidate Lists
```
- Fetch the YSRCP 2024 PDF (URL above) — already done, verify
- Search for and fetch TDP 2024, JSP 2024, Congress 2024 AP candidate lists
- Search for 2019 AP election party-wise candidate lists with caste
- For each PDF: extract SC candidates, parse name, extract surname
- Add to Raw Extracted Data sheet with Specific_Caste populated
```

### Step 3: Scrape MyNeta SC Constituencies
```
- Get constituency IDs for all 29 SC assembly seats (2024)
  - Start from https://www.myneta.info/AndhraPradesh2024/
  - Navigate to each SC constituency page
- For each constituency page:
  - Parse HTML table
  - Extract all candidate names
  - Extract surname (first word, skip honorifics)
  - Tag as SC (specific sub-caste unknown unless cross-referenced)
- Repeat for 2019: https://www.myneta.info/AndhraPradesh2019/
- Repeat for 4 SC Lok Sabha seats (2024 and 2019)
```

### Step 4: Search for Additional Sources
```
- Search for AP panchayat/MPTC results with SC winner names
- Search for APPSC selection lists with SC candidates
- Search for AP SC scholarship beneficiary lists
- For each source found: extract, parse, add to Raw Extracted Data
```

### Step 5: Deduplicate and Classify Surnames
```
- From Raw Extracted Data, extract unique surnames
- For each unique surname, determine which SC sub-caste(s) it appears with
- Create a "Classified Surnames" sheet:
  Surname, Caste(s) Found With, Frequency, Source Count, Sample Names
- Where specific caste is known (from party lists), tag accordingly
- Where only "SC" is known (from myneta), leave as "SC - unclassified"
```

### Step 6: Update Existing Sheets
```
- For each of the 3 group sheets (Group 1, 2, 3):
  - For sub-castes where new surnames were found, append to the 
    "Surnames/Family Names" column
  - Add a count column: "# of Unique Surnames Found"
- Update the Summary sheet with totals
```

### Step 7: Generate Report
```
- Total unique surnames extracted
- Breakdown by source
- Breakdown by caste (Mala vs Madiga vs others)
- Surnames with highest frequency
- Data gaps (which sub-castes still have no surname data)
```

---

## Important Notes

- **Surname extraction rule**: First word of the full name is the surname (intiperu) in Telugu naming convention. Skip honorifics: Dr, Sri, Smt, Prof, Adv.
- **Deduplication**: Same surname may appear across multiple sources — deduplicate by surname + caste combination.
- **Caste-neutral surnames**: Names like Kumar, Babu, Prasad, Rao, Reddy (unlikely in SC but possible) should be flagged but not excluded.
- **Privacy**: All data is from public government sources (election affidavits, government results). No private data is being collected.
- **Network**: Web scraping is limited to allowed domains. Use web_search and web_fetch for publicly accessible URLs.
- **Rate limiting**: Be respectful when scraping myneta.info — add delays between requests.
- **File output**: Save updated spreadsheet as `AP_SC_Surnames_Enriched.xlsx` in the outputs directory.

---

## Expected Output

1. **Enriched spreadsheet** with hundreds of real SC surnames mapped to specific sub-castes
2. **Raw data sheet** with every extracted record traceable to its source
3. **Classified surnames sheet** with unique surnames, their caste association, and frequency
4. **Coverage report** showing which sub-castes have good surname data and which remain sparse

---

## Quick Start Command for Claude Code

```
Read this plan document and the existing spreadsheet. Start with Step 2 
(party candidate lists) since they provide the highest-value data with 
specific caste identification. Then proceed to Step 3 (MyNeta scraping). 
After each step, save intermediate results. Focus on maximizing unique 
surname count per SC sub-caste.
```
