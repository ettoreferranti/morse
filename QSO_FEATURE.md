# QSO Practice Feature Specification

## Overview

This document describes the implementation of a realistic QSO (amateur radio contact) practice feature for the Morse Code learning application. Users will listen to simulated CW (Morse code) QSO exchanges and transcribe specific information elements to test their comprehension skills.

## Feature Requirements

### User Story
As a Morse code learner, I want to practice my listening skills using realistic QSO exchanges so I can prepare for actual amateur radio contacts.

### Requirements Summary
Based on requirements gathering (2025-11-28):

**Interaction Model:**
- Interactive practice mode where users transcribe specific QSO elements
- Scoring based on accuracy of transcribed information
- Points awarded for each correctly identified element

**QSO Content:**
- Start with standard ragchew (casual conversation) format
- Include variations in verbosity (chatty vs. minimal exchanges)
- Randomized elements: callsigns, names, locations, signal reports, equipment details

**Call Signs:**
- US + common DX regions (not US-centric, user is Europe-based)
- Random generation within valid format rules
- Support for: US (W/K/N), UK (G/M), Europe (DL, F, ON, etc.), VK (Australia), JA (Japan), etc.

**Integration:**
- New tab in GUI application
- Uses existing timing/speed settings from app configuration
- Clean audio (no QRM/interference initially)

**Abbreviations:**
- Authentic amateur radio abbreviations
- Most commonly used Q-codes and prosigns
- In-app glossary reference
- Prosigns sent as separate letters (not combined characters)

**Scoring:**
- Per-QSO scoring on: callsign, name, QTH, RST report, rig, antenna, power
- Partial credit for partially correct answers

## Technical Specification

### Architecture

```
New Components:
├── qso_data.py          # QSO data generation module
│   ├── CallSignGenerator class
│   ├── QSOTemplate class
│   └── Data lists (names, cities, equipment, etc.)
├── qso_practice.py      # QSO practice logic
│   └── QSOPracticeSession class
└── morse_gui.py         # Modified to add QSO tab
    └── create_qso_tab() method
```

### Data Model

#### QSO Exchange Structure
```python
QSOExchange = {
    'calling_station': {
        'callsign': 'G3YWX',
        'name': 'IAN',
        'qth': 'STAINES',
        'rst_sent': '599',
        'rst_received': '589',
        'rig': 'FT991A',
        'antenna': 'DIPOLE',
        'power': '100W'
    },
    'responding_station': {
        'callsign': 'W1ABC',
        'name': 'BOB',
        'qth': 'BOSTON',
        'rst_sent': '589',
        'rst_received': '599',
        'rig': 'IC7300',
        'antenna': 'VERTICAL',
        'power': '50W'
    },
    'verbosity': 'medium',  # minimal, medium, chatty
    'optional_elements': ['weather', 'equipment_details']
}
```

#### Call Sign Formats by Region

**United States (W, K, N prefixes):**
- Format: `[W|K|N][0-9][A-Z]{2,3}` or `[A-Z]{2}[0-9][A-Z]{2,3}`
- Examples: W1ABC, K6XYZ, N2MH, AA1AA, KC1XYZ
- Regions: 0-9 (geographic areas)

**United Kingdom (G, M prefixes):**
- Format: `[G|M][0-9][A-Z]{2,4}`
- Examples: G3YWX, M0ABC, G4XYZ

**Germany (DL, DA-DL prefixes):**
- Format: `D[A-L][0-9][A-Z]{2,3}`
- Examples: DL1ABC, DK2XY, DJ9ZZ

**France (F prefix):**
- Format: `F[0-9][A-Z]{2,3}`
- Examples: F1ABC, F6XYZ

**Australia (VK prefix):**
- Format: `VK[1-9][A-Z]{2,3}`
- Examples: VK2ABC, VK3XY

**Japan (JA-JS prefix):**
- Format: `J[A-S][0-9][A-Z]{2,3}`
- Examples: JA1ABC, JR2XYZ

**Belgium (ON prefix):**
- Format: `ON[0-9][A-Z]{2,3}`
- Examples: ON4ABC, ON7XYZ

