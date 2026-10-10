import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    HumanMessage
)

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Mistral AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #111827 50%,
            #1e1b4b 100%
        );
        color: white;
    }

    /* Header */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
        background: linear-gradient(
            90deg,
            #a78bfa,
            #60a5fa,
            #22d3ee
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 17px;
        margin-bottom: 30px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* Mode cards */
    .mode-card {
        padding: 15px;
        border-radius: 15px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 15px;
    }

    /* Info box */
    .info-box {
        padding: 18px;
        border-radius: 15px;
        background: rgba(59, 130, 246, 0.12);
        border: 1px solid rgba(96, 165, 250, 0.25);
        color: #dbeafe;
        margin-bottom: 20px;
    }

    /* Chat container */
    .chat-container {
        max-width: 900px;
        margin: auto;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# AI Model
# --------------------------------------------------

model = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.9
)


# --------------------------------------------------
# Mode Configuration
# --------------------------------------------------

modes = {
    "😡 Angry Mode": {
        "prompt": (
            "You are an angry AI agent. "
            "You respond aggressively, impatiently, and bluntly. "
            "Do not use offensive or hateful language. "
            "Keep your responses entertaining."
        ),
        "description": "Aggressive, impatient and blunt responses."
    },

    "😂 Funny Mode": {
        "prompt": (
            "You are a funny AI agent. "
            "Respond with humor, jokes, playful sarcasm, "
            "and entertaining explanations. "
            "Keep the conversation friendly."
        ),
        "description": "Funny, playful and humorous responses."
    },

    "😢 Sad Mode": {
        "prompt": (
            "You are a sad AI agent. "
            "Respond in a melancholic, emotional and slightly dramatic tone. "
            "Do not encourage self-harm or harmful behavior. "
            "Still provide useful and accurate answers."
        ),
        "description": "Melancholic, emotional and dramatic responses."
    }
}


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "😂 Funny Mode"


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🤖 AI Personality")

    st.markdown(
        """
        <div class="info-box">
        Choose how you want your AI assistant to behave.
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_mode = st.radio(
        "Choose AI Mode",
        list(modes.keys()),
        index=list(modes.keys()).index(
            st.session_state.selected_mode
        )
    )

    st.session_state.selected_mode = selected_mode

    st.markdown("---")

    st.markdown("### 🎭 Current Personality")

    st.markdown(
        f"""
        <div class="mode-card">
            <h3>{selected_mode}</h3>
            <p>{modes[selected_mode]["description"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    if st.button(
        "🗑️ New Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.markdown(
        """
        ### ⚡ Powered By

        **Mistral AI**

        Model: `mistral-small-2506`

        Built with ❤️ using LangChain + Streamlit
        """
    )


# --------------------------------------------------
# Main Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🤖 Mistral AI Personality Chat</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Choose a personality and start chatting with your AI assistant</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# Welcome Message
# --------------------------------------------------

if not st.session_state.messages:

    st.markdown(
        """
        <div class="info-box">
            👋 <b>Welcome!</b><br><br>
            Choose an AI personality from the sidebar and start
            a conversation below.
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Display Previous Messages
# --------------------------------------------------

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user"):
            st.markdown(message["content"])

    else:

        with st.chat_message("assistant"):
            st.markdown(message["content"])


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

prompt = st.chat_input(
    "💬 Ask something..."
)


# --------------------------------------------------
# Process User Message
# --------------------------------------------------

if prompt:

    # Add user message to UI history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build LangChain message history
    messages = [
        SystemMessage(
            content=modes[
                st.session_state.selected_mode
            ]["prompt"]
        )
    ]

    for message in st.session_state.messages:

        if message["role"] == "user":

            messages.append(
                HumanMessage(
                    content=message["content"]
                )
            )

        elif message["role"] == "assistant":

            messages.append(
                AIMessage(
                    content=message["content"]
                )
            )

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):

            try:

                response = model.invoke(messages)

                answer = response.content

                st.markdown(answer)

                # Save AI response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"❌ Something went wrong:\n\n{str(e)}"
                )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Mistral AI • LangChain • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)