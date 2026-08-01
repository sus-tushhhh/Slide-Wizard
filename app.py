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

model_name = st.sidebar.selectbox(label="Select Model : ",
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
    use css for next and previous buttons and don't use js and give 
    Final response output in HTML, no markdowns and
    strictly don't write html after ```
    user query given below:"""

    prompt = prompt+query

    response = leader_agent.invoke({'messages':[{'role':'user', 'content':prompt}]}) 
    code = response['messages'][-1].content[-1]['text'] 
    return code


# Frontend ---------------------------------------------------------------------------------------

icon = """<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#FF6C6C"><path d="m646-438-86 138q-11 17-30.5 14T505-309l-28-112-273 273q-11 11-27.5 11.5T148-148q-11-11-11-28t11-28l273-274-112-28q-20-5-23-24.5t14-30.5l138-85-12-163q-2-20 16-29t33 4l125 105 151-61q19-8 33 6t6 33l-61 151 105 124q13 15 4 33t-29 16l-163-11ZM134-706q-6-6-6-14t6-14l52-52q6-6 14-6t14 6l52 52q6 6 6 14t-6 14l-52 52q-6 6-14 6t-14-6l-52-52Zm421 263 48-79 93 7-60-71 35-86-86 35-71-59 7 92-79 49 90 22 23 90Zm151 309-52-52q-6-6-6-14t6-14l52-52q6-6 14-6t14 6l52 52q6 6 6 14t-6 14l-52 52q-6 6-14 6t-14-6ZM569-570Z"/></svg>"""

st.set_page_config(layout='wide', 
                   page_title='Slide Wizard', 
                   page_icon=icon,
                   initial_sidebar_state='expanded'
)


st.title("🪄 Slide Wizard &nbsp;|&nbsp; :red[AI Presentation Builder]", text_alignment='center')
st.write(" ")
st.sidebar.title("User Prompt", text_alignment='center')


user_prompt = st.sidebar.text_area(label="Enter prompt for ppt : ",
                                   placeholder="Write title, description about your ppt.")
n_slides = st.sidebar.number_input(label="Enter number of slides : ",
                                   min_value=2,
                                   max_value=15)

tab1, tab2, tab3 = st.tabs(["Generate Image",
                            "Fetch News",
                            "Generate PPT"])

if not user_prompt:
    st.sidebar.error("Please write a prompt.")
else:
    with tab1:
        if st.button("Generate Image", key='Image-Button'):
            with st.spinner("Generating Image"):
                try:
                    url = generate_image(user_prompt)
                    st.image(url)
                except Exception as e:
                    st.error(e)

    with tab2:
        if st.button("Generate News", key="News-Button"):
            with st.spinner("Generating News"):
                try: 
                    prompt = """Give Latest news related articles to given user query in dynamic html
                                Output with cards design format, strict HTML output, not any markdown
                                response.
                                User query: """ + user_prompt
                    response = leader_agent.invoke({'messages' : [{'role': 'user', 'content': prompt}]})
                    news_code = (response['messages'][-1].content[-1]['text']).strip('```')
                    st.html(news_code, unsafe_allow_javascript=True)

                except Exception as e:
                    st.error(e)

    with tab3:
        if st.sidebar.button(label="Generate PPT", shortcut="Enter", key='PPT-Button'):
            with st.spinner("Generating PPT"):
                try: 
                    ppt_code = run_agent(user_prompt + f"Number of slides = {n_slides}")
                    st.html(ppt_code, unsafe_allow_javascript=True)

                    with open('ppt.html', 'w') as f:
                        f.write(ppt_code)

                except Exception as e:
                    st.error(e)

            
