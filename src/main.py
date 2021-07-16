from controller import gamepad
from motor.motors import Motors


myGamepad = gamepad.Gamepad()
myMopets = Motors()

while True:
    myGamepad.get_data()
    myMopets.gamepadcontroll(myGamepad.lt, myGamepad.rt, myGamepad.ls, myGamepad.ab, myGamepad.bb, myGamepad.xb, myGamepad.yb)



