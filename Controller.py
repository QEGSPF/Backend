#import the required modules
import RPi.GPIO as GPIO
import time

class PowerController:
	def __init__( self ):
		# set the pins numbering mode
		GPIO.setmode(GPIO.BOARD)
	
		self.__controlPins = [11, 15, 16, 13]

		# Select the GPIO pins used for the encoder K0-K3 data inputs	
		for pin in self.__controlPins:
			GPIO.setup( pin, GPIO.OUT )
			GPIO.output( pin, False )	

		# Select the signal used to select ASK/FSK
		GPIO.setup( 18, GPIO.OUT ) 
		# Set the modulator to ASK for On Off Keying 
		GPIO.output( 18, False )
	
		# Select the signal used to enable/disable the monitor	
		GPIO.setup(22, GPIO.OUT)
		# Disable the modulator by setting CE pin lo
		GPIO.output (22, False)
		
		self.__setup = [
			{
				"ALL": [1,1,0,1],
				"1":   [1,1,1,1],
				"2":   [0,1,1,1],
				"3":   [1,0,1,1],
				"4":   [0,0,1,1],
			},
			{
				"ALL": [1,1,0,0],
				"1":   [1,1,1,0],
				"2":   [0,1,1,0],
				"3":   [1,0,1,0],
				"4":   [0,0,1,0],
			}
		]

		self.__plugStatus = [0,0,0,0]

	def resetTX( self ):
		self.setPlugOff( "ALL" )
		for pin in self.__controlPins:
			GPIO.output( pin, False )

	def setPlugOn( self, plug ):
		currentPin = 0
		for pin in self.__controlPins:
			GPIO.output( pin, self.__setup[ 0 ][ plug.upper() ][ currentPin ] )
			currentPin += 1
		time.sleep( 0.1 )
		GPIO.output( 22, True )
		time.sleep( 0.25 )
		GPIO.output( 22, False )

	def setPlugOff( self, plug ):
		currentPin = 0
		for pin in self.__controlPins:
			GPIO.output( pin, self.__setup[ 1 ][ plug.upper() ][ currentPin ] )
			currentPin += 1
		time.sleep( 0.1 )
		GPIO.output( 22, True )
		time.sleep( 0.25 )
		GPIO.output( 22, False )
"""
Controller = PowerController()
Controller.setPlugOn( "ALL" )
time.sleep(1)
Controller.setPlugOff( "ALL" )
time.sleep(1)
Controller.setPlugOn( "1" )
time.sleep(1)
Controller.setPlugOn( "2" )
time.sleep(1)
Controller.setPlugOn( "3" )
time.sleep(1)
Controller.setPlugOn( "4" )
time.sleep(1)
Controller.setPlugOff( "4" )
time.sleep(1)
Controller.setPlugOff( "3" )
time.sleep(1)
Controller.setPlugOff( "2" )
time.sleep(1)
Controller.setPlugOff( "1" )
time.sleep(1)
Controller.resetTX()
"""
