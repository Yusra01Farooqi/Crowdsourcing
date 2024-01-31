from numpy import string_
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os
import random
import pandas as pd
from datetime import datetime
from page_setup import setup_page

#hide sidebar
setup_page()

# Get query parameters
url_params = st.experimental_get_query_params()
camp_id = url_params.get('campId', [None])[0]
worker_id = url_params.get('workerId', [None])[0]
timestamp = datetime.now()
timestamp_file = timestamp.strftime("%Y%m%d_%H%M%S")

# Streamlit app
st.title('1/2 Transcription Quality Assessment')
youtube_video_url = "https://www.youtube.com/watch?v=37YU1ShrMpU&list=PLwrM2Wcy_MsCnq4XZitG3tjhvotoVbedy&index=10"

try:
    st.video(youtube_video_url)
    
except st.ScriptRunner.StopException as e:
    st.warning(str(e))


# Check if 'instances_completed' is in session state, redirect to entry page if not
if 'instances_completed' not in st.session_state:
    switch_page("index")

# Get the current index from session state
instances_completed = st.session_state.instances_completed

cc_checked = st.checkbox("I have turned on the captions (cc) in the video")
if cc_checked:
  with st.form(key='iqa_form'):
    if youtube_video_url:
        st.write("Transcription Quality Assessment")
        st.write ("Scale: 1 (Strongly Agree) - 5 (Strongly Disagree)")
        slider_val_1 = int(st.select_slider(" 1.The transcription is well-synced with the actual spoken content in the video.",options=['0','1', '2', '3', '4', '5',],key='slider1'))
        slider_val_2 = int(st.select_slider(" 2.The provided transcription accurately reflects the spoken content in the video.",options=['0','1', '2', '3', '4', '5',],key='slider2'))
        slider_val_3 = int(st.select_slider(" 3.The language in the transcription is not consistent with the spoken content.",options=['0','1', '2', '3', '4', '5',],key='slider3'))
        slider_val_4 = int(st.select_slider(" 4.The transcription is riddled with spelling and grammar errors in comparison to the spoken content.",options=['0','1', '2', '3', '4', '5',],key='slider4'))
        slider_val_5 = int(st.select_slider(" 5.The terminology and language in the transcription are consistent with the spoken content.",options=['0','1', '2', '3', '4', '5',],key='slider5'))
        slider_val_6 = int(st.select_slider(" 6.The transcription fails to capture linguistic nuances and expressions in spoken content.",options=['0','1', '2', '3', '4', '5',],key='slider6'))
        slider_val_7 = int(st.select_slider(" 7.The transcription is poorly synced with the actual spoken content in the video.",options=['0','1', '2', '3', '4', '5',],key='slider7'))
        st.session_state['current_video'] = youtube_video_url
    else:
        st.warning('No video found')

    submit_button = st.form_submit_button("Submit")

    selection = slider_val_1 >0
  # Submit button
    if submit_button:
          # Check if mandatory fields are filled
          if selection:
            data = {
                'Timestamp': [timestamp],
                'Worker': [worker_id],
                'Campaign' : [camp_id],
                'The transcription is well-synced with the actual spoken content in the video.':[slider_val_1],
                'The provided transcription accurately reflects the spoken content in the video':[slider_val_2],
                'The language in the transcription is not consistent with the spoken content.':[slider_val_3],
                'The transcription is riddled with spelling and grammar errors in comparison to the spoken content.':[slider_val_4],
                'The terminology and language in the transcription are consistent with the spoken content.':[slider_val_5],
                'The transcription fails to capture linguistic nuances and expressions in spoken content.':[slider_val_6],
                'The transcription is poorly synced with the actual spoken content in the video.':[slider_val_7],
            }
    
            df = pd.DataFrame(data)

            # Save the DataFrame to a CSV file
            df.to_csv(f'results/task_1/csv/{timestamp_file}_{worker_id}_Transcription Quality Assessment.csv', index=False)
            st.success('CSV file created successfully.')

            st.session_state.instances_completed += 1
            switch_page("Translation Quality Assessment")
          else:
            st.warning('Make sure all the questions are answered')
else:
  st.warning('Please click the check box first')