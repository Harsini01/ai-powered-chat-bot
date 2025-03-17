# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 22:20:34 2025

@author: harsi
"""

import google.generativeai as genai
import pandas as pd
import fitz  # PyMuPDF for PDFs

# Configure Google Gemini API
genai.configure(api_key="AIzaSyBiH-Rh7mpkldBpwKnsanR2hGrcAkTQZws")
model = genai.GenerativeModel("gemini-1.5-flash")

# Load Excel/CSV file
def read_excel(file_path):
    try:
        df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
        return df.to_string()
    except Exception as e:
        return str(e)

# Extract tables from PDF
def read_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = "\n".join([page.get_text("text") for page in doc])
        return text
    except Exception as e:
        return str(e)

# AI Chatbot Processing
def chatbot_response(user_input):
    # Load Excel/CSV file
    if user_input.lower().startswith("read excel:"):
        file_path = user_input[len("read excel:"):].strip()
        data = read_excel(file_path)
        prompt = f"Here is the Excel data:\n{data}\nSummarize key insights."
    # Load PDF file
    elif user_input.lower().startswith("read pdf:"):
        file_path = user_input[len("read pdf:"):].strip()
        data = read_pdf(file_path)
        prompt = f"Here is the extracted PDF text:\n{data}\nSummarize key insights."
    else:
        prompt = user_input  # Normal conversation

    response = model.generate_content(prompt)
    return response.text

# Run chatbot
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye!")
        break
    response = chatbot_response(user_input)
    print("Chatbot:", response)
