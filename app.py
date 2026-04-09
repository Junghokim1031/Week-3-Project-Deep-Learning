import streamlit as st

# ENV
from dotenv import load_dotenv
import os

# Model
import tensorflow as tf

# Pubmed Entrez
from Bio import Entrez

# Data
import pandas as pd
import numpy as np
import joblib
import nltk
from nltk.corpus import stopwords

#==================
# Pubmed에 필요한 email 입력
#==================
load_dotenv()
email = os.getenv("EMAIL")

#==================
# 기초 페이지 설정
#==================
st.set_page_config(
    page_title='Pubmed 폐 관련 논문 분석',
    page_icon='🧠',
    layout='wide'
)


#==================
# 모델
#==================
@st.cache_resource
def load_assets():
    model = tf.keras.models.load_model('./model/my_model.keras')
    return model

model = load_assets()


#==================
# 사이드바 입력
#==================
def user_input_features():
    st.sidebar.markdown("### 폐 관련 논문 분석")
    pubmed_id = st.sidebar.text_input("Pubmed ID", "")

    # 1. Provide a fallback email
    Entrez.email = "your_email@example.com" 

    # 2. Only run if the user has actually typed something
    if pubmed_id:
        try:
            # 3. Use retmode="xml" so Entrez.read() can parse it
            handle = Entrez.efetch(db="pubmed", id=pubmed_id, retmode="xml")
            record = Entrez.read(handle)
            handle.close()
            data = pd.DataFrame(record)
            return data
        except Exception as e:
            st.sidebar.error(f"Error fetching data: {e}")
            return None
    
    return None


#==================
# 메인 화면 구성
#==================
# The title and abstract of the Pubmed Article
st.title("Pubmed 폐 관련 논문~ 분석")
if(st.button('논문 분석')):
    data = user_input_features()
    if data is not None:
        st.subheader(data['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle'])
        st.write(data['PubmedArticle'][0]['MedlineCitation']['Article']['Abstract']['AbstractText'])
