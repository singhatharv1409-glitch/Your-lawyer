import streamlit as st
import os
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Nyaya AI - Legal Advisor",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ NYAYA AI: Indian Legal Intelligence Platform")
st.caption("Powered by Gemini • Statute & Case Analysis (BNS, BNSS, BSA, IPC)")

domain = st.sidebar.selectbox(
    "Select Primary Legal Domain",
    [
        "Criminal Law (BNS / IPC)",
        "Civil & Property Law",
        "Consumer Protection Act 2019",
        "Corporate & Contract Law",
        "Family & Matrimonial Law"
    ]
)

col1, col2 = st.columns([1, 1])

with col1:
    user_query = st.text_area(
        "Describe your legal issue:",
        placeholder="E.g., An e-commerce seller sent a defective phone and refuses a refund...",
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
                with st.spinner("Analyzing statutes..."):
                    try:
                        clean_key = str(raw_key).strip().strip('"').strip("'")
                        
                        # Initialize client passing the key directly to avoid 401 header errors
                        client = genai.Client(api_key=clean_key)
                        
                        system_prompt = (
                            "You are an expert Indian Legal AI Assistant trained in Indian statutes "
                            "(BNS 2023, BNSS, BSA, IPC, Consumer Protection Act).\n"
                            "Structure your answer into:\n"
                            "1. Core Legal Assessment\n"
                            "2. Applicable Legal Sections\n"
                            "3. Recommended Next Steps"
                        )

                        response = client.models.generate_content(
                            model='gemini-3.6-flash',
                            contents=f"Domain: {domain}\nQuery: {user_query}",
                            config=types.GenerateContentConfig(
                                system_instruction=system_prompt,
                                temperature=0.2
                            )
                        )
                        
                        st.markdown(response.text)
                        st.info("⚠️ Disclaimer: Informational guidance under Indian Law only. Not formal legal representation.")
                        
                    except Exception as e:
                        st.error(f"Error executing query: {str(e)}")
