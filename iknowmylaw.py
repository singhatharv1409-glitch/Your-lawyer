import streamlit as st
import os
import time
from google import genai
from google.genai import types

# Setup Page Config
st.set_page_config(
    page_title="Nyaya AI - Legal Intelligence",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ NYAYA AI: Indian Legal Intelligence Platform")
st.caption("Powered by Gemini • Statute & Case Analysis (BNS, BNSS, BSA, IPC)")

domain = st.sidebar.selectbox(
    "Select Primary Legal Domain",
    [
        "Consumer Protection Act 2019",
        "Criminal Law (BNS / IPC)",
        "Civil & Property Law",
        "Corporate & Contract Law",
        "Family & Matrimonial Law"
    ]
)

col1, col2 = st.columns([1, 1])

with col1:
    user_query = st.text_area(
        "Describe your legal issue:",
        placeholder="E.g., I bought a product for ₹50,000, it arrived broken, and the store refuses to issue a refund.",
        height=200
    )
    submit_btn = st.button("Generate Legal Analysis 🚀", type="primary")

with col2:
    if submit_btn:
        if not user_query.strip():
            st.warning("Please type a legal query first.")
        else:
            raw_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
            
            if not raw_key:
                st.error("🔑 API Key Missing! Please add GEMINI_API_KEY in Streamlit Secrets.")
            else:
                with st.spinner("Analyzing legal statutes and precedents..."):
                    clean_key = str(raw_key).strip().strip('"').strip("'")
                    client = genai.Client(api_key=clean_key)
                    
                    system_prompt = (
                        "You are an expert Indian Legal AI Assistant trained in Indian statutes "
                        "(BNS 2023, BNSS, BSA, IPC, Consumer Protection Act 2019).\n"
                        "Structure your answer cleanly into:\n"
                        "1. Core Legal Assessment\n"
                        "2. Applicable Legal Sections & Statutes\n"
                        "3. Recommended Next Steps"
                    )

                    # List models to try (primary and fallback)
                    models_to_try = ['gemini-2.5-flash', 'gemini-1.5-flash']
                    response_text = None
                    last_error = None

                    for model_name in models_to_try:
                        # Attempt up to 2 times per model for 503 spikes
                        for attempt in range(2):
                            try:
                                response = client.models.generate_content(
                                    model=model_name,
                                    contents=f"Domain: {domain}\nQuery: {user_query}",
                                    config=types.GenerateContentConfig(
                                        system_instruction=system_prompt,
                                        temperature=0.2
                                    )
                                )
                                response_text = response.text
                                break
                            except Exception as e:
                                last_error = e
                                time.sleep(1) # Short wait before retry
                        if response_text:
                            break

                    if response_text:
                        st.markdown(response_text)
                        st.info("⚠️ Disclaimer: Informational guidance under Indian Law only. Not formal legal advice.")
                    else:
                        st.error(f"Server is currently under heavy load. Please try clicking submit again. Details: {str(last_error)}")
