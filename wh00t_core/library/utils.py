from datetime import datetime
import time


def package_data(client_id: str, client_profile: str, message_category: str, message: str) -> str:
    return str({
        'id': client_id,
        'profile': client_profile,
        'time': message_time(),
        'category': message_category,
        'message': message
    })


def message_time() -> str:
    return datetime.fromtimestamp(time.time()).strftime('%m/%d %H:%M')
