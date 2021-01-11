import serial
import struct
import time

serial_port = port = "/dev/ttyACM0"
baud = 9600
timeout_val = 5
serial_port = serial.Serial(port, baud, timeout = timeout_val)
time.sleep(2)

done = False
buffer_size = 4*4
while not done:
    serial_port.write(b'w')
    sample = serial_port.read(buffer_size) 
    data = struct.unpack(4*"f", sample)
    print(data)
    
    time.sleep(.01) # Desired sample rate

