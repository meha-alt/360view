import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from docx import Document
import io

# Load environment variables
load_dotenv()

def apply_custom_css():
    st.markdown("""
    <style>
    /* Main app background with subtle gradient */
    .stApp {
        background: linear-gradient(135deg, 
        #8d6e63 0%,      /* Medium Brown */
        #a1887f 15%,     /* Light Brown */
        #bcaaa4 30%,     /* Warm Beige */
        #d7ccc8 45%,     /* Light Beige */
        #efebe9 60%,     /* Cream */
        #f3e5ab 75%,     /* Warm Cream */
        #ddbf94 90%,     /* Golden Brown */
        #8d6e63 100%     /* Back to Brown */
        );
    }
    .main-header {
        background: linear-gradient(135deg, #8b6f47 0%, #a0845c 50%, #b8956b 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(139, 111, 71, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6d4c36 0%, #8b6f47 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(109, 76, 54, 0.3) !important;
    }
    
    </style>
    
    """, unsafe_allow_html=True)

def create_docx(itinerary_text):
    doc = Document()
    for line in itinerary_text.split("\n"):
        doc.add_paragraph(line)
    
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def create_itinerary_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """You are SIKKIM_TRAVEL_PRO, an AI assistant that creates personalized travel itineraries for Sikkim based on user preferences and requirements.

Your task is to:
1. Analyze the provided travel preferences and details
2. Generate a well-structured, comprehensive itinerary in markdown format
3. Follow these guidelines:
   - Create a **detailed day-by-day itinerary** tailored to {travel_duration}
   - Include popular attractions, hidden gems, and local experiences
   - Consider {budget_range} when suggesting accommodations and activities
   - Factor in {travel_style} and {special_interests}
   - Include practical information (transportation, timings, costs)
   - Suggest local cuisine and dining options
   - Add cultural insights and travel tips
   - Consider weather and seasonal factors for {travel_season}
   
   - Be specific about locations, distances, and travel times
   - Provide alternative options for different weather conditions

Itinerary Structure:
[Header]
Sikkim Travel Itinerary | Duration | Season

[Trip Overview]
Brief overview of the planned journey

[Day-by-Day Itinerary]
Day 1: Location
- Morning: Activity/Sightseeing
- Afternoon: Activity/Sightseeing  
- Evening: Activity/Dining
- Accommodation: Hotel/Stay recommendation

[Transportation Guide]
Getting around Sikkim

[Accommodation Recommendations]
Budget-appropriate stay options

[Local Cuisine & Dining]
Must-try dishes and restaurants

[Packing List]
Season-appropriate items to pack

[Travel Tips & Cultural Insights]
Local customs and practical advice

[Budget Breakdown]
Estimated costs for activities and stays

[Emergency Information]
Important contacts and information"""),
        
        ("human", """Create a personalized Sikkim travel itinerary with these details:
        
Traveler Information:
- Name: {traveler_name}

- Number of Travelers: {group_size}
- Travel Duration: {travel_duration}

Travel Preferences:
- Budget Range: {budget_range}
- Travel Style: {travel_style}
- Accommodation Preference: {accommodation_type}
- Transportation: {transport_mode}

Interests & Activities:
{special_interests}

Travel Season & Dates:
{travel_season}

Special Requirements:
{special_requirements}

Specific Locations/Attractions:
{preferred_locations}

Additional Preferences:
{additional_preferences}""")
    ])

def generate_itinerary(user_inputs):
    llm = ChatGroq(temperature=0.3, model_name="openai/gpt-oss-20b")
    prompt = create_itinerary_prompt()
    chain = prompt | llm
    response = chain.invoke(user_inputs)
    return response.content

