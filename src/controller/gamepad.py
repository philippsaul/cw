
import configparser
import socket
import threading

try: 
    from controller import xboxcontroller
except:
    import xboxcontroller

try:
    from controller.ps4 import Controller
except:
    from ps4 import Controller

class Gamepad:
    def __init__(self, log):
        self.log = log
        self.ls = self.rt = self.lt = self.yb = self.ab = self.bb = self.xb = self.lb = self.trackpad = 0
        self.is_connected = True
        self.enable_gamepad = False
        self.config = configparser.ConfigParser()
        try:
            self.config.read('./settings.ini')
        except:
            self.config.read('../settings.ini')
        for section in self.config.sections():
            if self.config[section]['hostname'] == socket.gethostname():
                self.section = self.config[section]
                break
        if self.section == None:
            raise Exception("can't find hostname in settings.ini")
        
        if self.section["controller"] == "xbox":
            self.xbox = xboxcontroller.openController()
        elif self.section["controller"] == "ps4":
            self.ps4 = Controller(interface="/dev/input/js0", connecting_using_ds4drv=False, log=self.log)
            self.ps4_thread = threading.Thread(target=self.ps4.listen, name="test")
            self.ps4_thread.daemon = True
            self.ps4_thread.start()
        else:
            raise Exception('unknown remote controller - file: controller.py')
    
    def get_data(self):
        if self.section["controller"] == "xbox":
            self.ls = xboxcontroller.ausgabe(self.xbox, "ls")
            self.ls = self.truncate(self.ls , 3)
            self.ls = self.ls.replace("(","")
            self.ls = self.ls.replace(",","")
            self.rt = xboxcontroller.ausgabe(self.xbox, "rt")
            self.rt = self.truncate(self.rt , 3)
            self.rt = self.rt.replace("(","")
            self.rt = self.rt.replace(",","")
            self.rt = float(self.rt)
            self.ls = float(self.ls)
            self.lt = xboxcontroller.ausgabe(self.xbox, "lt")
            self.lt = self.truncate(self.lt , 3)
            self.lt = self.lt.replace("(","")
            self.lt = self.lt.replace(",","")
            self.lt = float(self.lt)

            self.yb = xboxcontroller.ausgabe(self.xbox, "yb")
            self.ab = xboxcontroller.ausgabe(self.xbox, "ab")
            self.bb = xboxcontroller.ausgabe(self.xbox, "bb")
            self.xb = xboxcontroller.ausgabe(self.xbox, "xb")

            self.BUTTON_NORTH = xboxcontroller.ausgabe(self.xbox, "yb")
            self.BUTTON_EAST = xboxcontroller.ausgabe(self.xbox, "bb")
            self.BUTTON_SOUTH = xboxcontroller.ausgabe(self.xbox, "ab")
            self.BUTTON_WEST = xboxcontroller.ausgabe(self.xbox, "xb")

            self.LEFT_TRIGGER = float(self.lt)
            self.RIGHT_TRIGGER = float(self.rt)
            self.LEFT_JOYSTICK_HORIZONTAL = float(self.ls)


        elif self.section["controller"] == "ps4":
            self.ls = float(self.ps4.ls/32767)
            self.rt = float((self.ps4.rt + 32767)/65534)
            self.lt = float((self.ps4.lt + 32767)/65534)
            self.yb = int(self.ps4.yb)
            self.ab = int(self.ps4.ab)
            self.bb = int(self.ps4.bb)
            self.xb = int(self.ps4.xb)
            self.lb = int(self.ps4.lb)

            self.BUTTON_NORTH = int(self.ps4.yb)
            self.BUTTON_EAST = int(self.ps4.bb)
            self.BUTTON_SOUTH = int(self.ps4.ab)
            self.BUTTON_WEST = int(self.ps4.xb)
            
            self.LEFT_TRIGGER = float((self.ps4.lt + 32767)/65534)
            self.RIGHT_TRIGGER = float((self.ps4.rt + 32767)/65534)
            self.LEFT_JOYSTICK_HORIZONTAL = float(self.ps4.ls/32767)

            self.trackpad = int(self.ps4.trackpad)

            self.is_connected = self.ps4.is_connected

        else: 
            raise Exception('error in gamepad')

    def truncate(self, f, n):
        '''Truncates/pads a float f to n decimal places without rounding'''
        s = '{}'.format(f)
        if 'e' in s or 'E' in s:
            return '{0:.{1}f}'.format(f, n)
        i, p, d = s.partition('.')
        return '.'.join([i, (d+'0'*n)[:n]])

# test = Gamepad()
# while True:
#     test.get_data()
#     print(test.lt)