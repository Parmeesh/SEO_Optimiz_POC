from newspaper import Article
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI
from bs4 import BeautifulSoup
from datetime import datetime
import streamlit as st
import requests
from openai import OpenAI as opAI
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import cloudinary, cloudinary.uploader

from Prompt import *

from dotenv import load_dotenv
load_dotenv()


def fetch_article(url):
    url=url
    article=Article(url)
    article.download()
    article.parse()
    r_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=10)
    splits=r_splitter.split_text(article.text)
    content=splits[0]
    print(len(splits))
    print(splits)
    metadata={
        'Title':article.title,
        'Authors':article.authors,
        'Publish Date':article.publish_date,
        'URL':article.url,
        'Summary': article.summary[:50],
        'Keywords': ', '.join(article.meta_keywords),
        'Top Image': article.top_image,
        'Tags':article.tags}
    return content, metadata, article.title

def local_css(style):
    with open(style) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


#------------------------Google---------------------------------------------------------------------------------
def init_Gemini_llm(googlekey):
    llm=GoogleGenerativeAI(model="gemini-pro",google_api_key=googlekey, temperature=0.5, max_output_tokens=2500)
    return llm

def seo_optimize_article(article,keyword_list, llm, prompt):
    formatted_prompt_seo=prompt.format(original_article=article, keyword_list=keyword_list)
    response=llm.invoke(str(formatted_prompt_seo))
    return response

def generate_new_article_metadata(article):
    soup = BeautifulSoup(article, 'html.parser')
    title = soup.find('title').text
    description = soup.find('meta',{'name':'description'})['content']
    keywords = soup.find('meta',{'name':'keywords'})['content']
    publish_date =  str(datetime.now().strftime("%Y-%m-%d"))
    return{
        'Title':title,
        'Description':description,
        'Keywords':keywords,
        'Publish Date':publish_date}, title

def generate_HTML_with_image_gemini(llm,prompt_image_gen,html_article, img_list):
        formatted_prompt_image = prompt_image_gen.format(html_article=html_article, img_list=img_list)
        print(formatted_prompt_image)
        response=llm.invoke(formatted_prompt_image)
        return response

#-----------------------------OpenAI--------------------------------------------------------

def init_OpenAI_llm(openai_key):
    llm=OpenAI(model_name="gpt-3.5-turbo-instruct",temperature=0.75, openai_api_key=openai_key,verbose=True, max_tokens=2500)
    return llm


def seo_optimize_article_Openai(article, llm, prompt):
    with get_openai_callback() as cb1:
        formatted_prompt_seo=prompt.format(original_article=article)
        print(formatted_prompt_seo)
        response=llm.predict(formatted_prompt_seo)
        print(cb1)
    return response, cb1

def generate_new_article_metadata_openai(article):
    soup=BeautifulSoup(article, 'lxml')
    title_tag=soup.find('title')
    title=title_tag.string if title_tag else 'No title found'
    meta_description_tag = soup.find('meta', attrs={'name': 'description'})
    meta_description = meta_description_tag['content'] if meta_description_tag else 'No meta description found'
    publish_date=str(datetime.now().strftime("%Y-%m-%d"))
    return{
        'Title':title,
        'Description':meta_description,
        'Publish Date':publish_date}, title

def generate_HTML_with_image_openai(llm,prompt_image_gen,html_article, img_list):
        with get_openai_callback() as cb:
            formatted_prompt_image = prompt_image_gen.format(html_article=html_article, img_list=img_list)
            print(formatted_prompt_image)
            response=llm.predict(formatted_prompt_image)
        return response, cb
#---------------------------------IMAGE---------------------------------------------------------------------
def init_cloudinary(cl_cloudname, cl_secret, cl_api):
    cloudinary.config(
                cloud_name = cl_cloudname,
                api_key = cl_api,
                api_secret = cl_secret)


def generate_images(llm,title):
    response = llm.images.generate(
        model="dall-e-2",
        prompt=title,
        size="512x512",
        # quality="standard",
        n=2,
        response_format="url")
    return response.data[0].url,response.data[1].url


def making_img_list(img_url1, img_url2 ):
    img_list=[]
    cloudin_upload1=cloudinary.uploader.upload(img_url1)
    img_list.append(cloudin_upload1['url'])
    cloudin_upload2=cloudinary.uploader.upload(img_url2)
    img_list.append(cloudin_upload2['url'])
    return img_list



#-------------------------------------API Keys Verification----------------------------------------

    
def openAI_api_key_valid(openAI_api_key):
    endpoint='https://api.openai.com/v1/chat/completions'
    headers = {
    'Authorization': f'Bearer {openAI_api_key}',
    'Content-Type': 'application/json',}
    data = {"model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "temperature": 0.7}
    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
        return True
    elif response.status_code == 401:
        print("Unauthorized. Check your API key.")
        return "wrong key"
    else:
        print("Error:", response.status_code)



def google_api_key_valid(google_ki_api_key):
    endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
    headers = {'Content-Type': 'application/json',}
    payload = {
        "contents": [{"parts": [{"text": "Hi, How are you?"}]}]}
    url_with_key = f"{endpoint}?key={google_ki_api_key}"

    response = requests.post(url_with_key, json=payload, headers=headers)

    print("Response Code:", response.status_code)
    if response.status_code == 200:
        return True  
    
    elif response.status_code == 400:
        return 'wrong key'
    else:
        print(f"Error {response.status_code}: {response.text}")

#-----------------------------------------------Google Search-------------------------------------------------
def get_url_top1_searches(title):
    SEARCH_API_KEY = 'AIzaSyDIBgrGOxCtDgLPeSqhkMF349UAZGbkt3E'
    SEARCH_ENGINE_ID = 'f5ed74e7757ee44c4'
    SEARCH_URL = 'https://www.googleapis.com/customsearch/v1'
    params={
        'q': title,
        'cx': SEARCH_ENGINE_ID,
        'key': SEARCH_API_KEY,
        'num': 1,
        'siteSearch': 'www.britannica.com/*'}
    
    response = requests.get(SEARCH_URL, params=params)
    if response.status_code == 200:
        search_results = response.json()
        url_list = search_results['items'][0]['link']
        return url_list
    else:
        print(f"Error: {response.status_code}")
    

def get_text(url):
    article=Article(url)
    article.download()
    article.parse()
    r_splitter=RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=15)
    splits=r_splitter.split_text(article.text)
    return splits[0]

def get_keywords(llm, article_text):
    format_prompt_keywords= prompt_for_keywords.format(article_text=article_text)
    response = llm.invoke(format_prompt_keywords)
    keyword_list = [item.split(". ", 1)[-1] for item in response.split('\n')]
    return keyword_list