**Netherlands (PA, PD, PE prefixes):**
- Format: `P[A|D|E][0-9][A-Z]{2,3}`
- Examples: PA3XYZ, PD0ABC

**Italy (I prefix):**
- Format: `I[0-9][A-Z]{2,4}`
- Examples: I2ABC, I4XYZ

### QSO Template Format

#### Standard Ragchew Template (Minimal)
```
CQ CQ CQ DE {CALL1} {CALL1} {CALL1} K
{CALL1} DE {CALL2} {CALL2} K
{CALL2} DE {CALL1} GM OM TNX FER CALL UR RST {RST1} {RST1} NAME {NAME1} {NAME1} QTH {QTH1} {QTH1} HW CPY K
{CALL1} DE {CALL2} FB OM UR RST {RST2} {RST2} NAME {NAME2} {NAME2} QTH {QTH2} {QTH2} K
{CALL2} DE {CALL1} TNX QSO 73 ES GUD DX DE {CALL1} SK
{CALL1} DE {CALL2} 73 {NAME1} DE {CALL2} SK
```

#### Standard Ragchew Template (Medium)
```
CQ CQ CQ DE {CALL1} {CALL1} {CALL1} K
{CALL1} DE {CALL2} {CALL2} AR K
{CALL2} DE {CALL1} GE OM TNX FER CALL UR RST {RST1} {RST1} NAME HR IS {NAME1} {NAME1} QTH {QTH1} {QTH1} HW K
{CALL1} DE {CALL2} FB {NAME1} UR RST {RST2} {RST2} NAME {NAME2} {NAME2} QTH {QTH2} {QTH2} RIG {RIG2} ANT {ANT2} K
{CALL2} DE {CALL1} NICE SETUP {NAME2} HR RUNNING {RIG1} TO {ANT1} PWR {PWR1} K
{CALL1} DE {CALL2} SOLID COPY OM QSB NIL WX {WX} K
{CALL2} DE {CALL1} TNX QSO {NAME2} QRU 73 ES GUD DX DE {CALL1} SK
{CALL1} DE {CALL2} 73 {NAME1} HPE CUAGN DE {CALL2} SK
```

#### Standard Ragchew Template (Chatty)
```
CQ CQ CQ DE {CALL1} {CALL1} {CALL1} CQ CQ CQ DE {CALL1} {CALL1} K
{CALL1} DE {CALL2} {CALL2} AR KN
{CALL2} DE {CALL1} GA OM TNX FER CALL UR RST {RST1} {RST1} {RST1} NAME HR IS {NAME1} {NAME1} QTH {QTH1} {QTH1} HW CPY K
{CALL1} DE {CALL2} R R FB {NAME1} SOLID COPY UR RST {RST2} {RST2} {RST2} NAME {NAME2} {NAME2} {NAME2} QTH {QTH2} {QTH2} {QTH2} K
{CALL2} DE {CALL1} NICE TO MEET U {NAME2} RIG HR IS {RIG1} {RIG1} PWR {PWR1} ANT {ANT1} {ANT1} HW ABT U K
{CALL1} DE {CALL2} NICE RIG OM HR RUNNING {RIG2} {RIG2} PWR {PWR2} ANT {ANT2} {ANT2} WX {WX} TEMP {TEMP} K
{CALL2} DE {CALL1} NICE WX {NAME2} HR WX {WX2} ES {TEMP2} BEEN ON AIR LONG TIME TODAY K
{CALL1} DE {CALL2} R R {NAME1} SAME HR BAND CONDITIONS FB TODAY QSB VERY LOW K
{CALL2} DE {CALL1} AGR OM SIGS SOLID TNX FER NICE QSO {NAME2} QRU 73 ES HPE CUAGN DE {CALL1} SK
{CALL1} DE {CALL2} 73 73 {NAME1} VY NICE TO MEET U HPE CUAGN SN DE {CALL2} SK
```

### Abbreviation Dictionary

