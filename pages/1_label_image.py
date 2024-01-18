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

# Function to get an image from the specified directory at the given index
def get_random_image(directory):
    images = [f for f in os.listdir(directory) if f.endswith(('.JPG','.jpg', '.jpeg', '.png','.PNG'))]
    if images:
        return os.path.join(directory, random.choice(images))
    else:
        return None

def get_random_youtube_link(file_path):
    try:
        # Read the file and store links in a list
        with open(file_path, 'r') as file:
            links = file.readlines()

        # Choose a random link from the list
        random_link = random.choice(links)

        return random_link

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Get query parameters
url_params = st.experimental_get_query_params()
camp_id = url_params.get('campId', [None])[0]
worker_id = url_params.get('workerId', [None])[0]
timestamp = datetime.now()
timestamp_file = timestamp.strftime("%Y%m%d_%H%M%S")

# Streamlit app
st.title('1/2 Transcription Quality Assessment')
file_path = "references/files/youtube.txt"
youtube_video_link = str(file_path)
st.video(youtube_video_link)
# Check if 'instances_completed' is in session state, redirect to entry page if not
if 'instances_completed' not in st.session_state:
    switch_page("index")

# Get the current index from session state
instances_completed = st.session_state.instances_completed

# Load the initial image
selected_image = get_random_image("references/files")

with st.form(key='image_form'):
  if selected_image:
      #st.image(selected_image, caption='Current Image', use_column_width=True)
      st.write("Transcription Quality Assessment")
      slider_val_1 = st.select_slider(" 1.The provided transcription accurately reflects the spoken content in the video",options=['1', '2', '3', '4', '5',],key='slider1')
      slider_val_2 = st.select_slider(" 2.The transcription fails to capture linguistic nuances and expressions in the actual spoken content",options=['1', '2', '3', '4', '5',],key='slider2')
      slider_val_3 = st.select_slider(" 3.The transcription is riddled with spelling and grammar errors in comparison to the spoken content",options=['1', '2', '3', '4', '5',],key='slider3')
      slider_val_4 = st.select_slider(" 4.The terminology and language in the transcription are consistent with the spoken content.",options=['1', '2', '3', '4', '5',],key='slider4')
      slider_val_5 = st.select_slider(" 1.The provided transcription accurately reflects the spoken content in the video",options=['1', '2', '3', '4', '5',],key='slider5')
      st.session_state['current_image'] = selected_image
  else:
      st.warning('No images found in the specified directory.')

selection = st.selectbox('This building is named after:', ['', 'Helmholtz', 'Kirchhoff', 'Humboldt', 'Meitner', 'Hopper'])

# Submit button
if st.form_submit_button('Submit'):
      # Check if mandatory fields are filled
      if selection:
          image_name=os.path.basename(selected_image)
          # Create a DataFrame with the collected data
          data = {
              'Timestamp': [timestamp],
              'Worker': [worker_id],
              'Campaign' : [camp_id],
              'Image Name': [image_name],
              'Label': [selection],
          }
 
          df = pd.DataFrame(data)

          # Save the DataFrame to a CSV file
          df.to_csv(f'results/task_1/csv/{timestamp_file}_{worker_id}_image_labeling.csv', index=False)
          st.success('CSV file created successfully.')

          st.session_state.instances_completed += 1
          switch_page("upload_image")

      else:
          st.warning('Please select your answer first')
