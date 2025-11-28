"""
QSO Data Module - Reference data for realistic amateur radio QSO practice

This module provides all reference data needed to generate realistic amateur radio
QSO (contact) exchanges, including:
- Amateur radio abbreviations and Q-codes
- Operator names
- Geographic locations (QTH) by region
- Radio equipment (transceivers, antennas)
- Signal reports and other technical data

Author: Generated with Claude Code
Date: 2025-11-28
Issue: #2 - QSO Feature: Data Module Foundation
"""

import re
import logging

# ============================================================================
# ABBREVIATION DICTIONARY
# ============================================================================

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
    'OT': 'Old Timer',

    # Common phrases
    'TNX': 'Thanks',
    'TKS': 'Thanks',
    'FB': 'Fine Business (excellent)',
    'HPE': 'Hope',
    'CUAGN': 'See You Again',
    'CUL': 'See You Later',
    'SN': 'Soon',
    'VY': 'Very',
    'ES': 'And',
    'FER': 'For',
    'HW': 'How',
    'ABT': 'About',
    'AGR': 'Agree',
    'CPY': 'Copy',

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
    'SIGS': 'Signals',
    'BAND': 'Frequency Band',

    # Signal quality
    'RST': 'Readability-Strength-Tone',
    'QSB': 'Fading',
    'QRM': 'Interference',
    'QRN': 'Static',
    'NIL': 'Nothing/None',
    'SOLID': 'Very strong signal',

    # Prosigns (procedural signals)
    'AR': 'End of message',
    'K': 'Over/Invitation to transmit',
    'KN': 'Go ahead, specific station only',
    'SK': 'End of contact/Silent Key',
    'CQ': 'Calling any station',
    'DE': 'From (this is)',
    'VA': 'End of work',

    # Q-codes (commonly used)
    'QTH': 'Location',
    'QRU': 'Nothing more to send',
    'QSL': 'Acknowledgement/Confirm',
    'QRZ': 'Who is calling me?',
    'QSY': 'Change frequency',
    'QSO': 'Contact/Conversation',
    'QRP': 'Low power',
    'QRO': 'High power',
    'QRT': 'Stop transmitting',

    # Numbers and expressions
    '73': 'Best regards',
    '88': 'Love and kisses',
    '599': 'Perfect signal (RST)',
    '589': 'Very good signal (RST)',
    '579': 'Good signal (RST)',
    '569': 'Fair signal (RST)',
    '559': 'Weak but readable (RST)',
}

# ============================================================================
# OPERATOR NAMES
# ============================================================================

COMMON_NAMES = [
    # Common male names in amateur radio
    'BOB', 'JOHN', 'MIKE', 'TOM', 'DAVE', 'BILL', 'JIM', 'STEVE', 'PAUL', 'MARK',
    'IAN', 'CHRIS', 'PETER', 'ALAN', 'BRIAN', 'GARY', 'LARRY', 'TONY', 'FRED', 'ROGER',
    'DAN', 'KEN', 'RON', 'JACK', 'ED', 'AL', 'JOE', 'SAM', 'TED', 'BEN',

    # European names
    'HANS', 'JEAN', 'PIERRE', 'LUIGI', 'CARLOS', 'JOSE', 'ANTONIO', 'MARCO',
    'KLAUS', 'HELMUT', 'FRANZ', 'GEORG', 'ERIK', 'LARS', 'SVEN', 'PAOLO',

    # Common female names (YL operators)
    'MARY', 'SUE', 'LINDA', 'KAREN', 'NANCY', 'BARBARA', 'SARAH', 'ANNA',
    'LISA', 'LAURA', 'JANE', 'BETTY', 'RUTH', 'CAROL', 'DIANE', 'HELEN',
]

# ============================================================================
# GEOGRAPHIC LOCATIONS (QTH)
# ============================================================================

# United States cities
US_CITIES = [
    'BOSTON', 'CHICAGO', 'DENVER', 'SEATTLE', 'PORTLAND', 'AUSTIN', 'DALLAS',
    'MIAMI', 'ATLANTA', 'PHOENIX', 'DETROIT', 'MINNEAPOLIS', 'CLEVELAND',
    'PHILADELPHIA', 'NEW YORK', 'LOS ANGELES', 'SAN DIEGO', 'HOUSTON',
    'NASHVILLE', 'MEMPHIS', 'CHARLOTTE', 'RALEIGH', 'TAMPA', 'ORLANDO',
    'KANSAS CITY', 'ST LOUIS', 'MILWAUKEE', 'COLUMBUS', 'INDIANAPOLIS',
    'CINCINNATI', 'PITTSBURGH', 'BUFFALO', 'ROCHESTER', 'ALBANY', 'HARTFORD',
]

# United Kingdom cities
UK_CITIES = [
    'LONDON', 'MANCHESTER', 'BIRMINGHAM', 'LEEDS', 'GLASGOW', 'EDINBURGH',
    'BRISTOL', 'LIVERPOOL', 'CARDIFF', 'BELFAST', 'STAINES', 'OXFORD',
    'CAMBRIDGE', 'BRIGHTON', 'PLYMOUTH', 'SOUTHAMPTON', 'NOTTINGHAM',
    'SHEFFIELD', 'NEWCASTLE', 'YORK', 'READING', 'BATH', 'EXETER',
]

# German cities
GERMAN_CITIES = [
    'BERLIN', 'MUNICH', 'HAMBURG', 'COLOGNE', 'FRANKFURT', 'STUTTGART',
    'DUSSELDORF', 'DORTMUND', 'ESSEN', 'LEIPZIG', 'BREMEN', 'DRESDEN',
    'HANNOVER', 'NUREMBERG', 'BONN', 'HEIDELBERG',
]

