import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Streamlit page with custom theme
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Get API key and initialize Groq client with error handling
api_key = st.secrets["GROQ_API_KEY"]
if not api_key:
    st.error("⚠️ GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
    st.stop()

try:
    # Initialize Groq client with only the API key
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"⚠️ Error initializing Groq client: {str(e)}")
    st.stop()

# Add custom CSS with new color scheme
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    /* Header styling */
    .stTitle {
        color: #00ff9d !important;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Description text styling */
    .description {
        color: #b3b3b3;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .chat-message.user {
        background-color: #2d3748;
        border-left: 5px solid #00ff9d;
    }
    .chat-message.assistant {
        background-color: #1a365d;
        border-left: 5px solid #00b4d8;
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        background-color: #2d3748;
        color: #ffffff;
        border: 1px solid #4a5568;
        border-radius: 10px;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #00ff9d !important;
        color: #1a1a1a !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        padding: 0.5rem 2rem !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background-color: #00cc7d !important;
        transform: translateY(-2px);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #b3b3b3;
        padding: 1rem;
        border-top: 1px solid #2d3748;
        margin-top: 2rem;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: #00ff9d !important;
    }
    
    /* Error message styling */
    .stAlert {
        background-color: #7f1d1d;
        color: #ffffff;
        border: none;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# App title and description
st.title("🤖 AI Chat Assistant")
st.markdown('<p class="description">Your intelligent conversation partner powered by advanced AI. Ask me anything!</p>', unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
        st.write(message["content"])

# User input


if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(prompt)
    text = """Role : You are a expert in the field of habit formation.You have 30 year experience in the field of habit formation.
   Task: You have to make a 30 days plan in which each task to be done in 2 minutes and if make array of tasks for each day and also solve user query about habits
   constraints: You solve only habits related query.And give answer in the context of habits.If user query is not related to habits then politely explain you specialize only in habit formation.You simply say "I'm sorry, I can only help with habits related queries if you have query about habit than you can ask me ." and the stop the answer the user query is : """ + prompt

    
    try:
        # Show loading spinner
        with st.spinner("Thinking... 🤔"):
            # Get response from Groq
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": text,
                    }
                ],
                model="llama3-70b-8192",
                temperature=0.7,
                max_tokens=1024,
            )
            
            # Get the response
            response = chat_completion.choices[0].message.content
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display assistant response
            with st.chat_message("assistant", avatar="🤖"):
                st.write(response)
    except Exception as e:
        st.error(f"⚠️ Error generating response: {str(e)}")

# Add clear chat button with custom styling
if st.session_state.messages:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Clear Chat 🧹"):
            st.session_state.messages = []
            st.experimental_rerun()

# Add footer
st.markdown("""
    <div class="footer">
        <p>Powered by Groq AI 🚀</p>
        <p style="font-size: 0.8rem;">Built with Streamlit ❤️</p>
    </div>
""", unsafe_allow_html=True)
