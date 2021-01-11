#
#      ____   ____  ___    ____   __________       __   ________   _______    ________   ___  
#     /   /  /   / /   \  /    \ \   _____  \     /  / /  _____/  /  ___  \  /  _____/  /  /  
#    /   /  /   / /     \/  /\  \ \  \    |  |   /  / /  /       /  /  /  / /  /       /  /   
#   /   /__/   / /   /\____/  \  \ \  \___/  |  /  / /  /_____  /  /__/  / /  /_____  /  /____
#  /__________/ /___/          \__\ \_______/  /__/  \_______/ /________/  \_______/ /_______/ 
#
#   ||  ||        ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
# 
# Simple script to test reading in input and writing output to serial port 
# Written by: Sydrak Abdi
# 01/06/2020


import time
import serial

# Establish the connection on a specific port
port = "/dev/ttyACM0"
baud = 9600
timeout_val = 5
serial_port = serial.Serial(port, baud, timeout = timeout_val)

start = time.time()
done = False

while not done:
    print("From Arduino:")

    serial_input = serial_port.readline()
    print(serial_input)

    serial_input_str = serial_input.decode('utf-8')
    serial_input_flt = float(serial_input_str)

    print("To Arduino:")
    serial_output_flt = serial_input_flt + 0.1
    serial_output_str = str(serial_output_flt) + "\r\n"
    serial_output = serial_output_str.encode('utf-8')

    print(serial_output)
    serial_port.write(serial_output) 
    
    current = time.time()
    elapsed = current - start
    if elapsed > 3:
        done = True