# French cities
FRENCH_CITIES = [
    'PARIS', 'LYON', 'MARSEILLE', 'TOULOUSE', 'NICE', 'NANTES', 'STRASBOURG',
    'MONTPELLIER', 'BORDEAUX', 'LILLE', 'RENNES', 'REIMS', 'TOURS',
]

# Italian cities
ITALIAN_CITIES = [
    'ROME', 'MILAN', 'FLORENCE', 'VENICE', 'NAPLES', 'TURIN', 'BOLOGNA',
    'GENOA', 'PALERMO', 'VERONA', 'PADUA', 'TRIESTE',
]

# Belgian cities
BELGIAN_CITIES = [
    'BRUSSELS', 'ANTWERP', 'GHENT', 'BRUGES', 'LIEGE', 'NAMUR', 'CHARLEROI',
]

# Dutch cities
DUTCH_CITIES = [
    'AMSTERDAM', 'ROTTERDAM', 'UTRECHT', 'THE HAGUE', 'EINDHOVEN', 'TILBURG',
    'GRONINGEN', 'LEIDEN', 'HAARLEM',
]

# Spanish cities
SPANISH_CITIES = [
    'MADRID', 'BARCELONA', 'VALENCIA', 'SEVILLA', 'BILBAO', 'MALAGA',
    'ZARAGOZA', 'MURCIA', 'PALMA', 'GRANADA',
]

# Asian/Pacific cities
ASIA_PACIFIC_CITIES = [
    'TOKYO', 'OSAKA', 'KYOTO', 'YOKOHAMA', 'NAGOYA', 'SAPPORO',
    'SYDNEY', 'MELBOURNE', 'BRISBANE', 'PERTH', 'ADELAIDE', 'AUCKLAND',
    'WELLINGTON', 'CHRISTCHURCH',
]

# Combined European cities
EU_CITIES = (
    GERMAN_CITIES + FRENCH_CITIES + ITALIAN_CITIES +
    BELGIAN_CITIES + DUTCH_CITIES + SPANISH_CITIES
)

# All cities combined for random selection
ALL_CITIES = US_CITIES + UK_CITIES + EU_CITIES + ASIA_PACIFIC_CITIES

# ============================================================================
# RADIO EQUIPMENT
# ============================================================================

# Transceivers by manufacturer
ICOM_RIGS = ['IC7300', 'IC7610', 'IC9700', 'IC705', 'IC7100', 'IC7851']
YAESU_RIGS = ['FT991A', 'FT710', 'FTDX10', 'FTDX101D', 'FT818', 'FT891']
KENWOOD_RIGS = ['TS590', 'TS890', 'TS480', 'TS990', 'TS570']
ELECRAFT_RIGS = ['K3', 'K4', 'KX3', 'KX2', 'K2']

# All transceivers
TRANSCEIVERS = ICOM_RIGS + YAESU_RIGS + KENWOOD_RIGS + ELECRAFT_RIGS

# Antenna types
ANTENNAS = [
    'DIPOLE', 'VERTICAL', 'BEAM', 'YAGI', 'LOOP', 'WIRE', 'INVERTED V',
    'G5RV', 'WINDOM', 'DOUBLET', 'GROUND PLANE', 'DELTA LOOP', 'QUAD',
    'HEX BEAM', 'MAGNETIC LOOP', 'END FED', 'LONG WIRE', 'FOLDED DIPOLE',
]

# Power levels (common amateur radio power outputs)
POWER_LEVELS = ['5W', '10W', '25W', '50W', '100W', '150W', '200W', '400W']

# ============================================================================
# WEATHER & ENVIRONMENTAL DATA
# ============================================================================

WEATHER_CONDITIONS = [
    'SUNNY', 'CLOUDY', 'RAIN', 'CLEAR', 'OVERCAST', 'SNOW', 'FOGGY',
    'PARTLY CLOUDY', 'WINDY', 'STORMS', 'DRIZZLE', 'FAIR',
]

# Temperature values (in Celsius, common in amateur radio)
TEMPERATURES = [
    '-10C', '-5C', '0C', '5C', '10C', '15C', '20C', '25C', '30C', '35C',
]

# ============================================================================
# SIGNAL REPORTS (RST)
# ============================================================================

# RST = Readability (1-5), Strength (1-9), Tone (1-9)
# Most common signal reports in real QSOs
RST_REPORTS = [
    '599',  # Perfect signal
    '589',  # Excellent signal
    '579',  # Very good signal
    '569',  # Good signal
    '559',  # Fair signal
    '549',  # Weak but clear
    '539',  # Weak
    '449',  # Poor but readable
]

# ============================================================================
# VALIDATION AND SANITIZATION FUNCTIONS
# ============================================================================

def validate_name(name):
    """
    Validate operator name.

    Args:
        name (str): Operator name to validate

    Returns:
        bool: True if valid, False otherwise

    Security: Validates name format to prevent injection attacks
    """
    if not isinstance(name, str):
        logging.warning(f"Invalid name type: {type(name)}")
        return False

    # Names should be 2-20 uppercase letters/spaces only
    if not re.match(r'^[A-Z][A-Z\s]{1,19}$', name.strip()):
        logging.warning(f"Invalid name format: {name}")
        return False

    # Check against known names
    if name.strip() not in COMMON_NAMES:
        logging.info(f"Name not in predefined list: {name}")
        # Still valid, just not in our list

    return True


