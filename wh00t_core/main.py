import os
import logging.config
import time
from threading import Thread
from typing import Optional
from library.client_network import ClientNetwork
from library.network_commons import NetworkCommons

TEST_HOST: str = '127.0.0.1'
TEST_PORT: int = 3001
APP_ID: str = 'wh00t_core'
APP_PROFILE: str = NetworkCommons().get_app_profile()
client_username: str = 'wh00t-bot'
network_commons: NetworkCommons = NetworkCommons()


def send_socket_message(socket_network: ClientNetwork, message: str, message_category: str,
                        data_object: Optional[dict] = None):
    socket_network.sock_it()
    receive_thread: Thread = Thread(target=socket_network.receive)
    receive_thread.start()
    time.sleep(2)
    socket_network.send_message(message_category, message, client_username, data_object)
    socket_network.close_it()


if __name__ == '__main__':
    logging.config.fileConfig(fname=os.path.abspath('wh00t_core/bin/logging.conf'), disable_existing_loggers=False)
    logger: logging.Logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    socket_network_without_logging: ClientNetwork = ClientNetwork(TEST_HOST, TEST_PORT, APP_ID, APP_PROFILE)
    socket_network_with_logging: ClientNetwork = ClientNetwork(TEST_HOST, TEST_PORT, APP_ID, APP_PROFILE, logging)

    # with logger
    send_socket_message(
        socket_network_with_logging,
        'hello world - with logger',
        network_commons.get_chat_message_category()
    )

    # without logger
    send_socket_message(
        socket_network_without_logging,
        'hello world - without logger',
        network_commons.get_chat_message_category()
    )

    # chat message with data
    voice_message = 'Good Morning... perhaps it is time to drink some water'
    send_socket_message(
        socket_network_without_logging,
        voice_message,
        network_commons.get_chat_message_category(),
        {'voice': voice_message}
    )
