import json
from summary_prompt import DAILY_SUMMARY_PROMPT


def generate_daily_summary(model, date_str, user_messages):
    messages_text = "\n".join(user_messages)
    prompt = f"Date: {date_str}\n\nUser messages:\n{messages_text}\n\n{DAILY_SUMMARY_PROMPT}"
    
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    
    # Remove markdown code blocks if present
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])
    
    summary_data = json.loads(response_text)
    
    return {
        "date": date_str,
        "emotions_felt": summary_data.get("emotions_felt", {}),
        "keywords_used_by_user": summary_data.get("keywords_used_by_user", []),
        "chat_summary": summary_data.get("chat_summary", "")
    }
