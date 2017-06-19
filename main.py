#!/usr/bin/env python3
from time import time, sleep
import RPi.GPIO as GPIO
from Controller import SocketController
from InputTransducers import AnalougeInput, DigitalInput
from QPFSQLDB import QPFSQLDB as db

"""
    System setup and configuration
"""

GPIO.setmode( GPIO.BOARD )
GPIO.setwarnings( False )

POLLING_DELAY = 30

MOIST_PIN = 1
TEMP_PIN = 1
LIGHT_PIN = 1

PUMP_THRESHOLD = 2
LIGHT_THRESHOLD = 2

PUMP_SOCKET = 1
LIGHT_SOCKET = 2

MYSQL_HOST = "localhost"
MYSQL_USER = "precision"
MYSQL_PASS = "farming01"
MYSQL_DBSE = "farmingdb"
MYSQL_TABLE = "farmingtable"

"""
    Start the fun 
"""
with db(MYSQL_HOST,MYSQL_USER,MYSQL_PASS,1,MYSQL_DBSE,MYSQL_TABLE,True) as MYSQL_CONN:
    with SocketController() as Controller:
        while True:
            try:

                startTime = time()

                moistureValue = 0
                temperatureValue = 0
                lightValue = 0

                with AnalougeInput( name="Light Dependent Resistor", pin=LIGHT_PIN ) as Input:
                    lightValue = Input.getValue()
                    print( "[ %s ] Reading value of: %u%s" % ( Input.name, lightValue, "" ) )

                    if lightValue > LIGHT_THRESHOLD:
                        Controller.set_on( LIGHT_SOCKET )
                    else:
                        Controller.set_off( LIGHT_SOCKET )

                with AnalougeInput( name="Moisture Sensor", pin=MOIST_PIN ) as Input:
                    moistureValue = Input.getValue()
                    print( "[ %s ] Reading value of: %u%s" % ( Input.name, moistureValue, "" ) )

                    if moistureValue < PUMP_THRESHOLD:
                        Controller.set_on( PUMP_SOCKET )
                    else:
                        Controller.set_off( PUMP_SOCKET )

                with DigitalInput( name="Digital Temperature Sensor", pin=TEMP_PIN ) as Input:
                    temperatureValue = Input.getValue()
                    print( "[ %s ] Reading value of: %u%s" % ( Input.name, temperatureValue, "C" ) )

                MYSQL_CONN.use(MYSQL_DBSE)
                MYSQL_CONN.update(MYSQL_TABLE,moistureValue,temperatureValue,lightValue,moistureValue < PUMP_THRESHOLD,lightValue > LIGHT_THRESHOLD)

                # Sleep for the remainder of 30 seconds
                sleep( POLLING_DELAY - time() + startTime )

            except BaseException:
                print( "Gracefully exiting" )
                MYSQL_CONN.close()
                Controller.reset()
                GPIO.cleanup()
                break