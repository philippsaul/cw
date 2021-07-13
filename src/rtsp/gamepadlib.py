import inputs

print(inputs.devices.gamepads)

pads = inputs.devices.gamepads

if len(pads) == 0:
    raise Exception("Couldn't find any Gamepads!")

while True:
    events = inputs.get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)