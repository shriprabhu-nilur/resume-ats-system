from dotenv import load_dotenv


load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import base64
import io 

import google.genai as genai

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


def get_response(input,pdf_content,prompt):

    response = client.models.generate_content(
    
    model="gemini-2.5-flash",                                          
    contents=[input,pdf_content[0],prompt]
)
    return response.text

def input_pdf_setup(uploade_file):

    if uploade_file is not None:

        image = pdf2image.convert_from_bytes(uploade_file.read())

        first_page = image[0]


        img_byte_arr = io.BytesIO()

        first_page.save(img_byte_arr, format='JPEG')
 
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [

            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    
    else:
        raise FileNotFoundError("NO file is uploaded")
    

# streamlit app


st.set_page_config(page_title="Resume ATS Expert")
st.header("ATS Tracking System")

input_text = st.text_area("Job description", key="input")

uploaded_file = st.file_uploader("Uploade Your Resume (PDF)....", type=["pdf"] )

if uploaded_file is not None:
    st.write("PDF uploaded successfully")


submit_1 = st.button("Tell me about the Resume")

submit_2 = st.button("How can i improve my Skills")


# submit_4 = st.button("What are the key words that are missing")


submit_3 = st.button("Percentage match")

input_prompt_1 = [
""" You are an experienced HR with Tech experience in the field of any one job role from Data science ,
    Full stack develper , Genrative ai , Agentic ai,web devlopment ,Data Enginner,ml ,dl
    Your task is to review the provided resume against the job description for this profile
    Please share the professional evaluation on whether the candidate's profile aligns with 
    hilights the strenghts and weekness for in the relation fo job descrioption
 """
]

input_prompt_3 = """
You are an advanced ATS (Applicant Tracking System) analyzer.

Analyze the uploaded resume against the provided job description.

Your tasks:
1. Calculate the percentage match between the resume and the job description.
2. Identify missing keywords and skills.
3. Highlight matching skills and qualifications.
4. Give improvement suggestions to increase ATS score.
5. Mention strengths of the candidate profile.
6. Provide the final ATS score out of 100.

Return the response in this format:

ATS Match Percentage: %
Matching Skills:
- 

Missing Keywords:
- 

Strengths:
- 

Suggestions for Improvement:
- 

Final ATS Score: /100

Job Description:
{job_description}
"""


if submit_1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response=get_response(input_prompt_1,pdf_content,input_text)

        st.subheader("The response is :")
        st.write(response)
    else:
        st.write("please uploade the resume")


elif submit_3:

    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response=get_response(input_prompt_3,pdf_content,input_text)

        st.subheader("The response is :")
        st.write(response)
    else:
        st.write("please uploade the resume")








