# from ps4test import Controller
from ps4test import Controller
import threading
import time

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window

download_thread = threading.Thread(target=controller.listen, name="test")
download_thread.start()

# controller.listen(timeout=60)
while True:
    print(controller.xb)
    # time.sleep(0.1)

