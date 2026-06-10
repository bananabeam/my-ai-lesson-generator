import streamlit as st
from google import genai

# 1. Page layout configuration
st.set_page_config(page_title="AI Daily Lesson Log Generator", layout="centered")

# Custom design to mimic the clean card structure
st.markdown("""
    <style>
    .title-text { color: #1a73e8; font-weight: bold; text-align: center; font-size: 2.5rem; margin-bottom: 0px; }
    .subtitle-text { text-align: center; color: #5f6368; font-size: 1.1rem; margin-bottom: 25px; }
    .credit { text-align: center; color: #80868b; font-size: 0.85rem; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

# 2. Header Elements
st.markdown('<h1 class="title-text">AI Daily Lesson Log Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">K-12 & SHS One Day Lesson Log</p>', unsafe_allow_html=True)
st.markdown('<p class="credit">Inspired by Reymond P. Samoranos</p>', unsafe_allow_html=True)

st.info("Instantly create a detailed single-day lesson plan. You can input your specific Standards/Competency, or leave them blank and let the AI generate them based on the Subject and Grade.")

# 3. Form Inputs Layout
col1, col2, col3 = st.columns([2, 2, 3])

with col1:
    subject = st.text_input("Subject", value="Mathematics")
with col2:
    grade_level = st.text_input("Grade Level", value="Grade 6")
with col3:
    daily_topic = st.text_input("Daily Topic (Optional)", placeholder="e.g., Fractions, Ecosystems")

st.markdown("### Custom Standards (Optional)")
content_standard = st.text_area("A. Content Standard", placeholder="e.g., Demonstrates understanding of the four fundamental operations involving fractions.")

# 4. Connecting to Gemini and Generating Content
if st.button("Generate Lesson Log", type="primary"):
    # Securely fetch the API key you will set up in Step 4
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)
        
        with st.spinner("Generating your lesson log with Gemini AI..."):
            prompt = f"""
            You are an expert K-12 and Senior High School (SHS) curriculum developer.
            Create a detailed single-day Lesson Log based on these inputs:
            - Subject: {subject}
            - Grade Level: {grade_level}
            - Daily Topic: {daily_topic if daily_topic else 'Suggest an appropriate topic for this grade and subject'}
            - Content Standard: {content_standard if content_standard else 'Generate an appropriate content standard'}
            
            Structure the output professionally with sections: Objectives, Learning Resources, Procedures, and Reflection.
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            st.success("Done!")
            st.markdown("---")
            st.markdown(response.text)
            
    except Exception as e:
        st.error("Error: Please make sure your GEMINI_API_KEY is correctly added to your Streamlit App Secrets.")
