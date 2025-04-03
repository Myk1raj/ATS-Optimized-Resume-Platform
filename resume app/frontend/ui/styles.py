# frontend/ui/styles.py
import streamlit as st

def apply_styles():
    """Apply custom CSS styles to the Streamlit app"""
    st.set_page_config(page_title="Resume Crafter", page_icon="📄", layout="wide")
    
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #1E0F4B 0%, #2D1B69 50%, #451F98 100%);
            color: white;
        }
        .stButton > button {
            background: linear-gradient(90deg, #8B7FD3 0%, #9B8FE3 100%);
            color: white;
            border-radius: 20px;
            padding: 10px 30px;
            border: none;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(139, 127, 211, 0.2);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(139, 127, 211, 0.3);
        }
        .stTextInput > div > div > input, .stTextArea textarea {
            background: rgba(255, 255, 255, 0.05);
            color: white;
            border-radius: 15px;
            border: 1px solid rgba(139, 127, 211, 0.3);
            backdrop-filter: blur(10px);
        }
        .upload-section {
            text-align: center;
            padding: 40px;
            border: 2px dashed rgba(139, 127, 211, 0.5);
            border-radius: 20px;
            margin: 20px 0;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.1) 100%);
            backdrop-filter: blur(10px);
        }
        .resume-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.1) 100%);
            padding: 25px;
            border-radius: 20px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        .resume-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        .form-like {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.1) 100%);
            padding: 30px;
            border-radius: 20px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        .download-button {
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(90deg, #8B7FD3 0%, #9B8FE3 100%);
            color: white;
            text-decoration: none;
            border-radius: 20px;
            margin: 10px 0;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(139, 127, 211, 0.2);
            width: 100%;
            text-align: center;
        }
        .download-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(139, 127, 211, 0.3);
            color: white;
        }
        .section-header {
            background: linear-gradient(90deg, #8B7FD3 0%, #9B8FE3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
        }
        div[data-baseweb="tab-list"] {
            gap: 10px;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 10px;
        }
        button[role="tab"] {
            flex: 1;
            padding: 10px;
            background-color: transparent !important;
            color: white !important;
            border-radius: 10px !important;
        }
        button[role="tab"][data-baseweb="tab"] {
            background-color: rgba(139, 127, 211, 0.3) !important;
        }
        h1, h2, h3 {
            color: white;
        }
        .gradient-text {
            background: linear-gradient(90deg, #8B7FD3 0%, #9B8FE3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)