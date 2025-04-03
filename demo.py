import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Streamlit page
st.set_page_config(
    page_title="Habit Builder Assistant",
    page_icon="🌱",
    layout="centered"
)

# Get API key and initialize Groq client with error handling
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("⚠️ GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
    st.stop()

try:
    client = Groq(api_key=api_key)  # Correct initialization
except Exception as e:
    st.error(f"⚠️ Error initializing Groq client: {str(e)}")
    st.stop()


# Add enhanced custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f9fafb;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 0.75rem;
    }
    .chat-message {
        padding: 1.25rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .chat-message.user {
        background-color: #ebf5ff;
        border-left: 4px solid #3b82f6;
    }
    .chat-message.assistant {
        background-color: #ffffff;
        border-left: 4px solid #10b981;
    }
    .stSpinner>div>div {
        border-color: #10b981 transparent transparent transparent;
    }
    footer {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# App title and description with better formatting
st.title("🌱 Habit Builder Assistant")
st.markdown("""
    Welcome to your personal habit-building assistant! I can help you:
    
    ✅ **Build new positive habits**  
    🚫 **Break bad habits**  
    📅 **Create a 30-day plan**  
    ⏱️ **Provide 2-minute daily tasks**  
    📈 **Gradually increase task duration**  
    
    *Based on proven habit formation science*
""")

# Initialize chat history with system message if empty
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Hi! I'm your Habit Builder Assistant. What habit would you like to work on today?"
    }]

# Display chat messages with improved formatting
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input with clear placeholder
prompt = st.chat_input(
    "E.g., 'I want to start meditating daily' or 'How can I stop procrastinating?'",
    key="habit_input"
)

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Prepare the prompt with more detailed instructions
    system_prompt = """You are an expert habit coach specializing in the science of habit formation. 
    Your task is to help users build good habits and break bad ones using evidence-based techniques:
    
    1. Always suggest starting with a 2-minute version of the habit (2-Minute Rule)
    2. Provide a 30-day gradual progression plan
    3. Recommend increasing duration/intensity by 1% each week (Compound Growth)
    4. Suggest habit stacking where appropriate
    5. Include accountability mechanisms
    6. Address potential obstacles
    
    If the query isn't about habits, politely explain you specialize only in habit formation.
    
    User query: """ + prompt
    
    try:
        # Show loading spinner with custom message
        with st.spinner("🧠 Crafting your personalized habit strategy..."):
            # Get response from Groq with temperature control for more consistent results
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    *[
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in st.session_state.messages[-4:]  # Keep context window manageable
                    ]
                ],
                model="llama-3-70b-8192",
                temperature=0.7,
                max_tokens=1024
            )
            
            # Get and clean the response
            response = chat_completion.choices[0].message.content.strip()
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display assistant response with better formatting
            with st.chat_message("assistant"):
                st.markdown(response)
                
    except Exception as e:
        st.error(f"⚠️ Sorry, I encountered an error: {str(e)}")
        st.info("Please try again or rephrase your question.")

# Add footer with more information
st.markdown("""
    ---
    <div style='text-align: center; color: #64748b; font-size: 0.9em'>
        <p>🌿 Based on principles from Atomic Habits by James Clear</p>
        <p>⚡ Powered by Groq's ultra-fast AI and Streamlit</p>
    </div>
""", unsafe_allow_html=True)