#### Common Morse Abbreviations
```python
ABBREVIATIONS = {
    # Greetings
    'GM': 'Good Morning',
    'GA': 'Good Afternoon',
    'GE': 'Good Evening',
    'GN': 'Good Night',

    # Friendly terms
    'OM': 'Old Man (fellow operator)',
    'YL': 'Young Lady',
    'XYL': 'Wife',

    # Common phrases
    'TNX': 'Thanks',
    'TKS': 'Thanks',
    'FB': 'Fine Business (excellent)',
    'HPE': 'Hope',
    'CUAGN': 'See You Again',
    'CUL': 'See You Later',
    'SN': 'Soon',
    'VY': 'Very',

    # Technical
    'HR': 'Here',
    'UR': 'Your/You\'re',
    'U': 'You',
    'R': 'Roger/Received',
    'RIG': 'Transceiver',
    'ANT': 'Antenna',
    'PWR': 'Power',
    'WX': 'Weather',
    'TEMP': 'Temperature',

    # Signal reports
    'RST': 'Readability-Strength-Tone',
    'QSB': 'Fading',
    'QRM': 'Interference',
    'QRN': 'Static',

    # Prosigns
    'AR': 'End of message',
    'K': 'Over/Invitation to transmit',
    'KN': 'Go ahead, specific station only',
    'SK': 'End of contact/Silent Key',
    'CQ': 'Calling any station',
    'DE': 'From (this is)',

    # Q-codes
    'QTH': 'Location',
    'QRU': 'Nothing more to send',
    'QSL': 'Acknowledgement/Confirm',
    'QRZ': 'Who is calling me?',
    'QSY': 'Change frequency',
    'QSO': 'Contact/Conversation',

    # Numbers
    '73': 'Best regards',
    '88': 'Love and kisses',
    '599': 'Perfect signal (RST)',
    '589': 'Very good signal (RST)',
    '579': 'Good signal (RST)'
}
```

### Data Lists

#### Common Names (First names commonly used in amateur radio)
```python
COMMON_NAMES = [
    'BOB', 'JOHN', 'MIKE', 'TOM', 'DAVE', 'BILL', 'JIM', 'STEVE', 'PAUL', 'MARK',
    'IAN', 'CHRIS', 'PETER', 'ALAN', 'BRIAN', 'GARY', 'LARRY', 'TONY', 'FRED', 'ROGER',
    'HANS', 'JEAN', 'PIERRE', 'LUIGI', 'CARLOS', 'JOSE', 'ANTONIO', 'MARCO',
    'MARY', 'SUE', 'LINDA', 'KAREN', 'NANCY', 'BARBARA', 'SARAH', 'ANNA'
]
```

#### Common Cities/QTH
```python
# US Cities
US_CITIES = [
    'BOSTON', 'CHICAGO', 'DENVER', 'SEATTLE', 'PORTLAND', 'AUSTIN', 'DALLAS',
    'MIAMI', 'ATLANTA', 'PHOENIX', 'DETROIT', 'MINNEAPOLIS', 'CLEVELAND'
]

# UK Cities
UK_CITIES = [
    'LONDON', 'MANCHESTER', 'BIRMINGHAM', 'LEEDS', 'GLASGOW', 'EDINBURGH',
    'BRISTOL', 'LIVERPOOL', 'CARDIFF', 'BELFAST', 'STAINES', 'OXFORD'
]

# European Cities
EU_CITIES = [
    'BERLIN', 'MUNICH', 'HAMBURG', 'COLOGNE',  # Germany
    'PARIS', 'LYON', 'MARSEILLE', 'TOULOUSE',  # France
    'ROME', 'MILAN', 'FLORENCE', 'VENICE',     # Italy
    'BRUSSELS', 'ANTWERP', 'GHENT',            # Belgium
    'AMSTERDAM', 'ROTTERDAM', 'UTRECHT',        # Netherlands
    'MADRID', 'BARCELONA', 'VALENCIA'          # Spain
]

# Other regions
ASIA_CITIES = ['TOKYO', 'OSAKA', 'KYOTO', 'SYDNEY', 'MELBOURNE', 'BRISBANE']
```

