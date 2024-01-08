import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import hashlib
from datetime import datetime
import pandas as pd
from page_setup import setup_page

#hide sidebar using script
setup_page()

if ('instances_completed' not in st.session_state) or ('timestamp_registered' not in st.session_state):
  switch_page("index")
else:
  instances_completed = st.session_state.instances_completed
  timestamp_registered = st.session_state.timestamp_registered

st.title('Thank You!')
st.write('After you completed all assignments, please press the button to request your payment code:')

if st.button('Request'):
  if instances_completed >=2: #adjust to number of pages!
      # Get query parameters
      url_params = st.experimental_get_query_params()

      # Get 'campId' and 'workerId' from the dictionary, defaulting to None if not present
      camp_id = url_params.get('campId', [None])[0]
      worker_id = url_params.get('workerId', [None])[0]

      # Secret key for authentication
      secret_key_auth = 'cs_is_@m@zing'

      # Hash the concatenated string
      payment_code= hashlib.sha256((camp_id + worker_id + secret_key_auth).encode('utf-8')).hexdigest()
      
      timestamp_finished = datetime.now()
      timestamp_file = timestamp_finished.strftime("%Y%m%d_%H%M%S")

      #record registered worker
      data = {
          'Registered_Timestamp': [timestamp_registered],
          'Finished_Timestamp': [timestamp_finished],
          'Worker': [worker_id],
          'Campaign' : [camp_id],
          'Payment_Code' : [payment_code],
      }
      df = pd.DataFrame(data)

      # Save the DataFrame to a CSV file
      df.to_csv(f'results/finished/csv/{timestamp_file}_{worker_id}_registered.csv', index=False)
      st.success(f'Payment Code: #{payment_code}#') 
  else:
    switch_page("index") #redundant







