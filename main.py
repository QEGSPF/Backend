#!/usr/bin/env python3
from pmysql.cursors import DictCursor
from pmysql import connect
from time import time, sleep
import RPi.GPIO as GPIO
from Controller import SocketController
from InputTransducers import InputTransducer, AnalougeInput, DigitalInput

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

"""
    Start the fun 
"""
with connect( host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASS, db=MYSQL_DBSE, charset="utf8mb4", cursorclass=DictCursor ) as MYSQL_CONN:
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
                
                with MYSQL_CONN.cursor() as cursor:
                    # Add record
                    cursor.execute( "INSERT INTO `pfdata` ( `time`, `moisture`, `temperature`, `light`, `pump_on`, `light_on` ) VALUES ( NOW(), %s, %s, %s, %s, %s )", ( moistureValue, temperatureValue, lightValue, Controller.getSocketStatus( PUMP_SOCKET ), Controller.getSocketStatus( LIGHT_SOCKET ) ) )
                    MYSQL_CONN.commit()

                # Sleep for the remainder of 30 seconds
                sleep( POLLING_DELAY - time() + startTime )
                
            except BaseException:
                print( "Gracefully exiting" )
                MYSQL_CONN.close()
                Controller.reset()
                GPIO.cleanup()
                break 