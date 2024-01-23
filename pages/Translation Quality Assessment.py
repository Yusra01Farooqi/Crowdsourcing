import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os
import random
import pandas as pd
import imghdr
from datetime import datetime
from page_setup import setup_page
from numpy import string_

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
        random_link = random.choice(links).strip()

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
st.title('2/2 Translation Quality Assessment (if applicable)')
file_path = "references/files/youtube.txt"
# youtube_video_link = str(file_path)
# st.video(youtube_video_link)



try:
    # with open('/content/project_group_12/references/files/youtube_video_link.txt', 'r') as file:

    #   my_variable = file.read()
    youtube_video_link = get_random_youtube_link(file_path)
    # youtube_video_link = my_variable
    st.video(youtube_video_link)
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

with st.form(key='image_form'):
  if selected_image:
      #st.image(selected_image, caption='Current Image', use_column_width=True)
      st.write("Transcription Quality Assessment")
      slider_val_1 = int(st.select_slider(" 1.The provided translation inaccurately conveys the meaning of the spoken content in the video.",options=['0','1', '2', '3', '4', '5',],key='slider1'))
      slider_val_2 = int(st.select_slider(" 2.The translation reads fluently in comparison to the actual spoken content.",options=['0','1', '2', '3', '4', '5',],key='slider2'))
      slider_val_3 = int(st.select_slider(" 3.The translation appropriately considers cultural nuances and sensitivities evident in the spoken content.",options=['0','1', '2', '3', '4', '5',],key='slider3'))
      slider_val_4 = int(st.select_slider(" 4.The provided translation accurately conveys the meaning of the spoken content in the video.",options=['0','1', '2', '3', '4', '5',],key='slider4'))
      st.header("Provide specific suggestions for improving the transcriptions and translations.")
      feedback = st.text_area("Your Feedback", "")
      st.session_state['current_image'] = selected_image
  else:
      st.warning('No images found in the specified directory.')

# selection = st.selectbox('This building is named after:', ['', 'Helmholtz', 'Kirchhoff', 'Humboldt', 'Meitner', 'Hopper'])
  submit_button = st.form_submit_button("Submit")

  selection = slider_val_1 >0  and slider_val_2 >0 and slider_val_3 >0 and slider_val_4 >0 
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
                'Question 1':[slider_val_1],
                'Question 2':[slider_val_2],
                'Question 3':[slider_val_3],
                'Question 4':[slider_val_4],
                'Question 5':[feedback],

                # 'Image Name': [image_name],
                # 'Label': [selection],
            }
  
            df = pd.DataFrame(data)

            # Save the DataFrame to a CSV file
            df.to_csv(f'results/task_1/csv/{timestamp_file}_{worker_id}_image_labeling.csv', index=False)
            st.success("Feedback submitted successfully!")

            st.session_state.instances_completed += 1
            switch_page("payment")

        else:
            st.warning('Please select your answer first')




# # Function to save uploaded image to the specified directory
# def save_uploaded_image(uploaded_file, save_directory, worker_id, timestamp):
#     if uploaded_file is not None:
#         file_type = imghdr.what(None, h=uploaded_file.read(32))
#         if file_type:
#             # Construct the new file name
#             new_file_name = f"{timestamp}_{worker_id}.{file_type}"
#             saved_path = os.path.join(save_directory, new_file_name)
#             with open(saved_path, 'wb') as f:
#                 f.write(uploaded_file.getvalue())
#             return saved_path
#     return None

# # Get query parameters
# url_params = st.experimental_get_query_params()
# camp_id = url_params.get('campId', [None])[0]
# worker_id = url_params.get('workerId', [None])[0]
# timestamp = datetime.now()
# timestamp_file = timestamp.strftime("%Y%m%d_%H%M%S")

# # Streamlit app
# st.title('2/2 Image Upload Page')

# # Check if 'instances_completed' is in session state, redirect to entry page if not
# if 'instances_completed' not in st.session_state:
#     switch_page("index")

# # Get the current index from session state
# instances_completed = st.session_state.instances_completed

# # Upload an image
# st.write("Upload an image of one of the following TU Ilmenau buildings:")
# st.write("*Helmholtzbau, Grace-Hopper-Bau, Kirchhoffbau, Meitnerbau or Humboldtbau*")
# uploaded_image = st.file_uploader("Drag and drop or browse your system to upload an image:", type=["jpg","JPG", "jpeg", "png","PNG"])
# #placing image saving here would repeat saving process on submission

# # Save the uploaded image
# if uploaded_image:
#     st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

# with st.form(key='image_form'):
#     selection = st.selectbox('This building is named after:', ['', 'Helmholtz', 'Kirchhoff', 'Humboldt', 'Meitner', 'Hopper'])

#     # Submit button
#     if st.form_submit_button('Submit'):

#         #saving must be placed here in order to prevent submission from repeating previous upload 
#         #(~form submission re-renders page in initial state)
#         saved_image_path = save_uploaded_image(uploaded_image, "results/task_2/files", worker_id, timestamp_file)

#         # Check if mandatory fields are filled
#         if selection and uploaded_image:
#             # Create a DataFrame with the collected data
#             data = {
#                 'Timestamp': [timestamp],
#                 'Worker': [worker_id],
#                 'Campaign' : [camp_id],
#                 'Image File': [f"{timestamp_file}_{worker_id}"],
#                 'Label': [selection],
#             }
#             df = pd.DataFrame(data)

#             # Save the DataFrame to a CSV file
#             df.to_csv(f'results/task_2/csv/{timestamp_file}_{worker_id}_image_upload.csv', index=False)
#             st.success('CSV file created successfully.')

#             st.session_state.instances_completed += 1
#             switch_page("payment")

#         else:
#             st.warning('Please upload and label a valid image before submitting!')
