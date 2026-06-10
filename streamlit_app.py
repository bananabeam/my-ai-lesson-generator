import streamlit as st
from google import genai

# Helper function to convert AI Markdown text into an error-free Word-compatible Document template
def convert_to_clean_doc(text):
    # Creating a structured layout format that opens flawlessly in Microsoft Word
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>5-Days Weekly Lesson Log</title>
        <style>
            body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #000000; padding: 20px; }}
            h1 {{ color: #1a73e8; font-size: 22pt; border-bottom: 2px solid #1a73e8; padding-bottom: 5px; margin-top: 20px; }}
            h2 {{ color: #b06000; font-size: 16pt; margin-top: 18px; border-bottom: 1px solid #eeeeee; padding-bottom: 3px; }}
            h3 {{ color: #333333; font-size: 13pt; margin-top: 14px; }}
            p {{ font-size: 11pt; margin-bottom: 8px; text-align: justify; }}
            ul, ol {{ margin-top: 5px; margin-bottom: 10px; padding-left: 20px; }}
            li {{ font-size: 11pt; margin-bottom: 4px; }}
            .header-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            .header-table td {{ border: 1px solid #dddddd; padding: 8px; font-size: 11pt; }}
        </style>
    </head>
    <body>
        <h2 style="text-align: center; color: #1a73e8;">5-Days WEEKLY LESSON LOG</h2>
        <p style="text-align: center; font-style: italic;">Generated via AI Lesson Log Generator</p>
        <br>
    """
    
    # Process each line and format basic Markdown tags into strict, universally accepted elements
    for line in text.split('\n'):
        line_str = line.strip()
        if not line_str:
            continue
        
        # Format headings safely
        if line_str.startswith("###"):
            html_content += f"<h3>{line_str.replace('###', '').strip()}</h3>"
        elif line_str.startswith("##"):
            html_content += f"<h2>{line_str.replace('##', '').strip()}</h2>"
        elif line_str.startswith("#"):
            html_content += f"<h1>{line_str.replace('#', '').strip()}</h1>"
        # Format lists safely
        elif line_str.startswith("- ") or line_str.startswith("* "):
            html_content += f"<li>{line_str[2:].strip()}</li>"
        else:
            # Handle clean bold formatting replacements natively
            processed_line = line_str
            while "**" in processed_line:
                processed_line = processed_line.replace("**", "<b>", 1).replace("**", "</b>", 1)
            html_content += f"<p>{processed_line}</p>"
            
    html_content += "</body></html>"
    return html_content

# 1. Wide Page Layout configuration to fit long text comfortably
st.set_page_config(page_title="AI 5-Days Lesson Log Generator", layout="wide")

# Custom design for background image tiling, transparency overlay, and responsive container cards
st.markdown("""
    <style>
    /* Injected tiled brand logo with a 50% opacity mask over the canvas */
    .stApp {
        background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), 
                          url("https://raw.githubusercontent.com/bananabeam/my-ai-lesson-generator/main/ChatGPT%20Image%20Feb%2025%2C%202026%2C%2008_32_02%20AM.png");
        background-repeat: repeat;
        background-size: 280px;
    }
    
    /* Centered content box layout */
    .block-container {
        max-width: 1100px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }
    
    /* Paper card container styling */
    .lesson-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 35px;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    
    .title-text { color: #1a73e8; font-weight: bold; text-align: center; font-size: 2.6rem; margin-bottom: 5px; }
    .subtitle-text { text-align: center; color: #3c4043; font-weight: 500; font-size: 1.2rem; margin-bottom: 12px; }
    .developer-text { text-align: center; color: #5f6368; font-size: 0.95rem; margin-bottom: 25px; }
    .developer-link { color: #1a73e8; text-decoration: none; font-weight: bold; }
    .intro-text { color: #4a4a4a; font-size: 1rem; line-height: 1.6; text-align: center; margin-bottom: 30px; }
    .custom-section-title { color: #b06000; font-weight: bold; font-size: 1.2rem; margin-top: 15px; margin-bottom: 15px; }
    .note-text { color: #5f6368; font-size: 0.9rem; font-style: italic; margin-top: 8px; }
    </style>
""", unsafe_allow_html=True)

# Wrap content inside a stylized workspace wrapper
st.markdown('<div class="lesson-card">', unsafe_allow_html=True)

# 2. Header Elements
st.markdown('<h1 class="title-text">AI 5-Days Lesson Log Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">K-12 & SHS 5-Dayss Weekly Lesson Log</p>', unsafe_allow_html=True)
st.markdown('<p class="developer-text">Developed by: <a class="developer-link" href="#">Adonis T. Reyes</a></p>', unsafe_allow_html=True)

st.markdown('<p class="intro-text">Instantly create a detailed weekly lesson plan spanning 5 Dayss. You can input your specific Standards/Competency, or leave them blank and let the AI generate them based on the Subject and Grade.</p>', unsafe_allow_html=True)

# 3. Main Data Row (3 Columns)
col1, col2, col3 = st.columns([1, 1, 1.2])

with col1:
    subject = st.text_input("Subject", placeholder="e.g., Science, English, Math")
with col2:
    grade_level = st.text_input("Grade Level", placeholder="e.g., Grade 7, Kindergarten")
with col3:
    daily_topic = st.text_input("Weekly Topic/Theme (Optional: AI will suggest if empty)", placeholder="e.g., Fractions, Ecosystems")

st.markdown("---")

# 4. Custom Standards Layout Section
st.markdown('<p class="custom-section-title">Custom Standards (A, B, C are Optional)</p>', unsafe_allow_html=True)

content_standard = st.text_area(
    "A. Content Standard", 
    placeholder="e.g., Demonstrates understanding of the four fundamental operations involving fractions."
)

performance_standard = st.text_area(
    "B. Performance Standard", 
    placeholder="e.g., Able to apply the four fundamental operations involving fractions to solve problems."
)

learning_competency = st.text_area(
    "C. Learning Competency (LC Code)", 
    placeholder="e.g., M6NS-Id-106: Adds and subtracts simple fractions and mixed numbers."
)

st.markdown('<p class="note-text"><b>D. Learning Objectives</b> will be automatically generated by the AI for each Days based on the standards and competency provided above.</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True) # End card container

st.markdown("<br>", unsafe_allow_html=True)

# 5. Generation Block
if st.button("Generate 5-Days Weekly Lesson Log", type="primary"):
    if not subject or not grade_level:
        st.error("Please fill in at least the 'Subject' and 'Grade Level' fields to get started.")
    else:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=api_key)
            
            with st.spinner("Creating your 5-Days weekly lesson log... This might take a moment longer."):
                prompt = f"""
                You are an expert K-12 and Senior High School (SHS) curriculum developer specializing in DepEd educational guidelines.
                Create a complete, detailed 5-Days Weekly Lesson Log (spanning Days 1 to Days 5) based on these specifications:
                
                - Subject: {subject}
                - Grade Level: {grade_level}
                - Core Weekly Topic/Theme: {daily_topic if daily_topic else 'Automatically determine a comprehensive weekly theme appropriate for this level'}
                
                CRITICAL INSTRUCTIONS FOR STANDARDS:
                - Content Standard: {content_standard if content_standard else 'Develop a standard DepEd-aligned content standard.'}
                - Performance Standard: {performance_standard if performance_standard else 'Develop a standard DepEd-aligned performance standard.'}
                - Learning Competency / Code: {learning_competency if learning_competency else 'Provide appropriate learning competency codes.'}
                
                Please generate the output beautifully using Markdown headers. Keep the structure organized by dividing the workflow across 5 Dayss (Days 1, Days 2, Days 3, Days 4, Days 5).
                
                For each Days, explicitly detail:
                1. Daily Objective (Derived from the core standards)
                2. Subject Matter / Core Sub-topic for that specific Days
                3. Learning Resources & Materials
                4. Procedures (Review/Motivation, Activity, Abstraction, Application, and Evaluation)
                
                Conclude the entire log with a single 'V. Remarks & Reflection' section at the very end.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                # Store the result text in a session state variable
                st.session_state['generated_log'] = response.text
                st.success("5-Days Lesson Log Successfully Generated!")
                
        except Exception as e:
            st.error("Authentication Error: Please verify that your GEMINI_API_KEY is correctly added to your Streamlit App Secrets.")

# 6. Display Result & Provide Instant Download Options
if 'generated_log' in st.session_state:
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.markdown("### Generated 5-Days Weekly Lesson Plan")
    st.markdown("---")
    st.markdown(st.session_state['generated_log'])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate clean standard document template
    clean_doc_data = convert_to_clean_doc(st.session_state['generated_log'])
    
    # Safely download as a structured Document file format 
    st.download_button(
        label="📥 Download Lesson Log (Open directly in Word)",
        data=clean_doc_data,
        file_name=f"5_Days_Lesson_Log_{subject.replace(' ', '_')}_{grade_level.replace(' ', '_')}.doc",
        mime="application/msword"
    )
    st.markdown('</div>', unsafe_allow_html=True)
