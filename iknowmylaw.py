import streamlit as st
import os
import time
from google import genai
from google.genai import types

# Page Setup
st.set_page_config(
    page_title="Nyaya AI - Legal Intelligence",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Atharv AI: Indian Legal Intelligence Platform")
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
                    clean_key = str(raw_key).strip().strip('"').strip("'")
                    client = genai.Client(api_key=clean_key)
                    
                    system_prompt = (
                        "You are an expert Indian Legal AI Assistant trained in Indian statutes "
                        "(BNS 2023, BNSS, BSA, IPC, Consumer Protection Act 2019).\n"
                        "Structure your answer cleanly into:\n"
                        "1. Core Legal Assessment\n"
                        "2. Applicable Legal Sections & Statutes\n"
                        "3. Actionable Next Steps"
                    )

                    # Retry parameters for 503 traffic spikes
                    max_retries = 3
                    delay = 2
                    response_text = None
                    last_error = None

                    for attempt in range(max_retries):
                        try:
                            response = client.models.generate_content(
                                model='gemini-3.6-flash',
                                contents=f"Domain: {domain}\nQuery: {user_query}",
                                config=types.GenerateContentConfig(
                                    system_instruction=system_prompt
                                )
                            )
                            response_text = response.text
                            break  # Success! Exit retry loop
                        except Exception as e:
                            last_error = e
                            if "503" in str(e) or "UNAVAILABLE" in str(e):
                                time.sleep(delay)
                                delay *= 2  # Exponential backoff (2s, 4s, 8s)
                            else:
                                break  # Don't retry non-503 errors

                    if response_text:
                        st.markdown(response_text)
                        st.info("⚠️ Disclaimer: Educational guidance under Indian Law only. Not formal legal advice.")
                        
                        # Add download button for report
                        st.download_button(
                            label="📥 Download Legal Advisory (TXT)",
                            data=response_text,
                            file_name="Nyaya_AI_Legal_Advisory.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"Server is experiencing high traffic. Please try clicking submit again. Details: {str(last_error)}")
