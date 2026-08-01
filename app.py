# Step 1 : Load Modules
import pytesseract
import streamlit as st
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool

import pandas as pd
import numpy as np
import time
from io import BytesIO
from PIL import Image
import requests

# Backend ----------------------------------------------------------------------------------------

st.sidebar.title(":green[Model Selection : ]")
model_name = st.sidebar.selectbox(label="", label_visibility='collapsed',
                             options=['gemini-3.5-flash-lite', 'gemini-3.5-flash', 'gemini-3.1-flash-lite'],
                             index=0)

# Step 2 : Create models and clients
gemini_model = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=st.secrets.api_key.GOOGLE_API_KEY
)

tavily_client = TavilyClient(
    api_key=st.secrets.api_key.TAVILY_API_KEY
)


# Step 3 : Tools
def search_latest_info(query: str):
    """This functions helps to retrieve latest information based
       on given user query related research or contents."""

    return tavily_client.search(query)


def generate_image(image_prompt: str):
    """This function helps user generate image with free api
       with image prompt."""

    url = f'https://image.pollinations.ai/{image_prompt}'

    # content = requests.get(url).content
    # buffer = BytesIO(content)
    # img = Image.open(buffer)
    requests.get(url)

    return url


# Step 4 : Create Agent
leader_agent = create_agent(
    model=gemini_model,
    tools=[search_latest_info, generate_image]
)


# Step 5 : Agent function
def run_agent(query, leader_agent = leader_agent):

    prompt = f"""Based on Below given Query,
    your task is to call specific tool, first to
    promptify user prompt, than call image tool,
    latest search if required.give slide dynamic, ui ux,
    with creative design, keep help of function to generate image
    based on given topic for each and every slide,
    Generate image using
    with number of slide asked, and use time sleep to hit image request on server 
    and using file handling embed this in output html, 
    use css for navigation and give 
    Final response output in HTML, no markdowns and
    strictly don't write html after ```
    user query given below:"""

    prompt = prompt+query

    response = leader_agent.invoke({'messages':[{'role':'user', 'content':prompt}]}) 
    code = response['messages'][-1].content[-1]['text'] 
    return code


# Frontend ---------------------------------------------------------------------------------------

# Hide all anchors
st.markdown(r"""
    <style>
    .css-15zrgzn {display: none}
    </style>
    """, unsafe_allow_html=True) 

icon = """<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#FF6C6C"><path d="m646-438-86 138q-11 17-30.5 14T505-309l-28-112-273 273q-11 11-27.5 11.5T148-148q-11-11-11-28t11-28l273-274-112-28q-20-5-23-24.5t14-30.5l138-85-12-163q-2-20 16-29t33 4l125 105 151-61q19-8 33 6t6 33l-61 151 105 124q13 15 4 33t-29 16l-163-11ZM134-706q-6-6-6-14t6-14l52-52q6-6 14-6t14 6l52 52q6 6 6 14t-6 14l-52 52q-6 6-14 6t-14-6l-52-52Zm421 263 48-79 93 7-60-71 35-86-86 35-71-59 7 92-79 49 90 22 23 90Zm151 309-52-52q-6-6-6-14t6-14l52-52q6-6 14-6t14 6l52 52q6 6 6 14t-6 14l-52 52q-6 6-14 6t-14-6ZM569-570Z"/></svg>"""

st.set_page_config(layout='wide', 
                   page_title='Slide Wizard', 
                   page_icon=icon,
                   initial_sidebar_state='expanded'
)


st.title("🪄 Slide Wizard &nbsp;|&nbsp; :red[AI Presentation Builder]", text_alignment='center')
st.write(" ")

st.sidebar.title(":green[User Prompt : ]")
all_prompt = st.sidebar.text_area(label="Enter prompt for all features : ")

side_n_slides = st.sidebar.number_input(label="Enter number of slides : ", key="Side-N-Slides",
                                        min_value=2,
                                        max_value=15)

all_button = st.sidebar.button(label="Generate Everything", key='All-Button', type='primary')

with st.container(border=True, horizontal_alignment='center'):
    heading, download_button = st.columns([9, 1], vertical_alignment='bottom')
    with heading:
        st.subheader(":violet[PPT Generation : ]")


    input_section, n_slides_section, button_section = st.columns([6, 3, 1], vertical_alignment='bottom')
    with input_section:
        ppt_input = st.text_input("Enter PPT Prompt : ", 
                                  placeholder="Topic, Description, etc", key='PPT-Input')
    with n_slides_section:
        n_slides = st.number_input(label="Enter number of slides : ", 
                                    key='N-Slides',
                                    min_value=2,
                                    max_value=15)
    with button_section:
        ppt_button = st.button("Generate Image", key="PPT-Button", type='primary')


    if ppt_button or all_button:
        if ppt_input or all_prompt:
            with st.spinner("Generating PPT"):
                try: 
                    ppt_code = run_agent((all_prompt or ppt_input) + f"Number of slides = {(max(n_slides, side_n_slides))}")
                    st.html(ppt_code, unsafe_allow_javascript=True, width='content')

                    # with open('ppt.html', 'w') as f:
                    #     f.write(ppt_code)
                    with download_button:
                        st.download_button('Download HTML',
                                            data = ppt_code,
                                            file_name='ppt_wizard.html',
                                            mime="application/html")

                except Exception as e:
                    st.error(e)
        else:
            st.error('Please provide a prompt for news.')
            


left, right = st.columns(2)

with left:
    with st.container(border=True, horizontal_alignment='center', vertical_alignment='center'):
        st.subheader(":violet[Image Generation : ]")
        input_section, button_section = st.columns([4,1])
        with input_section:
            image_input = st.text_input("", label_visibility='collapsed', placeholder="Enter Image Prompt")
        with button_section:
            image_button = st.button("Generate Image", key="Image-Button", type='primary')

        if image_button or all_button:
            if image_input or all_prompt:
                with st.container(height=700, border=False, vertical_alignment='center', horizontal_alignment='center'):
                    with st.spinner("Generating Image"):
                        try:
                            url = generate_image((image_input or all_prompt))
                            st.image(url, width='stretch')
                        except Exception as e:
                            st.error(e)
            else:
                st.error('Please provide a prompt for news.')


with right:
    with st.container(border=True, horizontal_alignment='center', vertical_alignment='center'):
        st.subheader(":violet[News Generation : ]")
        input_section, button_section = st.columns([4,1])
        with input_section:
            news_input = st.text_input("", label_visibility='collapsed', placeholder="Enter News Prompt")
        with button_section:
            news_button = st.button("Generate News", key="News-Button", type='primary')

        if news_button or all_button:
            if news_input or all_prompt:
                with st.container(height=700, border=False, vertical_alignment='center', horizontal_alignment='center'):
                    with st.spinner("Generating News"):
                        try: 
                            prompt = """Give Latest news related articles to given user query in dynamic html
                                        Output with cards design format, strict HTML output, not any markdown
                                        response.
                                        User query: """ + (news_input or all_prompt)
                            response = leader_agent.invoke({'messages' : [{'role': 'user', 'content': prompt}]})
                            news_code = (response['messages'][-1].content[-1]['text']).strip('```')
                            st.html(news_code, unsafe_allow_javascript=True, width='stretch')

                        except Exception as e:
                            st.error(e)
            else:
                st.error('Please provide a prompt for news.')
        

        
