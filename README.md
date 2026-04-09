# Pubmed 폐 관련 논문 분석 (PubMed Lung Paper Analysis)

This project is a machine learning-based web application built with **Streamlit** and **TensorFlow**. It analyzes medical research papers (from PubMed) related to lung diseases using a deep learning model. The user can input the title and abstract of a paper, and the application will preprocess the text and output an analysis score.

## Features
- **Text Preprocessing:** Automatically removes English stopwords from the input using `nltk` (Natural Language Toolkit) before feeding it into the model.
- **Deep Learning Model:** Utilizes a trained TensorFlow `SavedModel` to analyze the textual content and generate a score.
- **Interactive UI:** Built with Streamlit, providing an easy-to-use interface to analyze the target papers.

## Project Structure
```text
.
├── app.py               # Main Streamlit application file
├── data.ipynb           # Jupyter notebook for data exploration and model training
├── requirements.txt     # Python package dependencies
├── dataset/             # Directory containing the data used for the project
└── model/               # Directory containing the trained TensorFlow model
```

## Setup & Installation

### Prerequisites
Make sure you have Python installed on your system. It's recommended to use a virtual environment.

### 1. Clone the repository or navigate to the project directory
```bash
cd <project-directory>
```

### 2. Install Dependencies
Run the following command to install all required libraries:
```bash
pip install -r requirements.txt
```

*(Note: NLTK stopwords will be automatically downloaded the first time the app is run.)*

## Running the Application

To start the Streamlit application locally, run the following command in your terminal:
```bash
streamlit run app.py
```

The application will open in your default web browser (typically at `http://localhost:8501`). Enter a paper's title and abstract into the respective fields and click **분석 (Analyze)** to see the results.

## Technologies Used
- **Python:** Base programming language
- **Streamlit:** Web application framework
- **TensorFlow:** Deep learning framework
- **NLTK:** Natural language processing library (for stopword removal)
