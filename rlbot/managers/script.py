from typing import Optional

from rlbot import flat
from rlbot.interface import SocketRelay
from rlbot.managers.rendering import RenderingManager
from rlbot.utils.logging import get_logger


class Script:
    """
    A convenience class for building scripts on top of.
    """

    def __init__(self, name):
        self.name = name
        self.logger = get_logger(name)

        self._game_interface = SocketRelay(logger=self.logger)
        self._game_interface.match_settings_handlers.append(self.handle_match_settings)
        self._game_interface.field_info_handlers.append(self.handle_field_info)
        self._game_interface.match_communication_handlers.append(
            self.handle_match_communication
        )
        self._game_interface.ball_prediction_handlers.append(
            self.handle_ball_prediction
        )
        self._game_interface.packet_handlers.append(self.handle_packet)

        self.renderer = RenderingManager(self._game_interface)

    def send_match_comm(
        self, content: bytes, display: Optional[str] = None, scripts_only: bool = False
    ):
        """
        Emits a match communication

        - `content`: The other content of the communication containing arbirtrary data.
        - `display`: The message to be displayed in the game, or None to skip displaying a message.
        - `scripts_only`: If True, only other scripts will receive the communication.
        """
        self._game_interface.send_match_comm(
            flat.MatchComm(
                0,
                2,
                scripts_only,
                display,
                content,
            )
        )

    def set_game_state(self, game_state: flat.DesiredGameState):
        self._game_interface.send_game_state(game_state)

    def run(self):
        self._game_interface.connect_and_run(True, False, True)
        del self._game_interface

    def handle_match_communication(self, match_Comm: flat.MatchComm):
        pass

    def handle_ball_prediction(self, ball_prediction: flat.BallPrediction):
        pass

    def handle_match_settings(self, match_settings: flat.MatchSettings):
        pass

    def handle_field_info(self, field_info: flat.FieldInfo):
        pass

    def handle_packet(self, packet: flat.GameTickPacket):
        pass
