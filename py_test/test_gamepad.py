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
# Testing using XBox One S gamepad input
# Modification of test_pygame.py test script written at: https://www.pygame.org/docs/ref/joystick.html
# Adding in dictionay to verify button mapping
# Written by: Sydrak Abdi
# 12/22/2020

import pygame


# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()

"""
VERIFY XBOX ONE S CONTROLLER MAPPING

Axis 0: Left  Stick L-R [-1,1]
Axis 1: Left  Stick U-D [-1,1]
Axis 2: Left  Trigg U-D [-1,1]
Axis 3: Right Stick L-R [-1,1]
Axis 4: Right Stick U-D [-1,1]
Axis 5: Right Trigg U-D [-1,1]

Butt 0:  A  Button   [0,1]
Butt 1:  B  Button   [0,1]
Butt 2:  X  Button   [0,1]
Butt 3:  Y  Button   [0,1]
Butt 4:  LB Button   [0,1]
Butt 5:  RB Button   [0,1]
Butt 6:  Menu Button [0,1]
Butt 7:  View Button [0,1]
Butt 8:  XBox Button [0,1]
Butt 9:  L3 Button   [0,1]
Butt 10: R3 Button   [0,1]

Hat 0: D-Pad
Left  (-1, 0)
Right ( 1, 0)
Up    ( 0, 1)
Down  ( 0,-1)
"""
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

# -------- Main Program Loop -----------
while not done:
    #
    # EVENT PROCESSING STEP
    #
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    #
    # DRAWING STEP
    #
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()

    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        try:
            jid = joystick.get_instance_id()
        except AttributeError:
            # get_instance_id() is an SDL2 method
            jid = joystick.get_id()
        textPrint.tprint(screen, "Joystick {}".format(jid))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()
        textPrint.tprint(screen, "Joystick name: {}".format(name))

        try:
            guid = joystick.get_guid()
        except AttributeError:
            # get_guid() is an SDL2 method
            pass
        else:
            textPrint.tprint(screen, "GUID: {}".format(guid))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.tprint(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):
            axis = joystick.get_axis(i)
            axis_dict_element = gamepad_axis_dict[i]
            textPrint.tprint(screen, "{} value: {:>6.3f}".format(axis_dict_element, axis))
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            butt_dict_element = gamepad_button_dict[i]
            textPrint.tprint(screen,
                             "{} value: {}".format(butt_dict_element, button))
        textPrint.unindent()

        hats = joystick.get_numhats()
        textPrint.tprint(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        # Hat position. All or nothing for direction, not a float like
        # get_axis(). Position is a tuple of int values (x, y).
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()

        textPrint.unindent()

    #
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    #

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second.
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()