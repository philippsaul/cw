from ps4test import Controller
import threading

ps4 = Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
ps4_thread = threading.Thread(target=ps4.listen, name="test")
ps4_thread.start()

# while True:
    # print(ps4.rt)
    # print((ps4.lt + 32767)/65534)
