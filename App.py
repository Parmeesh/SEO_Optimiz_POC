import streamlit as st
import streamlit.components.v1 as components
import time
import pandas as pd
import os
from dotenv import load_dotenv
import subprocess

from Functions import *

load_dotenv()

if "original_article" not in st.session_state:
    st.session_state["original_article"] = []

if "original_metadata" not in st.session_state:
    st.session_state["original_metadata"] = []

if "optimized_article" not in st.session_state:
    st.session_state["optimized_article"] = []

if "new_metadata" not in st.session_state:
    st.session_state["new_metadata"] = []

if "input_tokens" not in st.session_state:
    st.session_state["input_tokens"] = []

if "output_tokens" not in st.session_state:
    st.session_state["output_tokens"] = []

if "callback_openAI" not in st.session_state:
    st.session_state["callback_openAI"] = []

if "title_from_html_gemini" not in st.session_state:
    st.session_state["title_from_html_gemini"]=[]

if "title_from_html_openai" not in st.session_state:
    st.session_state["title_from_html_openai"]=[]

if "google_api_key" not in st.session_state:
    st.session_state["google_api_key"]=[]

if "openAI_api_key" not in st.session_state:
    st.session_state["openAI_api_key"]=[]

if "final_html_with_img_gemini" not in st.session_state:
    st.session_state["final_html_with_img_gemini"]=[]

if "count_input" not in st.session_state:
    st.session_state["count_input"]=[]

if "count_output" not in st.session_state:
    st.session_state["count_output"]=[]

if "final_html_with_img_openai" not in st.session_state:
    st.session_state["final_html_with_img_openai"]=[]

if "editor_key" not in st.session_state:
    st.session_state['editor_key']=[]

st.set_page_config(page_title="SEO Optimizer", layout="wide")
st.header(":blue[Article Generation 📋]")
local_css("style.css")
sidebar=st.sidebar.image("https://ispoc.impressicocrm.com/images/ibs-logo-big.png")

llm_options=["Gemini", "OpenAI"]
sidebar_selectbox=st.sidebar.selectbox(label="Select the model type you wish to use", options=llm_options)
    
sidebar_api_key_form=st.sidebar.form(key="api_form", clear_on_submit=False)
with sidebar_api_key_form:
    st.header("Configure API Keys for the Following Models")
    google_key=st.text_input(label="Google API Key", type='password')
    openai_key=st.text_input(label="OpenAI API Key", type='password')
    form_submit=st.form_submit_button(label="Configure")
    if form_submit:
        st.session_state["google_api_key"]=google_key
        if google_api_key_valid(st.session_state["google_api_key"])==True:
            st.toast(body="Google API Key Verified", icon="✅")
        else:
            st.toast(body="Google API Key Invalid", icon="❌")
            st.session_state["google_api_key"]=[]
        st.session_state["openAI_api_key"]=openai_key
        if openAI_api_key_valid(st.session_state["openAI_api_key"])==True:
            st.toast(body="OpenAI API Key Verified", icon="✅")
        else:
            st.toast(body="OpenAI API Key Invalid", icon="❌")
            st.session_state["openAI_api_key"]=[]
        time.sleep(5)
        st.experimental_rerun()

#---------------------------------------GEMINI------------------------------------------------------------------

