import time
import math

# Registers/etc:
PCA9685_ADDRESS    = 0x4a
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04


class PCA9685():
    def __init__(self, bus) -> None:
        """Initialize the PCA9685."""

        self._bus = bus
        self.set_all_pwm(4095, 4095)
        self._bus.write_byte_data(PCA9685_ADDRESS, MODE2, OUTDRV)
        self._bus.write_byte_data(PCA9685_ADDRESS, MODE1, ALLCALL)
        time.sleep(0.005)  # wait for oscillator
        mode1 = self._bus.read_byte_data(PCA9685_ADDRESS, MODE1)
        mode1 = mode1 & ~SLEEP  # wake up (reset sleep)
        self._bus.write_byte_data(PCA9685_ADDRESS, MODE1, mode1)
        time.sleep(0.005)  # wait for oscillator


    def set_pwm_freq(self, freq_hz):
        """Set the PWM frequency to the provided value in hertz."""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        prescale = int(math.floor(prescaleval + 0.5))
        oldmode = self._bus.read_byte_data(PCA9685_ADDRESS, MODE1);
        newmode = (oldmode & 0x7F) | 0x10    # sleep
        self._bus.write_byte_data(PCA9685_ADDRESS, MODE1, newmode)  # go to sleep
        self._bus.write_byte_data(PCA9685_ADDRESS, PRESCALE, prescale)
        self._bus.write_byte_data(PCA9685_ADDRESS, MODE1, oldmode)
        time.sleep(0.005)
        self._bus.write_byte_data(PCA9685_ADDRESS, MODE1, oldmode | 0x80)

    def set_pwm(self, channel: int, duty_cycle: float) -> None:
        """Sets pwm values. duty_cycle range 0-1 in float. Use predefined channels only."""
        on = int(4095 - 4095 * duty_cycle)
        off = 4095
        self._bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L+4*channel, on & 0xFF)
        self._bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_H+4*channel, on >> 8)
        # self._bus.write_byte_data(PCA9685_ADDRESS, LED0_OFF_L+4*channel, off & 0xFF)
        # self._bus.write_byte_data(PCA9685_ADDRESS, LED0_OFF_H+4*channel, off >> 8)

    def set_all_pwm(self, on, off) -> None:
        """Sets all PWM channels."""
        self._bus.write_byte_data(PCA9685_ADDRESS, ALL_LED_ON_L, on & 0xFF)
        self._bus.write_byte_data(PCA9685_ADDRESS, ALL_LED_ON_H, on >> 8)
        self._bus.write_byte_data(PCA9685_ADDRESS, ALL_LED_OFF_L, off & 0xFF)
        self._bus.write_byte_data(PCA9685_ADDRESS, ALL_LED_OFF_H, off >> 8)
