
import time


class Safety():
    def __init__(self, log, gamepad) -> None:
        self.gamepad = gamepad
        self.log = log

    def enable_gamepad(self) -> None:
        enable_gamepad_variable = False
        pushed = False
        released = False
        self.log.warning('Controller not enabled yet! Push and release both Trigger full.')

        while not enable_gamepad_variable:
            self.gamepad.get_data()
            rt = self.gamepad.rt
            lt = self.gamepad.lt

            if(rt >= 1.0) and (lt >= 1.0) and not pushed:
                pushed = True
                self.log.info('Pushed!')
            if(rt == 0) and (lt == 0) and pushed and not released:
                released = True
                self.log.info('Released!')
            if pushed and released:
                enable_gamepad_variable = True
                self.log.info('Controller enabled!')
            time.sleep(0.1)

    def safety(self) -> None:
        # manueller Stop über trackpad eines ps4 controllers
        if self.gamepad.trackpad:
            self.log.warning('Safety: Button pressed on Gamepad.')
            self.log.raise_Error()

        # Abschaltung wenn die Verbindung zum Controller abbricht
        if not self.gamepad.is_connected:
            self.log.error('Safety: Gamepad is disconnected!')
            self.log.raise_Error()
        