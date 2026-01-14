_daily_messages = {}


def add_user_message(date_str, message_text):
    if date_str not in _daily_messages:
        _daily_messages[date_str] = []
    _daily_messages[date_str].append(message_text)


def get_messages_for_date(date_str):
    return _daily_messages.get(date_str, [])


def clear_date(date_str):
    if date_str in _daily_messages:
        del _daily_messages[date_str]
