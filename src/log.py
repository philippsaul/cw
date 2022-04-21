from datetime import datetime

class log:
    def __init__(self) -> None:
        self.error = False
        
    def info(self, text):
        print(" -----INFO---- " + str(datetime.now()) +" --- "+ str(text))

    def warning(self, text):
        WARNING = '\033[93m'
        ENDC = '\033[0m'
        print(f"{WARNING}"+" ---WARNING--- " + str(datetime.now()) +" --- "+ str(text) + ENDC)
    
    def error(self, text):
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        print(f"{FAIL}"+" ----ERROR---- " + str(datetime.now()) +" --- "+ str(text) + ENDC)
        
    def raise_Error(self):
        self.error = True
        raise Exception()