def main():
    apply_custom_css()
    
    st.title("🏔️ Sikkim Tourism Itinerary Generator")
    st.subheader("Create your perfect Sikkim adventure")

    with st.expander("✈️ Plan Your Sikkim Journey", expanded=True):
        with st.form("itinerary_form"):
            col1, col2 = st.columns(2)
            with col1:
                traveler_name = st.text_input("Your Name*", placeholder="John Traveler")
                
            with col2:
                group_size = st.selectbox("Number of Travelers*", [1, 2, 3, 4, 5, 6, 7, 8, "More than 8"])
                travel_duration = st.selectbox("Trip Duration*", 
                    ["2-3 days", "4-5 days", "6-7 days", "1 week", "10-12 days", "2 weeks", "More than 2 weeks"])
            
            st.markdown("**Travel Preferences**")
            col3, col4 = st.columns(2)
            with col3:
                budget_range = st.selectbox("Budget Range (per person)*", 
                    ["Budget (₹5,000-15,000)", "Mid-range (₹15,000-30,000)", "Luxury (₹30,000-60,000)", "Ultra-luxury (₹60,000+)"])
                travel_style = st.selectbox("Travel Style*", 
                    ["Adventure & Trekking", "Cultural & Heritage", "Nature & Wildlife", "Relaxed Sightseeing", "Photography", "Spiritual Journey", "Mixed Experience"])
            with col4:
                accommodation_type = st.selectbox("Accommodation Preference", 
                    ["Hotels", "Homestays", "Resorts", "Guesthouses", "Camping", "Mixed", "No preference"])
                transport_mode = st.selectbox("Transportation", 
                    ["Private Car/Taxi", "Shared Jeep", "Public Transport", "Self-drive", "Motorcycle", "Mixed", "Need recommendation"])
            
            st.markdown("**Interests & Activities**")
            special_interests = st.text_area(
                "What interests you most in Sikkim?",
                placeholder="e.g., Kanchenjunga views, Buddhist monasteries, local cuisine, adventure sports, traditional villages, shopping, etc.",
                height=100
            )
            
            st.markdown("**Travel Season & Timing**")
            travel_season = st.text_area(
                "Preferred travel dates/season*",
                placeholder="e.g., March 2024, Summer 2024, Avoid monsoon, Rhododendron season (April-May), Clear mountain views preferred",
                height=80
            )
            
            st.markdown("**Specific Preferences**")
            preferred_locations = st.text_area(
                "Must-visit places in Sikkim",
                placeholder="e.g., Gangtok, Pelling, Lachen, Lachung, Yuksom, Ravangla, Zuluk, North Sikkim, West Sikkim",
                height=100
            )
            
            special_requirements = st.text_area(
                "Special requirements or restrictions",
                placeholder="e.g., Vegetarian food only, elderly travelers, medical conditions, accessibility needs, permits needed",
                height=80
            )
            
            additional_preferences = st.text_input(
                "Any other preferences?",
                placeholder="e.g., 'Avoid crowded places' or 'Include sunrise points' or 'Focus on local experiences'"
            )
            
            submitted = st.form_submit_button("🗺️ Generate My Sikkim Itinerary")
    
    if submitted:
        if not traveler_name or not travel_duration or not travel_season:
            st.error("Please fill in all required fields (*)")
        else:
            with st.spinner("🏔️ Crafting your perfect Sikkim adventure..."):
                user_inputs = {
                    "traveler_name": traveler_name,
                    
                    "group_size": group_size,
                    "travel_duration": travel_duration,
                    "budget_range": budget_range,
                    "travel_style": travel_style,
                    "accommodation_type": accommodation_type,
                    "transport_mode": transport_mode,
                    "special_interests": special_interests,
                    "travel_season": travel_season,
                    "preferred_locations": preferred_locations,
                    "special_requirements": special_requirements,
                    "additional_preferences": additional_preferences
                }
                
                try:
                    itinerary = generate_itinerary(user_inputs)
                    
                    st.success("✅ Your Sikkim itinerary is ready!")
                    st.markdown("---")
                    st.subheader("Your Personalized Sikkim Travel Itinerary")
                    st.markdown(itinerary, unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📥 Download Itinerary as Word Document",
                        data=create_docx(itinerary),
                        file_name=f"Sikkim_Itinerary_{traveler_name.replace(' ', '_')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                except Exception as e:
                    st.error(f"Error generating itinerary: {str(e)}")

if __name__ == "__main__":

    main()
