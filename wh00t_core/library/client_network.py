# Wh00t Socket Client Network Class
import logging
import os
import time
from typing import List, Any, Optional, Callable
from socket import AF_INET, socket, SOCK_STREAM
from .network_utils import NetworkUtils


class ClientNetwork:
    message_history: List[dict] = []

    def __init__(self, host: str, port: int, app_id: str, app_profile: str, logging_object: Optional = None):

        if logging_object:
            self.logger: Optional[logging.Logger] = logging_object.getLogger(type(self).__name__)
            self.logger.setLevel(logging_object.INFO)
        else:
            self.logger: Optional[logging.Logger] = None

        self.number_of_messages: int = 0
        self.client_socket: Optional[socket] = None
        self.client_socket_error: bool = False
        self.address: tuple = (host, port)
        self.app_id: str = app_id
        self.app_profile: str = app_profile

    @staticmethod
    def get_version() -> str:
        return NetworkUtils.get_version()

    def log(self, log_type: str, message: str) -> None:
        if self.logger:
            if log_type == 'INFO':
                self.logger.info(message)
            elif log_type == 'ERROR':
                self.logger.error(message)
            elif log_type == 'WARNING':
                self.logger.warning(message)
        else:
            print(f'{log_type} - {message}')

    def sock_it(self) -> None:
        try:
            self.log('INFO', f'Attempting socket connection to {self.address}')
            self.client_socket: Any = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.address)
            self.client_socket.send(NetworkUtils.byte_package(self.app_id, self.app_profile,
                                                              f'{self.app_id}_connect', ''))
            self.log('INFO', f'Connection to {self.address} has succeeded')
        except ConnectionRefusedError as connection_refused_error:
            self.log('ERROR', f'Received ConnectionRefusedError: {(str(connection_refused_error))}')
            os._exit(1)
        except OSError as os_error:  # Possibly client has left the chat.
            self.log('ERROR', f'Received an OSError: {(str(os_error))}')
            os._exit(1)

    def send_message(self, message_category: str, message: str) -> None:
        try:
            package_message: bytes = NetworkUtils.byte_package(self.app_id, self.app_profile, message_category, message)
            package_byte_length: int = len(package_message)
            buffer_percent: float = round((package_byte_length / NetworkUtils.BUFFER_SIZE) * 100, 2)
            self.log('INFO', f'Sending: {package_byte_length}B ({buffer_percent}% of buffer)')
            self.client_socket.send(package_message)
        except IOError as io_error:
            self.log('ERROR', f'Received IOError: {(str(io_error))}')
            self.client_socket.close()
            os._exit(1)

    def receive(self, call_back_comparator: Optional[Callable[[dict], bool]] = None) -> None:
        while self.client_socket:
            try:
                message: str = NetworkUtils.unpack_byte(self.client_socket.recv(NetworkUtils.BUFFER_SIZE))
                if len(message) == 0:
                    self.log('WARNING', 'Socket connection has dropped')
                    self.close_it()
                    if call_back_comparator:
                        call_back_comparator({})
                else:
                    packages: List[dict] = NetworkUtils.unpack_data(message)
                    self.number_of_messages += len(packages)

                    for package in packages:
                        self.message_history.append(package)
                        self.__trim_message_history()
                        self.log('INFO', f'Received Message: {str(package)}')
                        if call_back_comparator:
                            if not call_back_comparator(package):
                                return
            except OSError as os_error:  # Possibly client has left the chat.
                self.log('ERROR', f'Received OSError: {(str(os_error))}')
                break
            except SyntaxError as syntax_error:
                self.logger.error(f'Received SyntaxError: {str(syntax_error)}')
                break
            except KeyboardInterrupt:
                self.log('WARNING', 'Received a KeyboardInterrupt... now exiting')
                self.close_it()
                os._exit(1)

    def close_it(self) -> None:
        if self.client_socket:
            time.sleep(0.25)
            self.send_message(f'{self.app_id}_disconnect', '/exit')
            self.client_socket.close()
            self.client_socket = None

    def get_message_history(self) -> List[dict]:
        self.__trim_message_history()
        return self.message_history

    def __trim_message_history(self) -> None:
        if len(self.message_history) > 150:
            self.message_history.pop(0)
