import os
import logging.config
import time
from threading import Thread
from typing import Any, Optional
from library.client_network import ClientNetwork

TEST_HOST = '127.0.0.1'
TEST_PORT = 3001
APP_ID = 'wh00t_core'
APP_PROFILE = 'app'


def send_socket_message(host: str, port: int, app_id: str, app_profile: str,  logging_object: Optional = None):

    if logging_object:
        socket_network: ClientNetwork = ClientNetwork(host, port, app_id, app_profile)
        message = 'hello world - with logger'
    else:
        socket_network: ClientNetwork = ClientNetwork(host, port, app_id, app_profile, logging_object)
        message = 'hello world - without logger'

    socket_network.sock_it()
    receive_thread: Any = Thread(target=socket_network.receive)
    receive_thread.start()
    time.sleep(2)
    socket_network.send_message('network_test', message)
    socket_network.close_it()


if __name__ == '__main__':

    # without logger
    send_socket_message(TEST_HOST, TEST_PORT, APP_ID, APP_PROFILE)

    # with logger
    logging.config.fileConfig(fname=os.path.abspath('wh00t_core/bin/logging.conf'), disable_existing_loggers=False)
    logger: Any = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    send_socket_message(TEST_HOST, TEST_PORT, APP_ID, APP_PROFILE, logging)
