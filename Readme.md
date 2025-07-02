# 🔐 MPIN Strength Checking

This project helps evaluate the strength of a 4-digit or 6-digit MPIN (Mobile Personal Identification Number) based on:
- Whether it's a **commonly used MPIN** (fetched via web scraping)
- Whether it's **derived from demographic data**, such as:
  - User's Date of Birth
  - Spouse's Date of Birth
  - Wedding Anniversary

The goal is to guide users toward choosing **stronger and less predictable MPINs** to enhance mobile banking security.

---

## 📁 Folder Structure

Mpin_Strength_Checking/
│
├── Mpin_2.py                      # Python script for logic
├── test_mpin.py                   # Python script for test cases             
├── README.md                      # Project overview and usage guide
└── requirements.txt               # Python dependencies

---

## 🚀 Features

- **Web scraping** using `BeautifulSoup` to fetch the latest common MPINs from a live website.
- **Custom MPIN analysis** based on:
  - User's date of birth
  - Spouse's date of birth (optional)
  - Anniversary date (optional)
- **Strength classification**:
  - `STRONG`: Secure MPIN not based on common patterns or demographic data.
  - `WEAK`: MPIN is too common or easily guessable from user demographics.
- **Detailed reasons** for weakness (e.g., `COMMONLY_USED`, `DEMOGRAPHIC_DOB_SELF`, etc.)
- **20+ automated test cases** to validate the logic.

---

## 📦 Requirements

Install the required dependencies using:

```bash
pip install -r requirements.txt
Contents of requirements.txt:
```

## ✅ How to Run
Open the Mpin_Strength_Checking.ipynb in Jupyter Notebook.

Run the entire notebook to:

Interactively check MPIN strength

Automatically execute all test cases

## 🧪 Sample Use Case
Input:

Date of Birth: 01-01-1990
Spouse DOB: (skip)
Anniversary: (skip)
MPIN: 0101

Output:

🔒 MPIN Strength: WEAK
- Reason: DEMOGRAPHIC_DOB_SELF


## 📌 Notes
The project avoids hardcoding commonly used MPINs and fetches them live using web scraping.

Input dates must be in dd-mm-yyyy format.

MPINs must be 4 or 6 digits long.


## 👤 Author
Yash Kumar

[LinkedIn](https://www.linkedin.com/in/yash-kumar-950b19292?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

[GitHub](https://github.com/YASH-KUMAR-2004)