#### Radio Equipment
```python
TRANSCEIVERS = [
    'IC7300', 'IC7610', 'IC9700',  # Icom
    'FT991A', 'FT710', 'FTDX10',   # Yaesu
    'TS590', 'TS890', 'TS480',      # Kenwood
    'K3', 'K4', 'KX3'               # Elecraft
]

ANTENNAS = [
    'DIPOLE', 'VERTICAL', 'BEAM', 'YAGI', 'LOOP', 'WIRE', 'INVERTED V',
    'G5RV', 'WINDOM', 'DOUBLET', 'GROUND PLANE', 'DELTA LOOP'
]

POWER_LEVELS = ['5W', '10W', '25W', '50W', '100W', '150W']
```

#### Weather Conditions
```python
WEATHER = ['SUNNY', 'CLOUDY', 'RAIN', 'CLEAR', 'OVERCAST', 'SNOW']
TEMPERATURES = ['10C', '15C', '20C', '25C', '30C', '5C', '0C', '-5C']
```

#### RST Signal Reports
```python
RST_REPORTS = [
    '599',  # Perfect
    '589',  # Excellent
    '579',  # Very good
    '569',  # Good
    '559',  # Fair
    '449'   # Poor but readable
]
```

## GUI Design

### QSO Practice Tab Layout

```
┌─────────────────────────────────────────────────────────────┐
│ QSO Practice                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Status: [Ready to Start / Playing / Transcribing]          │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Progress: [████████████░░░░░░░░░░] 60% (3/5 QSOs)     │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Current Score: 18/21 (85.7%)                               │
│                                                              │
│  ┌─── Transcription Form ───────────────────────────────┐   │
│  │                                                       │   │
│  │  Calling Station (heard first):                      │   │
│  │    Callsign: [_____________]                         │   │
│  │    Name:     [_____________]                         │   │
│  │    QTH:      [_____________]                         │   │
│  │    RST Rcvd: [___]                                   │   │
│  │                                                       │   │
│  │  Responding Station:                                 │   │
│  │    Callsign: [_____________]                         │   │
│  │    Name:     [_____________]                         │   │
│  │    QTH:      [_____________]                         │   │
│  │    RST Rcvd: [___]                                   │   │
│  │                                                       │   │
│  │  Optional (if mentioned):                            │   │
│  │    Rig:      [_____________]                         │   │
│  │    Antenna:  [_____________]                         │   │
│  │    Power:    [_____________]                         │   │
│  │                                                       │   │
│  │  [Replay Audio]  [Submit]  [Skip]                    │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─── Results History ──────────────────────────────────┐   │
│  │ QSO 1: 7/7 (100%) ✓                                  │   │
│  │ QSO 2: 6/7 (86%)  - Missed antenna                   │   │
│  │ QSO 3: 5/7 (71%)  - Incorrect RST, missed power      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  [Start Practice (5 QSOs)] [Configure]                      │
│                                                              │
│  ┌─── Quick Reference: Common Abbreviations ───────────┐   │
│  │ GM=Good Morning  OM=Old Man  TNX=Thanks  FB=Fine     │   │
│  │ RST=Signal Report  QTH=Location  73=Best Regards     │   │
│  │ [Show Full Glossary]                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Glossary Dialog

```
┌─────────────────────────────────────────────────────────┐
│ Amateur Radio Abbreviations & Q-Codes                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Search: ____________]                                 │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Greetings & Friendly Terms                       │   │
│  │   GM  - Good Morning                             │   │
│  │   GA  - Good Afternoon                           │   │
│  │   GE  - Good Evening                             │   │
│  │   OM  - Old Man (fellow operator)                │   │
│  │   FB  - Fine Business (excellent)                │   │
│  │                                                   │   │
│  │ Common Phrases                                    │   │
│  │   TNX - Thanks                                    │   │
│  │   HPE - Hope                                      │   │
│  │   CUAGN - See You Again                          │   │
│  │   73  - Best Regards                             │   │
│  │                                                   │   │
│  │ Q-Codes                                           │   │
│  │   QTH - Location                                 │   │
│  │   QSO - Contact/Conversation                     │   │
│  │   QRU - Nothing more to send                     │   │
│  │   QSL - Acknowledgement                          │   │
│  │                                                   │   │
│  │ Technical                                         │   │
│  │   RST - Readability-Strength-Tone                │   │
│  │   RIG - Transceiver                              │   │
│  │   ANT - Antenna                                   │   │
│  │   PWR - Power                                     │   │
│  │                                                   │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  [Close]                                                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Implementation Work Breakdown

