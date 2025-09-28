import streamlit as st

st.set_page_config(
    page_title="View360",  
    page_icon="🛕",             
    layout="wide"               
)

# ---- Page styling ----
st.markdown(
    """
    <style>
    .stApp {
         background: 
         radial-gradient(circle at top left, rgba(255, 223, 100, 0.4) 0%, transparent 50%),
        linear-gradient(
         135deg,
              #6b3f3f 0%,
                #7a4b4b 15%,
                #8f5959 30%,
                #a2736f 45%,
                #b37f7f 55%,
                #e0b84d 65%,
                #c4a392 75%,
                #a2736f 90%,
                #6b3f3f 100%
        );
        font-family: "Georgia", serif;
    }
    h1 {
        text-align: center;
        color: #003366;
    }
    
    audio {
        background: #003366;
        border-radius: 25px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Rumtek Monastery 360° Tour")

col1, col2 = st.columns(2)

# Left column - Audio section
with col2:
    # Fix: Use binary reading for Streamlit Cloud
    try:
        with open("Rumtek_Monastery.mp3", "rb") as audio_file:
            audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mpeg")
    except FileNotFoundError:
        st.error("Audio file not found")
    except Exception as e:
        st.error(f"Error loading audio: {e}")

# Right column - Panorama section
with col1:
    try:
        with open("panorama_aframe.html", "r", encoding="utf-8", errors="ignore") as f:
            html_code = f.read()
        
        st.components.v1.html(
            html_code,
            height=500, 
            width=800,  # made smaller (was 800)
            scrolling=False
        )
    except FileNotFoundError:
        st.error("panorama_aframe.html file not found")
    except Exception as e:
        st.error(f"Error loading HTML file: {e}")
