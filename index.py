import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os
import random
import pandas as pd
from datetime import datetime
from page_setup import setup_page

#hide sidebar - must be first command on page
setup_page()

# Get query parameters
url_params = st.experimental_get_query_params()

# Get 'campId' and 'workerId' from the dictionary, defaulting to None if not present
camp_id = url_params.get('campId', [None])[0]
worker_id = url_params.get('workerId', [None])[0]
timestamp = datetime.now()
timestamp_file=timestamp.strftime("%Y%m%d_%H%M%S")

#record registered worker
data = {
    'Timestamp_Registered': [timestamp],
    'Worker': [worker_id],
    'Campaign' : [camp_id],
}
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv(f'results/registered/csv/{timestamp_file}_{worker_id}_registered.csv', index=False)
st.success('Registered User!')

st.title('LingualInspect')
st.write('Welcome to LinguaInspect: Community-Driven Educational Video QA')
st.write('TASK INSTRUCTIONS: \n Your mission is to ensure the accuracy of transcriptions and translations. The transcriptions and translations have already been provided and are embedded with the video. Your task is to compare them with the actual spoken content in the video and provide assessments')
st.write('1. Watch the video carefully.')
st.write('2. Review the embedded transcriptions and translations.')
st.write('3. Assess how accurately they match the spoken content in the video.')
st.write('4. Answer the questions provided on the next page based on your observations.')
st.write('5. Click the checkbox below to confirm that you have read and understood the instructions.')

st.session_state['instances_completed']=0
st.session_state['timestamp_registered']=timestamp

if st.button('Start'):
  switch_page("label_image") #redirect to first task page

