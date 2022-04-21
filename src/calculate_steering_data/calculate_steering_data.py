
import time

from settings_read import read_settings


# funktion soll anhand der eingangsparameter entscheiden welche steuerungsdaten zurückgegeben werden
class Calculate_steering_data:
    def __init__(self, log, gamepad) -> None:
        self.gamepad = gamepad
        self.log = log

        # auslesen der values von der settings.ini datei
        self.deadzone_thr = float(read_settings('deadzone_throttle'))
        self.deadzone_str = float(read_settings('deadzone_steering'))
        

    def calc(self):
        throttle = 0
        steering = 0
        
        self.start_angle = None
        if self.gamepad.rt > self.deadzone_thr or self.gamepad.lt > self.deadzone_thr:
            throttle = self.gamepad.rt - self.gamepad.lt
        if abs(self.gamepad.ls) > self.deadzone_str:
            steering = self.gamepad.ls

        return throttle, steering
