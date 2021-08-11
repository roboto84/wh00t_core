from datetime import datetime
import time
import ast


class NetworkUtils:
    MESSAGE_ENCODING: str = 'utf8'

    @staticmethod
    def package_data(client_id: str, client_profile: str, message_category: str, message: str) -> str:
        return str({
            'id': client_id,
            'profile': client_profile,
            'time': NetworkUtils.message_time(),
            'category': message_category,
            'message': message
        })

    @staticmethod
    def unpack_data(message: str) -> dict:
        return ast.literal_eval(message)

    @staticmethod
    def byte_package(client_id: str, client_profile: str, message_category: str, message: str) -> bytes:
        return bytes(NetworkUtils.package_data(client_id, client_profile, message_category, message), 'utf8')

    @staticmethod
    def utf8_bytes(package: str) -> bytes:
        return bytes(package, NetworkUtils.MESSAGE_ENCODING)

    @staticmethod
    def unpack_byte(package: bytes) -> str:
        return package.decode(NetworkUtils.MESSAGE_ENCODING, errors='replace')

    @staticmethod
    def message_time() -> str:
        return datetime.fromtimestamp(time.time()).strftime('%m/%d %H:%M')
