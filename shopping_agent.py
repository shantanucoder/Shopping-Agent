import os
import tempfile
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from shopping_agent import agent

st.set_page_config(page_title="AI Shopping Assistant", page_icon="🛍️", layout="wide")

st.title("🛍️ AI Shopping Assistant")
st.write("Find organic products, search by photo, check ratings, and place orders!")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar - Image Search Upload Section
with st.sidebar:
    st.header("📸 Image Search")
    uploaded_file = st.file_uploader("Upload a product photo", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Save image to temporary directory for the agent tool to read
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        st.image(uploaded_file, caption="Uploaded Product Image", use_container_width=True)
        
        if st.button("Search with Image"):
            # Format image message for the agent
            image_prompt = f"I uploaded an image at this path: {tmp_path}. Please describe it and find matching products."
            
            # Display and store user prompt
            st.session_state.messages.append(HumanMessage(content=image_prompt))
            
            with st.spinner("Analyzing image..."):
                result = agent.invoke({"messages": st.session_state.messages})
                response_text = result["messages"][-1].content
                st.session_state.messages.append(AIMessage(content=response_text))
            
            st.rerun()

# Main Chat Interface
st.subheader("💬 Chat with Assistant")

# Display Conversation History
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

# User Chat Input Box
if user_input := st.chat_input("What are you looking for today? (e.g., 'I want organic honey under 15 dollar')"):
    # Add User Message
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.write(user_input)

    # Generate Response from Agent
    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            result = agent.invoke({"messages": st.session_state.messages})
            response_text = result["messages"][-1].content
            st.write(response_text)
            st.session_state.messages.append(AIMessage(content=response_text))
