history = {}

def get_history(user_id):
    if user_id not in history:
        history[user_id] = []
    return history[user_id]


def add_message(user_id, role, content):
    get_history(user_id).append({
        "role": role,
        "content": content
    })


def clear_history(user_id):
    history[user_id] = []