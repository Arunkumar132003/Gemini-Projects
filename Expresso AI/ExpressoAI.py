import os
from dotenv import load_dotenv
import PIL.Image
import streamlit as st
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.sidebar.markdown('## LIST OF MODELS')

selected_model = st.sidebar.selectbox('Select Model', ['Expresso AI (Text only)', 'Expresso AI (Text and Image)'])

st.markdown("<h1 style='text-align: center;'>Expresso <span style='color: orange'>AI</span></h1>", unsafe_allow_html=True)
st.write('Welcome to Expresso AI. Select a model from the sidebar.')

if selected_model == 'Expresso AI (Text only)':
    input_text = st.text_input('Ask your question', key='input')
    submit = st.button('Submit')

    def getresponse(prompt):
        model = genai.GenerativeModel('gemini-pro')
        if prompt != "":
            response = model.generate_content(prompt)
            return response.text

    if submit:
        try:
            response = getresponse(input_text)
            if response is not None:
                st.write(response)
            else:
                st.warning('Enter your question')
        except:
            st.warning('An error occurred. Please try again.')

else:
    model = genai.GenerativeModel('gemini-pro-vision')
    input_text = st.text_input('Ask your question', key='input')
    img = st.file_uploader('Upload image')
    submit = st.button('Submit')

    def getresponse(input_text, img):
        if input_text != "":
            response = model.generate_content([input_text, img]) if img else model.generate_content(input_text)
            return response.text

    if img is not None:
        img = PIL.Image.open(img)
        st.image(img, caption='Uploaded image', use_column_width=True)

    if submit:
        try:
            response = getresponse(input_text, img)
            if response is not None:
                st.write(response)
            else:
                st.warning('Enter your question')
        except:
            st.warning('An error occurred. Please try again.')
