#import the required modules
import RPi.GPIO as GPIO
import time

class SocketController:
	def __init__( self ):
		# set the pins numbering mode
		# But don't because that's done elsewhere
		#GPIO.setmode( GPIO.BOARD )

		self.control_pins = [ 11, 15, 16, 13 ]

		# Select the GPIO pins used for the encoder K0-K3 data inputs	
		for pin in control_pins:
			GPIO.setup( pin, GPIO.OUT )
			GPIO.output( pin, False )	

		# Select the signal used to select ASK/FSK
		GPIO.setup( 18, GPIO.OUT ) 
		# Set the modulator to ASK for On Off Keying 
		GPIO.output( 18, False )

		# Select the signal used to enable/disable the monitor	
		GPIO.setup( 22, GPIO.OUT )
		# Disable the modulator by setting CE pin lo
		GPIO.output ( 22, False )

		self.control_data = {
			"ALL": [ 1,1,0 ],
			"1":   [ 1,1,1 ],
			"2":   [ 0,1,1 ],
			"3":   [ 1,0,1 ],
			"4":   [ 0,0,1 ],
		}

		self.socketStatus = {
			"1": False,
			"2": False,
			"3": False,
			"4": False
		}

	def reset():
		set_off( "ALL" )
		for pin in self.control_pins:
			GPIO.output( pin, False )
		
	def set_on( plug ):
		if( not type( plug ) == "string" ): plug = str( plug )
		for pin in range( 0, 2 ):
			GPIO.output( self.control_pins[ pin  ], self.control_data[ plug.upper()  ][ pin  ] )
		GPIO.output( 13, True )
		time.sleep( 0.1 )
		GPIO.output( 22, True )
		time.sleep( 0.25 )
		GPIO.output( 22, False )
	
		self.setSocketStatus( plug, True )
		
	def set_off( plug ):
		if( not type( plug ) == "string" ): plug = str( plug )
		for pin in range( 0, 2 ):
			GPIO.output( self.control_pins[ pin  ], self.control_data[ plug.upper()  ][ pin  ] )
		GPIO.output( 13, False )
		time.sleep( 0.1 )
		GPIO.output( 22, True )
		time.sleep( 0.25 )
		GPIO.output( 22, False )
		
		self.setSocketStatus( plug, False )
		
	def setSocketStatus( plug, state ):
		if( plug.upper() == "ALL" ):
			for( plug in self.SocketStatus ):
				plug = state
		else:
			self.SocketStatus[ plug  ] = state

	def getSocketStatus( plug ):
		return self.SocketStatus[ plug  ]