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

st.title('Introduction')
st.write('Welcome to this template demo app, presenting you a basic example of how to use Streamlit to create a Microtasking app.')
st.write('This demo consists of two tasks: \n1) labeling images of buildings on campus\n2) uploading campus images to label')
st.write('Please use this as a template to realize your own app consisting of a custom Streamlit GUI.')
st.write('Apply your knowledge gained from the lecture/seminar contents and the session/payment/file mangement utilities demonstrated in this app.')

st.session_state['instances_completed']=0
st.session_state['timestamp_registered']=timestamp

if st.button('Start'):
  switch_page("label_image") #redirect to first task page

