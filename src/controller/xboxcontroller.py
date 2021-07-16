from __future__ import print_function
import xbox

# Format floating point number to string format -x.xxx
def fmtFloat(n):
    return '{:6.3f}'.format(n)

def openController():
    return xbox.Joystick() 

def ausgabe(joy, argument):
    if(argument == "rt"):
        return joy.rightTrigger()
    elif(argument == "ls"):
        return joy.leftStick()
    elif(argument == "lt"):
        return joy.leftTrigger()
    elif(argument == "xb"):
        return joy.X()
    elif(argument == "yb"):
        return joy.Y()
    elif(argument == "ab"):
        return joy.A()
    elif(argument == "bb"):
        return joy.B()


