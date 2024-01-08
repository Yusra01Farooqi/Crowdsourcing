import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os
import random
import pandas as pd
import imghdr
from datetime import datetime
from page_setup import setup_page

#hide sidebar
setup_page()

from datetime import datetime

# Function to save uploaded image to the specified directory
def save_uploaded_image(uploaded_file, save_directory, worker_id, timestamp):
    if uploaded_file is not None:
        file_type = imghdr.what(None, h=uploaded_file.read(32))
        if file_type:
            # Construct the new file name
            new_file_name = f"{timestamp}_{worker_id}.{file_type}"
            saved_path = os.path.join(save_directory, new_file_name)
            with open(saved_path, 'wb') as f:
                f.write(uploaded_file.getvalue())
            return saved_path
    return None

# Get query parameters
url_params = st.experimental_get_query_params()
camp_id = url_params.get('campId', [None])[0]
worker_id = url_params.get('workerId', [None])[0]
timestamp = datetime.now()
timestamp_file = timestamp.strftime("%Y%m%d_%H%M%S")

# Streamlit app
st.title('2/2 Image Upload Page')

# Check if 'instances_completed' is in session state, redirect to entry page if not
if 'instances_completed' not in st.session_state:
    switch_page("index")

# Get the current index from session state
instances_completed = st.session_state.instances_completed

# Upload an image
st.write("Upload an image of one of the following TU Ilmenau buildings:")
st.write("*Helmholtzbau, Grace-Hopper-Bau, Kirchhoffbau, Meitnerbau or Humboldtbau*")
uploaded_image = st.file_uploader("Drag and drop or browse your system to upload an image:", type=["jpg","JPG", "jpeg", "png","PNG"])
#placing image saving here would repeat saving process on submission

# Save the uploaded image
if uploaded_image:
    st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

with st.form(key='image_form'):
    selection = st.selectbox('This building is named after:', ['', 'Helmholtz', 'Kirchhoff', 'Humboldt', 'Meitner', 'Hopper'])

    # Submit button
    if st.form_submit_button('Submit'):

        #saving must be placed here in order to prevent submission from repeating previous upload 
        #(~form submission re-renders page in initial state)
        saved_image_path = save_uploaded_image(uploaded_image, "results/task_2/files", worker_id, timestamp_file)

        # Check if mandatory fields are filled
        if selection and uploaded_image:
            # Create a DataFrame with the collected data
            data = {
                'Timestamp': [timestamp],
                'Worker': [worker_id],
                'Campaign' : [camp_id],
                'Image File': [f"{timestamp_file}_{worker_id}"],
                'Label': [selection],
            }
            df = pd.DataFrame(data)

            # Save the DataFrame to a CSV file
            df.to_csv(f'results/task_2/csv/{timestamp_file}_{worker_id}_image_upload.csv', index=False)
            st.success('CSV file created successfully.')

            st.session_state.instances_completed += 1
            switch_page("payment")

        else:
            st.warning('Please upload and label a valid image before submitting!')
