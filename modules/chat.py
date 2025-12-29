import streamlit as st
import google.generativeai as genai
import os
import pandas as pd

class ChatManager:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("models/gemini-2.5-flash")
        else:
            self.model = None

    def _get_dataset_context(self):
        """Generates a summary of the currently active dataset."""
        if "active_dataset" in st.session_state and "cloud_datasets" in st.session_state:
            name = st.session_state["active_dataset"]
            df = st.session_state["cloud_datasets"].get(name)
            
            if df is not None:
                buffer = []
                buffer.append(f"Current Dataset: {name}")
                buffer.append(f"Shape: {df.shape}")
                buffer.append(f"Columns: {list(df.columns)}")
                buffer.append("Sample Data (first 3 rows):")
                buffer.append(df.head(3).to_markdown(index=False))
                
                # Basic stats for numeric columns
                numeric_df = df.select_dtypes(include=['number'])
                if not numeric_df.empty:
                     buffer.append("Numeric Stats:")
                     buffer.append(numeric_df.describe().to_markdown())
                
                return "\n".join(buffer)
        
        return "No dataset is currently loaded."

    def get_system_prompt(self):
        base_prompt = """
        You are AutoDS, an expert Data Science Assistant. 
        Your goal is to help users analyze their data, suggest cleaning steps, explain ML concepts, and guide them through this application.
        
        Context about the user's data is provided below. Use it to give specific, relevant answers.
        If the user asks to perform an action (like "drop column X"), explain how they can do it in the "Manual Mode" of the relevant module.
        """
        
        data_context = self._get_dataset_context()
        
        # Action History
        history_context = ""
        if "action_log" in st.session_state and st.session_state["action_log"]:
            history_context = "\n\n=== USER ACTIONS HISTORY ===\n" + "\n".join(st.session_state["action_log"])
        
        return f"{base_prompt}\n\n=== DATASET CONTEXT ===\n{data_context}{history_context}\n"

    def generate_response(self, user_input, history):
        if not self.model:
            return "⚠️ Gemini API Key is missing. Please check your .env file."
        
        try:
            # Construct chat history for the model
            chat = self.model.start_chat(history=history)
            
            # Add system context to the message (or pre-prompting)
            # Gemini Python SDK handles history, but for context we often prepend it to the latest message 
            # or rely on the chat session if we could set system instruction (Gemini 1.5/2.5 supports system instruction in model init, 
            # but simpler here to just prepend context/instruction if session is fresh, or rely on prompt engineering).
            
            # For 2.5 Flash, robust system instructions are supported. 
            # Only sending context in the immediate prompt for now to ensure freshness if data changes.
            
            full_prompt = f"{self.get_system_prompt()}\n\nUser Question: {user_input}"
            
            response = chat.send_message(full_prompt)
            return response.text
        except Exception as e:
            return f"Error interacting with AI: {str(e)}"
            
    def generate_insight(self, prompt, data_summary=None):
        """Generate a one-off insight for a specific module."""
        if not self.model:
             return "⚠️ Gemini API Key is missing."
        
        context = ""
        if data_summary:
            context = f"DATA CONTEXT:\n{data_summary}\n\n"
            
        full_prompt = f"{context}You are an expert Data Science Assistant. {prompt}"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error thinking: {str(e)}"
