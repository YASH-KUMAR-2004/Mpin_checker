from Mpin_2 import fetch_common_digit_pins_from_pocketlint
from Mpin_2 import get_valid_date
from Mpin_2 import generate_all_combinations

from datetime import datetime
from bs4 import BeautifulSoup
import requests
def run_tests():
    test_cases = [
        # Common 4-digit
        {"pin": "1234", "dob": None, "spdob": None, "anni": None, "expected": ["COMMONLY_USED"]},
        # Common 6-digit
        {"pin": "123456", "dob": None, "spdob": None, "anni": None, "expected": ["COMMONLY_USED"]},
        # DOB match (4-digit: ddmm)
        {"pin": "1508", "dob": datetime(1990, 8, 15), "spdob": None, "anni": None, "expected": ["DEMOGRAPHIC_DOB_SELF"]},
        # Spouse DOB match (4-digit: mmdd)
        {"pin": "0612", "dob": None, "spdob": datetime(1985, 12, 6), "anni": None, "expected": ["DEMOGRAPHIC_DOB_SPOUSE"]},
        # Anniversary match (4-digit: ddmm)
        {"pin": "2507", "dob": None, "spdob": None, "anni": datetime(2000, 7, 25), "expected": ["DEMOGRAPHIC_ANNIVERSARY"]},
        # DOB match (6-digit: ddmmyy)
        {"pin": "150890", "dob": datetime(1990, 8, 15), "spdob": None, "anni": None, "expected": ["DEMOGRAPHIC_DOB_SELF"]},
        # Spouse DOB match (6-digit: mmddyy)
        {"pin": "120685", "dob": None, "spdob": datetime(1985, 12, 6), "anni": None, "expected": ["DEMOGRAPHIC_DOB_SPOUSE"]},
        # Anniversary match (6-digit: ddmmYYYY)
        {"pin": "250720", "dob": None, "spdob": None, "anni": datetime(2020, 7, 25), "expected": ["DEMOGRAPHIC_ANNIVERSARY"]},
        # Combination match: common + dob
        {"pin": "1234", "dob": datetime(2012, 3, 4), "spdob": None, "anni": None, "expected": ["COMMONLY_USED"]},
        
        # Not common, not demographic
        {"pin": "111111", "dob": None, "spdob": None, "anni": datetime(2011, 11, 11), "expected": ["COMMONLY_USED", "DEMOGRAPHIC_ANNIVERSARY"]},
        # Invalid combo: wrong date parts
        {"pin": "999999", "dob": datetime(2000, 1, 1), "spdob": None, "anni": None, "expected": []},
        # Full year match
        {"pin": "1987", "dob": datetime(1987, 11, 22), "spdob": None, "anni": None, "expected": ["DEMOGRAPHIC_DOB_SELF"]},
        # Last two year digits + dd
        {"pin": "8711", "dob": datetime(1987, 11, 22), "spdob": None, "anni": None, "expected": ["DEMOGRAPHIC_DOB_SELF"]},
        # All fields present but no match
        {"pin": "0000", "dob": datetime(2000, 2, 2), "spdob": datetime(2001, 3, 3), "anni": datetime(2002, 4, 4), "expected": ["COMMONLY_USED"]},
        # Spouse full year match
        {"pin": "1975", "dob": None, "spdob": datetime(1975, 6, 6), "anni": None, "expected": ["DEMOGRAPHIC_DOB_SPOUSE"]},
        # Spouse dd + yy
        {"pin": "0575", "dob": None, "spdob": datetime(1975, 5, 5), "anni": None, "expected": ["DEMOGRAPHIC_DOB_SPOUSE"]},
        # Anniversary mm + yy
        {"pin": "0723", "dob": None, "spdob": None, "anni": datetime(2023, 7, 1), "expected": ["DEMOGRAPHIC_ANNIVERSARY"]},
        # All reasons matched
        {"pin": "010190", "dob": datetime(1990, 1, 1), "spdob": datetime(1990, 1, 1), "anni": datetime(1990, 1, 1),
         "expected": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE", "DEMOGRAPHIC_ANNIVERSARY"]},
        # Random MPIN
        {"pin": "839201", "dob": None, "spdob": None, "anni": None, "expected": []},
        {"pin": "839201", "dob": None, "spdob": None, "anni": None, "expected": []},

    ]
    
    print("📡 Fetching most common MPINs from Pocket-Lint...")

    common4 = set(fetch_common_digit_pins_from_pocketlint("p", "Common four-digit PINs", 4))
    common6 = set(fetch_common_digit_pins_from_pocketlint("p", "Common six-digit PINs", 6))
    

    passed = 0
    for idx, case in enumerate(test_cases, 1):
        pin = case["pin"]
        pin_len = len(pin)

        reasons = []

        if pin_len == 4 and pin in common4:
            reasons.append("COMMONLY_USED")
        elif pin_len == 6 and pin in common6:
            reasons.append("COMMONLY_USED")

        if case["dob"] and pin in generate_all_combinations([case["dob"]], pin_len):
            reasons.append("DEMOGRAPHIC_DOB_SELF")
        if case["spdob"] and pin in generate_all_combinations([case["spdob"]], pin_len):
            reasons.append("DEMOGRAPHIC_DOB_SPOUSE")
        if case["anni"] and pin in generate_all_combinations([case["anni"]], pin_len):
            reasons.append("DEMOGRAPHIC_ANNIVERSARY")

        if sorted(reasons) == sorted(case["expected"]):
            print(f"✅ Test {idx:02d} Passed")
            passed += 1
        else:
            print(f"❌ Test {idx:02d} Failed")
            print(f"   PIN: {pin}")
            print(f"   Expected: {case['expected']}")
            print(f"   Got     : {reasons}")

    print(f"\n✅ {passed} out of {len(test_cases)} tests passed.")

run_tests()
