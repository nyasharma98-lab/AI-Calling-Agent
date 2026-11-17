import streamlit as st
import requests
import pandas as pd
from voice.gemini_brain import get_gemini_response
import tempfile
from streamlit_mic_recorder import mic_recorder
from voice.speech_to_text import convert_speech_to_text
from voice.text_to_speech import generate_speech_audio

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="AI Calling Agent",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------------
# BACKEND CONNECTION
# -----------------------------------

DEFAULT_API_URL = "https://ai-calling-agent-nriy.onrender.com"

st.sidebar.title("🤖 AI Calling Agent")
st.sidebar.caption("AI-powered communication platform")

api_url = st.sidebar.text_input(
    "Backend API URL",
    value=DEFAULT_API_URL
).strip().rstrip("/")


def api_get(endpoint):
    try:
        response = requests.get(
            f"{api_url}{endpoint}",
            timeout=60
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        st.error(f"Backend connection error: {error}")
        return None


def api_post(endpoint, data):
    try:
        response = requests.post(
            f"{api_url}{endpoint}",
            json=data,
            timeout=60
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        st.error(f"Request failed: {error}")
        return None


# -----------------------------------
# BACKEND STATUS
# -----------------------------------

health = api_get("/health")

if health:
    st.sidebar.success("Backend Connected")
else:
    st.sidebar.error("Backend Disconnected")


# -----------------------------------
# NAVIGATION
# -----------------------------------

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Talk to AI",
        "Outbound Calls",
        "Incoming Calls",
        "Customers",
        "Call History",
        "Analytics",
        "Agent Settings"
    ]
)


# -----------------------------------
# DASHBOARD
# -----------------------------------

if page == "Dashboard":

    st.title("🤖 AI Calling Agent")
    st.caption("Your intelligent communication dashboard")

    st.divider()

    analytics = api_get("/call-performance")

    if analytics:

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Calls",
            analytics.get("total_calls", 0)
        )

        col2.metric(
            "Completed Calls",
            analytics.get("completed_calls", 0)
        )

        col3.metric(
            "Failed Calls",
            analytics.get("failed_calls", 0)
        )

        col4.metric(
            "Pending Calls",
            analytics.get("pending_calls", 0)
        )

        st.subheader("Call Completion Rate")

        st.metric(
            "Completion Rate",
            f'{analytics.get("completion_rate", 0)}%'
        )

    st.divider()

    st.subheader("Platform Features")

    col1, col2 = st.columns(2)

    with col1:
        st.info("🎙️ Talk to your AI agent")
        st.info("📞 Make outbound calls")
        st.info("📥 Manage incoming calls")

    with col2:
        st.info("👥 Customer management")
        st.info("📊 Call analytics")
        st.info("📋 Call history")


# -----------------------------------
elif page == "Talk to AI":

    st.title("🎙️ Talk to AI Agent")

    st.write("Chat with your intelligent AI voice agent.")

    st.divider()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display conversation
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Typed message
    user_message = st.chat_input(
        "Type a message to your AI agent..."
    )

    if user_message:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message
        })

        with st.spinner("AI Agent is thinking..."):

            ai_response = get_gemini_response(user_message)
            audio_bytes = generate_speech_audio(ai_response)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": ai_response
        })

        st.audio(audio_bytes, format="audio/mp3")

    st.divider()

    st.subheader("🎤 Voice Conversation")

    audio = mic_recorder(
        start_prompt="🎙️ Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        key="voice_recorder"
    )

    if audio and audio.get("bytes"):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as audio_file:

            audio_file.write(audio["bytes"])
            audio_path = audio_file.name

        with st.spinner("Understanding your voice..."):

            spoken_text = convert_speech_to_text(audio_path)

        if spoken_text:

            st.session_state.chat_history.append({
                "role": "user",
                "content": spoken_text
            })

            with st.spinner("AI Agent is thinking..."):

                ai_response = get_gemini_response(spoken_text)
                audio_bytes = generate_speech_audio(ai_response)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": ai_response
            })

            st.audio(audio_bytes, format="audio/wav")

            st.rerun()

        else:
            st.warning("Sorry, I couldn't understand your voice.")

    # Clear conversation
    if st.button("Clear Conversation"):
        st.session_state.chat_history = []
        st.rerun()



# -----------------------------------
# OUTBOUND CALLS
# -----------------------------------

