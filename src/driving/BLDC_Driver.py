
import time

import Jetson.GPIO as GPIO
import smbus
from log import log

import driving.sin
from driving.AS5600 import AS5600
from driving.PCA9685 import PCA9685


class BLDC():
    def __init__(self) -> None:
        """Initialize the Driver."""

        self.output_enable_pin = 7
        # range 24 to 1526 Hz
        self.pwm_frequency = 1200
        
        self.channel_motor0_input1 = 0
        self.channel_motor0_input2 = 1
        self.channel_motor0_input3 = 2
        self.channel_motor0_enable1 = 6
        self.channel_motor0_enable2 = 7
        self.channel_motor0_enable3 = 8

        self.channel_motor1_input1 = 3
        self.channel_motor1_input2 = 4
        self.channel_motor1_input3 = 5
        self.channel_motor1_enable1 = 9
        self.channel_motor1_enable2 = 10
        self.channel_motor1_enable3 = 11

        self.channel_motor0_sleep = 12
        self.channel_motor1_sleep = 13
        self.channel_motor0_reset = 14
        self.channel_motor1_reset = 15

        bus = smbus.SMBus(bus = 0)
        self.myAS5600 = AS5600(bus)
        self.myPCA9685 = PCA9685(bus)
        self.myPCA9685.set_pwm_freq(self.pwm_frequency)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.output_enable_pin, GPIO.OUT, initial = GPIO.HIGH) # disables output

        self.sin = driving.sin.sin
        self.steps = 25
        self.polpair = 7
        self.degrees_per_polpair = 360.0/self.polpair
        self.degrees_per_step = self.degrees_per_polpair/360.0

        self.phase_motor0 = 0
        self.phase_motor1 = 0
        self.max_torque = 1



    def enable_all_channels(self, state: bool =True) -> None:
        """Enables Channel. Disables Channels with state=False."""
        self.myPCA9685.set_pwm(self.channel_motor0_enable1, int(state))
        self.myPCA9685.set_pwm(self.channel_motor0_enable2, int(state))
        self.myPCA9685.set_pwm(self.channel_motor0_enable3, int(state))
        self.myPCA9685.set_pwm(self.channel_motor1_enable1, int(state))
        self.myPCA9685.set_pwm(self.channel_motor1_enable2, int(state))
        self.myPCA9685.set_pwm(self.channel_motor1_enable3, int(state))

    def set_motor_sleep(self, motor: int = None, state: bool = True) -> None:
        """Motors can sleep (Save Power).
        motor= 0, 1 or not filled for both Motors.
        set_motor_sleep(state=False) -> wakes both Motors."""
        if motor == None:
            self.myPCA9685.set_pwm(self.channel_motor0_sleep, int(not state))
            self.myPCA9685.set_pwm(self.channel_motor1_sleep, int(not state))
        elif motor == 0:
            self.myPCA9685.set_pwm(self.channel_motor0_sleep, int(not state))
        elif motor == 1:
            self.myPCA9685.set_pwm(self.channel_motor1_sleep, int(not state))
        else:
            print('No Motor with number {motor} found. Choose 0 or 1.')

    def set_motor_reset(self, motor: int = None, state: bool = True) -> None:
        """sets Motors reset pin.
        motor= 0, 1 or not filled for both Motors.
        set_motor_reset(state=False) -> enables both Motors."""
        if motor == None:
            self.myPCA9685.set_pwm(self.channel_motor0_reset, int(not state))
            self.myPCA9685.set_pwm(self.channel_motor1_reset, int(not state))
        elif motor == 0:
            self.myPCA9685.set_pwm(self.channel_motor0_reset, int(not state))
        elif motor == 1:
            self.myPCA9685.set_pwm(self.channel_motor1_reset, int(not state))
        else:
            print('No Motor with number {motor} found. Choose 0 or 1.')

    def pca9685_output_enable(self, state: bool = True) -> None:
        """Set True to enable Output, Pin state LOW/GND."""
        if state:
            GPIO.output(self.output_enable_pin, GPIO.LOW)
        else:
            GPIO.output(self.output_enable_pin, GPIO.HIGH)

    def init_rotation(self, motor: int):
        """tbd"""
        if motor == 0:
            self.myPCA9685.set_pwm(self.channel_motor0_input1, self.max_torque * self.sin[self.phase_motor0])
            self.myPCA9685.set_pwm(self.channel_motor0_input2, self.max_torque * self.sin[(self.phase_motor0 + 120) % 360])
            self.myPCA9685.set_pwm(self.channel_motor0_input3, self.max_torque * self.sin[(self.phase_motor0 + 240) % 360])
            time.sleep(0.9)
            self.myAS5600.set_zero_position(0, (self.myAS5600.get_zero_position(0)/4095)*360 + self.myAS5600.get_rotation_degree(0))
            time.sleep(0.1)
            self.myPCA9685.set_pwm(self.channel_motor0_input1, 0)
            self.myPCA9685.set_pwm(self.channel_motor0_input2, 0)
            self.myPCA9685.set_pwm(self.channel_motor0_input3, 0)
            # print(self.myAS5600.get_rotation_degree(0)) # debugging
            # print((self.myAS5600.get_zero_position(0)/4095)*359) # debugging
        elif motor == 1:
            self.myPCA9685.set_pwm(self.channel_motor1_input1, self.max_torque * self.sin[self.phase_motor1])
            self.myPCA9685.set_pwm(self.channel_motor1_input2, self.max_torque * self.sin[(self.phase_motor1 + 120) % 360])
            self.myPCA9685.set_pwm(self.channel_motor1_input3, self.max_torque * self.sin[(self.phase_motor1 + 240) % 360])
            time.sleep(0.9)
            self.myAS5600.set_zero_position(1, (self.myAS5600.get_zero_position(1)/4095)*360 + self.myAS5600.get_rotation_degree(1))
            time.sleep(0.1)
            self.myPCA9685.set_pwm(self.channel_motor1_input1, 0)
            self.myPCA9685.set_pwm(self.channel_motor1_input2, 0)
            self.myPCA9685.set_pwm(self.channel_motor1_input3, 0)
        else:
            print('No Motor with number {motor} found. Choose 0 or 1.')

    def check_magnet_strength(self, chip: int) -> None:
        status, message = self.myAS5600.get_magnet_status(chip)
        if status == 'Error':
            log.error('Magnet strength chip {}: {}'.format(chip, message))
        elif status == 'Warning':
            log.warning('Magnet strength chip {}: {}'.format(chip, message))
        elif status == 'OK':
            log.info('Magnet strength chip {}: {}'.format(chip, message))


    def set_max_torque(self, torque: float) -> None:
        self.max_torque = torque if torque <= 1.0 else print('Torque value out of range.')
    
    def startup(self) -> None:
        self.pca9685_output_enable()
        self.enable_all_channels()
        self.set_motor_reset(state=False)
        self.set_motor_sleep(state=False)
        self.check_magnet_strength(0)
        self.check_magnet_strength(1)
        self.init_rotation(0)
        self.init_rotation(1)

    def __calc_phase_torque(self, throttle: float, old_phase: int, actual_rotation: float) -> list:
        """Calculates with throttel value new phase and torque."""
        phase_increment = self.steps * throttle
        new_phase = (old_phase + phase_increment) % 360
        actual_rotation %= self.degrees_per_polpair

        rotation_difference = actual_rotation - (new_phase / self.polpair)
        if rotation_difference < -(self.degrees_per_polpair/2):
            rotation_difference += self.degrees_per_polpair
        elif rotation_difference > (self.degrees_per_polpair/2):
            rotation_difference -= self.degrees_per_polpair
            
        if abs(rotation_difference) <= self.degrees_per_polpair/4:
            x = abs(rotation_difference / (self.degrees_per_polpair/4))
            torque = (1 + (x-1)**3) * self.max_torque
            # torque = (1 - (1-x**2)**4) * self.max_torque # alternative to previos liine
            if torque < 0.1 and throttle == 0:
                torque = 0
            elif torque > self.max_torque:
                torque = self.max_torque
        else:
            if(phase_increment > 0 and rotation_difference < 0) or (phase_increment < 0 and rotation_difference > 0):
                new_phase = old_phase
            new_phase += rotation_difference/2
            torque = self.max_torque
            
        # print('{:2.1f} | {:2.1f} | {:2.2f} | {:2.1f} | {:1.2f}'.format(new_phase/self.polpair, actual_rotation, phase_increment, rotation_difference, torque), end='              \r') # debugging
        return int(round(new_phase, 0))%360, round(torque, 2)

    def set_motor0_phase(self, throttle: float) -> float:
        rotation = self.myAS5600.get_rotation_degree(0)
        self.phase_motor0, torque = self.__calc_phase_torque(-throttle, self.phase_motor0, rotation)

        self.myPCA9685.set_pwm(self.channel_motor0_input1, torque * self.sin[self.phase_motor0])
        self.myPCA9685.set_pwm(self.channel_motor0_input2, torque * self.sin[(self.phase_motor0 + 120) % 360])
        self.myPCA9685.set_pwm(self.channel_motor0_input3, torque * self.sin[(self.phase_motor0 + 240) % 360])

        return rotation

    def set_motor1_phase(self, throttle: float) -> float:
        rotation = self.myAS5600.get_rotation_degree(1)
        self.phase_motor1, torque = self.__calc_phase_torque(throttle, self.phase_motor1, rotation)

        self.myPCA9685.set_pwm(self.channel_motor1_input1, torque * self.sin[self.phase_motor1])
        self.myPCA9685.set_pwm(self.channel_motor1_input2, torque * self.sin[(self.phase_motor1 + 120) % 360])
        self.myPCA9685.set_pwm(self.channel_motor1_input3, torque * self.sin[(self.phase_motor1 + 240) % 360])

        return rotation

