from datetime import datetime

class log:
    def info(text):
        print(" -----INFO---- " + str(datetime.now()) +" --- "+ str(text))

    def warning(text):
        WARNING = '\033[93m'
        ENDC = '\033[0m'
        print(f"{WARNING}"+" ---WARNING--- " + str(datetime.now()) +" --- "+ str(text) + ENDC)
    
    def error(text):
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        print(f"{FAIL}"+" ----ERROR---- " + str(datetime.now()) +" --- "+ str(text) + ENDC)