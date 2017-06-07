import RPi.GPIO as GPIO
from time import sleep

class InputTransducer:
	def __init__( self, *, name="InputTransducer", pin=0 ):
		self.name = name
		self.pin = pin
		
	def getValue():
		return 0
		
class AnalougeInput( InputTransducer ):

	def getValue():
		lastMeasure = 0
		# Discharge capacitor
		GPIO.setup( self.pin, GPIO.OUT )
		GPIO.output( self.pin, GPIO.LOW )
		sleep( 0.1 )

		GPIO.setup( self.pin, GPIO.IN )
		# Count loops until voltage across
		# capacitor reads high on GPIO
		# Unreliable, but perhaps better than enforcing delays
		while ( GPIO.input( self.pin ) == GPIO.LOW ):
			lastMeasure += 1

		return lastMeasure
		
class DigitalInput( InputTransducer ):
	
	def __init__( self, *, id=None ):
		self.deviceID == id
	
	def getValue():
		try:
			mytemp = 0
			filename = 'w1_slave'
			f = open( '/sys/bus/w1/devices/' + self.deviceID + '/' + filename, 'r' )
			line = f.readline() # read 1st line
			crc = line.rsplit( ' ',1 )
			crc = crc[ 1 ].replace( '\n', '' )
			
			if crc=='YES':
			
			  line = f.readline() # read 2nd line
			  mytemp = line.rsplit( 't=',1 ) / float( 1000 )
			  
			else:
			
			  mytemp = -1
			  
			f.close()

			return int( mytemp[ 1 ] )

		  except:
		  
			return -1