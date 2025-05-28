
from typing import List, Dict, Union
import pandas as pd
from pathlib import Path
from utils import load_master_data
from rapidfuzz import process, fuzz

SUPPORTED_LENGTHS = {2, 4, 6, 8}
# MOCK ADK CLASSES – REPLACE WHEN YOU GET REAL ADK
class Agent:
    def __init__(self, **kwargs):
        pass

class UserMessage:
    def __init__(self, text):
        self.text = text

class AgentMessage:
    @staticmethod
    def from_dict(d):
        return d
def load_master_data() -> pd.DataFrame:
    path = Path(__file__).parent / "data/HSN_Master_Data.xlsx"
    df = pd.read_excel(path, dtype=str)
    
    # Remove spaces and unify column names
    df.columns = df.columns.str.strip().str.replace(" ", "")
    
    # Now use the column name without spaces
    df["HSNCode"] = df["HSNCode"].str.strip().str.zfill(8)
    df["Description"] = df["Description"].str.strip()
    
    return df


class HSNValidationAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.master = load_master_data()
        self.codes_set = set(self.master["HSNCode"])

    def _is_valid_format(self, code: str) -> bool:
        return code.isdigit() and len(code) in SUPPORTED_LENGTHS

    def _exists(self, code: str) -> bool:
        return code in self.codes_set

    def _parents_exist(self, code: str) -> bool:
        if len(code) != 8:
            return True  # Skip hierarchy check for codes shorter than 8 digits

        parents = [code[:l].ljust(8, '0') for l in (2, 4, 6)]
        print("Checking parents for", code, "->", parents)

        for parent in parents:
            if parent not in self.codes_set:
                print(f"Missing parent code: {parent}")
                return False

        return True



    def validate_code(self, code: str) -> Dict[str, Union[str, bool]]:
        raw_code = code.strip()
        code = raw_code.zfill(8)

        if not self._is_valid_format(raw_code):
            return {"code": code, "valid": False, "reason": "Invalid format (numeric 2/4/6/8 digits expected)"}
    
        if not self._exists(code):
            return {"code": code, "valid": False, "reason": "Code not found in master data"}

    # ✅ Only check parents if it's originally 8 digits
        if len(raw_code) == 8 and not self._parents_exist(code):
            return {"code": code, "valid": False, "reason": "Hierarchy incomplete – parent code missing"}

        desc = self.master[self.master["HSNCode"] == code]["Description"].values[0]
        return {"code": code, "valid": True, "description": desc}


    def suggest_codes(self, query: str, top_k: int = 5) -> List[Dict[str, str]]:
        matches = process.extract(query, self.master["Description"], scorer=fuzz.WRatio, limit=top_k)
        return [{
            "code": self.master.iloc[idx]["HSNCode"],
            "description": self.master.iloc[idx]["Description"],
            "score": score
        } for _, score, idx in matches]

    async def on_message(self, msg: UserMessage) -> AgentMessage:
        user_input = msg.text.strip()
        if user_input.replace(",", "").replace(" ", "").isdigit():
            codes = user_input.replace(",", " ").split()
            results = [self.validate_code(code) for code in codes]
            return AgentMessage.from_dict({"content": {"validation": results}})
        else:
            suggestions = self.suggest_codes(user_input)
            return AgentMessage.from_dict({"content": {"suggestions": suggestions}})
