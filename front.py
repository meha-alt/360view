import streamlit as st
import base64

# Page config
st.set_page_config(page_title="MONASTERY360", page_icon="🛕", layout="wide")

# Encode the image
with open("sikkim2.jpg", "rb") as img_file:
    encoded_string = base64.b64encode(img_file.read()).decode()

# Background image with f-string
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
    }}
    
    .main-header{{
        background: linear-gradient(135deg,  #B8860B 0%,    /* Dark Goldenrod */
    #C18F00 15%,   /* Deep Gold */
    #D4A017 30%,   /* Amber Gold */
    #E0B14B 45%,   /* Warm Golden */
    #DFAF4C 55%,   /* Rich Gold */
    #C9971B 65%,   /* Burnished Gold */
    #A87300 75%,   /* Bronze Gold */
    #8B5E00 90%,   /* Dark Metallic Gold */
    #6F4E00 100%   /* Deep Brownish Gold */
);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 5rem;
        box-shadow: 0 8px 32px rgba(139, 111, 71, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    .subtitle {{
        text-align: center;
        font-size: 20px !important;
        color: white !important;
        margin-top: 0px;
        margin-bottom: 50px;
    }}
    
    .card {{
        background-color: rgba(0,0,0,0.6);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: #f8e5a1;
        width: 300px;
        display: inline-block;
        margin: 10px;
    }}
    .btn-red {{
        background-color: #d95d39;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
    }}
    .btn-yellow {{
        background-color: #f1c40f;
        color: black;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle
st.markdown('<div class="main-header"><h1>MONASTERY360</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle"><h1>Disclaimer: More features are to be added</h1></div>', unsafe_allow_html=True)


# Cards layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card">
            <h3>Dharma Guide</h3>
            <p>Your AI Powered Tourist Guide Get Your Personalized Itinerary</p>
            <a href="https://dharma-guide.onrender.com" target="_blank" class="btn-red">Enter Sacred Path</a>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <h3>360° View</h3>
            <p>Immerse yourself in panoramic views of majestic monasteries and peaks</p>
            <a href="https://three60view.onrender.com" target="_blank" class="btn-yellow">Behold the Vision</a>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="card">
            <h3>Interactive Map</h3>
            <p>Navigate through sacred sites, ancient trails, and hidden treasures</p>
            <a href="https://tani-debug.github.io/sikkim-monastery-explorer/" target="_blank" class="btn-yellow">Explore the Realm</a>
        </div>
        """,
        unsafe_allow_html=True
    )

