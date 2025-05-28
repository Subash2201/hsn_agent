
# 🧾 HSN Code Validation & Suggestion Agent

An intelligent assistant built using Python and Streamlit that validates HSN (Harmonized System of Nomenclature) codes and provides description-based suggestions. It follows proper HSN hierarchy and supports fuzzy search to help users find relevant codes.

---

## 📦 Features

- ✅ Validate single or multiple HSN codes (2, 4, 6, or 8 digits)
- 🔍 Suggest relevant HSN codes based on product descriptions using fuzzy matching
- 🧠 Verifies code hierarchy (parents must exist for 8-digit codes)
- 🚀 Built using [Google ADK](https://github.com/google/adk) framework (mocked in current version)
- 📊 Reads master data from Excel file

---

## 📁 Project Structure

```
hsn-agent/
│
├── streamlit_app.py             # Streamlit UI to interact with the agent
├── agent.py                     # Core logic for validation & suggestion
├── utils.py                     # Helper functions (e.g., data loading)
├── data/
│   └── HSN_Master_Data.xlsx     # Master data file (HSNCode & Description)
└── README.md                    # This file
```

---

## 🔧 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/hsn-agent.git
cd hsn-agent
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

> `requirements.txt` should include:  
> `pandas`, `openpyxl`, `streamlit`, `rapidfuzz`

3. **Add the HSN Master Data**

- Place your `HSN_Master_Data.xlsx` inside the `data/` folder.
- It must contain two columns:
  - `HSN Code`
  - `Description`

4. **Run the Streamlit app**

```bash
streamlit run streamlit_app.py
```

---

## 🧠 How Validation Works

- Input codes are padded to 8 digits (e.g., `01` → `00000001`)
- Validation steps:
  - ✔️ Format check (must be numeric with length 2/4/6/8)
  - ✔️ Presence in master data
  - ✔️ For 8-digit codes: all parent levels (2, 4, 6) must exist

---

## ✅ Example Validations

### 🔹 2-digit code

```
Input: 01
Padded: 00000001
✅ Format: valid
✅ Exists in master data
✅ No hierarchy check needed
```

---

### 🔹 3-digit code

```
Input: 110
Padded: 00000110
❌ Format: invalid (only 2, 4, 6, or 8-digit codes allowed)
```

---

### 🔹 4-digit code

```
Input: 1101
Padded: 00001101
✅ Format: valid
✅ Exists in master data
✅ No hierarchy check needed
```

---

### 🔹 8-digit code (valid)

```
Input: 11011010
Padded: 11011010
✅ Format: valid
✅ Exists in master data
✅ Parent codes exist:
   ✔ 11      (11000000)
   ✔ 1101    (11010000)
   ✔ 110110  (11011000)
✅ All checks passed
```

---

### 🔹 8-digit code (invalid parent)

```
Input: 01011010
Padded: 01011010
✅ Format: valid
✅ Exists in master data
❌ Parent code 01010000 is missing → Invalid hierarchy
```

---

## 💡 Suggestions via Description

You can also enter product descriptions to get code suggestions:

```
Input: plastic chair

Top Matches:
1. Code: 94037000 - Description: Furniture of plastics
2. Code: 39269099 - Description: Other plastic articles, not elsewhere specified
...
```

---