def validate_qth(qth):
    """
    Validate QTH (location).

    Args:
        qth (str): Location to validate

    Returns:
        bool: True if valid, False otherwise

    Security: Validates QTH format to prevent injection attacks
    """
    if not isinstance(qth, str):
        logging.warning(f"Invalid QTH type: {type(qth)}")
        return False

    # QTH should be 2-30 uppercase letters/spaces only
    if not re.match(r'^[A-Z][A-Z\s]{1,29}$', qth.strip()):
        logging.warning(f"Invalid QTH format: {qth}")
        return False

    return True


def validate_rst(rst):
    """
    Validate RST signal report.

    Args:
        rst (str): RST report to validate (e.g., '599')

    Returns:
        bool: True if valid, False otherwise

    Security: Validates RST format
    """
    if not isinstance(rst, str):
        logging.warning(f"Invalid RST type: {type(rst)}")
        return False

    # RST must be exactly 3 digits: R(1-5), S(1-9), T(1-9)
    if not re.match(r'^[1-5][1-9][1-9]$', rst):
        logging.warning(f"Invalid RST format: {rst}")
        return False

    return True


def validate_equipment(equipment):
    """
    Validate equipment name (rig, antenna, etc.).

    Args:
        equipment (str): Equipment name to validate

    Returns:
        bool: True if valid, False otherwise

    Security: Validates equipment format to prevent injection attacks
    """
    if not isinstance(equipment, str):
        logging.warning(f"Invalid equipment type: {type(equipment)}")
        return False

    # Equipment should be 2-30 alphanumeric characters/spaces
    if not re.match(r'^[A-Z0-9][A-Z0-9\s]{1,29}$', equipment.strip()):
        logging.warning(f"Invalid equipment format: {equipment}")
        return False

    return True


def validate_power(power):
    """
    Validate power level.

    Args:
        power (str): Power level to validate (e.g., '100W')

    Returns:
        bool: True if valid, False otherwise

    Security: Validates power format
    """
    if not isinstance(power, str):
        logging.warning(f"Invalid power type: {type(power)}")
        return False

    # Power should be 1-4 digits followed by 'W'
    if not re.match(r'^\d{1,4}W$', power):
        logging.warning(f"Invalid power format: {power}")
        return False

    # Check reasonable range (1W to 1500W for amateur radio)
    try:
        watts = int(power[:-1])
        if not (1 <= watts <= 1500):
            logging.warning(f"Power out of range: {power}")
            return False
    except ValueError:
        return False

    return True


def sanitize_text(text, max_length=100):
    """
    Sanitize text input for use in QSO generation.

    Args:
        text (str): Text to sanitize
        max_length (int): Maximum allowed length

    Returns:
        str: Sanitized text (uppercase, trimmed, validated)

    Security: Removes potentially dangerous characters and enforces limits
    """
    if not isinstance(text, str):
        logging.warning(f"Non-string input to sanitize_text: {type(text)}")
        return ""

    # Convert to uppercase and strip whitespace
    text = text.upper().strip()

    # Remove control characters and null bytes
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)

    # Limit length
    if len(text) > max_length:
        logging.warning(f"Text too long, truncating: {len(text)} > {max_length}")
        text = text[:max_length]

    # Only allow alphanumeric, spaces, and common punctuation
    text = re.sub(r'[^A-Z0-9\s\-/]', '', text)

    return text


# ============================================================================
# DATA CATEGORIES FOR ORGANIZED ACCESS
# ============================================================================

ABBREVIATION_CATEGORIES = {
    'greetings': ['GM', 'GA', 'GE', 'GN'],
    'friendly': ['OM', 'YL', 'XYL', 'OT'],
    'common_phrases': ['TNX', 'TKS', 'FB', 'HPE', 'CUAGN', 'CUL', 'SN', 'VY', '73', '88'],
    'technical': ['HR', 'UR', 'U', 'R', 'RIG', 'ANT', 'PWR', 'WX', 'TEMP', 'RST'],
    'q_codes': ['QTH', 'QRU', 'QSL', 'QRZ', 'QSY', 'QSO', 'QRP', 'QRO', 'QRT'],
    'prosigns': ['AR', 'K', 'KN', 'SK', 'CQ', 'DE', 'VA'],
    'signal_quality': ['QSB', 'QRM', 'QRN', 'SOLID', 'NIL'],
}

CITIES_BY_REGION = {
    'us': US_CITIES,
    'uk': UK_CITIES,
    'germany': GERMAN_CITIES,
    'france': FRENCH_CITIES,
    'italy': ITALIAN_CITIES,
    'belgium': BELGIAN_CITIES,
    'netherlands': DUTCH_CITIES,
    'spain': SPANISH_CITIES,
    'asia_pacific': ASIA_PACIFIC_CITIES,
}

EQUIPMENT_BY_TYPE = {
    'icom': ICOM_RIGS,
    'yaesu': YAESU_RIGS,
    'kenwood': KENWOOD_RIGS,
    'elecraft': ELECRAFT_RIGS,
}

# ============================================================================
# CALL SIGN GENERATOR
# ============================================================================

