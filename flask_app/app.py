"""
Flask application for handling RAG search queries.
"""

from flask import Flask, request, jsonify
from typing import Dict, Any

from utils import (
    search_articles, 
    fetch_article_content, 
    concatenate_content, 
    generate_answer
)

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query() -> Any:
    """
    Process incoming search query.
    
    Returns:
        Flask response with generated answer or error message.
    """
    try:
        # Parse incoming JSON request
        data: Dict[str, str] = request.get_json() or {}
        user_query: str = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({"error": "No query provided"}), 400
        
        # Step 1: Search and scrape articles based on the query
        app.logger.info("Step 1: Searching articles...")
        articles = search_articles(user_query)
        
        if not articles:
            return jsonify({"error": "No relevant articles found"}), 404
        
        # Step 2: Fetch and concatenate content
        app.logger.info("Step 2: Fetching and concatenating content...")
        for article in articles:
            article["content"] = fetch_article_content(article["url"])
        
        concatenated_content = concatenate_content(articles)
        
        # Step 3: Generate an answer using the LLM
        app.logger.info("Step 3: Generating an answer using the LLM...")
        generated_answer = generate_answer(concatenated_content, user_query)
        
        # Return the generated answer as JSON
        return jsonify({"answer": generated_answer}), 200
    
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)