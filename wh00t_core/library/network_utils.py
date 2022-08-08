from datetime import datetime
from typing import List, Tuple, Optional
from .network_commons import NetworkCommons
from .__init__ import __version__
import time
import ast
import re


class NetworkUtils:
    _network_commons: NetworkCommons = NetworkCommons()

    def utf8_bytes(self, package: str) -> bytes:
        return bytes(package, self._network_commons.get_message_encoding())

    def unpack_byte(self, package: bytes) -> str:
        return package.decode(self._network_commons.get_message_encoding(), errors='replace')

    def get_byte_buffer_calc(self, message_package: bytes) -> Tuple[int, float]:
        package_byte_length: int = len(message_package)
        return package_byte_length, round((package_byte_length / self._network_commons.get_buffer_size()) * 100, 2)

    def byte_package(self, client_id: str, client_profile: str, message_category: str, message: str,
                     client_username: Optional[str] = None, data: Optional[dict] = None) -> bytes:
        return bytes(NetworkUtils.package_data(
            client_id,
            client_profile,
            message_category,
            message,
            client_username,
            data),
            self._network_commons.get_message_encoding())

    @staticmethod
    def get_version() -> str:
        return __version__

    @staticmethod
    def package_data(client_id: str, client_profile: str, message_category: str,
                     message: str, username: Optional[str] = None, data: Optional[str] = None) -> str:
        packaged_data = str({
            'id': client_id,
            'username': username if username else client_id,
            'profile': client_profile,
            'time': NetworkUtils.message_time(),
            'category': message_category,
            'message': message,
            'data': data
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
    def message_time() -> str:
        return datetime.fromtimestamp(time.time()).strftime('%m/%d %H:%M:%S')
