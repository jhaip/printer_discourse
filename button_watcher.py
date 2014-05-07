#!/usr/bin/python

from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess, time, socket
from Adafruit_Thermal import *

ledPin       = 18
buttonPin    = 23
holdTime     = 2     # Duration for button hold (shutdown)
tapTime      = 0.01  # Debounce time for button taps
nextInterval = 0.0   # Time of next recurring operation
dailyFlag    = False # Set after daily trigger occurs
lastId       = '1'   # State information passed to/from interval script
printer      = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)


# Called when button is briefly tapped.  Prints out the IP address
def tap():
    GPIO.output(ledPin, GPIO.HIGH)  # LED on while working
    #subprocess.call(["python", "timetemp.py"])
    #printer.feed(3)
    #printer.println("button tapped!")
    #printer.feed(3)
    # Show IP address (if network is available)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        printer.print('My IP address is ' + s.getsockname()[0])
        printer.feed(3)
    except:
        printer.boldOn()
        printer.println('Network is unreachable. Restarting the wifi')
        printer.boldOff()
        printer.feed(3)
        subprocess.call(["sudo", "/etc/init.d/networking", "restart"])
    GPIO.output(ledPin, GPIO.LOW)


# Called when button is held down.  Prints image, invokes shutdown process.
def hold():
    GPIO.output(ledPin, GPIO.HIGH)
    #printer.printImage(Image.open('gfx/goodbye.png'), True)
    printer.feed(3)
    printer.println("powering off");
    printer.feed(3)
    subprocess.call("sync")
    subprocess.call(["shutdown", "-h", "now"])
    GPIO.output(ledPin, GPIO.LOW)


# Initialization

# Use Broadcom pin numbers (not Raspberry Pi pin numbers) for GPIO
GPIO.setmode(GPIO.BCM)

# Enable LED and button (w/pull-up on latter)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LED on while working
GPIO.output(ledPin, GPIO.HIGH)

# Processor load is heavy at startup; wait a moment to avoid
# stalling during greeting.
time.sleep(30)

# Show IP address (if network is available)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    printer.print('My IP address is ' + s.getsockname()[0])
    printer.feed(3)
    printer.println("running startup script")
    subprocess.call(["startprinter.sh",str(sys.argv[1]),str(sys.argv[2])])
except:
    printer.boldOn()
    printer.println('Network is unreachable.')
    printer.boldOff()
    printer.print('Connect display and keyboard\n'
    'for network troubleshooting.')
    printer.feed(3)
    #exit(0)

# Print greeting image
# printer.printImage(Image.open('gfx/hello.png'), True)
printer.println("Hello World!")
printer.feed(3)
GPIO.output(ledPin, GPIO.LOW)

# Poll initial button state and time
prevButtonState = GPIO.input(buttonPin)
prevTime        = time.time()
tapEnable       = False
holdEnable      = False

# Main loop
while(True):

    # Poll current button state and time
    buttonState = GPIO.input(buttonPin)
    t           = time.time()

    # Has button state changed?
    if buttonState != prevButtonState:
        prevButtonState = buttonState   # Yes, save new state/time
        prevTime        = t
    else:                             # Button state unchanged
        if (t - prevTime) >= holdTime:  # Button held more than 'holdTime'?
            # Yes it has.  Is the hold action as-yet untriggered?
            if holdEnable == True:        # Yep!
                hold()                      # Perform hold action (usu. shutdown)
                holdEnable = False          # 1 shot...don't repeat hold action
                tapEnable  = False          # Don't do tap action on release
        elif (t - prevTime) >= tapTime: # Not holdTime.  tapTime elapsed?
            # Yes.  Debounced press or release...
            if buttonState == True:       # Button released?
                if tapEnable == True:       # Ignore if prior hold()
                    tap()                     # Tap triggered (button released)
                    tapEnable  = False        # Disable tap and hold
                    holdEnable = False
            else:                         # Button pressed
                tapEnable  = True           # Enable tap and hold actions
                holdEnable = True

    # LED blinks while idle, for a brief interval every 2 seconds.
    # Pin 18 is PWM-capable and a "sleep throb" would be nice, but
    # the PWM-related library is a hassle for average users to install
    # right now.  Might return to this later when it's more accessible.
    if ((int(t) & 1) == 0) and ((t - int(t)) < 0.15):
        GPIO.output(ledPin, GPIO.HIGH)
    else:
        GPIO.output(ledPin, GPIO.LOW)
