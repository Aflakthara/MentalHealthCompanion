import json
import os

DAILY_SUMMARY_FILE = "daily_summaries.json"


def load_daily_summaries():
    if not os.path.exists(DAILY_SUMMARY_FILE):
        return []
    with open(DAILY_SUMMARY_FILE, 'r') as f:
        return json.load(f)


def save_daily_summary(summary_dict):
    summaries = load_daily_summaries()
    summaries.append(summary_dict)
    with open(DAILY_SUMMARY_FILE, 'w') as f:
        json.dump(summaries, f)
