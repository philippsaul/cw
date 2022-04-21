
import time
from threading import Thread
from driving.BLDC_Driver import BLDC
from settings_read import read_settings

class Drivetrain(Thread):
    def __init__(self, log, gpio, output_enable_pin) -> None:
        Thread.__init__(self)
        self.driving_direction = float(read_settings('driving_direction'))
        self.test_str = "test"
        self.steering_data = [0, 0]
        self.myBLDC = BLDC(log, gpio, output_enable_pin)
        self.myBLDC.set_max_torque(float(read_settings('max_torque')))
        self.myBLDC.startup()


    def __del__(self) -> None:
        self.myBLDC.set_motor_sleep()
        self.myBLDC.pca9685_output_enable(state=False)


    def update_steering_data(self, steering_data: list) -> None:
        self.steering_data = steering_data
        

    def drive(self, steering_data: list) -> None:
        throttle, steering = steering_data
        # act_rotation_0_sum, act_rotation_1_sum, difference = self.myBLDC.myAS5600.rotation_difference()
        # if act_rotation_0_sum + act_rotation_1_sum > 0.1:
        #     d_const = 0.5*difference / (0.5*(act_rotation_0_sum + act_rotation_1_sum))
        # else:
        d_const = 0
        motor0_speed = throttle*abs(throttle) - steering*abs(steering) - d_const
        motor1_speed = throttle*abs(throttle) + steering*abs(steering) + d_const

        motor0_speed = max(min(motor0_speed,1),-1)
        motor1_speed = max(min(motor1_speed,1),-1)

        self.myBLDC.set_motor0_phase(motor0_speed * -self.driving_direction, self.myBLDC.get_rotation(0))
        self.myBLDC.set_motor1_phase(motor1_speed * self.driving_direction, self.myBLDC.get_rotation(1))
        # print('{:2.1f} | {:2.1f} | {:2.1f}'.format(motor0_speed, motor1_speed, d_const), end='              \r') # debugging

    def test(self, func_str: str):
        self.test_str = func_str

    def run(self) -> None:
        while True:
            self.drive(self.steering_data)
            time.sleep(0.0001)
        # pass
              