if sidebar_selectbox=="Gemini":
    Tab1, Tab2, Tab3 = st.tabs(['SEO Optmization','Image Generation', 'Editor'])
    with Tab1:
        _container_=st.container()
        with _container_:
            colum=st.columns([2,7,1])
            with colum[0]:
                st.image("https://media.licdn.com/dms/image/D4D12AQEbzFbpNTU-rQ/article-cover_image-shrink_720_1280/0/1701947391966?e=2147483647&v=beta&t=4nVhyq0JzWoFbb3q_rC3nGwtWdYZQ1K0GJsCkRETDek")
            with colum[2]:
                reset_button=st.button(label="Reset")
        if reset_button:
            st.session_state["original_article"] = []
            st.session_state["original_metadata"] = []
            st.session_state["optimized_article"] = []
            st.session_state["new_metadata"] = []
            st.session_state["input_tokens"] = []
            st.session_state["output_tokens"] = []
        
        st.markdown(body="Optimize your article's online visibility with this Tab. Simply provide the URL of your article, and it'll analyze, enhance, and generate SEO-optimized HTML content using Google's Gemini-Pro.")
        article_url=st.text_input(label="Enter the URL of your article for SEO optimization:", placeholder="https://example.com/article")
        submit_button=st.button(label="Optimize")
        if article_url and submit_button:
            if st.session_state["google_api_key"]==[]:
                st.error(body="Google API Key Required", icon="🚨")
            else:
                llm=init_Gemini_llm(str(st.session_state["google_api_key"]))
                
                my_bar=st.progress(0)
                with st.spinner("In progress....."):
                    for percent_complete in range(0,25):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete+1, text="Fetching content from Article.....")
                    st.session_state["original_article"], st.session_state["original_metadata"], orig_article_title=fetch_article(url=article_url)
                    print("title=",orig_article_title)
                    print("original_article_sessionstate=", st.session_state['original_article'])
                    print("type of st.sessionstate.original_article=", type(st.session_state['original_article']))
                    url_=get_url_top1_searches(orig_article_title)
                    print("url list=",url_)
                    art_text=get_text(url_)
                    keyword_list=get_keywords(llm=llm, article_text=art_text)
                    print(keyword_list)
                    print("type of keyword list=", type(keyword_list))
                    # print("Original Article looks like this-", st.session_state['original_article'])
                    for percent_complete in range(25,50):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete+1, text="SEO Optimizing the Article.....")
                    optimized_article_string=seo_optimize_article(article=st.session_state["original_article"],keyword_list=keyword_list, llm=llm, prompt=prompt_gemini_seo)
                    st.session_state["optimized_article"]=optimized_article_string.strip()[7:-3].strip()
                    print("optimized Article is-",st.session_state["optimized_article"])

                    for percent_complete in range(50,75):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete+1, text="Generating new Metadata.....")
                    st.session_state["new_metadata"], st.session_state["title_from_html_gemini"]=generate_new_article_metadata(str(st.session_state["optimized_article"]))
                    print("title to be given for image generation is",st.session_state["title_from_html_gemini"])

                    for percent_complete in range(75,100):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete+1, text="Process Completed")

                    st.success(body="Article Optimization successfull", icon="✅")
                st.markdown("---")
                container1=st.container()
                with container1:
                    st.header("Original Article", divider="rainbow")
                    cols=st.columns([3,1])
                    with cols[0]:
                        st.write(st.session_state['original_article'])
            
                    with cols[1]:
                        st.write(st.session_state["original_metadata"])
                st.markdown('---')
                container2=st.container()
                
                with container2:
                    st.header("Optimized Article", divider="rainbow")
                    components.html(html=str(st.session_state["optimized_article"]), height=600, scrolling=True)
                st.markdown('---')
                container3=st.container()
                with container3:
                    st.header("Optimized Article HTML and Metadata", divider="rainbow")
                    columns=st.columns([3,1])
                    with columns[0]:
                        st.markdown(
                            f"""
                            <style>
                            .stCodeBlock {{
                                height: 600px;
                                overflow-y: scroll;
                            }}
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
                        st.code(st.session_state['optimized_article'], language='html',line_numbers=True)
                    with columns[1]:
                        st.write(st.session_state["new_metadata"])
                st.markdown('---')


    with Tab2:
        st.header("Image generation Tab")
        st.markdown("Explore creative possibilities by leveraging DALL-E-2 to generate compelling images. Simply initiate the process by pressing the button, and seamlessly integrate the generated images into your optimized article.")
        gen_im=st.button(label="Generate")
        if gen_im:
            if st.session_state["openAI_api_key"]==[]:
                st.error(body="OpenAI API Key is Required", icon="🚨")
            else:
                my_pbar=st.progress(0)
                with st.spinner("In progress....."):
                    for percent_complete in range(25):
                        time.sleep(0.01)
                        my_pbar.progress(percent_complete+1, text="Initializing cloudinary.....")
                    init_cloudinary(cl_api=os.environ['CLOUDINARY_API_KEY'],cl_secret=os.environ['COUDINARY_API_SECRET'], cl_cloudname=os.environ['CLOUDINARY_CLOUD_NAME'])
                    llm=init_Gemini_llm(googlekey=str(st.session_state["google_api_key"]))
                    for percent_complete in range(25,50):
                        time.sleep(0.01)
                        my_pbar.progress(percent_complete+1, text="Initializing DallE-2.....")
                    image_llm =opAI(api_key=str(st.session_state['openAI_api_key']))
                    if st.session_state["optimized_article"]==[]:
                        c=st.columns([1,6,1])
                        with c[1]:
                            st.image("Error404.png")
                        st.error("Error 404: No Data Found. Please navigate to First tab and upload the corresponding article URL for further processing.",icon="🚨")
                    else:
                        for percent_complete in range(50,75):
                            time.sleep(0.01)
                            my_pbar.progress(percent_complete+1, text="Generating Images.....")
                        IMG_URL1, IMG_URL2=generate_images(llm=image_llm,title=str(st.session_state["title_from_html_gemini"]))
                        print("image generated")
                        print("IMG_URL1=", IMG_URL1)
                        print("IMG_URL2=", IMG_URL2)

                        img_list=making_img_list(img_url1=IMG_URL1, img_url2=IMG_URL2)
                        print("image lis is generated")
                        for percent_complete in range(75,99):
                            time.sleep(0.01)
                            my_pbar.progress(percent_complete+1, text="Generating HTML with images.....")
                        st.session_state["final_html_with_img_gemini"]=generate_HTML_with_image_gemini(llm,html_article=st.session_state["optimized_article"], img_list=img_list, prompt_image_gen=prompt_image_gen)
                        for percent_complete in range(99,100):
                            time.sleep(0.01)
                            my_pbar.progress(percent_complete+1, text="Process Completed.....")
                        st.success(body="Images Generated and added to the Optimized Article",icon="✅")
                        st.header(body="Optimized Article", divider="rainbow")
                        colus=st.columns([1,1])
                        with colus[0]:
                            st.markdown(
                            f"""
                            <style>
                            .stCodeBlock {{
                                height: 600px;
                                overflow-y: scroll;
                            }}
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
                            st.code(st.session_state["optimized_article"], language='html', line_numbers=True)

                        with colus[1]:
                            components.html(html=st.session_state["optimized_article"], height=600, scrolling=True)
                        st.markdown("---")

                        st.header(body="Final SEO Optimized Article with Generated Images", divider="rainbow")
                        cos=st.columns([1,1])
                        with cos[0]:
                            st.markdown(
                            f"""
                            <style>
                            .stCodeBlock {{
                                height: 600px;
                                overflow-y: scroll;
                            }}
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
                            st.code(st.session_state["final_html_with_img_gemini"], language='html', line_numbers=True)
                        with cos[1]:
                            components.html(html=str(st.session_state["final_html_with_img_gemini"]), height=600, scrolling=True)
                        st.markdown("---")



    with Tab3:
        import subprocess as sp
        print(st.session_state['final_html_with_img_gemini'])
        st.header('Editor Window to make manual changes')
        editor_key=st.text_input(label="Enter the API Key of TinyMCE Editor for initializing your WYSWYG Editor-", type='password')
        editorButton=st.button(label='Start')
        if editor_key and editorButton:
            st.session_state['editor_key']=editor_key
            with st.spinner(text="Initializing WYSWYG Editor....."):
                
                # proc = subprocess.Popen(["python", "editor.py"])
                extProc = sp.Popen(['python','editor.py']) 
                time.sleep(30)
                payload = {"content": st.session_state['final_html_with_img_gemini']}
                response = requests.post('http://localhost:3002/get-html-content',json=payload)
                print(response)
                if response.ok:
                    response_data= response.json()
                else:
                    st.error('Failed to send data')
                    sp.Popen.terminate(extProc)
                editor_html_template1='''<!DOCTYPE html>
                                <html>
                                <head>
                                    <title>WYSWYG Editor</title>
                                    <script src="https://cdn.tiny.cloud/1/'''
                editor_html_template2='''/tinymce/6/tinymce.min.js" referrerpolicy="origin"></script>
                                    <script>
                                document.addEventListener('DOMContentLoaded', function() {
                                    fetch('http://localhost:3002/content-flask', {
                                            method: 'POST', // Specify the method
                                            headers: {
                                                'Content-Type': 'application/json', // Ensure correct content type
                                            }
                                        })
                                        .then(response => response.json()) // Corrected part
                                        .then(data => {
                                            tinymce.init({
                                                height:700,
                                                selector: '#myEditor',
                                                plugins: 'a11ychecker advcode casechange formatpainter linkchecker autolink lists checklist media mediaembed pageembed permanentpen powerpaste table advtable tinycomments tinymcespellchecker',
                                                tinycomments_mode: 'embedded',
                                                tinycomments_author: 'Author name',
                                                setup: function (editor) {
                                                editor.ui.registry.addButton('downloadButton', {
                                                    text: 'Download 📥',
                                                    onAction: function () {
                                                        var content = editor.getContent();
                                                        fetch('http://localhost:3002/download-html-content', {
                                                            method: 'POST',
                                                            body: JSON.stringify({ content: content }),
                                                            headers: {
                                                                'Content-Type': 'application/json',
                                                            },
                                                        }).then(response => {
                                                            if (response.ok) {
                                                                response.blob().then(blob => {
                                                                    var url = window.URL.createObjectURL(blob);
                                                                    var a = document.createElement('a');
                                                                    a.href = url;
                                                                    a.download = 'document.docx';
                                                                    document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
                                                                    a.click();    
                                                                    a.remove();
                                                                }
                                                            });
                                                        }
                                                    });
                                                    editor.on('init', function () {
                                                        editor.setContent(data.content); // Corrected part
                                                    });
                                                },
                                                toolbar: 'saveButton |undo redo| bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pageembed | charmap emoticons | fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | a11ycheck ltr rtl | showcomments addcomment '
                                            });
                                        });
                                });
                                </script>

                                </head>
                                <body>
                                <h2>Article Editor</h2>
                                <textarea id="myEditor"></textarea>
                                </body>
                                </html>'''
                st.markdown('---')
                components.html(html=(editor_html_template1+st.session_state['editor_key']+editor_html_template2), height=800, scrolling=True)
                st.markdown('---')



#----------------------------------------------OPENAI--------------------------------------------------------
else:
    Tab1, Tab2 = st.tabs(['SEO Optmization','Image Generation'])
    with Tab1:
        container_=st.container()
        with container_:
            colum=st.columns([2,7,1])
            with colum[0]:
                st.image("data:image/png;base64,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")
            with colum[2]: 
                reset_button=st.button(label="Reset")
                if reset_button:
                    st.session_state["original_article"] = []
                    st.session_state["original_metadata"] = []
                    st.session_state["optimized_article"] = []
                    st.session_state["new_metadata"] = []
                    st.session_state["callback_openAI"] = []

        st.markdown(body="Optimize your article's online visibility with this Tab. Simply provide the URL of your article, and it'll analyze, enhance, and generate SEO-optimized HTML content using OpenAI's GPT-3.5 Turbo.")
        article_url=st.text_input(label="Enter the URL of your article for SEO optimization:", placeholder="https://example.com/article")
        submit_button=st.button(label="Optimize")

        if article_url and submit_button:
            if st.session_state["openAI_api_key"]==[]:
                st.error(body="OpenAI API Key Required", icon="🚨")
            else:
                llm=init_OpenAI_llm(str(st.session_state["openAI_api_key"]))
                my_bar=st.progress(0)
                with st.spinner("In progress....."):
                    for percent_complete in range(0,25):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete+1, text="Fetching Content from Article.....")
                    st.session_state["original_article"], st.session_state["original_metadata"]=fetch_article(url=article_url)

                    for percent_complete in range(25,50):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete+1, text="SEO Optimizing the Article.....")
                    st.session_state["optimized_article"], st.session_state["callback_openAI"]=seo_optimize_article_Openai(article=st.session_state["original_article"], llm=llm, prompt=prompt_openai_seo)
                    print(st.session_state["callback_openAI"])

                    for percent_complete in range(50,75):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete+1, text="Generating New Metadata.....")
                    st.session_state["new_metadata"], st.session_state["title_from_html_openai"]=generate_new_article_metadata_openai(st.session_state["optimized_article"])
                    print(st.session_state["title_from_html_openai"])
                    
                    for percent_complete in range(75,99):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete+1, text="Calculatimg Cost...")
                    cost_data = [line.split(": ") for line in str(st.session_state["callback_openAI"]).strip().split("\n")]
                    cost_table=pd.DataFrame(cost_data, columns=['Metric','Value'])

                    for percent_complete in range(99,100):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete+1, text="Process Completed")

                    st.success(body="Article Optimization Successfull", icon="✅")
                st.markdown('---')
                container1=st.container()
                with container1:
                    st.header("Original Article", divider="rainbow")
                    cols=st.columns([3,1])
                    with cols[0]:
                        st.write(st.session_state["original_article"])
                    with cols[1]:
                        st.write(st.session_state["original_metadata"])
                st.markdown('---')
                OpenAIcontainer2=st.container()
                with OpenAIcontainer2:
                    st.header("Optimized Article", divider="rainbow")
                    components.html(st.session_state["optimized_article"], height=600, scrolling=True)

                st.markdown('---')
                container3=st.container()
                with container3:
                    st.header("Optimized Article HTML and Metadata", divider="rainbow")
                    columns=st.columns([3,1])
                    with columns[0]:
                        st.markdown(
                            f"""
                            <style>
                            .stCodeBlock {{
                                height: 600px;
                                overflow-y: scroll;
                            }}
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
                        st.code(st.session_state['optimized_article'], language='html', line_numbers=True)
                       
                    with columns[1]:
                        st.write(st.session_state["new_metadata"])

                st.markdown('---')
                st.header(body="Cost Analysis", divider="rainbow")
                st.table(cost_table)
                st.markdown('---')

    with Tab2:
        st.header("Image generation Tab")
        st.markdown("Explore creative possibilities by leveraging DALL-E-2 to generate compelling images. Simply initiate the process by pressing the button, and seamlessly integrate the generated images into your optimized article.")
        gen_im=st.button(label="Generate")
        if gen_im:
                progress_bar=st.progress(0)
                with st.spinner("In progress....."):
                    for percent_complete in range(0,25):
                        time.sleep(0.01)
                        progress_bar.progress(percent_complete+1, text="Initializing Cloudinary.....")
                    init_cloudinary(cl_api=os.environ['CLOUDINARY_API_KEY'],cl_secret=os.environ['COUDINARY_API_SECRET'], cl_cloudname=os.environ['CLOUDINARY_CLOUD_NAME'])
                    llm=init_OpenAI_llm(openai_key=str(st.session_state["openAI_api_key"]))
                    
                    for percent_complete in range(25,50):
                        time.sleep(0.01)
                        progress_bar.progress(percent_complete+1, text="Initializing DallE-2.....")
                    image_llm = opAI(api_key=str(st.session_state['openAI_api_key']))
                    if st.session_state["optimized_article"]==[]:
                        co=st.columns([1,6,1])
                        with co[1]:
                            st.image("Error404.png")
                        st.error("Error 404: No Data Found. Please navigate to First tab and upload the corresponding article URL for further processing.",icon="🚨")
                        
                    else:
                        for percent_complete in range(50,75):
                            time.sleep(0.01)
                            progress_bar.progress(percent_complete+1, text="Generating Images.....")
                        IMG_URL1, IMG_URL2=generate_images(llm=image_llm,title=st.session_state["title_from_html_openai"])
                        print("image generated")
                        print("IMG_URL1=", IMG_URL1)
                        print("IMG_URL2=", IMG_URL2)

                        img_list=making_img_list(img_url1=IMG_URL1, img_url2=IMG_URL2)
                        print("image list is generated")
                        for percent_complete in range(75,99):
                            time.sleep(0.01)
                            progress_bar.progress(percent_complete+1, text="Generating HTML with images.....")
                        st.session_state["final_html_with_img_openai"], cb=generate_HTML_with_image_openai(llm,html_article=st.session_state["optimized_article"], img_list=img_list, prompt_image_gen=prompt_image_gen)
                        for percent_complete in range(99,100):
                            time.sleep(0.01)
                            progress_bar.progress(percent_complete+1, text="Process Completed.....")
                        st.success(body="Images generated and added to the Optimized Article",icon="✅")
                        st.header(body="Optimized Article", divider="rainbow")
                        colu=st.columns([1,1])
                        with colu[0]:
                            st.markdown(
                            f"""
                            <style>
                            .stCodeBlock {{
                                height: 600px;
                                overflow-y: scroll;
                            }}
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
                            st.code(st.session_state["optimized_article"], language='html', line_numbers=True)
                        with colu[1]:
                            components.html(st.session_state["optimized_article"], height=600, scrolling=True)
                        st.markdown("---")

                        st.header(body="Final SEO Optimized Article with generated Images", divider="rainbow")
                        co=st.columns([1,1])
                        with co[0]:
                            st.markdown(
                            f"""
                            <style>
                            .stCodeBlock {{
                                height: 600px;
                                overflow-y: scroll;
                            }}
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
                            st.code(st.session_state["final_html_with_img_openai"], language='html', line_numbers=True)
                        with co[1]:
                            components.html(st.session_state["final_html_with_img_openai"], height=600, scrolling=True)
                        st.markdown("---")

                        cost_data_=[line.split(": ") for line in str(st.session_state["callback_openAI"]).strip().split("\n")]
                        cost_data_.append(["Cost of Image Generation (USD)", "$0.036"])
                        costTable=pd.DataFrame(cost_data_, columns=["Metric", "Value"])
                        st.header(body="Cost Analysis", divider="rainbow")
                        st.table(costTable)
                        st.markdown("---")





