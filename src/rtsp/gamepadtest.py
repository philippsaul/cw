import struct

# infile_path = "/dev/input/js0"
# EVENT_SIZE = struct.calcsize("llHHI")
# file = open(infile_path, "rb")
# event = file.read(EVENT_SIZE)
# while event:
#     print(struct.unpack("llHHI", event))
#     (tv_sec, tv_usec, type, code, value) = struct.unpack("llHHI", event)
#     event = file.read(EVENT_SIZE)

infile_path = "/dev/input/js0"
EVENT_SIZE = struct.calcsize("LhBB")
file = open(infile_path, "rb")
event = file.read(EVENT_SIZE)
while event:

    (tv_msec,  value, type, number) = struct.unpack("LhBB", event)
    event = file.read(EVENT_SIZE)

    if value == 1 and type == 1 and number == 1:
        print("zustand eins")
    if value == 0 and type == 1 and number == 1:
        print("zustand zwei")
    # print(struct.unpack("LhBB", event)[1])
    # print(struct.unpack("LhBB", event)[2])
    # print(struct.unpack("LhBB", event)[3])
    # print("\t")
