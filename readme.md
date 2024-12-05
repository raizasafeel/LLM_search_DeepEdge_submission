# LLM-based RAG (Retrieval-Augmented Generation) Search Application

## Project Overview
This is a web application that leverages Retrieval-Augmented Generation (RAG) to provide intelligent, context-aware search results. The application uses a combination of web scraping, search APIs, and large language models to generate informative answers to user queries.

## Key Features
- Web-based search interface using Streamlit
- Backend Flask API for processing queries
- Article retrieval using Serper API
- Web content scraping
- Answer generation using Google Gemini AI
- Modular architecture with separate components for search, content fetching, and answer generation

## Technologies Used
- Python
- Streamlit (Frontend)
- Flask (Backend)
- LangChain
- Google Serper API
- Google Gemini AI
- BeautifulSoup (Web Scraping)
- python-dotenv (Environment Variable Management)

## Prerequisites
- Python 3.8+
- API Keys:
  1. Serper API Key
  2. Google Gemini API Key

## Setup and Installation

1. Download the zip file and make a copy of it
2. Create a Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```
3. Install Dependencies
bashCopypip install -r requirements.txt
4. Obtain API Keys
   Serper API Key:
   - Visit Serper.dev
   - Sign up for an account
   - Get your API key from the dashboard
   Google Gemini API Key:
   - Go to Google AI Studio
   - Create an API key for the Gemini model
5. Configure Environment Variables
- Replace .env file in the flask_app directory with your API keys:
   SERPER_API_KEY=your_serper_api_key_here
   GOOGLE_API_KEY=your_googlr_api_key_here

## Running the Application

1. Start the Flask Backend: 
- Navigate to the flask_app directory and run:
```
python app.py
```
- The backend will start on http://localhost:5001
2. Start the Streamlit Frontend
- In a separate terminal, navigate to the streamlit_app directory and run:
```
streamlit run app.py
```
The frontend will open in your default web browser

## Project Structure

```
Copyproject_root/
│
├── flask_app/
│   ├── app.py           # Flask backend application
│   ├── utils.py         # Utility functions for search and generation
│   └── .env             # Environment variables (not tracked in version control)
│
└── streamlit_app/
    └── app.py           # Streamlit frontend application
```

### How It Works

- User enters a query in the Streamlit interface
- The query is sent to the Flask backend
- The backend uses Serper API to search for relevant articles
- Articles are fetched and their content is scraped
- Google Gemini AI generates a comprehensive answer based on the retrieved content
- The answer is displayed in the Streamlit interface

### Customization

- Adjust temperature and other parameters in generate_answer() function to modify AI response characteristics
- Modify search parameters in search_articles() function to change article retrieval behavior

### Troubleshooting

- Ensure all API keys are correctly set in the .env file
- Check internet connectivity
- Verify that all dependencies are installed
- Make sure no other applications are using ports 5001 (Flask) or 8501 (Streamlit)