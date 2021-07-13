from __future__ import print_function
import xbox

# Format floating point number to string format -x.xxx
def fmtFloat(n):
    return '{:6.3f}'.format(n)
joy = xbox.Joystick() 

def ausgabe(argument):
    if(argument == "rt"):
        return joy.rightTrigger()
    elif(argument == "ls"):
        return joy.leftStick()

while True:
    print(joy.rightTrigger())
    print(joy.leftTrigger())

#joy.close()