class CallSignGenerator:
    """
    Generate realistic amateur radio call signs for various regions.

    Supports call sign generation for:
    - United States (W, K, N prefixes)
    - United Kingdom (G, M prefixes)
    - Germany (DL, DA-DL prefixes)
    - France (F prefix)
    - Italy (I prefix)
    - Belgium (ON prefix)
    - Netherlands (PA, PD, PE prefixes)
    - Spain (EA, EB prefixes)
    - Australia (VK prefix)
    - Japan (JA-JS prefixes)

    Author: Generated with Claude Code
    Date: 2025-11-28
    Issue: #3 - QSO Feature: Call Sign Generator
    """

    def __init__(self):
        """Initialize the call sign generator with region-specific patterns."""

        # US call sign patterns
        # Format: [Prefix][Region 0-9][Suffix 2-3 letters]
        self.us_prefixes_1 = ['W', 'K', 'N']
        self.us_prefixes_2 = [
            'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL',
            'KA', 'KB', 'KC', 'KD', 'KE', 'KF', 'KG', 'KH', 'KI', 'KJ', 'KK', 'KL',
            'KM', 'KN', 'KO', 'KP', 'KQ', 'KR', 'KS', 'KT', 'KU', 'KV', 'KW', 'KX', 'KY', 'KZ',
            'NA', 'NB', 'NC', 'ND', 'NE', 'NF', 'NG', 'NH', 'NI', 'NJ', 'NK', 'NL',
            'NM', 'NN', 'NO', 'NP', 'NQ', 'NR', 'NS', 'NT', 'NU', 'NV', 'NW', 'NX', 'NY', 'NZ',
            'WA', 'WB', 'WC', 'WD', 'WE', 'WF', 'WG', 'WH', 'WI', 'WJ', 'WK', 'WL',
            'WM', 'WN', 'WO', 'WP', 'WQ', 'WR', 'WS', 'WT', 'WU', 'WV', 'WW', 'WX', 'WY', 'WZ',
        ]
        self.us_regions = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # UK call sign patterns
        self.uk_prefixes = ['G', 'M']
        self.uk_regions = ['0', '1', '2', '3', '4', '5', '6', '7', '8']

        # German call sign patterns
        self.german_prefixes = ['DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL']
        self.german_regions = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # French call sign patterns
        self.french_regions = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # Italian call sign patterns
        self.italian_regions = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # Belgian call sign patterns
        self.belgian_regions = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # Dutch call sign patterns
        self.dutch_prefixes = ['PA', 'PD', 'PE']
        self.dutch_regions = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # Spanish call sign patterns
        self.spanish_prefixes = ['EA', 'EB', 'EC', 'ED', 'EE', 'EF', 'EG', 'EH']
        self.spanish_regions = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # Australian call sign patterns
        self.vk_regions = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        # Japanese call sign patterns
        self.japanese_prefixes = ['JA', 'JB', 'JC', 'JD', 'JE', 'JF', 'JG', 'JH', 'JI', 'JJ', 'JK', 'JL', 'JM', 'JN', 'JO', 'JP', 'JQ', 'JR', 'JS']
        self.japanese_regions = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # Letter pool for suffixes
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def generate_us(self):
        """
        Generate a US amateur radio call sign.

        Formats:
        - [W|K|N][0-9][A-Z]{2,3}  (e.g., W1ABC, K6XY)
        - [AA-AL|KA-KZ|NA-NZ|WA-WZ][0-9][A-Z]{2,3}  (e.g., AA1AA, KC1XYZ)

        Returns:
            str: Valid US call sign
        """
        import random

        # 70% chance of 1-letter prefix, 30% chance of 2-letter prefix
        if random.random() < 0.7:
            prefix = random.choice(self.us_prefixes_1)
        else:
            prefix = random.choice(self.us_prefixes_2)

        region = random.choice(self.us_regions)

        # Suffix: 2 or 3 letters (70% 3 letters, 30% 2 letters)
        suffix_length = 3 if random.random() < 0.7 else 2
        suffix = ''.join(random.choice(self.letters) for _ in range(suffix_length))

        return f"{prefix}{region}{suffix}"

    def generate_uk(self):
        """
        Generate a UK amateur radio call sign.

        Formats:
        - [G|M][0-9][A-Z]{2,4}  (e.g., G3YWX, M0ABC)

        Returns:
            str: Valid UK call sign
        """
        import random

        prefix = random.choice(self.uk_prefixes)
        region = random.choice(self.uk_regions)

        # Suffix: 2-4 letters (most commonly 3)
        suffix_length = random.choices([2, 3, 4], weights=[0.2, 0.6, 0.2])[0]
        suffix = ''.join(random.choice(self.letters) for _ in range(suffix_length))

        return f"{prefix}{region}{suffix}"

    def generate_german(self):
        """
        Generate a German amateur radio call sign.

        Format:
        - D[A-L][0-9][A-Z]{2,3}  (e.g., DL1ABC, DK2XY)

        Returns:
            str: Valid German call sign
        """
        import random

        prefix = random.choice(self.german_prefixes)
        region = random.choice(self.german_regions)

        # Suffix: 2 or 3 letters (mostly 3)
        suffix_length = 3 if random.random() < 0.8 else 2
        suffix = ''.join(random.choice(self.letters) for _ in range(suffix_length))

        return f"{prefix}{region}{suffix}"

    def generate_french(self):
        """
        Generate a French amateur radio call sign.

        Format:
        - F[0-9][A-Z]{2,3}  (e.g., F1ABC, F6XY)

        Returns:
            str: Valid French call sign
        """
        import random

        region = random.choice(self.french_regions)

        # Suffix: 2 or 3 letters (mostly 3)
        suffix_length = 3 if random.random() < 0.8 else 2
        suffix = ''.join(random.choice(self.letters) for _ in range(suffix_length))

        return f"F{region}{suffix}"

    def generate_italian(self):
        """
        Generate an Italian amateur radio call sign.

        Format:
        - I[0-9][A-Z]{2,4}  (e.g., I2ABC, I4XYZ)

        Returns:
            str: Valid Italian call sign
        """
        import random

        region = random.choice(self.italian_regions)

        # Suffix: 2-4 letters (mostly 3)
        suffix_length = random.choices([2, 3, 4], weights=[0.2, 0.6, 0.2])[0]
        suffix = ''.join(random.choice(self.letters) for _ in range(suffix_length))

        return f"I{region}{suffix}"

    def generate_belgian(self):
        """
        Generate a Belgian amateur radio call sign.

        Format:
        - ON[0-9][A-Z]{2,3}  (e.g., ON4ABC, ON7XY)

        Returns:
            str: Valid Belgian call sign
        """
        import random

        region = random.choice(self.belgian_regions)

        # Suffix: 2 or 3 letters (mostly 3)
        suffix_length = 3 if random.random() < 0.8 else 2
        suffix = ''.join(random.choice(self.letters) for _ in range(suffix_length))

        return f"ON{region}{suffix}"

    def generate_dutch(self):
        """
        Generate a Dutch amateur radio call sign.

        Format:
        - P[A|D|E][0-9][A-Z]{2,3}  (e.g., PA3XYZ, PD0ABC)

        Returns:
            str: Valid Dutch call sign
        """
        import random

        prefix = random.choice(self.dutch_prefixes)
        region = random.choice(self.dutch_regions)

        # Suffix: 2 or 3 letters (mostly 3)
        suffix_length = 3 if random.random() < 0.8 else 2
        suffix = ''.join(random.choice(self.letters) for _ in range(suffix_length))

        return f"{prefix}{region}{suffix}"

    def generate_spanish(self):
        """
        Generate a Spanish amateur radio call sign.

        Format:
        - E[A-H][0-9][A-Z]{2,3}  (e.g., EA1ABC, EB7XY)

        Returns:
            str: Valid Spanish call sign
        """
        import random

        prefix = random.choice(self.spanish_prefixes)
        region = random.choice(self.spanish_regions)

        # Suffix: 2 or 3 letters (mostly 3)
        suffix_length = 3 if random.random() < 0.8 else 2
        suffix = ''.join(random.choice(self.letters) for _ in range(suffix_length))

        return f"{prefix}{region}{suffix}"

    def generate_australian(self):
        """
        Generate an Australian amateur radio call sign.

        Format:
        - VK[1-9][A-Z]{2,3}  (e.g., VK2ABC, VK3XY)

        Returns:
            str: Valid Australian call sign
        """
        import random

        region = random.choice(self.vk_regions)

        # Suffix: 2 or 3 letters (mostly 3)
        suffix_length = 3 if random.random() < 0.8 else 2
        suffix = ''.join(random.choice(self.letters) for _ in range(suffix_length))

        return f"VK{region}{suffix}"

    def generate_japanese(self):
        """
        Generate a Japanese amateur radio call sign.

        Format:
        - J[A-S][0-9][A-Z]{2,3}  (e.g., JA1ABC, JR2XY)

        Returns:
            str: Valid Japanese call sign
        """
        import random

        prefix = random.choice(self.japanese_prefixes)
        region = random.choice(self.japanese_regions)

        # Suffix: 2 or 3 letters (mostly 3)
        suffix_length = 3 if random.random() < 0.8 else 2
        suffix = ''.join(random.choice(self.letters) for _ in range(suffix_length))

        return f"{prefix}{region}{suffix}"

    def generate(self, region=None):
        """
        Generate a call sign for a specific region or random region.

        Args:
            region (str, optional): Region code ('us', 'uk', 'germany', 'france', etc.)
                                   If None, randomly selects a region.

        Returns:
            str: Valid call sign for the specified or random region

        Raises:
            ValueError: If invalid region specified
        """
        import random

        # Map of region names to generator methods
        region_generators = {
            'us': self.generate_us,
            'uk': self.generate_uk,
            'germany': self.generate_german,
            'france': self.generate_french,
            'italy': self.generate_italian,
            'belgium': self.generate_belgian,
            'netherlands': self.generate_dutch,
            'spain': self.generate_spanish,
            'australia': self.generate_australian,
            'japan': self.generate_japanese,
        }

        # If no region specified, choose random based on realistic distribution
        if region is None:
            # Weight distribution to favor US/UK/EU for European user
            region = random.choices(
                list(region_generators.keys()),
                weights=[30, 20, 15, 10, 8, 5, 5, 4, 2, 1],  # US gets most, Japan least
                k=1
            )[0]

        # Validate region
        if region not in region_generators:
            valid_regions = ', '.join(region_generators.keys())
            raise ValueError(f"Invalid region '{region}'. Valid regions: {valid_regions}")

        # Generate and return call sign
        return region_generators[region]()

    def validate_callsign(self, callsign):
        """
        Validate if a call sign matches realistic patterns.

        Args:
            callsign (str): Call sign to validate

        Returns:
            bool: True if valid format, False otherwise

        Security: Validates format to prevent injection
        """
        if not isinstance(callsign, str):
            logging.warning(f"Invalid callsign type: {type(callsign)}")
            return False

        callsign = callsign.strip().upper()

        # Length check: 4-8 characters typical
        if not (4 <= len(callsign) <= 8):
            return False

        # Must contain at least one digit
        if not any(c.isdigit() for c in callsign):
            return False

        # Must contain at least one letter
        if not any(c.isalpha() for c in callsign):
            return False

        # Only alphanumeric characters allowed
        if not callsign.isalnum():
            return False

        # General pattern: starts with letters, contains digit, ends with letters
        # This is a simplified check - actual validation would be region-specific
        import re
        if not re.match(r'^[A-Z]{1,2}\d[A-Z]{2,4}$', callsign):
            return False

        return True


