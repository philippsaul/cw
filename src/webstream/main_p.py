import inputs
# import Jetson.GPIO as GPIO

# GPIO SETUP
# pwm_pin_motor_rechts = 32
# pwm_pin_motor_links = 33
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)

# GPIO.setup(pwm_pin_motor_rechts, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(pwm_pin_motor_links, GPIO.OUT,initial=GPIO.LOW)
# pwm1 = GPIO.PWM(pwm_pin_motor_rechts, 100)
# pwm2 = GPIO.PWM(pwm_pin_motor_links, 100)
# valpwm1 = 0
# valpwm2 = 0
# pwm1.start(valpwm1)
# pwm2.start(valpwm2)

print(inputs.devices.gamepads)

pads = inputs.devices.gamepads

if len(pads) == 0:
    raise Exception("Couldn't find any Gamepads!")

lenkwinkel = 128
while True:
    events = inputs.get_gamepad()
    for event in events:
        # print(event.ev_type, event.code, event.state)
        # print(event.code)
        if event.code == "BTN_TR":
            print(event.state)
            # pwm1.ChangeDutyCycle(event.state*100)
            # pwm2.ChangeDutyCycle()
            break
        if event.code == "ABS_X":
            lenkwinkel = int(event.state)
            print(lenkwinkel)
            break
        # Key BTN_TR 0