# Common settings

class NetworkCommons:
    # Common Network Settings
    _MESSAGE_ENCODING: str = 'utf8'
    _BUFFER_SIZE: int = 4096

    # Special Message String Commands
    _EXIT_COMMAND: str = '/exit'
    _DESTRUCT_COMMAND: str = '/boom'

    # Common Message Ids
    _SERVER_ID: str = 'wh00t_server'

    # Common Message Profiles
    _USER_PROFILE: str = 'user'
    _APP_PROFILE: str = 'app'

    def get_message_encoding(self):
        return self._MESSAGE_ENCODING

    def get_buffer_size(self):
        return self._BUFFER_SIZE

    def get_exit_command(self):
        return self._EXIT_COMMAND

    def get_destruct_command(self):
        return self._DESTRUCT_COMMAND

    def get_server_id(self):
        return self._SERVER_ID

    def get_app_profile(self):
        return self._APP_PROFILE

    def get_user_profile(self):
        return self._USER_PROFILE
