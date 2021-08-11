from datetime import datetime
import time
import ast


def package_data(client_id: str, client_profile: str, message_category: str, message: str) -> str:
    return str({
        'id': client_id,
        'profile': client_profile,
        'time': message_time(),
        'category': message_category,
        'message': message
    })


def unpack_data(message: str) -> dict:
    return ast.literal_eval(message)


def byte_package(client_id: str, client_profile: str, message_category: str, message: str) -> bytes:
    return bytes(package_data(client_id, client_profile, message_category, message), 'utf8')


def message_time() -> str:
    return datetime.fromtimestamp(time.time()).strftime('%m/%d %H:%M')
