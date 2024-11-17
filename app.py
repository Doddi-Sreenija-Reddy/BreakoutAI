import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from io import StringIO
import os
from dotenv import load_dotenv
import requests
import groq
from typing import List, Dict, Optional
import time  
load_dotenv()

class APIClients:
    """Handles API client initialization and configuration."""    
    def __init__(self):
        self.groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.serpapi_key = os.getenv("SERPAPI_API_KEY")

class WebSearcher:
    """Handles web search operations using SerpAPI."""    
    def __init__(self, serpapi_key: str):
        self.serpapi_key = serpapi_key
    
    def search(self, entity: str, prompt: str) -> str:
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": prompt.format(entity=entity),
                "api_key": self.serpapi_key,
                "num": 5
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            results = response.json().get("organic_results", [])
            
            snippets = [result.get("snippet", "") for result in results]
            return "\n".join(snippets)
        except requests.exceptions.RequestException as e:
            st.sidebar.error(f"Error during web search: {str(e)}")
            return ""

class LLMProcessor:
    """Handles LLM-based information extraction using Groq."""    
    def __init__(self, groq_client):
        self.groq_client = groq_client
    
    def extract_information(self, entity: str, prompt: str, search_results: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that extracts specific information from web search results."},
            {"role": "user", "content": f"Extract information from the following search results based on the prompt: '{prompt.format(entity=entity)}'\n\nSearch Results:\n{search_results}\n\nExtracted Information:"}
        ]
        try:
            response = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                max_tokens=150,
                temperature=0.5,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            st.sidebar.error(f"Error during LLM extraction: {str(e)}")
            return ""

class DataProcessor:
    """Handles data processing operations."""    
    def __init__(self, web_searcher: WebSearcher, llm_processor: LLMProcessor):
        self.web_searcher = web_searcher
        self.llm_processor = llm_processor
    
    def process_entities(self, entities: List[str], prompt: str) -> List[Dict[str, str]]:
        results = []
        num_entities = len(entities)
        
        for idx, entity in enumerate(entities):
            st.progress((idx + 1) / num_entities)
            search_results = self.web_searcher.search(entity, prompt)
            if search_results:
                extracted_info = self.llm_processor.extract_information(entity, prompt, search_results)
                results.append({"Entity": entity, "Extracted Information": extracted_info})
            else:
                results.append({"Entity": entity, "Extracted Information": "No data found"})
            time.sleep(0.5)
        
        return results

class DataLoader:
    """Handles data loading from different sources."""    
    @staticmethod
    def load_csv(uploaded_file) -> Optional[pd.DataFrame]:
        try:
            csv_data = uploaded_file.read().decode("utf-8")
            return pd.read_csv(StringIO(csv_data))
        except Exception as e:
            st.sidebar.error(f"Error reading CSV file: {str(e)}")
            return None
    
    @staticmethod
    def load_google_sheet(sheet_url: str) -> Optional[pd.DataFrame]:
        try:
            creds = Credentials.from_service_account_file(
                "credentials.json",
                scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            client = gspread.authorize(creds)
            sheet = client.open_by_url(sheet_url).sheet1
            data = sheet.get_all_values()
            headers = data.pop(0)
            return pd.DataFrame(data, columns=headers)
        except Exception as e:
            st.sidebar.error(f"Error connecting to Google Sheet: {str(e)}")
            return None

def main():
    """Main application function."""    
    st.set_page_config(page_title="BreakOutAI", layout="wide")
    
    st.markdown("""
        <style>
            body {
                background: linear-gradient(135deg, #6e7dff, #2c3e50);
                font-family: 'Poppins', sans-serif;
                color: #fff;
                animation: backgroundAnimation 10s ease infinite;
            }
            @keyframes backgroundAnimation {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            .stButton > button {
                background-color: #3498db;
                border-radius: 10px;
                color: white;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            .stButton > button:hover {
                background-color: #2980b9;
                transform: scale(1.05);
            }
            .stTextInput input {
                border-radius: 10px;
                padding: 10px;
            }
            .stTextArea textarea {
                border-radius: 10px;
                padding: 10px;
            }
            .stProgress > div {
                background-color: #1abc9c;
            }
            footer {
                font-size: 12px;
                color: #ecf0f1;
                background-color: #2c3e50;
                padding: 10px;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <h1 style="text-align:center; font-family: 'Poppins', sans-serif; animation: fadeIn 2s ease;">
            BreakoutAI
        </h1>
    """, unsafe_allow_html=True)
    
    api_clients = APIClients()    
    web_searcher = WebSearcher(api_clients.serpapi_key)
    llm_processor = LLMProcessor(api_clients.groq_client)
    data_processor = DataProcessor(web_searcher, llm_processor)
    
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'results' not in st.session_state:
        st.session_state.results = None
    
    with st.sidebar:
        st.markdown("<h2 style='color:#4CAF50;'>Data Input</h2>", unsafe_allow_html=True)
        data_source = st.radio("Choose data source:", ("CSV Upload", "Google Sheets"))
    
        if data_source == "CSV Upload":
            uploaded_file = st.file_uploader("Upload CSV file", type="csv")
            if uploaded_file is not None:
                st.session_state.data = DataLoader.load_csv(uploaded_file)
                if st.session_state.data is not None:
                    st.success("CSV file uploaded successfully!")
        else:
            sheet_url = st.text_input("Enter Google Sheet URL")
            if sheet_url:
                st.session_state.data = DataLoader.load_google_sheet(sheet_url)
                if st.session_state.data is not None:
                    st.success("Google Sheet connected successfully!")
    
    if st.session_state.data is not None:
        st.markdown("### Data Preview", unsafe_allow_html=True)
        st.dataframe(st.session_state.data.head(), use_container_width=True)
        
        st.markdown("### Select Primary Column", unsafe_allow_html=True)
        primary_column = st.selectbox(
            "Choose the column containing the entities",
            st.session_state.data.columns,
            key="primary_column"
        )
        
        st.markdown("<h3 style='color:#4CAF50;'>Custom Prompt</h3>", unsafe_allow_html=True)
        custom_prompt = st.text_area(
            "Enter your custom prompt for information extraction",
            "Who is the ceo of {entity}?",
            height=150
        )
        
        with st.container():
            if st.button("Process Data"):
                if primary_column:
                    entities = st.session_state.data[primary_column].dropna().tolist()
                    st.session_state.results = data_processor.process_entities(entities, custom_prompt)
                    st.success(f"Processed {len(st.session_state.results)} entities.")
                else:
                    st.error("Please select a primary column.")

    if st.session_state.results is not None:
        st.markdown("### Results", unsafe_allow_html=True)
        st.write(pd.DataFrame(st.session_state.results).set_index("Entity").style.set_properties(**{'background-color': '#ecf0f1'}))

    if st.session_state.results:
        result_df = pd.DataFrame(st.session_state.results)
        
        # Download results
        csv = result_df.to_csv(index=False)
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="ai_agent_results.csv",
            mime="text/csv"
        )
    else:
        st.info("Please upload a CSV file or connect to a Google Sheet to get started.")
    
    # Add custom styling
    st.markdown("""
    <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            border-radius: 4px;
        }

        .stButton > button:hover {
            background-color: #45a049;
        }

        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
    </style>
    """, unsafe_allow_html=True)
        
    st.markdown("""
        <footer style="text-align:center;padding:10px;background-color:#34495e;color:white;border-radius:5px;">
            <p>Powered by BreakoutAI</p>
        </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()