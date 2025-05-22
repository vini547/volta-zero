import pandas as pd
from transformers import pipeline
import streamlit as st
import time


# Load the model pipeline
llm = pipeline("text-generation", model="distilgpt2")

# Sample function to analyze and handle NaN values
def suggest_nan_treatment(feature_name: str):
    # Define a prompt for the LLM to decide on NaN handling
    prompt = f"Respond with just one of the strings in this list: ['Continuous', 'Discrete', 'Ordinal', 'Non-ordinal ', 'Binary', 'Time-Series','Text']: What type the feature'{feature_name}'?"

    # Get the LLM's response
    response = llm(prompt, max_length=250, num_return_sequences=1)[0]["generated_text"]

    return response

    
df = pd.read_csv('./input/SINASC_RO_2019.csv')

# Apply the treatment suggestions for each feature
for feature in df.columns:
    res = suggest_nan_treatment(feature)
    time.sleep(10)

    st.write(res)

