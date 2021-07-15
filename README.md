# :beers::beers: Campuswoche 2021 in Gelsenkirchen :beers::beers:
Have some fun and drink beer.

# SSH connection

connect to jetson nano (username: _jetbotusername_ and hostname: _jetbothostname_) with ssh in terminal:
```bash
ssh jetbotusername@jetbothostname
```
if _jetbothostname_ can't be found, replace with ip

## Install pip3
```bash
sudo apt install python3-pip
```

## Install GPIO

Use the package manager pip3 to install gpio's:

```bash
sudo pip3 install Jetson.GPIO
sudo python3 setup.py install
```

## Usage

```bash
php script.php
```

## PHP tutorial
https://www.guru99.com/comments-includeinclude-once-requirerequire-once.html