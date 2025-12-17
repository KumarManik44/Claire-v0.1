import streamlit as st
import requests
import base64

# 1. CONFIGURATION: Set the page to look like a mobile app
st.set_page_config(
    page_title="Claire",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CUSTOM CSS: The "JARVIS" Vibe (Dark mode, neon accents, clean fonts)
st.markdown("""
    <style>
    /* Import a modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide standard Streamlit header/footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Center the main container and give it some breathing room */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 600px;
    }

    /* Style the Title */
    .claire-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .claire-subtitle {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 3rem;
    }

    /* Chat Bubble Styling */
    .chat-bubble {
        background-color: #1E1E1E;
        border: 1px solid #333;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        color: #E0E0E0;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Highlight the 'Claire' label */
    .ai-label {
        color: #00d2ff;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        display: block;
    }

    /* Custom Spinner color */
    .stSpinner > div {
        border-top-color: #00d2ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. UI LAYOUT
st.markdown("<div class='claire-title'>CLAIRE</div>", unsafe_allow_html=True)
st.markdown("<div class='claire-subtitle'>Always Listening. Always Remembering.</div>", unsafe_allow_html=True)

# 4. AUDIO INPUT
# We use the standard widget, but the CSS above makes it fit in better
audio_file = st.audio_input("Tap to speak")

# 5. LOGIC (Strictly keeping your working code structure)
if audio_file:
    # "Personality" spinner message
    with st.spinner("Processing neural context..."):
        # Send to Backend
        files = {"file": audio_file}
        try:
            response = requests.post("http://localhost:8000/chat", files=files)
            
            if response.status_code == 200:
                data = response.json()
                text_response = data['text']
                
                # VISUAL: Display text in a custom styled card instead of raw text
                st.markdown(f"""
                    <div class="chat-bubble">
                        <span class="ai-label">Claire</span>
                        {text_response}
                    </div>
                """, unsafe_allow_html=True)
                
                # AUDIO: Decode and Play
                if data.get("audio_content"):
                    audio_bytes = base64.b64decode(data["audio_content"])
                    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                else:
                    st.warning("Audio generation failed (Check ElevenLabs API Key)")
            else:
                st.error(f"Backend Error: {response.status_code}")
                
        except Exception as e:
            st.error(f"Connection Error: {e}")

# 6. EMPTY STATE (Visual polish when idle)
else:
    st.markdown("""
        <div style="text-align: center; margin-top: 50px; opacity: 0.5;">
            Wait mode active. <br> ready for input.
        </div>
    """, unsafe_allow_html=True)