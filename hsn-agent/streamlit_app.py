# streamlit_app.py

import streamlit as st
from agent import HSNValidationAgent

agent = HSNValidationAgent()

st.set_page_config(page_title="HSN Code Validation Agent", layout="centered")

st.title("🔍 HSN Code Validation & Suggestion Agent")
st.markdown("Validate HSN codes or get suggestions based on product descriptions.")

tab1, tab2 = st.tabs(["📋 Validate Code", "💡 Suggest from Description"])

with tab1:
    code_input = st.text_input("Enter one or more HSN codes (comma or space separated):", "")
    if st.button("Validate"):
        if code_input.strip():
            codes = code_input.replace(",", " ").split()
            results = [agent.validate_code(c) for c in codes]
            for res in results:
                st.markdown(f"""
                **Code:** `{res['code']}`  
                ✅ Valid: **{res['valid']}**
                """)
                if res['valid']:
                    st.success(f"✔️ {res['description']}")
                else:
                    st.error(f"❌ {res['reason']}")
        else:
            st.warning("Please enter at least one code.")

with tab2:
    desc_input = st.text_input("Enter product/service description:", "")
    if st.button("Suggest"):
        if desc_input.strip():
            suggestions = agent.suggest_codes(desc_input)
            for s in suggestions:
                st.markdown(f"""
                **HSNCode:** `{s['code']}`  
                📄 **{s['description']}**  
                🎯 Score: `{s['score']}`
                """)
        else:
            st.warning("Please enter a description.")
