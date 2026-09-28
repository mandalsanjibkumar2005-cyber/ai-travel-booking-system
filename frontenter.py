import os
import uuid
import streamlit as st

# Load local .env file
from dotenv import load_dotenv
load_dotenv()

# Load Streamlit Cloud secrets if available
try:
    for key in [
        "GROQ_API_KEY",
        "AVIATIONSTACK_API_KEY",
        "TAVILY_API_KEY",
        "DATABASE_URL",
    ]:
        if key in st.secrets:
            os.environ[key] = st.secrets[key]
except Exception:
    pass

from langchain_core.messages import HumanMessage
from main import app

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Travel Booking System",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# IMAGES
# ============================================================

HERO_IMAGE = (
    "https://images.unsplash.com/photo-1469474968028-56623f02e42e"
    "?auto=format&fit=crop&w=1600&q=85"
)

DESTINATIONS = [
    ("Tokyo", "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=700&q=85"),
    ("Paris", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=700&q=85"),
    ("Bangkok", "https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=700&q=85"),
    ("Rome", "https://images.unsplash.com/photo-1529260830199-42c24126f198?auto=format&fit=crop&w=700&q=85"),
    ("Dubai", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=700&q=85"),
]

FEATURE_IMAGES = [
    ("✈️ Flights", "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=900&q=85"),
    ("🏨 Hotels", "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=900&q=85"),
    ("🗺️ Itinerary", "https://images.unsplash.com/photo-1527631746610-bca00a040d60?auto=format&fit=crop&w=900&q=85"),
]

# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(0,119,255,.16), transparent 30%),
            radial-gradient(circle at 90% 10%, rgba(70,90,255,.10), transparent 30%),
            #050914;
        color: white;
    }

    .hero-image {
        width: 100%;
        height: 280px;
        border-radius: 16px;
        overflow: hidden;
        margin: 0 0 24px 0;
    }

    .hero-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
        display: block;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070d1d, #091326);
        border-right: 1px solid rgba(255,255,255,.08);
    }

    .sidebar-title {
        font-size: 22px;
        font-weight: 800;
        padding: 12px 0 30px;
    }

    .sidebar-section {
        margin-top: 22px;
        margin-bottom: 10px;
        color: #6daeff;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .tech-item, .agent-item {
        padding: 12px 14px;
        margin: 7px 0;
        border-radius: 10px;
        font-size: 13px;
    }

    .tech-item {
        background: rgba(255,255,255,.035);
        border: 1px solid rgba(255,255,255,.07);
    }

    .agent-item {
        background: rgba(30,55,100,.45);
        border-left: 3px solid #1683ff;
    }

    .section-label {
        margin: 24px 0 12px;
        color: #55a8ff;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .stButton > button {
        width: 100%;
        min-height: 45px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,.10);
        background: linear-gradient(135deg, #087eff, #0055d9);
        color: white;
        font-weight: 700;
    }

    .stButton > button:hover {
        border-color: #63b0ff;
        box-shadow: 0 8px 25px rgba(0,119,255,.28);
    }

    textarea {
        background-color: #080f1e !important;
        color: #eaf2ff !important;
        border: 1px solid rgba(255,255,255,.16) !important;
        border-radius: 14px !important;
    }

    .result-card {
        background: rgba(10,18,36,.88);
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 16px;
        padding: 22px;
        margin: 12px 0;
    }

    .service-title {
        text-align: center;
        font-size: 16px;
        font-weight: 700;
        margin-top: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================

if "user_id" not in st.session_state:
    st.session_state.user_id = "aarohi_user"

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "result" not in st.session_state:
    st.session_state.result = None

if "request" not in st.session_state:
    st.session_state.request = ""

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown('<div class="sidebar-title">✈️ AI Travel Planner</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">User ID</div>', unsafe_allow_html=True)
    st.session_state.user_id = st.text_input(
        "User ID",
        value=st.session_state.user_id,
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-section">Powered By</div>', unsafe_allow_html=True)
    for item in [
        "◇ LangGraph",
        "● Groq · LLM",
        "▣ PostgreSQL",
        "⌕ Tavily Search",
        "✈ AviationStack",
    ]:
        st.markdown(f'<div class="tech-item">{item}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Agent Pipeline</div>', unsafe_allow_html=True)
    for item in [
        "① Flight Agent",
        "② Hotel Agent",
        "③ Itinerary Agent",
        "④ Final Agent",
    ]:
        st.markdown(f'<div class="agent-item">{item}</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 New Travel Session"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.result = None
        st.session_state.request = ""
        st.rerun()

# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
    <div class="hero-image">
        <img src="{HERO_IMAGE}" alt="Travel destination">
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DESTINATIONS
# ============================================================

st.markdown('<div class="section-label">Explore Destinations</div>', unsafe_allow_html=True)

cols = st.columns(5)
for col, (name, image_url) in zip(cols, DESTINATIONS):
    with col:
        st.image(image_url, width="stretch")
        st.caption(name)

# ============================================================
# QUICK TRIPS
# ============================================================

st.markdown('<div class="section-label">Describe Your Trip</div>', unsafe_allow_html=True)

quick_trips = [
    ("🇯🇵 7-Day Japan Trip", "Plan a complete 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs."),
    ("🇫🇷 Paris Trip", "Plan a Paris trip for 5 days including flights, hotels and major attractions."),
    ("🇦🇪 Dubai Weekend", "Plan a Dubai weekend trip including flights, hotels and sightseeing."),
    ("🇮🇩 Bali Backpacking", "Plan a 10-day Bali backpacking trip with budget hotels and activities."),
]

cols = st.columns(4)
for i, col in enumerate(cols):
    with col:
        if st.button(quick_trips[i][0], key=f"quick_{i}"):
            st.session_state.request = quick_trips[i][1]
            st.rerun()

# ============================================================
# TRAVEL REQUEST
# ============================================================

travel_request = st.text_area(
    "Travel Request",
    value=st.session_state.request,
    height=120,
    placeholder="Example: Plan a 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs.",
    label_visibility="collapsed",
)

st.session_state.request = travel_request

# ============================================================
# GENERATE
# ============================================================

generate = st.button("🚀 Generate My Travel Plan", width="stretch")
if generate:
    if not travel_request.strip():
        st.warning("Please describe your travel requirements first.")
    else:
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        with st.spinner("🤖 Four AI agents are working on your travel plan..."):
            try:
                result = app.invoke(
                    {
                        "messages": [HumanMessage(content=travel_request)],
                        "user_query": travel_request,
                        "flight_results": "",
                        "hotel_results": "",
                        "itinerary": "",
                        "llm_calls": 0,
                    },
                    config=config,
                )
                st.session_state.result = result
                st.success("✅ Your travel plan is ready!")
            except Exception as error:
                st.error("Something went wrong while generating your travel plan.")
                with st.expander("Show technical error"):
                    st.code(str(error))

# ============================================================
# RESULTS
# ============================================================

if st.session_state.result:
    result = st.session_state.result

    st.markdown("---")
    st.markdown('<div class="section-label">Your Travel Plan</div>', unsafe_allow_html=True)
    st.markdown("## ✨ AI Generated Travel Response")

    tab1, tab2, tab3, tab4 = st.tabs([
        "✨ Final Response",
        "✈️ Flights",
        "🏨 Hotels",
        "🗺️ Itinerary",
    ])

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------
    with tab1:
        messages = result.get("messages", [])
        if messages:
            final_message = messages[-1]
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(final_message.content)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No final response available.")

    # --------------------------------------------------------
    # FLIGHTS
    # --------------------------------------------------------
    with tab2:
        flight_results = result.get("flight_results", "")
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("### ✈️ Flight Information")
        st.write(flight_results or "No flight information available.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # HOTELS
    # --------------------------------------------------------
    with tab3:
        hotel_results = result.get("hotel_results", "")
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("### 🏨 Hotel Information")
        st.write(hotel_results or "No hotel information available.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # ITINERARY
    # --------------------------------------------------------
    with tab4:
        itinerary = result.get("itinerary", "")
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("### 🗺️ Your Itinerary")
        st.write(itinerary or "No itinerary available.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================
    # DOWNLOAD BUTTON
    # ========================================================

    messages = result.get("messages", [])
    final_response = messages[-1].content if messages else "No final response available."

    download_content = f"""AI TRAVEL BOOKING SYSTEM
========================

TRAVEL REQUEST
--------------
{travel_request}

FLIGHT RESULTS
--------------
{result.get('flight_results', 'No flight information available.')}

HOTEL RESULTS
-------------
{result.get('hotel_results', 'No hotel information available.')}

ITINERARY
---------
{result.get('itinerary', 'No itinerary available.')}

FINAL TRAVEL RESPONSE
---------------------
{final_response}

========================
Generated by AI Travel Booking System
LangGraph • Groq • PostgreSQL • Tavily • AviationStack
"""

    st.markdown("---")
    st.markdown("### 📥 Download Your Travel Plan")

    st.download_button(
        label="📥 Download Travel Plan",
        data=download_content,
        file_name="AI_Travel_Plan.txt",
        mime="text/plain",
        width="stretch",
    )

    # ========================================================
    # TRAVEL SERVICE IMAGE BOXES
    # ========================================================

    st.markdown("---")
    st.markdown("### 🌍 Travel Services")

    service_cols = st.columns(3)

    for col, (title, image_url) in zip(service_cols, FEATURE_IMAGES):
        with col:
            st.image(image_url, width="stretch")
            st.markdown(f'<div class="service-title">{title}</div>', unsafe_allow_html=True)

# ============================================================
# END
# ============================================================
