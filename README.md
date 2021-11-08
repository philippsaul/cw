# How2 setup the Robot:

Follow the official instructions about how to set up the jetson nano:
[NVIDIA JETSON NANO](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-2gb-devkit)

## SSH connection

connect to jetson nano (username: _jetbotusername_ and hostname: _jetbothostname_) with ssh in terminal:
```bash
ssh jetbotusername@jetbothostname
```
if _jetbothostname_ can't be found, replace with ip

## Update
```bash
sudo apt update
sudo apt upgrade
```

## Install pip3
```bash
sudo apt install python3-pip
```

## Install GPIO

**INFO:** used library: https://github.com/NVIDIA/jetson-gpio

**INSTALLATION:**
```bash
sudo pip3 install Jetson.GPIO
```

**IMPORTANT:** 	execute settings user permissions:
            
```bash
sudo groupadd -f -r gpio
sudo usermod -a -G gpio your_user_name
```
create file 99-gpio.rules with an editor of your choice:
```bash
sudo nano /etc/udev/rules.d/99-gpio.rules
```
take content from:
https://github.com/NVIDIA/jetson-gpio/blob/master/lib/python/Jetson/GPIO/99-gpio.rules


reboot jetson nano:
```bash
sudo reboot
```
:coffee: drink a very small coffee and wait for reboot :coffee:

**IMPORTANT:** 	activate PWM pins:
```bash
sudo /opt/nvidia/jetson-io/jetson-io.py
```

    -> configure 40-pin expansion header
    -> activate PWM channels
    -> save and reboot to reconfigure pins

## Webstreaming
Install flask:
```bash
pip3 install flask
```
if necessary, install everything for gstreamer:
```bash
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio opencv-python
```

## Controller
### PS4 Controller:
connect with following software:
```bash
sudo bluetoothctl
```
after connection, install:
```bash
pip3 install pyPS4Controller
```

### XBOX360 Controller:
```bash
pip3 install xboxdrv
```
---
AUTHORS: Linus Etemi, Lukas Holtkamp, Lars Hebing, Philipp Saul
---

---
DATE: 15.07.2021
---