# ============================================================================
# QSO TEMPLATE SYSTEM
# ============================================================================

class QSOTemplate:
    """
    Generate realistic QSO exchange templates with variable verbosity.

    Supports three verbosity levels:
    - minimal: Brief, essential exchange only
    - medium: Standard QSO with some details
    - chatty: Verbose QSO with weather, equipment, friendly conversation

    Templates use variable substitution:
    - {CALL1}, {CALL2}: Call signs
    - {NAME1}, {NAME2}: Operator names
    - {QTH1}, {QTH2}: Locations
    - {RST1}, {RST2}: Signal reports
    - {RIG1}, {RIG2}: Transceivers
    - {ANT1}, {ANT2}: Antennas
    - {PWR1}, {PWR2}: Power levels
    - {WX1}, {WX2}: Weather conditions
    - {TEMP1}, {TEMP2}: Temperatures

    Author: Generated with Claude Code
    Date: 2025-11-28
    Issue: #4 - QSO Feature: Template System
    """

    def __init__(self):
        """Initialize the template system with predefined templates."""
        import random
        self.random = random

    def generate_minimal(self):
        """
        Generate a minimal QSO template (brief exchange).

        Essential elements only:
        - Call signs
        - Signal reports
        - Names
        - Brief sign-off

        Returns:
            str: Minimal QSO template with variable placeholders
        """
        templates = [
            # Template 1: Very brief
            "CQ CQ CQ DE {CALL1} {CALL1} K = "
            "{CALL1} DE {CALL2} {CALL2} K = "
            "{CALL2} DE {CALL1} = TNX FER CALL UR RST {RST1} {RST1} = NAME HR IS {NAME1} {NAME1} = HW CPY K = "
            "{CALL1} DE {CALL2} = R R FB {NAME1} = UR RST {RST2} {RST2} = NAME HR IS {NAME2} {NAME2} = 73 ES TNX FER QSO K = "
            "{CALL2} DE {CALL1} = R R TNX {NAME2} = 73 ES CUAGN = {CALL1} SK = "
            "{CALL1} DE {CALL2} SK",

            # Template 2: Brief with QTH
            "CQ CQ DE {CALL1} K = "
            "{CALL1} DE {CALL2} K = "
            "{CALL2} DE {CALL1} = UR RST {RST1} = NAME {NAME1} = QTH {QTH1} = HW K = "
            "{CALL1} DE {CALL2} = R TNX = UR RST {RST2} = NAME {NAME2} = QTH {QTH2} = 73 K = "
            "{CALL2} DE {CALL1} = 73 GL {NAME2} SK = "
            "{CALL1} DE {CALL2} SK",

            # Template 3: Clean and simple
            "CQ DE {CALL1} K = "
            "{CALL1} DE {CALL2} {CALL2} K = "
            "{CALL2} DE {CALL1} = GM OM UR {RST1} = NAME {NAME1} {NAME1} = QTH {QTH1} = K = "
            "{CALL1} DE {CALL2} = TNX {NAME1} = UR {RST2} = NAME {NAME2} = QTH {QTH2} = 73 K = "
            "{CALL2} DE {CALL1} = 73 {NAME2} SK = "
            "{CALL1} DE {CALL2} SK",
        ]

        return self.random.choice(templates)

    def generate_medium(self):
        """
        Generate a medium verbosity QSO template (standard exchange).

        Includes:
        - Call signs
        - Signal reports
        - Names and locations
        - Equipment (rig, antenna, power)
        - Polite conversation

        Returns:
            str: Medium QSO template with variable placeholders
        """
        templates = [
            # Template 1: Standard with equipment
            "CQ CQ CQ DE {CALL1} {CALL1} K = "
            "{CALL1} DE {CALL2} {CALL2} K = "
            "{CALL2} DE {CALL1} = GM OM TNX FER CALL = UR RST {RST1} {RST1} = NAME HR IS {NAME1} {NAME1} = QTH {QTH1} = RIG HR {RIG1} = HW CPY K = "
            "{CALL1} DE {CALL2} = R R FB {NAME1} = UR RST {RST2} {RST2} = NAME HR {NAME2} {NAME2} = QTH {QTH2} = RIG {RIG2} = ANT {ANT2} = 73 ES TNX FER FB QSO K = "
            "{CALL2} DE {CALL1} = R TNX {NAME2} = FB RIG UR RUNNING = HPE CUAGN SN = 73 ES GL = {CALL1} SK = "
            "{CALL1} DE {CALL2} = 73 {NAME1} SK",

            # Template 2: Standard with power and antenna
            "CQ DE {CALL1} {CALL1} K = "
            "{CALL1} DE {CALL2} K = "
            "{CALL2} DE {CALL1} = GE OM = UR RST {RST1} = NAME {NAME1} = QTH {QTH1} = RIG {RIG1} = PWR {PWR1} = ANT {ANT2} = HW K = "
            "{CALL1} DE {CALL2} = R R TNX {NAME1} = UR RST {RST2} = NAME {NAME2} = QTH {QTH2} = RIG {RIG2} PWR {PWR2} = FB SIGS HR = 73 K = "
            "{CALL2} DE {CALL1} = TNX FER FB QSO {NAME2} = 73 ES GL SK = "
            "{CALL1} DE {CALL2} SK",

            # Template 3: Friendly medium exchange
            "CQ CQ DE {CALL1} K = "
            "{CALL1} DE {CALL2} {CALL2} K = "
            "{CALL2} DE {CALL1} = GA OM TNX = UR RST {RST1} {RST1} = NAME {NAME1} = QTH {QTH1} = RUNNING {RIG1} TO {ANT1} = HW CPY K = "
            "{CALL1} DE {CALL2} = FB {NAME1} = CPY SOLID = UR RST {RST2} = NAME {NAME2} = QTH {QTH2} = RIG {RIG2} {PWR2} = VY FB SIGS FM U = TNX FER QSO ES 73 K = "
            "{CALL2} DE {CALL1} = R TNX {NAME2} = 73 ES HPE CUAGN SN = {CALL1} SK = "
            "{CALL1} DE {CALL2} SK",
        ]

        return self.random.choice(templates)

    def generate_chatty(self):
        """
        Generate a chatty QSO template (verbose exchange).

        Includes:
        - All medium elements
        - Weather conditions and temperature
        - Equipment discussions
        - Friendly conversation
        - Multiple exchanges

        Returns:
            str: Chatty QSO template with variable placeholders
        """
        templates = [
            # Template 1: Weather and rig discussion
            "CQ CQ CQ DE {CALL1} {CALL1} {CALL1} K = "
            "{CALL1} DE {CALL2} {CALL2} K = "
            "{CALL2} DE {CALL1} = GM OM TNX FER CALL = UR RST {RST1} {RST1} SOLID CPY = NAME HR IS {NAME1} {NAME1} = QTH {QTH1} = WX HR {WX1} TEMP ABT {TEMP1} = RIG HR {RIG1} {PWR1} TO {ANT1} = HW CPY K = "
            "{CALL1} DE {CALL2} = R R FB {NAME1} VY NICE COPY = UR RST {RST2} {RST2} = NAME HR {NAME2} {NAME2} = QTH {QTH2} = WX HR {WX2} {TEMP2} = RUNNING {RIG2} {PWR2} TO {ANT2} = FB SIGS FM U OM = HW ABT RIG K = "
            "{CALL2} DE {CALL1} = R TNX {NAME2} = {RIG1} IS FB RIG VY STABLE = UR RIG {RIG2} ALSO FB = {ANT2} WRKS GREAT I HEAR = 73 ES TNX FER FB QSO OM K = "
            "{CALL1} DE {CALL2} = R R AGR {NAME1} = TNX FER INFO = HPE CUAGN SN = 73 ES GL {NAME1} = {CALL2} SK = "
            "{CALL2} DE {CALL1} = 73 {NAME2} CUAGN SK = "
            "{CALL1} DE {CALL2} SK",

            # Template 2: Equipment and antenna discussion
            "CQ CQ DE {CALL1} {CALL1} K = "
            "{CALL1} DE {CALL2} K = "
            "{CALL2} DE {CALL1} = GE OM VY NICE TO HEAR U = UR RST {RST1} {RST1} FB SIGS = NAME HR IS {NAME1} {NAME1} = QTH {QTH1} = RIG {RIG1} PWR {PWR1} = ANT {ANT1} ABT 20M UP = WX {WX1} TEMP {TEMP1} = HW CPY OM K = "
            "{CALL1} DE {CALL2} = R R FB {NAME1} CPY SOLID = UR RST {RST2} {RST2} VY FB = NAME {NAME2} {NAME2} = QTH {QTH2} = RUNNING {RIG2} AT {PWR2} = ANT {ANT2} = WX HR {WX2} ES {TEMP2} = UR {ANT1} FB OM HW HIGH K = "
            "{CALL2} DE {CALL1} = TNX {NAME2} = {ANT1} IS ABT 20M HIGH WRKS FB = UR ANT {ANT2} ALSO WRKING VY WELL I HEAR = {RIG2} IS NICE RIG = 73 ES TNX FER FB CHAT OM K = "
            "{CALL1} DE {CALL2} = R R {NAME1} AGR = TNX FER INFO ABT ANT = HPE WRK U AGN SN = 73 ES GL = {CALL2} SK = "
            "{CALL2} DE {CALL1} = 73 {NAME2} SK = "
            "{CALL1} DE {CALL2} SK",

            # Template 3: Very friendly long QSO
            "CQ CQ CQ DE {CALL1} K = "
            "{CALL1} DE {CALL2} {CALL2} K = "
            "{CALL2} DE {CALL1} = GA OM VY FB TO HEAR U = UR RST {RST1} {RST1} SOLID = NAME HR {NAME1} {NAME1} = QTH {QTH1} = WX HR IS {WX1} ES TEMP {TEMP1} VY NICE = RIG HR IS {RIG1} RUNNING {PWR1} = ANT IS {ANT1} = HW CPY OM K = "
            "{CALL1} DE {CALL2} = R R {NAME1} CPY 100 PERCENT = UR RST {RST2} {RST2} = NAME {NAME2} {NAME2} = QTH {QTH2} = WX HR {WX2} TEMP {TEMP2} = RIG {RIG2} PWR {PWR2} TO {ANT2} = VY FB SIGS FM U OM SOLID CPY = HW LONG RUNNING {RIG1} K = "
            "{CALL2} DE {CALL1} = TNX {NAME2} = HAD {RIG1} ABT 5 YRS NOW VY SOLID RIG = UR RIG {RIG2} ALSO FB I HEAR = WX SOUNDS NICE THERE = HR {WX1} TODAY = 73 ES TNX FER VY FB QSO OM K = "
            "{CALL1} DE {CALL2} = R R {NAME1} TNX FER INFO = {RIG1} IS GREAT RIG = HPE WRK U AGN SN ON THIS BAND = 73 ES GL {NAME1} = {CALL2} SK = "
            "{CALL2} DE {CALL1} = 73 ES CUAGN {NAME2} SK = "
            "{CALL1} DE {CALL2} SK",
        ]

        return self.random.choice(templates)

    def generate(self, verbosity='medium'):
        """
        Generate a QSO template with specified verbosity level.

        Args:
            verbosity (str): Verbosity level ('minimal', 'medium', 'chatty')
                           Defaults to 'medium' if not specified.

        Returns:
            str: QSO template with variable placeholders

        Raises:
            ValueError: If invalid verbosity level specified
        """
        verbosity = verbosity.lower().strip()

        if verbosity == 'minimal':
            return self.generate_minimal()
        elif verbosity == 'medium':
            return self.generate_medium()
        elif verbosity == 'chatty':
            return self.generate_chatty()
        else:
            raise ValueError(
                f"Invalid verbosity '{verbosity}'. "
                "Valid options: 'minimal', 'medium', 'chatty'"
            )

    def substitute_variables(self, template, variables):
        """
        Substitute variables in a QSO template.

        Args:
            template (str): Template string with {VARIABLE} placeholders
            variables (dict): Dictionary mapping variable names to values
                            Required keys: CALL1, CALL2, NAME1, NAME2, QTH1, QTH2,
                                          RST1, RST2, RIG1, RIG2, ANT1, ANT2,
                                          PWR1, PWR2, WX1, WX2, TEMP1, TEMP2

        Returns:
            str: Template with all variables substituted

        Raises:
            KeyError: If required variable is missing
            ValueError: If variable validation fails

        Security: Validates all variables before substitution
        """
        # Required variables for all templates
        required_vars = {
            'CALL1', 'CALL2', 'NAME1', 'NAME2', 'QTH1', 'QTH2',
            'RST1', 'RST2', 'RIG1', 'RIG2', 'ANT1', 'ANT2',
            'PWR1', 'PWR2', 'WX1', 'WX2', 'TEMP1', 'TEMP2'
        }

        # Check all required variables are present
        missing_vars = required_vars - set(variables.keys())
        if missing_vars:
            raise KeyError(f"Missing required variables: {', '.join(sorted(missing_vars))}")

        # Validate each variable type
        # Call signs
        call_gen = CallSignGenerator()
        if not call_gen.validate_callsign(variables['CALL1']):
            raise ValueError(f"Invalid CALL1: {variables['CALL1']}")
        if not call_gen.validate_callsign(variables['CALL2']):
            raise ValueError(f"Invalid CALL2: {variables['CALL2']}")

        # Names
        if not validate_name(variables['NAME1']):
            raise ValueError(f"Invalid NAME1: {variables['NAME1']}")
        if not validate_name(variables['NAME2']):
            raise ValueError(f"Invalid NAME2: {variables['NAME2']}")

        # QTH (locations)
        if not validate_qth(variables['QTH1']):
            raise ValueError(f"Invalid QTH1: {variables['QTH1']}")
        if not validate_qth(variables['QTH2']):
            raise ValueError(f"Invalid QTH2: {variables['QTH2']}")

        # RST reports
        if not validate_rst(variables['RST1']):
            raise ValueError(f"Invalid RST1: {variables['RST1']}")
        if not validate_rst(variables['RST2']):
            raise ValueError(f"Invalid RST2: {variables['RST2']}")

        # Equipment
        if not validate_equipment(variables['RIG1']):
            raise ValueError(f"Invalid RIG1: {variables['RIG1']}")
        if not validate_equipment(variables['RIG2']):
            raise ValueError(f"Invalid RIG2: {variables['RIG2']}")
        if not validate_equipment(variables['ANT1']):
            raise ValueError(f"Invalid ANT1: {variables['ANT1']}")
        if not validate_equipment(variables['ANT2']):
            raise ValueError(f"Invalid ANT2: {variables['ANT2']}")

        # Power levels
        if not validate_power(variables['PWR1']):
            raise ValueError(f"Invalid PWR1: {variables['PWR1']}")
        if not validate_power(variables['PWR2']):
            raise ValueError(f"Invalid PWR2: {variables['PWR2']}")

        # Weather and temperature (basic validation)
        for var in ['WX1', 'WX2', 'TEMP1', 'TEMP2']:
            if not isinstance(variables[var], str):
                raise ValueError(f"Invalid {var}: must be string")
            if not re.match(r'^[A-Z0-9\s\-/]{1,30}$', variables[var].upper().strip()):
                raise ValueError(f"Invalid {var} format: {variables[var]}")

        # Perform substitution
        result = template
        for var_name, var_value in variables.items():
            placeholder = '{' + var_name + '}'
            result = result.replace(placeholder, str(var_value).upper().strip())

        return result


