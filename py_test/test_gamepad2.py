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
# 01/04/2020

import logging
import time
from threading import Thread

import pygame
from progress_bar import printProgressBar 

# Defining dictionaries to keep track
gamepad_axis_dict = {
    0 : "LStick_LR [-1,1]",
    1 : "LStick_UD [-1,1]",
    2 : "LTrigg_UD [-1,1]",
    3 : "RStick_LR [-1,1]",
    4 : "RStick_UD [-1,1]",
    5 : "RTrigg_UD [-1,1]"
}

gamepad_button_dict = {
    0 : "A Button [0,1]",
    1 : "B Button [0,1]",
    2 : "X Button [0,1]",
    3 : "Y Button [0,1]",
    4 : "LB Button [0,1]",
    5 : "RB Button [0,1]",
    6 : "View Button [0,1]",
    7 : "Menu Button [0,1]",
    8 : "XBox Button [0,1]",
    9 : "L3 Button [0,1]",
    10: "R3 Button [0,1]"
}

class Gamepad:

    class GamepadEventList:
        _axis_length = 6
        _button_length = 11
        _hat_length = 1

        _axis   = [0, 0, 0, 0, 0, 0]
        _button = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        _hat    = (0,0)


    def print_axis(self):
        print("Axis Values   : ", self._gamepad._axis)
        
    def print_button(self):
        print("Button Values : ", self._gamepad._button)
    
    def print_hat(self):
        print("Hat Values    : ", self._gamepad._hat)   

    _gamepad  = GamepadEventList()

    def __init__(self):
        pygame.init()
        joystick_count = pygame.joystick.get_count()

        if joystick_count != 1:
            print('ERROR: [%d] gamepad(s) detected.' % joystick_count)
            print('ERROR: Only programmed to handle 1 gamepad currently.')
            print('ERROR: Exiting...')
            return

    def joystick_init(self):
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        self._gamepad.axis   = joystick.get_axis
        self._gamepad.button = joystick.get_button
        self._gamepad.hat    = joystick.get_hat
        return joystick

    def get_event(self, joystick):

        # Usually axis run in pairs, up/down for one, and left/right for the other.
        axes = joystick.get_numaxes()                   # Number of Axes

        if axes != self._gamepad._axis_length:
            print("ERROR: Unexpected number of gamepad axes.")
            print("ERROR: Exiting...")
            return

        for i in range(axes):
            axis  = joystick.get_axis(i)                 # Axis Value
            self._gamepad._axis[i] = axis
            axis_dict_element = gamepad_axis_dict[i]    # Axis Name


        buttons = joystick.get_numbuttons()             # Number of Buttons

        if buttons != self._gamepad._button_length:
            print("ERROR: Unexpected number of gamepad buttons.")
            print("ERROR: Exiting...")
            return

        for i in range(buttons):
            button = joystick.get_button(i)             # Button Value
            self._gamepad._button[i] = button
            butt_dict_element = gamepad_button_dict[i]  # Button Name

        hats = joystick.get_numhats()                   # Number of Hats

        if hats != self._gamepad._hat_length:
            print("ERROR: Unexpected number of gamepad hats.")
            print("ERROR: Exiting...")
            return

        # Hat position. All or nothing for direction, not a float like
        # get_axis(). Position is a tuple of int values (x, y).
            self._gamepad._hat[i] = joystick.get_hat(i) # Hat Value


if __name__ == '__main__':

    input = Gamepad()
    joystick = input.joystick_init()
    
    ####################################################################
    # CONTROL PANEL
    done = False
    max_time = 30
    print_raw_input = False
    print_progress_bar = True
    # Choosing variable to print in progress bar. Based on dictionary definitions
    # [0-5,6-17] : [Axes, Buttons]
    progress_bar_varable = 17
    ####################################################################

    if print_progress_bar:
        # Initial call to print 0% progress
        if progress_bar_varable < 6:
            print_data_name = gamepad_axis_dict[progress_bar_varable]
        elif progress_bar_varable > 5:
            print_data_name = gamepad_button_dict[progress_bar_varable-6]
        elif progress_bar_varable > 17:
            print("ERROR: Attempting to access value outside of preassigned range.")
            print("ERROR: Exiting...")
            #return

        printProgressBar(0, max_time, prefix = print_data_name, suffix = '', length = 50)

    start = time.time()
    while not done:
        pygame.event.get()

        ##for event in pygame.event.get(): # User did something.
          ##  if event.type == pygame.JOYBUTTONDOWN:
            ##    #print("Joystick button pressed.")
              ##  #print("")
            ##elif event.type == pygame.JOYBUTTONUP:
                #print("Joystick button released.")
                #print("")

        input.get_event(joystick)
        
        current = time.time()
        elapsed = current - start

        if input._gamepad._button[8] == 1 or elapsed > max_time:
            done = True

        if print_raw_input:
            input.print_axis()
            input.print_button()
            input.print_hat()

        if print_progress_bar:
            # Update Progress Bar
            print_data = []
            if progress_bar_varable < 6:
                print_data = input._gamepad._axis[progress_bar_varable] + 1
            elif progress_bar_varable > 5:
                print_data = input._gamepad._button[progress_bar_varable-6]

            printProgressBar(print_data, 2, prefix = print_data_name, suffix = '', length = 50)

        time.sleep(0.0625) 

