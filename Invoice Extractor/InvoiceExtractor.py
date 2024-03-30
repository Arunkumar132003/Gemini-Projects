import os 
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import google.generativeai as genai 
from PIL import Image 
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model= genai.GenerativeModel('gemini-pro-vision')

def input_image_setup(img_file):
    if img_file is not None:
        data = img_file.getvalue()

        image_parts = [
            {
                "mime_type": img_file.type, 
                "data": data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File is not uploaded")

def get_response(role,img,input):
    response= model.generate_content([role,img[0],input])
    return response.text

st.header('INVOICE EXTRACTOR')
input= st.text_input('Enter your question',key=input)
img_file= st.file_uploader('Upload your file')
submit= st.button('Submit')
if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

role=""" 
    As an expert in understanding invoices, your role is to analyze input images that 
    represent invoices and provide answers to questions based on the information contained within those images.
"""

if submit:
    image_data = input_image_setup(img_file)
    response=get_response(role,image_data,input)
    st.write(response)
