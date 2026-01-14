DAILY_SUMMARY_PROMPT = """Analyze all user messages from a single day and output JSON with the following structure:
- emotions_felt: a dictionary mapping emotion names to intensity values (1-10)
- keywords_used_by_user: a list of short phrases or keywords the user mentioned
- chat_summary: a 1-2 line summary in third person describing the conversation

Output only valid JSON, no markdown formatting, no explanations, no additional text."""
