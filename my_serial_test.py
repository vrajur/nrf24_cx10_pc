#Script to test pygame 
#Copied from https://gist.github.com/MarquisLP/b534c95e4a11efaf376e


"""This module contains all of the necessary PyGame components for
running a simplified game loop.
Use it for test cases on PyGame-related code.
"""
import sys
import pygame
from pygame.locals import *
# Import additional modules here.

import serial, time


throttle=1000
aileron=1500
elevator=1500
rudder=1500 # yaw, rotates the drone

tg=10
ag=50
eg=50
rg=50 

values = {
    'throttle' : 1000,
    'aileron'  : 1500,
    'elevator' : 1500,
    'rudder' : 1500, # yaw, rotates the drone
    'tg' : 10,
    'ag' : 50,
    'eg' : 50,
    'rg' : 50
}

arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=0.01)	# Arduino Serial Port Name on Desktop (Ubuntu)
time.sleep(1)	# give the connection a second to settle
#arduino.write("1500, 1500, 1500, 1500\n")


# Feel free to edit these constants to suit your requirements.
FRAME_RATE = 60.0
SCREEN_SIZE = (640, 480)


def pygame_modules_have_loaded():
    success = True

    if not pygame.display.get_init:
        success = False
    if not pygame.font.get_init():
        success = False
    if not pygame.mixer.get_init():
        success = False

    return success

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.font.init()

if pygame_modules_have_loaded():
    game_screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Test')
    clock = pygame.time.Clock()

    def declare_globals():
        # The class(es) that will be tested should be declared and initialized
        # here with the global keyword.
        # Yes, globals are evil, but for a confined test script they will make
        # everything much easier. This way, you can access the class(es) from
        # all three of the methods provided below.
        pass

    def prepare_test():
        # Add in any code that needs to be run before the game loop starts.
        pass

    def handle_input(key, arduino, values):
        # Add in code for input handling.
        # key_name provides the String name of the key that was pressed.
        keyname = pygame.key.name(key)
        print keyname

        #Unpack Values:
        throttle = values['throttle']
        aileron = values['aileron']
        elevator = values['elevator']
        rudder = values['rudder']
        tg = values['tg']
        ag = values['ag']
        eg = values['eg']
        rg = values['rg']


        #Special Keys:
        if key == pygame.K_ESCAPE or key == pygame.K_q:
        	print "[PC]: ESC exiting"
        	safe_quit(arduino)

        elif key == pygame.K_RETURN:
        	print "[PC]: Enter"

        #WASD:
        elif key == pygame.K_w:
        	throttle += tg

        elif key == pygame.K_a:
        	rudder -= rg

        elif key == pygame.K_s:
        	throttle -= tg

        elif key == pygame.K_d:
        	rudder += rg

        #Arrow Keys:
        elif key == pygame.K_DOWN:
        	elevator -= eg

        elif key == pygame.K_UP:
        	elevator += eg
        
        elif key == pygame.K_RIGHT:
        	aileron += ag

        elif key == pygame.K_LEFT:
        	aileron -= ag

        command="%i,%i,%i,%i"% (throttle, aileron, elevator, rudder)
        # string commands to the Arduino are prefaced with  [PC]           
        print "[PC]: "+command 
        arduino.write(command+"\n")

        #Repack Values:
        values['throttle'] = throttle 
        values['aileron'] = aileron 
        values['elevator'] = elevator 
        values['rudder'] = rudder 
        values['tg'] = tg
        values['ag'] = ag
        values['eg'] = eg 
        values['rg'] = rg 

        return values


    def update(screen, time):
        # Add in code to be run during each update cycle.
        # screen provides the PyGame Surface for the game window.
        # time provides the seconds elapsed since the last update.
        pygame.display.update()

    def safe_quit(arduino):
    	# close the connection
	    arduino.close()
	    # re-open the serial port which will also reset the Arduino Uno and
	    # this forces the quadcopter to power off when the radio loses conection. 
	    arduino=serial.Serial('/dev/ttyACM0', 115200, timeout=.01)
	    arduino.close()
	    # close it again so it can be reopened the next time it is run.  

	    pygame.quit()
	    sys.exit()

    def setup():
    	throttle=1000
        aileron=1500
        elevator=1500
        rudder=1500 # yaw, rotates the drone

        tg=10
        ag=50
        eg=50
        rg=50 

        arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=0.01)	# Arduino Serial Port Name on Desktop (Ubuntu)
        time.sleep(1)	# give the connection a second to settle
        #arduino.write("1500, 1500, 1500, 1500\n")

    def keydown_loop(event, arduino, values):
    	while True:
    		key_name = pygame.key.name(event.key)
    		values = handle_input(event.key, arduino, values)

    		for event2 in pygame.event.get():
    			if event2.type == KEYUP:
    				return values

    		time.sleep(.5)



    # Add additional methods here.

    def main():
        declare_globals()
        prepare_test()
        setup()


        values = {
            'throttle' : 1000,
            'aileron'  : 1500,
            'elevator' : 1500,
            'rudder' : 1500, # yaw, rotates the drone 
            'tg' : 10,
            'ag' : 50,
            'eg' : 50, 
            'rg' : 50
            }

        arduino = serial.Serial('/dev/ttyACM0', 115200, timeout = 0.01)
        time.sleep(1) # give the connection a second to settle
        #arduino.write("1500, 1500, 1500, 1500\n")

        print values


        while True:

            data = arduino.readline()
            if data:
                #String responses from Arduino Uno are prefaced with [AU]
                print "[AU]: "+data 

            for event in pygame.event.get():
                if event.type == QUIT:
                    safe_quit(arduino)

                if event.type == KEYDOWN:
                	# keydown_loop(event, arduino, values)
                    key_name = pygame.key.name(event.key)
                    values = handle_input(event.key, arduino, values)

            milliseconds = clock.tick(FRAME_RATE)
            seconds = milliseconds / 1000.0
            update(game_screen, seconds)

            sleep_time = (1000.0 / FRAME_RATE) - milliseconds
            if sleep_time > 0.0:
                pygame.time.wait(int(sleep_time))
            else:
                pygame.time.wait(1)

    main()
