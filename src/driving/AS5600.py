
PCA9544_ADDRESS     = 0x77
PCA9544_CHANNEL_0   = 0x05
PCA9544_CHANNEL_1   = 0x04

AS5600_ADDRESS      = 0x36
MAGNET_STATUS       = 0x0B
ZERO_POSITION_H     = 0x01
ZERO_POSITION_L     = 0x02
RAW_ANGLE_H         = 0x0C
RAW_ANGLE_L         = 0x0D
ANGLE_H             = 0x0E
ANGLE_L             = 0x0F

class AS5600():
    def __init__(self, bus) -> None:
            """Initialize the AS5600."""
            self._bus = bus
            self.current_selected_as5600 = None


    def select_AS5600(self, channel: int):
        """Choose an AS5600 by selecting a channel of the PCA9544 I2C Multiplexer."""
        if self.current_selected_as5600 != channel:
            if channel == 0:
                self._bus.write_byte(PCA9544_ADDRESS, PCA9544_CHANNEL_0)
                self.current_selected_as5600 = channel
            elif channel == 1:
                self._bus.write_byte(PCA9544_ADDRESS, PCA9544_CHANNEL_1)
                self.current_selected_as5600 = channel

    def get_raw_rotation(self, chip: int) -> int:
        """Returns a value from 0 to 4095."""
        self.select_AS5600(chip)
        angle_h = self._bus.read_byte_data(AS5600_ADDRESS, RAW_ANGLE_H)
        angle_l = self._bus.read_byte_data(AS5600_ADDRESS, RAW_ANGLE_L)
        return angle_l + (angle_h << 8)

    def get_rotation_degree(self, chip: int) -> float:
        """Returns a value from 0 to 359.9"""
        self.select_AS5600(chip)
        angle_h = self._bus.read_byte_data(AS5600_ADDRESS, ANGLE_H)
        angle_l = self._bus.read_byte_data(AS5600_ADDRESS, ANGLE_L)
        return (360*(angle_l + (angle_h << 8))/4095)%360

    def get_zero_position(self, chip: int) -> int:
        """Returns the Zero-Position."""
        self.select_AS5600(chip)
        angle_h = self._bus.read_byte_data(AS5600_ADDRESS, ZERO_POSITION_H)
        angle_l = self._bus.read_byte_data(AS5600_ADDRESS, ZERO_POSITION_L)
        return int(angle_l + (angle_h << 8))

    def set_zero_position(self, chip: int, angle: float) -> None:
        """Sets the Zero-Position, select a chip and set an rotation in drgree."""
        self.select_AS5600(chip)
        raw_angle = int(round(4095*((angle%360/360))))
        self._bus.write_byte_data(AS5600_ADDRESS, ZERO_POSITION_H, raw_angle >> 8)
        self._bus.write_byte_data(AS5600_ADDRESS, ZERO_POSITION_L, raw_angle & 0xFF)

    def get_magnet_status(self, chip: int) -> list:
        """Check Magnet strength. Returns status and message.
        Status: 0 not operatable.
        Status: 1 operatable.
        Message contains more details."""
        self.select_AS5600(chip)
        message = 'No magnet was detected.'
        status = 'Error'
        tmp_buffer = self._bus.read_byte_data(AS5600_ADDRESS, MAGNET_STATUS)
        if tmp_buffer & 0b00100000:
            message = 'Magnet was detected. '
            status = 'OK'
        if tmp_buffer & 0b00010000:
            message += 'AGC maximum gain overflow, magnet too weak.'
        if tmp_buffer & 0b00001000:
            message += 'AGC minimum gain overflow, magnet too strong.'
        if tmp_buffer & 0b00110000 or tmp_buffer & 0b00101000:
            status = 'Warning'
        return status, message


# import time
# import smbus
# x = AS5600(smbus.SMBus(bus = 0))
# while True:
#     print(round(x.get_rotation_degree(0),2), end='\r')
#     time.sleep(0.05)


