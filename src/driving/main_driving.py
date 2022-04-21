
import time

from driving.BLDC_Driver import BLDC

class Drivetrain():
    def __init__(self) -> None:

        self.myBLDC = BLDC()
        self.myBLDC.startup()

        self.last_time = 0
        self.last_rotation_value = 0

    def __del__(self) -> None:
        self.myBLDC.set_motor_sleep()
        self.myBLDC.pca9685_output_enable(state=False)


    def drive(self, steering_data: list) -> None:
        throttle, steering = steering_data

        motor0_speed = throttle*abs(throttle) - steering*abs(steering)
        motor1_speed = throttle*abs(throttle) + steering*abs(steering)

        motor0_speed = max(min(motor0_speed,1),-1)
        motor1_speed = max(min(motor1_speed,1),-1)

        motor0_rotation = self.myBLDC.set_motor0_phase(motor0_speed)
        # motor1_rotation = self.myBLDC.set_motor1_phase(motor1_speed)

        diff = motor0_rotation - self.last_rotation_value
        if diff >= 180:
            diff -= 360
        elif diff < -180:
            diff += 360

        speed = diff/(time.time()-self.last_time)
        self.last_time = time.time()
        self.last_rotation_value = motor0_rotation

        print(round(speed,2),end='       \r')
        time.sleep(0.1)