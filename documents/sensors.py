#import necessary libraries and packages
from time import sleep
import RPi.GPIO as GPIO

#print to make sure program is running
print("Starting up...")

#define which pins your sensors are connected to.
#if you're wiring your own breadboards and need help, pinout.xyz has a reference for which pins are which
pins = [17, 22, 25, 5]

#ask the user to label each detector by which type of particle/marble it'll be sensing at the beginning of the run
detectors = {}
print("Enter what each sensor is detecting:")
for pin in pins:
  name = input(f"GPIO{pin}:").strip()
  if not name: #i.e. if you just hit enter without any text
    name = f"GPIO{pin}"
  detectors[pin] = name #maps each pin number to its chosen name

#create a dictionary that will keep track of how many times each sensor is tripped, starting at 0 each time the program is run
counts = {name: 0 for name in detectors.values()}

#count each time each sensor is tripped
def make_callback(pin, name):
  def callback(channel):
    state = GPIO.input(pin) 
    if state == 1: #for this sensor, HIGH means the beam is broken
      counts[name] += 1
      print(f"{name} (GPIO{pin}): Tripped") #this is for testing your setup. I advise commenting it out when doing mystery particles
  return callback

GPIO.setmode(GPIO.BCM) #use GPIO numbering, not physical pin position

for pin, name in detectors.items():
  GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #PUD_DOWN sets the pin's resting state to LOW
  GPIO.add_event_detect(pin, GPIO.BOTH, callback = make_callback(pin, name), bouncetime = 5) #GPIO.BOTH watches for the pin changing in either direction
  #bouncetime ensures no accidental double triggering

try:
  while True:
    sleep(1) #keeps the program active

#end program with control + c
except KeyboardInterrupt:
  for name in detectors.values():
    print(f"{name} was triggered {counts[name]} times")
  GPIO.cleanup()  #releases the GPIO pins so they're not left 'claimed' for the next run
