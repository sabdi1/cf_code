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
# Modification of ramp.py script written by Bitcraze
# Simple script that connects to Crazyflie, and hovers utilizing gamepad controls
# Written by: Sydrak Abdi
# 01/4/2020

import logging
import time
from threading import Thread

import pygame

import cflib
from cflib.crazyflie import Crazyflie

from manual_motor_control import MotorControl
from test_gamepad2 import Gamepad

if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    
    # Initialize Gamepad and Joystick
    input = Gamepad()
    joystick = input.joystick_init()
    
    # Scan for Crazyflies and use the first one found
    print('Scanning interfaces for Crazyflies...')
    available = cflib.crtp.scan_interfaces()

    print('Crazyflies found:')
    
    for i in available:
        print(i[0])

    if len(available) > 0:

        ####################################################################
        # CONTROL PANEL
        done = False
        max_time = 60

        ####################################################################

        # Initilizing Crazyflie and MotorControl
        motor = MotorControl(available[0][0])

        # Unlock startup thrust protection
        motor._cf.commander.send_setpoint(0, 0, 0, 0)

        start = time.time()
        thrust_mult_old = 0

        while not done:

            # Get Event from Gamepad
            pygame.event.get()

            # Read in and sort event form gamepad
            input.get_event(joystick)

            # Calculating elapsed time
            current = time.time()
            elapsed = current - start

            # Button and time killswitch
            if input._gamepad._button[8] == 1 or elapsed > max_time:
                done = True

            roll         = -30*round(input._gamepad._axis[3])           # Integer : degs
            pitch        = -30*round(input._gamepad._axis[4])           # Integer : degs
            yawrate      = 30*round(input._gamepad._axis[0])           # Interger: degs/s
            thrust_mult  = -input._gamepad._axis[1]                 # Integer : 10001 - 60000
            
            # Creating a deadzone
            if abs(thrust_mult) < 0.1:
                thrust_mult = 0

            # If thrust command is recoil form joystick
            if thrust_mult > 0:
                if thrust_mult < thrust_mult_old:
                    thrust_mult = 0
            elif thrust_mult < 0:
                if thrust_mult > thrust_mult_old:
                    thrust_mult = 0

            # If using altitude hold
            if input._gamepad._button[5] == 1:
                thrust_cmd = thrust_cmd
            elif input._gamepad._button[5] == 0: 
                thrust_step = 5000
                thrust_cmd += thrust_step * thrust_mult
                
                if thrust_cmd < 0:
                    thrust_cmd = 0

                thrust_cmd = round(thrust_cmd)
            
            thrust_mult_old = thrust_mult
            
            '''
            print("Thrust : %d" %thrust_cmd)
            print(isinstance(roll, int))
            print(isinstance(pitch, int))
            print(isinstance(yawrate, int))
            print(isinstance(thrust_cmd, int))
            '''

            cmd_vel = [roll, pitch, yawrate, thrust_cmd]
            
            motor._ramp_motors(cmd_vel)
            time.sleep(0.1)

        motor._cf.commander.send_setpoint(0, 0, 0, 0)

        # Make sure that the last packet leaves before the link is closed
        # since the message queue is not flushed before closing
        time.sleep(0.1)
        motor._cf.close_link()

    else:
        print('No Crazyflies found, cannot run example')

