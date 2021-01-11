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
#..Simple scripts that connects to the Crazyflie, reads out logging variables asynchronously, and disconnects form the Crazyflie


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

# LogConfig class is a representation of one log configuration that enables logging from the Crayflie
from cflib.crazyflie.log import LogConfig

# The SyncLogger class provides synchronous access to log data from the Crazyflie
from cflib.crazyflie.syncLogger import SyncLogger

######################################################################################################

# URI to the Crazyflie to connect to
# This is the radio uri of the crazyflie, and currently displaying the default.
uri = 'radio://0/80/2M/E7E7E7E7E7'

# Only output error from the logging framework
logging.basicConfig(level=logging.ERROR)

# This callback will be called once the log variables have received it and prints the contents.
def log_stab_callback(timestamp, data, logconf):
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))

# Here you add the logging configuration to to the logging framework of the Crazyflie. 
# It will check if the log configuration is part of the TOC, which is a list of all the logging 
# variables defined in the Crazyflie. You can test this out by changing one of the lg_stab variables 
# to a completely bogus name like 'not.real'. In this case you would receive the following message:

#KeyError: 'Variable not.real not in TOC'

def simple_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    
    logconf.data_received_cb.add_callback(log_stab_callback)
    
    logconf.start()
    time.sleep(5)
    logconf.stop()

# Utilized in simple_log_sunc.py
# Takes an instance of scf and the logging configuration and prints logged values
def simple_log(scf, logconf):
    with SyncLogger(scf,lg_stab) as logger:
        for log_entry in logger:
            
            timestamp    = log_entry[0]
            data         = log_entry[1]
            logconf_name = log_entry[2]

            print('[%d][%s]: %s' %(timestamp, logconf_name, data))

            break

# Utilized in simple_connect.py
# Prints simple, pauses for specified time, prints another message
def simple_connect():
    print("Yeah, I'm connected! :D")
    time.sleep(3)
    print("Now I will disconnect :'(")

# Main function
if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    
    # Defining logging configuration
    lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch','float')
    lg_stab.add_variable('stabilizer.yaw',  'float')

    # The syncCrazyflie will create a synchronous Crazyflie instance with the specified link_uri. 
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:

        simple_log_async(scf, lg_stab)

