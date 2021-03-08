# Wh00t Socket Client Network Class

import os
import time
import ast
from typing import List, Any, NoReturn, Optional
from socket import AF_INET, socket, SOCK_STREAM
from .utils import package_data


class ClientNetwork:
    BUFFER_SIZE: int = 1024
    message_history: List[dict] = []

    def __init__(self, host: str, port: int, app_id: str, app_profile: str, logging_object: Optional = None) -> NoReturn:

        if logging_object:
            self.logger = logging_object.getLogger(type(self).__name__)
            self.logger.setLevel(logging_object.INFO)
        else:
            self.logger = None

        self.number_of_messages: int = 0
        self.client_socket: Any = None
        self.client_socket_error: bool = False
        self.address: tuple = (host, port)
        self.app_id: str = app_id
        self.app_profile: str = app_profile

    def log(self, log_type: str, message: str) -> NoReturn:
        if self.logger:
            if log_type == 'INFO':
                self.logger.info(message)
            elif log_type == 'ERROR':
                self.logger.error(message)
            elif log_type == 'WARNING':
                self.logger.warning(message)
        else:
            print(f'{log_type} - {message}')

    def sock_it(self) -> NoReturn:
        try:
            self.log('INFO', f'Attempting socket connection to {self.address}')
            self.client_socket: Any = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.address)
            package: str = package_data(self.app_id, self.app_profile, f'{self.app_id}_connect', '')
            self.client_socket.send(bytes(package, 'utf8'))
            self.log('INFO', f'Connection to {self.address} has succeeded')
        except ConnectionRefusedError as connection_refused_error:
            self.log('ERROR', f'Received ConnectionRefusedError: {(str(connection_refused_error))}')
            os._exit(1)
        except OSError as os_error:  # Possibly client has left the chat.
            self.log('ERROR', f'Received an OSError: {(str(os_error))}')
            os._exit(1)

    def send_message(self, message_category: str, message: str) -> NoReturn:
        try:
            packaged_message: str = package_data(self.app_id, self.app_profile, message_category, message)
            self.client_socket.send(bytes(packaged_message, 'utf8'))
        except IOError as io_error:
            self.log('ERROR', f'Received IOError: {(str(io_error))}')
            self.client_socket.close()
            os._exit(1)

    def receive(self) -> NoReturn:
        while self.client_socket:
            try:
                message: str = self.client_socket.recv(self.BUFFER_SIZE).decode('utf8', errors='replace')
                package: dict = ast.literal_eval(message)
                self.number_of_messages += 1
                self.message_history.append(package)
                self.__trim_message_history()
                self.log('INFO', f'Received Message: {str(package)}')
            except OSError as os_error:  # Possibly client has left the chat.
                self.log('ERROR', f'Received OSError: {(str(os_error))}')
                break
            except KeyboardInterrupt:
                self.log('WARNING', 'Received a KeyboardInterrupt... now exiting')
                self.close_it()
                os._exit(1)

    def close_it(self) -> NoReturn:
        time.sleep(0.25)
        self.send_message(f'{self.app_id}_disconnect', '/exit')
        self.client_socket.close()
        self.client_socket = None

    def get_message_history(self) -> List[dict]:
        self.__trim_message_history()
        return self.message_history

    def __trim_message_history(self) -> NoReturn:
        if len(self.message_history) > 150:
            self.message_history.pop(0)
