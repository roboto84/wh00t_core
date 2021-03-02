import os
import logging.config
import time
from threading import Thread
from typing import Any
from library.client_network import ClientNetwork

TEST_HOST = '127.0.0.1'
TEST_PORT = 3001

if __name__ == '__main__':
    logging.config.fileConfig(fname=os.path.abspath('wh00t_core/bin/logging.conf'), disable_existing_loggers=False)
    logger: Any = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    socket_network: ClientNetwork = ClientNetwork(TEST_HOST, TEST_PORT, 'wh00t_core', 'app', logging)
    socket_network.sock_it()
    receive_thread: Any = Thread(target=socket_network.receive)
    receive_thread.start()
    time.sleep(2)
    socket_network.send_message('network_test', 'hello world')
    socket_network.close_it()
