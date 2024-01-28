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

# Get query parameters
url_params = st.experimental_get_query_params()
camp_id = url_params.get('campId', [None])[0]
worker_id = url_params.get('workerId', [None])[0]
timestamp = datetime.now()
timestamp_file = timestamp.strftime("%Y%m%d_%H%M%S")

# Streamlit app

st.title('2/2 Translation Quality Assessment')
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
# Dropdown menu
option = st.selectbox('Please select the language you want to see translation in', ('','Urdu', 'Hindi', 'German'))

# Display text based on the selected option
if option == 'German':
    st.write('Du hast Deutsch ausgewählt.')
    st.write('Oh, hallo Kathy, wie geht es dir?')
    st.write('Hi Vicki. Gut, danke. Und dir?')
    st.write('Auch gut.')
    st.write('Hallo zusammen.')
    st.write('Na, wie geht\'s?')
    st.write('Nun, ich habe letzte Nacht nur sechs Stunden geschlafen')
    st.write('und ich bin mit ein paar Rückenschmerzen aufgewacht. Und')
    st.write('mein Bauch spielt verrückt. Ich hatte Cornflakes zum')
    st.write('Frühstück und ich glaube, die Milch war ein bisschen')
    st.write('falsch. Und ich mache mir ein bisschen Sorgen um meinen Cholesterin')
    st.write('Cholesterinspiegel. Ich werde den Arzt danach fragen.')
    st.write('das fragen. Aber wenigstens bleibe ich regelmäßig. Keine Verstopfung.')

elif option == 'Urdu':
    st.write('آپ نے اردو منتخب کی ہے۔')
    st.write('اوہ ہیلو کیتھی، آپ کیسی ہیں؟')
    st.write('ہیلو وکی۔ ٹھیک شکریہ اور آپ؟')
    st.write('زبردست.')
    st.write('سلام سب کو.')
    st.write('آپ کیسے ہو؟')
    st.write('ٹھیک ہے، میں کل رات صرف چھ گھنٹے سویا تھا اور میں کمر میں تھوڑا درد کے ساتھ بیدار ہوا۔')
    st.write('اور میرا پیٹ کام کر رہا ہے۔ میں نے ناشتے میں کارن فلیکس لیا تھا اور مجھے لگتا ہے کہ دودھ  تھوڑا بگاڑا ہوا تھا۔ اور میں اپنے کولیسٹرول کی سطح کے بارے میں تھوڑا سا پریشان ہوں۔')
    st.write('میں ڈاکٹر سے اس بارے میں پوچھنے جا رہا ہوں۔ لیکن کم سے کم میں باقاعدہ ہوں۔')
    st.write('قبض نہیں ہو رہا۔')

elif option == 'Hindi':
    st.write('आपने हिंदी चयन किया है।')
    st.write('ओह हेलो कैथी, आप कैसी हैं?')
    st.write('हाय विकी. ठीक धन्यवाद?')
    st.write('महान।')
    st.write('सुनिये सब लोग।')
    st.write('आप कैसे हैं?')
    st.write('ख़ैर, मैं कल रात केवल छह घंटे सोया और जब उठा तो मुझे पीठ में थोड़ा दर्द हो रहा था।')
    st.write('और मेरा पेट बढ़ रहा है। मैंने नाश्ते में कॉर्नफ्लेक्स खाया और मुझे लगता है कि दूध थोड़ा कम था।')
    st.write('और मैं अपने कोलेस्ट्रॉल के स्तर को लेकर थोड़ा चिंतित हूं। मैं इसके बारे में डॉक्टर से पूछने जा रहा हूं। लेकिन कम से कम मैं नियमित रह रहा हूं।')
    st.write('कोई कब्ज नहीं.')

# Load the initial image
with st.form(key='image_form'):
  if youtube_video_url:
      st.write("Translation Quality Assessment")
      st.write ("Scale: 1 (Strongly Agree) - 5 (Strongly Disagree)")
      slider_val_1 = int(st.select_slider(" 1.The provided translation inaccurately conveys the meaning of the spoken content in the video.",options=['0','1', '2', '3', '4', '5',],key='slider1'))
      slider_val_2 = int(st.select_slider(" 2.The translated words are easy to understand in the new language.",options=['0','1', '2', '3', '4', '5',],key='slider2'))
      slider_val_3 = int(st.select_slider(" 3.The translation appropriately considers cultural nuances and sensitivities evident in the spoken content.",options=['0','1', '2', '3', '4', '5',],key='slider3'))
      slider_val_4 = int(st.select_slider(" 4. The provided translation accurately conveys the meaning of the spoken content in the video.",options=['0','1', '2', '3', '4', '5',],key='slider4'))
      st.write("Provide specific suggestions for improving the transcriptions and translations.")
      feedback = st.text_area("Your Feedback", "")
      # Generate a simple math problem as a fun validity check
      num1 = random.randint(1, 10)
      num2 = random.randint(1, 10)
      correct_answer = num1 + num2
      user_answer = st.number_input(f'What is the sum of {num1} and {num2}?')
      st.session_state['current_video'] = youtube_video_url
  else:
      st.warning('No video found')

  submit_button = st.form_submit_button("Submit")

  selection = slider_val_1 >0
# Submit button
  if submit_button:
        # Check if mandatory fields are filled
        if selection:
            # Create a DataFrame with the collected data
            data = {
                'Timestamp': [timestamp],
                'Worker': [worker_id],
                'Campaign' : [camp_id],
                'Language' : [option],
                'Correct' : [correct_answer],
                'User' : [user_answer],
                'The provided translation inaccurately conveys the meaning of the spoken content in the video.':[slider_val_1],
                'The translated words are easy to understand in the new language.':[slider_val_2],
                'The translation appropriately considers cultural nuances and sensitivities evident in the spoken content.':[slider_val_3],
                'The provided translation accurately conveys the meaning of the spoken content in the video.':[slider_val_4],
                'Provide specific suggestions for improving the transcriptions and translations.':[feedback],
                
            }
  
            df = pd.DataFrame(data)

            # Save the DataFrame to a CSV file
            df.to_csv(f'results/task_2/csv/{timestamp_file}_{worker_id}_Translation Quality Assessment.csv', index=False)
            st.success('CSV file created successfully.')

            st.session_state.instances_completed += 1
            switch_page("payment")

        else:
            st.warning('Please select your answer first')
