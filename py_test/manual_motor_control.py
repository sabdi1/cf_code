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

import cflib
from cflib.crazyflie import Crazyflie

logging.basicConfig(level=logging.ERROR)


class MotorControl:
    """Class that connects to a Crazyflie and ramps the motors up/down and then disconnects"""

    def __init__(self, link_uri):
        """ Initialize and run the example with the specified link_uri """

        self._cf = Crazyflie(rw_cache='./cache')

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        self._cf.open_link(link_uri)

        print('Connecting to %s' % link_uri)

    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""

        # Start a separate thread to do the motor test.
        # Do not hijack the calling thread!
        Thread(target=self._ramp_motors).start()

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)

    def _ramp_motors(self, cmd_vel):

        roll    = round(cmd_vel[0])
        pitch   = round(cmd_vel[1])
        yawrate = round(cmd_vel[2])
        thrust  = round(cmd_vel[3])
        
        print(cmd_vel)

        self._cf.commander.send_setpoint(roll, pitch, yawrate, thrust)


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    
    # Scan for Crazyflies and use the first one found
    print('Scanning interfaces for Crazyflies...')
    available = cflib.crtp.scan_interfaces()

    print('Crazyflies found:')
    
    for i in available:
        print(i[0])

    if len(available) > 0:

        # Unlock startup thrust protection
        motor = MotorControl(available[0][0])

        motor._cf.commander.send_setpoint(0, 0, 0, 0)


        thrust_mult = 1
        thrust_step = 1000
        thrust = 20000

        while thrust >= 20000:
            print("Thrust : %d" %thrust)

            cmd_vel = [0, 0, 0, thrust]
            motor._ramp_motors(cmd_vel)
            time.sleep(0.1)

            if thrust >= 75000:
                thrust_mult = -1

            thrust += thrust_step * thrust_mult

        motor._cf.commander.send_setpoint(0, 0, 0, 0)

        # Make sure that the last packet leaves before the link is closed
        # since the message queue is not flushed before closing
        time.sleep(0.1)
        motor._cf.close_link()
    else:
        print('No Crazyflies found, cannot run example')