### Phase 1: Data Generation (Backend)
**Issue #1: QSO Data Module Foundation**
- Create `qso_data.py` module
- Implement data lists (names, cities, equipment, etc.)
- Implement abbreviation dictionary
- Add validation and sanitization

**Issue #2: Call Sign Generator**
- Implement `CallSignGenerator` class
- Support for US, UK, EU, VK, JA call sign formats
- Region-based generation logic
- Validation against realistic patterns

**Issue #3: QSO Template System**
- Implement `QSOTemplate` class
- Create minimal/medium/chatty templates
- Template variable substitution
- Randomization logic for optional elements

**Issue #4: QSO Generator Integration**
- Integrate CallSignGenerator with templates
- Random selection of all elements
- Generate complete QSO exchange text
- Export to Morse-ready format

### Phase 2: Practice Logic (Backend)
**Issue #5: QSO Practice Session Manager**
- Create `qso_practice.py` module
- Implement `QSOPracticeSession` class
- Audio playback integration with MorseCode class
- Session state management

**Issue #6: Scoring System**
- Implement answer validation logic
- Fuzzy matching for partial credit
- Score calculation per QSO
- Session statistics tracking

### Phase 3: GUI Integration (Frontend)
**Issue #7: QSO Practice Tab UI**
- Add new tab to `morse_gui.py`
- Create transcription form with input fields
- Implement progress tracking display
- Add results history panel

**Issue #8: Glossary Feature**
- Create abbreviation glossary dialog
- Implement search functionality
- Quick reference display in main tab
- Link to full glossary

**Issue #9: Audio Controls & Workflow**
- Implement play/replay functionality
- Submission and validation flow
- Skip functionality
- Session management (start/stop/configure)

### Phase 4: Configuration & Polish
**Issue #10: Configuration Extension**
- Add QSO-specific settings to config.json
- Number of QSOs per session
- Verbosity level selection
- Region preferences for call signs

**Issue #11: Documentation & Help**
- Update README.md with QSO feature
- Update CONFIG.md with new settings
- Add user guide for QSO practice
- Update CLAUDE.md with architecture notes

### Phase 5: Future Enhancements (Deferred)
- Contest-style QSO templates
- DX expedition scenarios
- QRM/QSB audio effects (interference/fading)
- Statistics persistence and progress tracking
- Difficulty progression system
- Custom QSO template creation

## Testing Strategy

### Unit Tests
- Call sign generation validation
- Template rendering correctness
- Scoring logic accuracy
- Fuzzy matching edge cases

### Integration Tests
- End-to-end QSO generation
- Audio playback with existing MorseCode class
- GUI interaction flow
- Configuration loading

### Manual Testing
- Test all call sign regions
- Verify abbreviations are realistic
- Check verbosity variations
- Test scoring with various inputs
- Verify audio timing matches settings

## Success Criteria

1. ✅ Users can practice with realistic QSO exchanges
2. ✅ Call signs represent diverse geographic regions
3. ✅ Scoring accurately reflects comprehension
4. ✅ UI is intuitive and provides helpful feedback
5. ✅ Abbreviations match real amateur radio usage
6. ✅ Audio playback uses existing app settings
7. ✅ Feature integrates seamlessly with existing app

## Future Considerations

### Planned Enhancements (TODO markers in code)
- Add QRM (interference) simulation
- Add QSB (fading) effects
- Contest-style exchanges
- DX expedition scenarios
- Progress tracking across sessions
- Customizable difficulty levels
- User-defined templates

### Technical Debt Prevention
- Keep QSO logic modular and testable
- Use existing security validation patterns
- Follow established code style
- Maintain comprehensive documentation
- Add logging for debugging

---

**Document Version:** 1.0
**Last Updated:** 2025-11-28
**Status:** Ready for Implementation
