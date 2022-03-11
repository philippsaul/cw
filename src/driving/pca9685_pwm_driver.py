import Adafruit_PCA9685
import time

class pca9685():
    def __init__(self) -> None:
        self.pca9685 = Adafruit_PCA9685.PCA9685(address = 0x4a, busnum = 1)
        self.pca9685.set_pwm_freq(1000)

        self.channel_motor1_input1 = 0
        self.channel_motor1_input2 = 1
        self.channel_motor1_input3 = 2
        self.channel_motor1_enable1 = 6
        self.channel_motor1_enable2 = 7
        self.channel_motor1_enable3 = 8
        self.channel_motor2_input1 = 3
        self.channel_motor2_input2 = 4
        self.channel_motor2_input3 = 5
        self.channel_motor2_enable1 = 9
        self.channel_motor2_enable2 = 10
        self.channel_motor2_enable3 = 11
        self.channel_motor1_sleep = 12
        self.channel_motor2_sleep = 13
        self.channel_motor1_reset = 14
        self.channel_motor2_reset = 15

        def set_pwm(self, channel: int, period: float = 0) -> None:
            '''Sets pwm values. Period range 0-1 in float. Use predefined channels only.'''
            self.pca9685.set_pwm(channel, 0, int(4095 * period))

        def enable_all(self):
            '''Enables Channel and Motor Driver.'''
            set_pwm(self.channel_motor1_enable1, 1)
            set_pwm(self.channel_motor1_enable2, 1)
            set_pwm(self.channel_motor1_enable3, 1)
            set_pwm(self.channel_motor2_enable1, 1)
            set_pwm(self.channel_motor2_enable2, 1)
            set_pwm(self.channel_motor2_enable3, 1)

            set_pwm(self.channel_motor1_sleep, 1)
            set_pwm(self.channel_motor2_sleep, 1)
            set_pwm(self.channel_motor1_reset, 1)
            set_pwm(self.channel_motor2_reset, 1)

        def set_motor_sleep(self, motor: int = None, state: bool = True) -> None:
            '''Motors can sleep (Save Power).
            motor= 1, 2 or not filled for both Motors.
            set_motor_sleep(state=False) -> wakes both Motors.'''
            if motor == None:
                set_pwm(self.channel_motor1_sleep, int(not state))
                set_pwm(self.channel_motor2_sleep, int(not state))
            elif motor == 1:
                set_pwm(self.channel_motor1_sleep, int(not state))
            elif motor == 2:
                set_pwm(self.channel_motor2_sleep, int(not state))
            else:
                print('No Motor with number {motor} found. Choose 1 or 2.')

        def set_motor_reset(self, motor: int = None, state: bool = True) -> None:
            '''sets Motors reset pin.
            motor= 1, 2 or not filled for both Motors.
            set_motor_reset(state=False) -> enables both Motors.'''
            if motor == None:
                set_pwm(self.channel_motor1_reset, int(not state))
                set_pwm(self.channel_motor2_reset, int(not state))
            elif motor == 1:
                set_pwm(self.channel_motor1_reset, int(not state))
            elif motor == 2:
                set_pwm(self.channel_motor2_reset, int(not state))
            else:
                print('No Motor with number {motor} found. Choose 1 or 2.')



# test
mypca = pca9685()
mypca.enable_all()

while True:
    print('Doing stuff')
    mypca.set_pwm(mypca.channel_motor1_input3, 0)
    time.sleep(5)
    mypca.set_pwm(mypca.channel_motor1_input3, 0.5)
    time.sleep(5)
    mypca.set_pwm(mypca.channel_motor1_input3, 1)
    time.sleep(5)