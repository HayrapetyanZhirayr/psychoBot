USER_HISTORY = {}


def update_user_history(user_id, role, content):
    if user_id not in USER_HISTORY:
        USER_HISTORY[user_id] = [{'role':role, 'content':content}]
    else:
        USER_HISTORY[user_id].append({'role':role, 'content':content})


def get_history(user_id):
    if user_id in USER_HISTORY:
        return USER_HISTORY[user_id]
    return []