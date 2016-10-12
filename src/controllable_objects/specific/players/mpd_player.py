##############################################################################################
# FIXME List:
# CC15 - Consider Change 15
#   Выбрасывает исключение в случае неудачного подключения. Вопрос: отсавить как есть или 
#   перехватывать?
# CC16 - Consider Change 16
#   Может возвращать None вместо "undefined"?
##############################################################################################


import logging
import contextlib

from controllable_objects.abstract.abs_player import AbsPlayer
from connections.mpd_client import MPDClientConnection


class MPDPlayer(AbsPlayer):
    def __init__(self, con_instance: MPDClientConnection, con_params=None, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)

    @contextlib.contextmanager
    def connection(self):
        try:
            self.con_instance.reconnect()
            yield
        finally:
            self.con_instance.disconnect()

    @staticmethod
    def __mpd_state_to_self_state(mpd_state: str):
        if mpd_state == "play":
            return MPDPlayer.States.playing
        elif mpd_state == "stop":
            return MPDPlayer.States.stopped
        elif mpd_state == "pause":
            return MPDPlayer.States.paused
        else:
            logging.debug("Warning: unknown state of MPD player: {0}".format(mpd_state))
            return MPDPlayer.States.undefined

    def get_state(self):
        try:
            with self.connection():
                status = self.con_instance.status()
        except ConnectionRefusedError:
            return MPDPlayer.States.undefined

        return self.__mpd_state_to_self_state(status["state"])

    def play(self) -> None:  # CC15
        with self.connection():
            self.con_instance.play()

    def stop(self) -> None:  # CC15
        with self.connection():
            self.con_instance.stop()

    def pause(self) -> None:  # CC15
        with self.connection():
            self.con_instance.pause()

    def next(self) -> None:  # CC15
        with self.connection():
            self.con_instance.next()

    def prev(self) -> None:  # CC15
        with self.connection():
            self.con_instance.previous()

    def get_current_track(self) -> str:  # CC16
        try:
            with self.connection():
                return self.con_instance.currentsong()
        except ConnectionRefusedError:
            return "undefined"