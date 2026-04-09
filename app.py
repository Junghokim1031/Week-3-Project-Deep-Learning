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

import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
import io

#import ssl/
# This bypasses the certificate verification
# ssl._create_default_https_context = ssl._create_unverified_context

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
    model = tf.saved_model.load('./model/my_model_folder')
    return model

model = load_assets()

#==================
# Pubmed 논문 가져오기
#==================

def remove_stopwords(text):
    if not text: return ""
    # 공백 기준으로 단어 분리
    words = text.split()
    # 불용어 제거 (소문자로 비교하여 필터링)
    filtered_words = [w for w in words if w.lower() not in stop_words]
    return " ".join(filtered_words)

def model_predict(text_string):
    text_string = text_string.lower()
    text_string = remove_stopwords(text_string)
    
    # 1. 텐서 변환
    input_tensor = tf.constant([text_string])
    
    # 2. SavedModel의 기본 시그니처(serve)를 호출
    # 모델을 직접 호출하는 대신, .serve() 메서드를 사용합니다.
    predictions = model.serve(input_tensor)
    
    # 3. 결과값 추출
    if isinstance(predictions, dict):
        output_key = list(predictions.keys())[0]
        score = float(predictions[output_key][0][0])
    else:
        score = float(predictions[0][0])
        
    return score

#==================
# 메인 화면 구성
#==================
st.title("Pubmed 폐 관련 논문 분석")
title = st.text_input("제목")
abstract = st.text_input("초록")
Content = title + ": " + abstract

if st.button('논문 분석'):
    if Content.strip() == ":":
        st.warning("분석할 제목이나 초록을 입력해주세요.")
    else:
        score = model_predict(Content)
        st.write(f"분석 점수: **{score:.4f}**")