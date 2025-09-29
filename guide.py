import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import json
from dotenv import load_dotenv
from docx import Document
import io
from pathlib import Path

load_dotenv()

st.set_page_config(
    page_title="DharmaGuide",  
    page_icon="🛕")         
    
# --- Apply Custom CSS ---
def apply_custom_css():
    st.markdown("""
    <style>
    .stApp {
        background:
          radial-gradient(circle at top left, rgba(255, 223, 100, 0.4) 0%, transparent 50%),
          linear-gradient(135deg, #6b3f3f 0%, #7a4b4b 15%, #8f5959 30%, #a2736f 45%, #b37f7f 55%, #e0b84d 65%, #c4a392 75%, #a2736f 90%, #6b3f3f 100%);
    }
    .main-header {
        background: linear-gradient(135deg, #8b6f47 0%, #a0845c 50%, #b8956b 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(139, 111, 71, 0.3);
        border: 1px solid rgba(255,255,255,0.2);
        color: #fff;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6d4c36 0%, #8b6f47 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.45rem 1.2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(109, 76, 54, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()
st.markdown('<div class="main-header"><h1>DHARMA GUIDE</h1></div>', unsafe_allow_html=True)
st.markdown("### Note: More cities will be added as we expand our Database")

# --- Load DB safely ---
DB_PATH = Path("data.json")
if not DB_PATH.exists():
    st.error("data.json not found in the app folder. Please place your combined JSON file named 'data.json' in the same folder.")
    st.stop()

try:
    with DB_PATH.open("r", encoding="utf-8") as f:
        TOURIST_DB = json.load(f)
except Exception as e:
    st.error(f"Failed to load data.json: {e}")
    st.stop()

# --- derive city choices and tags from your structure ---
city_choices = sorted(list(TOURIST_DB.keys()))

# collect tags safely from each city's Places
all_tags_set = set()
for city_name, city_data in TOURIST_DB.items():
    # places may be under 'Places' or 'places'
    places = city_data.get("Places") or city_data.get("places") or []
    for p in places:
        # Tags might be 'Tags' or 'tags'
        tags = p.get("Tags") or p.get("tags") or []
        for t in tags:
            if isinstance(t, str):
                all_tags_set.add(t)
all_tags = sorted(all_tags_set)

# --- helper to create Word doc ---
def create_docx(itinerary_text):
    doc = Document()
    for line in itinerary_text.split("\n"):
        doc.add_paragraph(line)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- Trip Preferences Form ---
with st.form("trip_form"):
    st.subheader("Trip Preferences")
    traveler_name = st.text_input("Traveler Name", value="Traveler")
    days = st.slider("Number of days in the region", 1, 7, 2)
    city_focus = st.multiselect("Which city/area to focus on?", city_choices, default=city_choices[:2])
    start_time = st.time_input("Preferred sightseeing start time")
    end_time = st.time_input("Preferred sightseeing end time")

    tags_selected = st.multiselect("Select your interests", all_tags)
    pace = st.radio("Trip pace", ["Fast (many places/day)", "Relaxed (fewer places/day)"])

    free_only = st.checkbox("Only free attractions?", value=False)
    transport_mode = st.selectbox("Preferred travel mode", ["Private Car", "Shared Taxi", "Local Transport"])

    st.markdown("### Hotel Preferences")
    max_budget = st.number_input("Approximate maximum budget per night (INR)", min_value=500, max_value=50000, value=5000, step=500)
    hotel_class = st.selectbox("Hotel preference", ["Budget", "Mid-range", "Luxury"])
    min_rating = st.slider("Minimum hotel rating (out of 10)", min_value=1, max_value=10, value=7)
    submitted = st.form_submit_button("Generate Itinerary")

if submitted:
    # basic validation
    if not city_focus:
        st.error("Please choose at least one city.")
        st.stop()

    start_time_str = start_time.strftime("%H:%M")
    end_time_str = end_time.strftime("%H:%M")

    # Create a compact context to send — here we send full city data (you can pre-filter if you want)
    compact_context = {}
    for c in city_focus:
        compact_context[c] = TOURIST_DB.get(c, {})

    context_json = json.dumps(compact_context, indent=2, ensure_ascii=False)

    system_prompt = """
You are a travel assistant. ONLY use the provided CONTEXT JSON for factual answers.
Do NOT make up facts. Format a friendly, day-wise itinerary for the traveler.
"""
    human_prompt = f"""
Traveler name: {traveler_name}
Trip days: {days}
City focus: {city_focus}
Sightseeing: {start_time_str} to {end_time_str}
Interests: {tags_selected}
Pace: {pace}
Free attractions only: {free_only}
Transport mode: {transport_mode}

Hotel preferences:
- Max budget per night: {max_budget} INR
- Hotel class preference: {hotel_class}
- Minimum rating: {min_rating}/10

CONTEXT:
{context_json}

Please create a day-wise itinerary using only places in CONTEXT that match the selected interests and cities. 
If no places match, select from all available places.
Use plain text with line breaks, not HTML.
"""
    messages = [SystemMessage(content=system_prompt.strip()), HumanMessage(content=human_prompt)]

    try:
        llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.2)
        response = llm(messages)
        st.subheader("Generated Itinerary")
        if hasattr(response, "content"):
            itinerary = response.content.replace("<br>", "\n")
            st.markdown(itinerary)
            docx_buffer = create_docx(itinerary)
            st.download_button(
                label="Download Itinerary as Word Document",
                data=docx_buffer,
                file_name=f"{traveler_name}_itinerary.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            st.write(str(response))
    except Exception as e:
        st.error(f"Error calling LLM: {e}")

                
    
  


    
            