elif page == "Outbound Calls":

    st.title("📞 Outbound Calling")

    st.write(
        "Make AI-powered calls to customers."
    )

    st.divider()

    with st.form("outbound_call_form"):

        customer_name = st.text_input(
            "Customer Name"
        )

        phone_number = st.text_input(
            "Customer Phone Number"
        )

        call_purpose = st.text_area(
            "Purpose of Call",
            placeholder="Explain why the AI agent should call."
        )

        consent = st.checkbox(
            "I have permission to contact this person."
        )

        submitted = st.form_submit_button(
            "Initiate AI Call"
        )

        if submitted:

            if not customer_name or not phone_number:
                st.warning("Enter customer name and phone number.")

            elif not consent:
                st.warning(
                    "Please confirm that you have permission to call."
                )

            else:
                st.warning(
                    "The outbound telephony connection is not configured yet. "
                    "No phone call has been placed."
                )

    st.divider()

    st.subheader("Outbound Call Features")

    st.write("- Customer phone number")
    st.write("- AI conversation")
    st.write("- Call status")
    st.write("- Call duration")
    st.write("- Call summary")


# -----------------------------------
# INCOMING CALLS
# -----------------------------------

elif page == "Incoming Calls":

    st.title("📥 Incoming Calls")

    st.write(
        "Manage incoming calls handled by your AI agent."
    )

    st.divider()

    st.info(
        "Incoming calls will become active after connecting "
        "your Exotel phone number and configuring its webhook."
    )

    st.subheader("Incoming Call Features")

    st.write("- AI automatically answers calls")
    st.write("- Understands customer questions")
    st.write("- Responds using AI voice")
    st.write("- Saves call details")
    st.write("- Generates call summaries")

    st.subheader("Phone Number Status")

    st.warning("No telephony number connected yet.")


# -----------------------------------
# CUSTOMER MANAGEMENT
# -----------------------------------

elif page == "Customers":

    st.title("👥 Customer Management")

    st.write("Add and manage your customers.")

    st.divider()

    with st.form("customer_form"):

        name = st.text_input("Customer Name")

        phone = st.text_input("Phone Number")

        submitted = st.form_submit_button(
            "Add Customer"
        )

        if submitted:

            if not name or not phone:
                st.warning("Please enter both name and phone number.")

            else:

                result = api_post(
                    "/customers",
                    {
                        "name": name,
                        "phone": phone
                    }
                )

                if result is not None:
                    st.success("Customer added successfully!")
                    st.rerun()

    st.divider()

    st.subheader("Customer List")

    customers = api_get("/customers")

    if customers is not None:

        if customers:
            st.dataframe(
                pd.DataFrame(customers),
                use_container_width=True
            )

        else:
            st.info("No customers found.")


# -----------------------------------
# CALL HISTORY
# -----------------------------------

elif page == "Call History":

    st.title("📋 Call History")

    st.write("View previously recorded calls.")

    st.divider()

    calls = api_get("/calls")

    if calls is not None:

        if calls:

            st.dataframe(
                pd.DataFrame(calls),
                use_container_width=True
            )

        else:
            st.info("No call records available yet.")


# -----------------------------------
# ANALYTICS
# -----------------------------------

elif page == "Analytics":

    st.title("📊 Call Analytics")

    st.write(
        "Understand your AI Calling Agent's performance."
    )

    st.divider()

    analytics = api_get("/call-performance")

    if analytics:

        st.json(analytics)

        st.subheader("Call Performance")

        total = analytics.get("total_calls", 0)
        completed = analytics.get("completed_calls", 0)
        failed = analytics.get("failed_calls", 0)

        chart_data = pd.DataFrame({
            "Call Status": [
                "Completed",
                "Failed"
            ],
            "Number of Calls": [
                completed,
                failed
            ]
        })

        if total > 0:
            st.bar_chart(
                chart_data.set_index("Call Status")
            )
        else:
            st.info("No call analytics available yet.")


# -----------------------------------
# AGENT SETTINGS
# -----------------------------------

elif page == "Agent Settings":

    st.title("⚙️ Agent Settings")

    st.write("Configure your AI agent.")

    st.divider()

    agent_name = st.text_input(
        "Agent Name",
        value="AI Assistant"
    )

    language = st.selectbox(
        "Preferred Language",
        [
            "English",
            "Hindi",
            "English and Hindi"
        ]
    )

    personality = st.selectbox(
        "Agent Personality",
        [
            "Professional",
            "Friendly",
            "Customer Support"
        ]
    )

    if st.button("Save Settings"):

        st.session_state.agent_name = agent_name
        st.session_state.agent_language = language
        st.session_state.agent_personality = personality

        st.success("Settings saved for this session.")


# -----------------------------------
# FOOTER
# -----------------------------------

st.sidebar.divider()

st.sidebar.caption(
    "AI Calling Agent | Python + Streamlit + FastAPI + Gemini"
)