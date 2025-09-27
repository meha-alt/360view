import streamlit as st

st.set_page_config(layout="wide")

# ---- Page styling ----
st.markdown(
    """
    <style>
    .stApp {
         background: radial-gradient(circle at top, #f9f3e7, #e5d1a8, #cbb68c);
        color: #3b2f1e;
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
