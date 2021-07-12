from pyPS4Controller.controller import Controller

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)


def ausgabe(argument):
    if(argument == "rt"):
        return Controller.rightTrigger()
    elif(argument == "ls"):
        return Controller.leftStick()



controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)