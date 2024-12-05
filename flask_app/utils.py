"""
Utility module for RAG-based search application.

This module provides functions for searching articles, fetching content, 
and generating answers using Google's Serper API and Gemini LLM.
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()

# API keys
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
LLM_API_KEY = os.getenv("GEMINI_API_KEY")

def process_serper_results(response: Dict) -> List[Dict[str, str]]:
    """
    Converts the Serper API response to a list of dictionaries containing article details.
    
    Args:
        response (dict): The Serper API response.

    Returns:
        list[dict]: A list of processed article data (URL, heading, text).
    """
    results = response.get('organic', [])
    processed_results = [
        {
            "url": result.get("link", ""), 
            "heading": result.get("title", ""), 
            "text": result.get("snippet", "")
        }
        for result in results
    ]
    return processed_results

def search_articles(query: str) -> List[Dict[str, str]]:
    """
    Searches for articles related to the query using Serper API.
    
    Args:
        query (str): The search query.

    Returns:
        list[dict]: A list of articles with URL, heading, and text.
    """
    search = GoogleSerperAPIWrapper()
    results = search.results(query)
    articles = process_serper_results(results)
    return articles

def fetch_article_content(url: str) -> Optional[str]:
    """
    Fetches the article content, extracting headings and text.
    
    Args:
        url (str): The URL of the article to fetch.

    Returns:
        Optional[str]: Extracted content or None if fetching fails.
    """
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
        headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2"]) if h.get_text(strip=True)]
        
        # Combine headings and paragraphs into a single content string
        content = "\n".join(headings + paragraphs)
        return content.strip() or None

    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def concatenate_content(articles: List[Dict[str, str]]) -> str:
    """
    Concatenates the content of the provided articles into a single string.
    
    Args:
        articles (list): List of article dictionaries.

    Returns:
        str: Concatenated content of all articles.
    """
    full_text = ""
    for article in articles:
        # Safely get content, use empty string if None
        content = article.get('content', '') or ''
        full_text += f"{article.get('heading', '')} {article.get('text', '')} {content}\n\n"

    return full_text.strip()

def generate_answer(concatenated_content: str, user_query: str) -> str:
    """
    Generates an answer using the Gemini LLM based on concatenated content and user query.
    
    Args:
        concatenated_content (str): Combined content from searched articles.
        user_query (str): The original user's search query.

    Returns:
        str: Generated answer from the LLM.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    messages = [
        SystemMessage(content="You are a helpful article generator that takes a topic and related content, then generates concise, informative information."),
        HumanMessage(content=f"Topic: {user_query}\n\nContext: {concatenated_content}")
    ]

    output = llm.invoke(messages)
    return output.content