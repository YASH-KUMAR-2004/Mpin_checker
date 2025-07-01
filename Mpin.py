from datetime import datetime

# Function to validate date input
def get_valid_date(prompt):
    while True:
        date_str = input(prompt).strip()
        if date_str == "":
            return None  # Allow skipping if user presses Enter
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            return date_obj
        except ValueError:
            print("❌ Invalid date format or value! Please enter in DD-MM-YYYY format.")

# Function to generate date-based PINs
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

# ---- MAIN EXECUTION ----

# Step 1: Get MPIN input and validate length
pin = input("Enter your 4 or 6 digit MPIN: ").strip()
if not (pin.isdigit() and len(pin) in [4, 6]):
    print("❌ You entered an invalid PIN. It must be 4 or 6 digits.")
    exit()

# Step 2: Get date inputs
dob = get_valid_date("Enter your date of birth (DD-MM-YYYY) or press Enter to skip: ")
spdob = get_valid_date("Enter your spouse's date of birth (DD-MM-YYYY) or press Enter to skip: ")
anni = get_valid_date("Enter your anniversary date (DD-MM-YYYY) or press Enter to skip: ")

# Step 3: Define common PINs
common4 = {
    "1234", "0000", "1111", "1212", "7777",
    "1004", "2000", "4444", "2222", "6969",
    "9999", "3333", "5555", "6666", "1122",
    "1313", "8888", "4321", "1010", "2580"
}

common6 = {
    "123456", "000000", "111111", "121212", "654321",
    "112233", "123123", "456456", "159753", "222222",
    "999999", "333333", "444444", "555555", "666666",
    "101010", "777777", "987654", "123321", "147258"
}

# Step 4: Start evaluation
reasons = []
pin_len = len(pin)

# Check if it's a commonly used PIN
if pin_len == 4 and pin in common4:
    reasons.append("COMMONLY_USED")
elif pin_len == 6 and pin in common6:
    reasons.append("COMMONLY_USED")

# Check demographic reasons
if dob and pin in generate_all_combinations([dob], pin_len):
    reasons.append("DEMOGRAPHIC_DOB_SELF")
if spdob and pin in generate_all_combinations([spdob], pin_len):
    reasons.append("DEMOGRAPHIC_DOB_SPOUSE")
if anni and pin in generate_all_combinations([anni], pin_len):
    reasons.append("DEMOGRAPHIC_ANNIVERSARY")

# Step 5: Output result
if reasons:
    print("\nStrength: WEAK")
    print("Reasons:", reasons)
else:
    print("\nStrength: STRONG")
    print("Reasons: []")
