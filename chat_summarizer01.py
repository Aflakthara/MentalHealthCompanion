import json
import re
from datetime import datetime
from typing import Dict, List, Optional
import google.generativeai as genai


def summarize_chat(chat_text: str, api_key: str, date: Optional[str] = None) -> Dict[str, any]:
    """
    Convert chat text into a summary containing date, mood, and strong emotion keywords.
    
    Args:
        chat_text: The chat conversation text to summarize
        api_key: Google Gemini API key
        date: Optional date string (YYYY-MM-DD format). If None, uses current date.
    
    Returns:
        Dictionary with keys: 'date', 'mood', 'emotion_keywords'
    """
    # Configure API
    genai.configure(api_key=api_key)
    
    # Get model
    try:
        model = genai.GenerativeModel("gemini-pro")
    except:
        try:
            model = genai.GenerativeModel("gemini-1.5-pro")
        except:
            model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Set date (use provided date or current date)
    if date:
        summary_date = date
    else:
        summary_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create prompt for extraction
    prompt = f"""Analyze the following chat conversation and extract:
1. Overall mood (one word: e.g., "Happy", "Sad", "Anxious", "Angry", "Stressed", "Calm", "Neutral")
2. Strong emotion keywords (3-5 specific emotion words that best describe the emotional state)

Chat conversation:
{chat_text}

Return ONLY a valid JSON object with this exact format:
{{
    "mood": "one word mood",
    "emotion_keywords": ["keyword1", "keyword2", "keyword3"]
}}
"""
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            mood = data.get('mood', 'Neutral')
            emotion_keywords = data.get('emotion_keywords', [])
            
            return {
                'date': summary_date,
                'mood': mood,
                'emotion_keywords': emotion_keywords
            }
    except Exception as e:
        print(f"Error generating summary: {e}")
    
    # Fallback response
    return {
        'date': summary_date,
        'mood': 'Neutral',
        'emotion_keywords': []
    }


def summarize_chat_messages(messages: List[Dict], api_key: str, date: Optional[str] = None) -> Dict[str, any]:
    """
    Convert a list of chat messages into a summary.
    
    Args:
        messages: List of message dicts with 'role' and 'content' keys
        api_key: Google Gemini API key
        date: Optional date string (YYYY-MM-DD format)
    
    Returns:
        Dictionary with keys: 'date', 'mood', 'emotion_keywords'
    """
    # Format messages into chat text
    chat_text = ""
    for msg in messages:
        role = msg.get('role', 'user').capitalize()
        content = msg.get('content', '')
        chat_text += f"{role}: {content}\n"
    
    return summarize_chat(chat_text, api_key, date)


# Example usage
if __name__ == "__main__":
    # Example chat text
    sample_chat = """User: I'm feeling really overwhelmed today. My boss gave me way too much work.
    Assistant: That sounds really stressful. Want to talk about it?
    User: I just don't know if I can handle all of this. I'm anxious and scared I'll fail."""
    
    # You would need to set your API key
    API_KEY = "your-api-key-here"
    
    summary = summarize_chat(sample_chat, API_KEY)
    print(json.dumps(summary, indent=2))

