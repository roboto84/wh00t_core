# Wh00t Socket Client Network Class
import logging
import os
import time
import inspect
import asyncio
from typing import List, Optional, Callable, Coroutine
from socket import AF_INET, socket, SOCK_STREAM
from .network_utils import NetworkUtils
from .network_commons import NetworkCommons


class ClientNetwork:
    _network_commons: NetworkCommons = NetworkCommons()
    _network_utils: NetworkUtils = NetworkUtils()
    _message_history: List[dict] = []
    _number_of_messages: int = 0
    _client_socket: Optional[socket] = None

    def __init__(self, host: str, port: int, app_id: str, app_profile: str,
                 logging_object: Optional = None):
        if logging_object:
            self._logger: Optional[logging.Logger] = logging_object.getLogger(type(self).__name__)
            self._logger.setLevel(logging_object.INFO)
        else:
            self._logger: Optional[logging.Logger] = None
        self._address: tuple[str, int] = (host, port)
        self._app_id: str = app_id
        self._app_profile: str = app_profile

    @staticmethod
    def get_version() -> str:
        return NetworkUtils.get_version()

    def _log(self, log_type: str, message: str) -> None:
        if self._logger:
            if log_type == 'INFO':
                self._logger.info(message)
            elif log_type == 'ERROR':
                self._logger.error(message)
            elif log_type == 'WARNING':
                self._logger.warning(message)
        else:
            print(f'{log_type} - {message}')

    def sock_it(self, client_username: Optional[str] = None) -> None:
        try:
            self._log('INFO', f'Attempting socket connection to {self._address}')
            self._client_socket: socket = socket(AF_INET, SOCK_STREAM)
            self._client_socket.connect(self._address)
            self._client_socket.send(
                self._network_utils.byte_package(self._app_id,
                                                 self._app_profile,
                                                 f'{self._app_id}_connect',
                                                 '',
                                                 client_username))
            self._log('INFO', f'Connection to {self._address} has succeeded')
        except ConnectionRefusedError as connection_refused_error:
            self._log('ERROR', f'Received ConnectionRefusedError: {(str(connection_refused_error))}')
            os._exit(1)
        except OSError as os_error:  # Possibly client has left the chat.
            self._log('ERROR', f'Received an OSError: {(str(os_error))}')
            os._exit(1)

    def send_message(self, message_category: str, message: str, client_username: Optional[str] = None) -> None:
        try:
            message_package: bytes = self._network_utils.byte_package(self._app_id, self._app_profile,
                                                                      message_category, message, client_username)
            (package_byte_length, buffer_percent) = self._network_utils.get_byte_buffer_calc(message_package)
            self._log('INFO', f'Sending: {package_byte_length}B ({buffer_percent}% of buffer)')
            self._client_socket.send(message_package)
        except IOError as io_error:
            self._log('ERROR', f'Received IOError: {(str(io_error))}')
            self._client_socket.close()
            os._exit(1)

    def receive(self, call_back_comparator: Optional[Callable[[dict], bool]] or Optional[Coroutine] = None) -> None:
        while self._client_socket:
            try:
                message: str = self._network_utils.unpack_byte(
                    self._client_socket.recv(self._network_commons.get_buffer_size()))
                is_comparator_coroutine: bool = inspect.iscoroutinefunction(call_back_comparator)
                if len(message) == 0:
                    self._log('WARNING', 'Socket connection has dropped')
                    self.close_it()
                    if call_back_comparator:
                        if is_comparator_coroutine:
                            asyncio.get_event_loop().run_until_complete(call_back_comparator({}))
                        else:
                            call_back_comparator({})
                else:
                    packages: List[dict] = NetworkUtils.unpack_data(message)
                    self._number_of_messages += len(packages)
                    for package in packages:
                        self._message_history.append(package)
                        self.__trim_message_history()
                        self._log('INFO', f'Received Message: {str(package)}')
                        if call_back_comparator:
                            if inspect.iscoroutinefunction(call_back_comparator):
                                comparator_result = asyncio.get_event_loop().run_until_complete(
                                    call_back_comparator(package))
                            else:
                                comparator_result = call_back_comparator(package)
                            if not comparator_result:
                                return
            except OSError as os_error:  # Possibly client has left the chat.
                self._log('ERROR', f'Received OSError: {(str(os_error))}')
                break
            except SyntaxError as syntax_error:
                self._logger.error(f'Received SyntaxError: {str(syntax_error)}')
                break
            except KeyboardInterrupt:
                self._log('WARNING', 'Received a KeyboardInterrupt... now exiting')
                self.close_it()
                os._exit(1)

    def close_it(self) -> None:
        if self._client_socket:
            time.sleep(0.25)
            self.send_message(f'{self._app_id}_disconnect', self._network_commons.get_exit_command())
            self._client_socket.close()
            self._client_socket = None

    def get_message_history(self) -> List[dict]:
        self.__trim_message_history()
        return self._message_history

    def __trim_message_history(self) -> None:
        max_message_history: int = 35
        if len(self._message_history) >= max_message_history:
            self._message_history.pop(0)
