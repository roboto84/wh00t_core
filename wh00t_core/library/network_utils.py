from datetime import datetime
from typing import List
from .__init__ import __version__
import time
import ast
import re


class NetworkUtils:
    MESSAGE_ENCODING: str = 'utf8'
    BUFFER_SIZE: int = 2048

    @staticmethod
    def get_version() -> str:
        return __version__

    @staticmethod
    def package_data(client_id: str, client_profile: str, message_category: str, message: str) -> str:
        packaged_data = str({
            'id': client_id,
            'profile': client_profile,
            'time': NetworkUtils.message_time(),
            'category': message_category,
            'message': message
        })
        return NetworkUtils.outer_package(packaged_data)

    @staticmethod
    def package_dict(package: dict) -> str:
        return NetworkUtils.outer_package(str(package))

    @staticmethod
    def outer_package(package: str) -> str:
        return f'ª{re.escape(package)}ª'

    @staticmethod
    def unpack_data(message: str) -> List[dict]:
        dict_packages = []
        str_packages: List[str] = re.findall(r'ª.*?ª', message)

        for package in str_packages:
            stripped_package = package.lstrip('ª').rstrip('ª')
            unescaped_package = re.sub(r'\\(.)', r'\1', stripped_package)
            dict_packages.append(ast.literal_eval(unescaped_package))
        return dict_packages

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
