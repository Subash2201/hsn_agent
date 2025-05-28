import pandas as pd
from pathlib import Path

def load_master_data(file_path: Path = None) -> pd.DataFrame:
    if file_path is None:
        file_path = Path(__file__).parent / "data/HSN_Master_Data.xlsx"

    df = pd.read_excel(file_path, dtype=str)

    # Sanitize all column names (strip, remove BOMs/spaces)
    df.columns = [col.strip().replace("\ufeff", "").replace(" ", "") for col in df.columns]

    # DEBUG: Print column names
    print("Excel Columns:", df.columns.tolist())

    # Rename sanitized columns to expected names
    if "HSNCode" not in df.columns or "Description" not in df.columns:
        raise ValueError("❌ Expected columns 'HSNCode' and 'Description' not found. Got: " + str(df.columns.tolist()))

    # Normalize column values
    df["HSNCode"] = df["HSNCode"].str.strip().str.zfill(8)
    df["Description"] = df["Description"].str.strip()

    return df