# ============================================================================
# MODULE METADATA
# ============================================================================

__version__ = '1.2.0'
__author__ = 'Generated with Claude Code'
__date__ = '2025-11-28'

# Export public API
__all__ = [
    # Dictionaries
    'ABBREVIATIONS',
    'ABBREVIATION_CATEGORIES',

    # Names
    'COMMON_NAMES',

    # Locations
    'US_CITIES',
    'UK_CITIES',
    'EU_CITIES',
    'GERMAN_CITIES',
    'FRENCH_CITIES',
    'ITALIAN_CITIES',
    'BELGIAN_CITIES',
    'DUTCH_CITIES',
    'SPANISH_CITIES',
    'ASIA_PACIFIC_CITIES',
    'ALL_CITIES',
    'CITIES_BY_REGION',

    # Equipment
    'TRANSCEIVERS',
    'ICOM_RIGS',
    'YAESU_RIGS',
    'KENWOOD_RIGS',
    'ELECRAFT_RIGS',
    'ANTENNAS',
    'POWER_LEVELS',
    'EQUIPMENT_BY_TYPE',

    # Environmental
    'WEATHER_CONDITIONS',
    'TEMPERATURES',

    # Technical
    'RST_REPORTS',

    # Validation functions
    'validate_name',
    'validate_qth',
    'validate_rst',
    'validate_equipment',
    'validate_power',
    'sanitize_text',

    # Call sign generator
    'CallSignGenerator',

    # QSO template system
    'QSOTemplate',
]
