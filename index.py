import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os
import random
import pandas as pd
from datetime import datetime
from page_setup import setup_page

# Hide sidebar - must be the first command on the page
setup_page()

# Get query parameters
url_params = st.experimental_get_query_params()

# Get 'campId' and 'workerId' from the dictionary, defaulting to None if not present
camp_id = url_params.get('campId', [None])[0]
worker_id = url_params.get('workerId', [None])[0]
timestamp = datetime.now()
timestamp_file = timestamp.strftime("%Y%m%d_%H%M%S")

# Record registered worker
data = {
    'Timestamp_Registered': [timestamp],
    'Worker': [worker_id],
    'Campaign': [camp_id],
}
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv(f'results/registered/csv/{timestamp_file}_{worker_id}_registered.csv', index=False)
st.success('Registered User!')

# Centered title and stylish card with a lighter blue background
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='color: #333333;'>LinguaInspect</h1>
    </div>
    <div style='background-color: #f0f8ff; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); padding: 20px;'>
        <h2 style='color: #333333;'>Welcome to LinguaInspect: Community-Driven Educational Video QA</h2>
        <h3 style='color: #333333;'>Task Instructions:</h3>
        <p style='color: #333333;'>Your mission is to ensure the accuracy of transcriptions and translations. For transcriptions, make sure captions are on in the video and the translations are embedded. Compare them with the actual spoken content and provide assessments.</p>
        <ol style='color: #333333;'>
            <li>Make sure captions (cc) are on in the video before you start.</li>
            <li>Watch the video carefully.</li>
            <li>Review the transcriptions.</li>
            <li>Assess how accurately they match the spoken content in the video.</li>
            <li>Answer the questions below the video based on your observations.</li>
            <li>Submit and go to the translation page.</li>
            <li>Select the language you can best assess the translation from the given options.</li>
            <li>Answer the questions after reading the given translation.</li>
            <li>Click the checkbox below to confirm that you have read and understood the instructions.</li>
        </ol>
    </div>
    """,
    unsafe_allow_html=True
)

st.session_state['instances_completed']=0
st.session_state['timestamp_registered']=timestamp

agree = st.checkbox('I have read and understood the instructions')

if agree:
  if st.button('Start'):
    switch_page("Transcription Quality Assessment") #redirect to first task page

