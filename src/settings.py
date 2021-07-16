import socket

hostname = socket.gethostname()
liste = [10]


def userdata():
    if(hostname == "linus"):
        liste[0] = "xbox"
        liste[1] = 0.05 #Deadzone throttle 
        liste[2] = 35.00 #minimaler Anlauf boost
        liste[3] = 25.00 #minmaler Load
        liste[4] = 40.00 #"Radius" bezogen auf PWM Kurve nicht größer als 40 höherer Wert = stärkere kurve
        liste[5] = 30.00 #minimaler Kurven Radius kleiner als max_wert
        liste[6] = 0.1 #Deadzone Steering
        return liste
    elif(hostname == "lars"):
        liste[0] = "xbox"
        liste[1] = 0.05 #Deadzone throttle 
        liste[2] = 35.00 #minimaler Anlauf boost
        liste[3] = 25.00 #minmaler Load
        liste[4] = 35.00 #"Radius" bezogen auf PWM Kurve nicht größer als 40 höherer Wert = stärkere kurve
        liste[5] = 25.00 #minimaler Kurven Radius kleiner als max_wert 
        liste[6] = 0.1 #Deadzone Steering
        return liste
    elif(hostname == "lukas"):
        liste[0] = "ps4"
        liste[1] = 0.05 #Deadzone throttle 
        liste[2] = 35.00 #minimaler Anlauf boost
        liste[3] = 25.00 #minmaler Load
        liste[4] = 35.00 #"Radius" bezogen auf PWM Kurve nicht größer als 40 höherer Wert = stärkere kurve
        liste[5] = 25.00 #minimaler Kurven Radius kleiner als max_wert 
        liste[6] = 0.1 #Deadzone Steering
        return liste
    elif(hostname == "philipp"):
        liste[0] = "ps4"
        liste[1] = 0.05 #Deadzone throttle 
        liste[2] = 35.00 #minimaler Anlauf boost
        liste[3] = 25.00 #minmaler Load
        liste[4] = 35.00 #"Radius" bezogen auf PWM Kurve nicht größer als 40 höherer Wert = stärkere kurve
        liste[5] = 25.00 #minimaler Kurven Radius kleiner als max_wert 
        liste[6] = 0.1 #Deadzone Steering
        return liste
    else:
        liste[0] = "ps4"
        liste[1] = 0.05 #Deadzone throttle 
        liste[2] = 35.00 #minimaler Anlauf boost
        liste[3] = 25.00 #minmaler Load
        liste[4] = 35.00 #"Radius" bezogen auf PWM Kurve nicht größer als 40 höherer Wert = stärkere kurve
        liste[5] = 25.00 #minimaler Kurven Radius kleiner als max_wert 
        liste[6] = 0.1 #Deadzone Steering
        return liste

