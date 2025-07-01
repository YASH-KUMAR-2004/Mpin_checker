from datetime import datetime
import requests
from bs4 import BeautifulSoup

# ✅ Function to fetch common 4- or 6-digit PINs from Pocket-Lint
def fetch_common_digit_pins_from_pocketlint(tag_, id_, length):
    url = "https://www.pocket-lint.com/these-are-the-20-most-common-phone-pins-is-your-device-vulnerable/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print("❌ Failed to fetch PINs from Pocket-Lint:", e)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    heading = soup.find(lambda tag: tag.name.startswith(tag_) and id_ in tag.get_text())

    if not heading:
        print("❌ PIN section not found")
        return []

    pin_list = []
    ul_tag = heading.find_next("ul")
    if ul_tag:
        for li in ul_tag.find_all("li"):
            text = li.get_text(strip=True)
            if text.isdigit() and len(text) == length:
                pin_list.append(text)

    return pin_list

# ✅ Function to validate date input
def get_valid_date(prompt):
    while True:
        date_str = input(prompt).strip()
        if date_str == "":
            return None
        try:
            return datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            print("❌ Invalid date! Please use DD-MM-YYYY format.")

# ✅ Function to generate all combinations from a list of dates
def generate_all_combinations(dates, pin_length=4):
    def generate_date_pins(date_obj, pin_length):
        dd = f"{date_obj.day:02d}"
        mm = f"{date_obj.month:02d}"
        yyyy = f"{date_obj.year}"
        yy = yyyy[-2:]

        pins = set()
        if pin_length == 4:
            pins.update([
                dd + mm,
                mm + dd,
                yy + mm,
                mm + yy,
                yyyy[-4:],     # YYYY
                dd + yy,
                yy + dd
            ])
        elif pin_length == 6:
            pins.update([
                dd + mm + yy,
                yy + mm + dd,
                mm + dd + yy,
                dd + mm + yyyy[-2:],
                yyyy + mm,
                yyyy + dd,
                dd + yyyy,
                mm + yyyy
            ])
        return pins

    all_pins = set()
    for date in dates:
        if date:
            all_pins.update(generate_date_pins(date, pin_length))
    return list(all_pins)

# ✅ MAIN EXECUTION
if __name__ == "__main__":
    print("📡 Fetching most common MPINs from Pocket-Lint...")
    common4 = set(fetch_common_digit_pins_from_pocketlint("p", "Common four-digit PINs", 4))
    common6 = set(fetch_common_digit_pins_from_pocketlint("p", "Common six-digit PINs", 6))

    pin = input("\n🔐 Enter your 4 or 6 digit MPIN: ").strip()
    if not (pin.isdigit() and len(pin) in [4, 6]):
        print("❌ Invalid MPIN length! It must be 4 or 6 digits.")
        exit()

    # Get user demographic info
    dob = get_valid_date("📅 Enter your Date of Birth (DD-MM-YYYY), or press Enter to skip: ")
    spdob = get_valid_date("📅 Enter your Spouse's DOB, or press Enter to skip: ")
    anni = get_valid_date("📅 Enter your Anniversary Date, or press Enter to skip: ")

    pin_len = len(pin)
    reasons = []

    # Check common PINs
    if pin_len == 4 and pin in common4:
        reasons.append("COMMONLY_USED")
    elif pin_len == 6 and pin in common6:
        reasons.append("COMMONLY_USED")

    # Check date-based patterns
    if dob and pin in generate_all_combinations([dob], pin_len):
        reasons.append("DEMOGRAPHIC_DOB_SELF")
    if spdob and pin in generate_all_combinations([spdob], pin_len):
        reasons.append("DEMOGRAPHIC_DOB_SPOUSE")
    if anni and pin in generate_all_combinations([anni], pin_len):
        reasons.append("DEMOGRAPHIC_ANNIVERSARY")

    # Print result
    print("\n🔎 MPIN Strength:", "WEAK" if reasons else "STRONG")
    print("📋 Reasons:", reasons if reasons else "[]")
