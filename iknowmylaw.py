import streamlit as st
import os
from google import genai
from google.genai import types

# Page Setup
st.set_page_config(
    page_title="Nyaya AI - Legal Intelligence",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ NYAYA AI: Indian Legal Intelligence Platform")
st.caption("Powered by Gemini • Statute & Case Analysis (BNS, BNSS, BSA, IPC)")

# Sidebar Navigation
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

# Layout Columns
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📝 Case Description")
    user_query = st.text_area(
        "Describe your legal issue:",
        placeholder="E.g., I ordered a product worth ₹75,000 from an online seller. It arrived broken...",
        height=220
    )
    submit_btn = st.button("Generate Legal Analysis 🚀", type="primary", use_container_width=True)

with col2:
    st.subheader("📋 Legal Advisory & Next Steps")
    if submit_btn:
        if not user_query.strip():
            st.warning("Please type a legal query before submitting.")
        else:
            raw_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
            
            if not raw_key:
                st.error("🔑 API Key Missing! Please add GEMINI_API_KEY in Streamlit Secrets.")
            else:
                with st.spinner("Analyzing relevant statutes and procedural remedies..."):
                    try:
                        clean_key = str(raw_key).strip().strip('"').strip("'")
                        
                        # New SDK Client
                        client = genai.Client(api_key=clean_key)
                        
                        system_prompt = (
                            "You are an expert Indian Legal AI Assistant trained in Indian statutes "
                            "(BNS 2023, BNSS, BSA, IPC, Consumer Protection Act 2019).\n"
                            "Structure your answer cleanly into:\n"
                            "1. Core Legal Assessment\n"
                            "2. Applicable Legal Sections & Statutes\n"
                            "3. Actionable Next Steps"
                        )

                        # Using gemini-2.5-flash on the modern Client API
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=f"Domain: {domain}\nQuery: {user_query}",
                            config=types.GenerateContentConfig(
                                system_instruction=system_prompt,
                                temperature=0.2
                            )
                        )
                        
                        st.markdown(response.text)
                        st.info("⚠️ Disclaimer: Educational guidance under Indian Law only. Not formal legal advice.")
                        
                    except Exception as e:
                        st.error(f"Error executing query: {str(e)}")
