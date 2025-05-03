import ollama
import streamlit as st
import torch

st.title("Ollama Python Chatbot")

# # # Initialize session state for chat history
if "messages" not in st.session_state:
     st.session_state["messages"] = []

# # # Initialize session state for the selected model
if "model" not in st.session_state:
     st.session_state["model"] = ""

# # # Get the list of available models safely
models = []
try:
     model_response = ollama.list()
# #     # Print the structure of the model response to debug
     st.write(model_response)  # This will show the structure in the Streamlit app
# #
# #     # Check for the models key and fetch model names correctly using 'model' key
     if "models" in model_response:
         models = [model["model"] for model in model_response["models"]]
     else:
         st.error("No 'models' key found in the response.")
# #
     if not models:
         st.error("No models available.")
except Exception as e:
     st.error(f"Error fetching models: {str(e)}")
# #
# # # If models are available, show the model selection dropdown
if models:
     st.session_state["model"] = st.selectbox("Choose your model", models)
else:
     st.session_state["model"] = "mistral:latest"  # Default to 'mistral:latest' if no models are available
# #
# #
def model_res_generator():
# #     # Check if CUDA (GPU) is available, otherwise fall back to CPU
     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# #
# #     # Stream the chatbot response using the selected model
     stream = ollama.chat(
         model=st.session_state["model"],
         messages=st.session_state["messages"],
         stream=True,
     )
# #
     for chunk in stream:
         yield chunk["message"]["content"]
# #
# #
# # # Display chat messages from history on app rerun
for message in st.session_state["messages"]:
     with st.chat_message(message["role"]):
         st.markdown(message["content"])

# # Handle user input and chat interactions
if prompt := st.chat_input("Enter prompt here.."):
# #     # Add the user's message to history
     st.session_state["messages"].append({"role": "user", "content": prompt})
# #
     with st.chat_message("user"):
         st.markdown(prompt)
# #
     with st.chat_message("assistant"):
         message = st.write_stream(model_res_generator())
         st.session_state["messages"].append({"role": "assistant", "content": message})