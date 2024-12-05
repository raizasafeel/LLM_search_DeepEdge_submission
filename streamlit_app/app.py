"""
Streamlit application for RAG-based search.
"""

import streamlit as st
import requests
import time

def search_api(query: str) -> str:
    """
    Send search query to Flask backend and retrieve answer.
    
    Args:
        query (str): User's search query.
    
    Returns:
        str: Generated answer or error message.
    """
    flask_url = "http://localhost:5001/query"
    
    try:
        # Make a POST request to the Flask API
        response = requests.post(flask_url, json={"query": query})
        
        # Handle the response from Flask
        if response.status_code == 200:
            return response.json().get("answer", "No answer received.")
        else:
            error_message = response.json().get("error", "Unknown error occurred.")
            st.error(f"Error: {response.status_code} - {error_message}")
            return None
    
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

def main() -> None:
    """
    Main Streamlit application function.
    Handles UI and search functionality.
    """
    st.title("LLM-based RAG Search")

    # Input for user query
    query = st.text_input("Enter your query:")

    if st.button("Search"):
        if not query.strip():
            st.error("Please enter a query.")
        else:
            # Add a loading spinner
            with st.spinner('Searching and generating answer...'):
                answer = search_api(query)
                
                if answer:
                    st.write("Answer:", answer)

if __name__ == "__main__":
    main()