# -*- coding: utf-8 -*-
#
#   ||  ||        ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#..Writing practice scripts via bitcraze instructions at:
#..https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_connect_log_param/
#
#..Simple scripts that connects to the Crazyflie, prints a message, and disconnects form the Crazyflie


# Importing standard python3 libs
import logging
import time

# Importing cflibs

######################################################################################################

# Module used to scan for Crazyflie instances
import cflib.crtp

# The Crazyflie class is used to easily connect/send/receive data from a Crazyflie
from cflib.crazyflie import Crazyflie

# The synCrazyflie class is a wrapper around the "normal" Crazyflie class. 
#   It handles the asynchronus nature of the Crazyflie API and turns it into blocking function.
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

######################################################################################################

# URI to the Crazyflie to connect to
# This is the radio uri of the crazyflie, and currently displaying the default.
uri = 'radio://0/80/2M/E7E7E7E7E7'

def simple_connect():
    print("Yeah, I'm connected! :D")
    time.sleep(3)
    print("Now I will disconnect :'(")

if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:

        simple_connect()

# The syncCrazyflie will create a synchronous Crazyflie instance with the specified link_uri. 
# As you can see we are currently calling an non-existing function, so you will need to make 
# that function first before you run the script.