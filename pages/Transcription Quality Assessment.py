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

# def get_random_youtube_link(file_path):
#     try:
#         # Read the file and store links in a list
#         with open(file_path, 'r') as file:
#             links = file.readlines()

#         # Choose a random link from the list
#         random_link = random.choice(links).strip()
#         with open('/content/project_group_12/references/files/youtube_video_link.csv', 'wb') as file:
#           file.write(random_link)
        
#         return random_link

#     except FileNotFoundError:
#         print(f"Error: File '{file_path}' not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# Get query parameters
url_params = st.experimental_get_query_params()
camp_id = url_params.get('campId', [None])[0]
worker_id = url_params.get('workerId', [None])[0]
timestamp = datetime.now()
timestamp_file = timestamp.strftime("%Y%m%d_%H%M%S")

# Streamlit app
st.title('1/2 Transcription Quality Assessment')
#file_path = "/content/project_group_12/references/files/Video01CaptionsOK.mp4"
# youtube_video_link = str(file_path)
# st.video(Video01CaptionsOK.mp4)
youtube_video_url = "https://www.youtube.com/watch?v=37YU1ShrMpU&list=PLwrM2Wcy_MsCnq4XZitG3tjhvotoVbedy&index=10"
#st.video(youtube_video_url)
try:
    # youtube_video_link = get_random_youtube_link(file_path)
    st.video(youtube_video_url)
    
except st.ScriptRunner.StopException as e:
    st.warning(str(e))


# Check if 'instances_completed' is in session state, redirect to entry page if not
if 'instances_completed' not in st.session_state:
    switch_page("index")

# Get the current index from session state
instances_completed = st.session_state.instances_completed

# Load the initial image
selected_image = get_random_image("references/files")
# youtube_video_url = "https://www.youtube.com/watch?v=J0NuOlA2xDc"
# st.video(youtube_video_url)
cc_checked = st.checkbox("I have turned on the captions (cc) in the video")
if cc_checked:
  with st.form(key='image_form'):
    if selected_image:
        #st.image(selected_image, caption='Current Image', use_column_width=True)
        st.write("Transcription Quality Assessment")
        st.write ("Scale: 1 (Strongly Agree) - 5 (Strongly Disagree)")
        slider_val_1 = int(st.select_slider(" 1.The transcription is well-synced with the actual spoken content in the video.",options=['0','1', '2', '3', '4', '5',],key='slider1'))
        slider_val_2 = int(st.select_slider(" 2.The provided transcription accurately reflects the spoken content in the video.",options=['0','1', '2', '3', '4', '5',],key='slider2'))
        slider_val_3 = int(st.select_slider(" 3.The language in the transcription is not consistent with the spoken content.",options=['0','1', '2', '3', '4', '5',],key='slider3'))
        slider_val_4 = int(st.select_slider(" 4.The transcription is riddled with spelling and grammar errors in comparison to the spoken content.",options=['0','1', '2', '3', '4', '5',],key='slider4'))
        slider_val_5 = int(st.select_slider(" 5.The terminology and language in the transcription are consistent with the spoken content.",options=['0','1', '2', '3', '4', '5',],key='slider5'))
        slider_val_6 = int(st.select_slider(" 6.The transcription fails to capture linguistic nuances and expressions in spoken content.",options=['0','1', '2', '3', '4', '5',],key='slider6'))
        slider_val_7 = int(st.select_slider(" 7.The transcription is poorly synced with the actual spoken content in the video.",options=['0','1', '2', '3', '4', '5',],key='slider7'))
        st.session_state['current_image'] = selected_image
    else:
        st.warning('No images found in the specified directory.')

  # selection = st.selectbox('This building is named after:', ['', 'Helmholtz', 'Kirchhoff', 'Humboldt', 'Meitner', 'Hopper'])
    submit_button = st.form_submit_button("Submit")

    selection = slider_val_1 >0  and slider_val_2 >0 and slider_val_3 >0 and slider_val_4 >0 and slider_val_5 >0 and slider_val_6 >0 and slider_val_7 >0
  # Submit button
    if submit_button:
          # Check if mandatory fields are filled
          if selection:
              # image_name=os.path.basename(selected_image)
              # Create a DataFrame with the collected data
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

                  # 'Image Name': [image_name],
                  # 'Label': [selection],
              }
    
              df = pd.DataFrame(data)

              # Save the DataFrame to a CSV file
              df.to_csv(f'results/task_1/csv/{timestamp_file}_{worker_id}_image_labeling.csv', index=False)
              st.success('CSV file created successfully.')

              st.session_state.instances_completed += 1
              switch_page("Translation Quality Assessment")

          else:
              st.warning('Please select your answer first')