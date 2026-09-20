import streamlit as st
import os
from google import genai
from google.genai import types

# Page Config
st.set_page_config(
    page_title="Nyaya AI - Indian Legal Intelligence",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    .disclaimer-box {
        background-color: #1e293b;
        border-left: 4px solid #f59e0b;
        padding: 12px;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #cbd5e1;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">⚖️ NYAYA AI: Indian Legal Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Powered by Gemini • Statute & Case Analysis (BNS, BNSS, BSA, IPC)</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Configuration & Guidelines")
domain = st.sidebar.selectbox(
    "Select Primary Legal Domain",
    [
        "Criminal Law (BNS / IPC)",
        "Civil & Property Law",
        "Consumer Protection Act 2019",
        "Corporate & Contract Law",
        "Family & Matrimonial Law",
        "Labor & Employment Law"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Include relevant details such as dates, monetary amounts, and location.")

# Layout
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📝 Case Statement & Query")
    user_query = st.text_area(
        label="Describe the factual situation:",
        placeholder="E.g., An e-commerce seller sent a defective product worth ₹45,000 and refused a refund...",
        height=220
    )
    submit_btn = st.button("Generate Legal Analysis 🚀", type="primary", use_container_width=True)

with col2:
    st.subheader("📋 Statutory Advisory & Next Steps")
    
    if submit_btn:
        if not user_query.strip():
            st.warning("Please enter a legal query before submitting.")
        else:
            api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
            
            if not api_key:
                st.error("🔑 API Key Missing! Please add GEMINI_API_KEY in Streamlit Cloud Secrets.")
            else:
                with st.spinner("Analyzing statutes and procedural law..."):
                    try:
                        # Clean key formatting and pass explicit x-goog-api-key header
                        clean_key = str(api_key).strip().strip('"').strip("'")
                        client = genai.Client(
                            api_key=clean_key,
                            http_options={'headers': {'x-goog-api-key': clean_key}}
                        )
                        
                        system_instruction = (
                            "You are an expert Indian Legal AI Assistant trained in Indian jurisprudence, "
                            "including Bharatiya Nyaya Sanhita (BNS), BNSS, BSA, IPC, CPC, and Consumer Protection Act.\n"
                            "Structure your response strictly into 3 sections:\n"
                            "1. Core Legal Assessment\n"
                            "2. Applicable Sections & Statutes\n"
                            "3. Actionable Next Steps"
                        )

                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=f"Domain: {domain}\nUser Query: {user_query}",
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.2,
                                max_output_tokens=800
                            )
                        )
                        
                        st.markdown(response.text)
                        
                        st.markdown(
                            '<div class="disclaimer-box">'
                            '<b>⚠️ Mandatory Legal Notice:</b> Information provided is for educational purposes under Indian laws only '
                            'and does not constitute formal legal advice under the Advocates Act, 1961.'
                            '</div>',
                            unsafe_allow_html=True
                        )

                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
