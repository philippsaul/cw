

from settings_read import read_settings

class Drivetrain():
    def __init__(self, log, BLDC) -> None:
        self.myBLDC = BLDC
        self.driving_direction = float(read_settings('driving_direction'))
        self.myBLDC.set_max_torque(float(read_settings('max_torque')))
        self.myBLDC.startup()


    def __del__(self) -> None:
        pass

    def cleanup(self) -> None:
        pass


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


        
