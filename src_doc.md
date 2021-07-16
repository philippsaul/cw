# General structure
The sourcecode is structered in folders implemented by a general main.py in src.
Based on this fact everything is shit.

## Add profile to jetson nano
Duplicate a profile from _settings.ini_, change to hostname of jetson nano and adjust the values to your needs. 

## Import something
If you want to import file B.py in A.py and B.py imports C.py, try it in following way:
```bash
-> A.py
----folder_ABC-----
--------> B.py
--------> C.py
```

You have to import C.py in B.py:
```bash
---B.py---

try: 
    from folder_ABC import C.py
except:
    import C.py
```

And in A.py you import B.py as follows:
```bash
---A.py---

import B.py
```

It's the same for all imports (including imports for *.ini files too!).

## Use Gamepad

You can use your gamepad as follow:
```python
myGamepad = Gamepad()
...
while True:
    myGamepad.get_data()
    myValue = myGamepad.myValue
```

## Use Motors:
````python
from motor.motors import Motors

myMotors = Motors()

while True:
    myMotors.turn(75.0, "right")
    myMotors.stop()
    
myMotors.clean()
````

## Steer your bot with gamepad:
````python
from controller import gamepad
from motor.motors import Motors


myGamepad = gamepad.Gamepad()
myMotors = Motors()

while True:
    myGamepad.get_data()
    myMotors.gamepadcontroll(myGamepad.lt, myGamepad.rt, myGamepad.ls, 
            myGamepad.ab, myGamepad.bb, myGamepad.xb, myGamepad.yb)
````
