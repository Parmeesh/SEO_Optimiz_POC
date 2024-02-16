from newspaper import Article
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI
from bs4 import BeautifulSoup
from datetime import datetime
import streamlit as st

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
    r_splitter = RecursiveCharacterTextSplitter(chunk_size=2800, chunk_overlap=10)
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
    return content, metadata
   

def local_css(style):
    with open(style) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


#------------------------Google---------------------------------------------------------------------------------
def init_Gemini_llm(googlekey):
    llm=GoogleGenerativeAI(model="gemini-pro",google_api_key=googlekey, temperature=0.7)
    return llm

def seo_optimize_article(article, llm, prompt):
    formatted_prompt_seo=prompt.format(original_article=article)
    # print(formatted_prompt_seo)
    response=llm.invoke(formatted_prompt_seo)
    # print("length of response after invoking the model is=", len(response))
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
        response=llm.predict(formatted_prompt_image)
        return response

#-----------------------------OpenAI--------------------------------------------------------

def init_OpenAI_llm(openai_key):
    llm=OpenAI(model_name="gpt-3.5-turbo-instruct",temperature=0.55, openai_api_key=openai_key,verbose=True, max_tokens=2000)
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
        quality="standard",
        n=2,
        response_format="url")
    return response.data[0].url, response.data[1].url


def making_img_list(img_url1, img_url2 ):
    img_list=[]
    cloudin_upload1=cloudinary.uploader.upload(img_url1)
    img_list.append(cloudin_upload1['url'])
    cloudin_upload2=cloudinary.uploader.upload(img_url2)
    img_list.append(cloudin_upload2['url'])
    return img_list



#-------------------------------------API Keys Verification----------------------------------------
def openAI_api_key_valid(openAI_api_key):
    try:
        llm=OpenAI(model_name="gpt-3.5-turbo-instruct", openai_api_key=openAI_api_key, max_tokens=3 )
        response = llm.invoke("hi")
    except Exception as e:
        return "wrong key"
    else:
        return True
    

def google_api_key_valid(google_ki_api_key):
    try:
        llm=GoogleGenerativeAI(model="gemini-pro",google_api_key=google_ki_api_key,max_retries=0)
        response = llm.invoke("hi")
    except Exception as e:
        return "wrong key"
    else:
        return True


