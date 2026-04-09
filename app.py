import streamlit as st
import tensorflow as tf
import nltk

# 1. Setup Page Config first
st.set_page_config(
    page_title='Pubmed 폐 관련 논문 분석',
    page_icon='🧠',
    layout='wide'
)

# 2. Define a single initialization function for NLTK
@st.cache_resource
def initialize_nltk():
    # This ensures downloads happen before we try to use them
    nltk.download('stopwords')
    nltk.download('punkt')
    from nltk.corpus import stopwords
    return set(stopwords.words('english'))

# 3. Initialize stopwords globally (but safely via the cached function)
stop_words = initialize_nltk()

# 4. Load Model
@st.cache_resource
def load_assets():
    # Ensure your model path is correct relative to your app root
    model = tf.saved_model.load('./model/my_model_folder')
    return model

model = load_assets()

# 5. Helper Functions
def remove_stopwords(text):
    if not text: return ""
    words = text.split()
    # Now stop_words is guaranteed to be loaded
    filtered_words = [w for w in words if w.lower() not in stop_words]
    return " ".join(filtered_words)

def model_predict(text_string):
    text_string = text_string.lower()
    text_string = remove_stopwords(text_string)
    
    input_tensor = tf.constant([text_string])
    predictions = model.serve(input_tensor)
    
    if isinstance(predictions, dict):
        output_key = list(predictions.keys())[0]
        score = float(predictions[output_key][0][0])
    else:
        score = float(predictions[0][0])
        
    return score

# 6. Main UI
st.title("Pubmed 폐 관련 논문 분석")
title = st.text_input("제목")
abstract = st.text_area("초록") # Changed to text_area for better UX
content = f"{title}: {abstract}"

if st.button('논문 분석'):
    if not title.strip() and not abstract.strip():
        st.warning("분석할 제목이나 초록을 입력해주세요.")
    else:
        with st.spinner('분석 중...'):
            score = model_predict(content)
            st.success(f"분석 완료!")
            st.metric(label="분석 점수", value=f"{score:.4f}")