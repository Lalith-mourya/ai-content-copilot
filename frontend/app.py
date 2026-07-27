import streamlit as st
import httpx
import os
from pathlib import Path

# Configure Page Settings
st.set_page_config(
    page_title="AI Content Production Copilot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and Inject Custom CSS
styles_path = Path(__file__).parent / "styles.css"
if styles_path.exists():
    with open(styles_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("Custom CSS file 'styles.css' not found. Rendering default Streamlit styling.")

# App Header
st.markdown("<h1>AI Content Production Copilot</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color: #a5b1c2; font-size: 1.1em; margin-bottom: 2rem;'> "
    "A multi-agent editorial assistant for writers and publishers. Check lore consistency, polish dialogue, "
    "translate dialects, and generate synthetic voiceovers instantly."
    "</p>",
    unsafe_allow_html=True
)

# Sidebar Configuration
st.sidebar.markdown("## Pipeline Controls")

# Groq API Key Input
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", help="Enter your Groq API Key to authenticate.")

# Backend API Configuration (Falls back to localhost if environment variable is not defined)
backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")


# Story Settings
st.sidebar.markdown("### Story Properties")
genre = st.sidebar.selectbox(
    "Genre",
    ["Drama", "Fantasy", "Sci-Fi", "Thriller", "Romance", "Horror", "Mystery"]
)
target_audience = st.sidebar.selectbox(
    "Target Audience",
    ["Young Adults", "Children", "General Adults", "Senior Citizens"]
)

# Localization & Voice Settings
st.sidebar.markdown("### Audio & Localization")
language = st.sidebar.selectbox(
    "Target Language",
    ["English", "Tamil", "Hindi", "Spanish", "Telugu"],
    help="Stories are edited in English first. Choose language to localize and narrate."
)
voice = st.sidebar.selectbox(
    "Voice Gender",
    ["Female", "Male"],
    help="Select the narrator profile gender."
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**How to Use:**\n"
    "1. Enter your Groq API Key in the sidebar.\n"
    "2. Paste your draft chapter.\n"
    "3. Provide character info/rules in the Series Bible.\n"
    "4. Set story properties & localization options.\n"
    "5. Click **Run Production Pipeline**."
)

# Main Grid Layout (Inputs on left, bible on right or stacked)
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### Original Draft Chapter")
    draft_input = st.text_area(
        "Paste your raw manuscript draft chapter here:",
        height=320,
        placeholder="Once upon a time, Jack and Sophia arrived at the old warehouse. Jack was nervous...",
        value=""
    )

with col_right:
    st.markdown("### Series Bible & Context")
    bible_input = st.text_area(
        "Character sheets, lore facts, and story rules:",
        height=320,
        placeholder="Sarah: Stubborn archaeologist. Her father, Dr. Sterling, went missing last year. She hates excuses.\nRohan: Former field agent, calls Sarah 'Sar', cautious but loyal.\nLore: The Obsidian Artifact must not be activated near metallic objects.",
        value=""
    )

# Execution Button
st.markdown("---")
run_button = st.button("Run Production Pipeline", use_container_width=True)

# Output Section
if run_button:
    if not groq_api_key.strip():
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not draft_input.strip():
        st.error("Please enter a draft chapter to analyze.")
    else:
        # Spinner for pipeline tracking
        with st.spinner("Executing Multi-Agent Content Pipeline..."):
            payload = {
                "original_draft": draft_input,
                "genre": genre,
                "target_audience": target_audience,
                "language": language,
                "voice": voice,
                "series_bible": bible_input,
                "api_key": groq_api_key
            }

            
            try:
                # Call backend API
                api_endpoint = f"{backend_url.rstrip('/')}/api/copilot/run"
                response = httpx.post(api_endpoint, json=payload, timeout=120.0)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("Pipeline Executed Successfully!")
                    
                    # Display Execution logs
                    with st.expander("System Trajectory & Logs", expanded=False):
                        for log in data.get("logs", []):
                            st.write(log)
                            
                    # Display Agent Results inside Tabs
                    tab_editorial, tab_polished, tab_translation, tab_audiobook = st.tabs([
                        "Planner Feedback", 
                        "Polished Script", 
                        "Translated Script", 
                        "Audiobook Player"
                    ])
                    
                    with tab_editorial:
                        st.markdown("### Consistency Assessment & Editorial Notes")
                        st.markdown(
                            f"<div class='report-card'>{data.get('planner_feedback', '')}</div>", 
                            unsafe_allow_html=True
                        )
                        
                    with tab_polished:
                        st.markdown("### Refined Chapter Draft")
                        st.markdown(
                            f"<div class='report-card'>{data.get('refined_draft', '')}</div>", 
                            unsafe_allow_html=True
                        )
                        st.download_button(
                            label="Download Polished Chapter (Markdown)",
                            data=data.get("refined_draft", ""),
                            file_name=f"polished_{genre.lower()}.md",
                            mime="text/markdown"
                        )
                        
                    with tab_translation:
                        st.markdown(f"### Localized Chapter ({language})")
                        st.markdown(
                            f"<div class='report-card'>{data.get('localized_draft', '')}</div>", 
                            unsafe_allow_html=True
                        )
                        st.download_button(
                            label=f"Download Localized Chapter ({language})",
                            data=data.get("localized_draft", ""),
                            file_name=f"translated_{language.lower()}_{genre.lower()}.md",
                            mime="text/markdown"
                        )
                        
                    with tab_audiobook:
                        st.markdown("### AI Narration Audiobook")
                        audio_url = data.get("audio_url")
                        
                        if audio_url:
                            st.write("Stream the narration directly below:")
                            st.audio(audio_url, format="audio/mp3")
                            
                            # Provide direct download link for user
                            st.markdown(f"[Direct Audiobook Download Link]({audio_url})")
                        else:
                            st.warning("Audio synthesis was skipped or failed. Check the logs for details.")

                            
                else:
                    st.error(f"Error from Backend API: {response.status_code} - {response.text}")
                    
            except httpx.ConnectError:
                st.error("Failed to connect to the backend server. Please verify FastAPI backend is running.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
