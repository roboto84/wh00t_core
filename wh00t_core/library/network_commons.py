# Common settings

class NetworkCommons:
    # Common Network Settings
    _MESSAGE_ENCODING: str = 'utf8'
    _BUFFER_SIZE: int = 8192
    _MESSAGE_HISTORY_LIMIT: int = 60

    # Special Message String Commands
    _EXIT_COMMAND: str = '/exit'
    _DESTRUCT_COMMAND: str = '/secret'
    _HISTORY_CLEAR_COMMANDS: list[str] = ['/clear', '/c']

    # Common Message Ids
    _SERVER_ID: str = 'wh00t_server'

    # Common Message Profiles
    _USER_PROFILE: str = 'user'
    _APP_PROFILE: str = 'app'

    # Common Message Categories
    _CHAT_MESSAGE_CATEGORY = 'chat_message'

    def get_message_encoding(self):
        return self._MESSAGE_ENCODING

    def get_buffer_size(self):
        return self._BUFFER_SIZE

    def get_message_history_limit(self):
        return self._MESSAGE_HISTORY_LIMIT

    def get_exit_command(self):
        return self._EXIT_COMMAND

    def get_destruct_command(self):
        return self._DESTRUCT_COMMAND

    def is_secret_message(self, message: str) -> bool:
        return self.get_destruct_command() in message

    def is_history_clear_command(self, message: str) -> bool:
        return message in self._HISTORY_CLEAR_COMMANDS

    def get_server_id(self):
        return self._SERVER_ID

    def get_app_profile(self):
        return self._APP_PROFILE

    def get_user_profile(self):
        return self._USER_PROFILE

    def get_chat_message_category(self):
        return self._CHAT_MESSAGE_CATEGORY
