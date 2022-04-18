
import time
from log import log


class Safety():
    def __init__(self, gamepad) -> None:
        self.gamepad = gamepad

    def enable_gamepad(self) -> None:
        enable_gamepad_variable = False
        pushed = False
        released = False
        log.warning('Controller not enabled yet! Push and release both Trigger full.')

        while not enable_gamepad_variable:
            self.gamepad.get_data()
            rt = self.gamepad.rt
            lt = self.gamepad.lt

            if(rt >= 1.0) and (lt >= 1.0) and not pushed:
                pushed = True
                log.info('Pushed!')
            if(rt == 0) and (lt == 0) and pushed and not released:
                released = True
                log.info('Released!')
            if pushed and released:
                enable_gamepad_variable = True
                log.info('Controller enabled!')
            time.sleep(0.1)

    def safety(seld) -> None:
        pass
        