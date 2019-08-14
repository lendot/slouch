# Circuit Playground Express Slouch Detector v3
#
# Push button(s) to set a target angle.
# Compute current angle using accelerometer and compare
# to preset slouch angle. Sound alarm if slouching after
# a preset period of time.
#
# Author: Carter Nelson
# MIT License (https://opensource.org/licenses/MIT)
import time
import math
from adafruit_circuitplayground.express import cpx
 
SLOUCH_ANGLE    = 7.0
SLOUCH_TIME     = 3
GRAVITY         = 9.80665

# if present, use this PCM file as the alarm sound
# file must be a 22kHz or lower 16-bit mono .wav
ALARM_SOUND_FILE = 'alarm.wav'

# set to True to immediately loop alarm sound without pausing
LOOP_ALARM = False

# Initialize target angle to zero
target_angle = 0
slouching = False


# number of readings to smooth over
NUM_READINGS = 5

angle_readings = [0]*NUM_READINGS
reading_idx = 0


# see whether there's an alam sound file to play
# Is there a better way to do this? CircuitPython doesn't have os.path
try:
    test_file = open(ALARM_SOUND_FILE,"rb")
    test_file.close()
    alarm_wave = True
except:
    alarm_wave = False


def sound_alarm():
    if alarm_wave:
        # play the pcm data
        cpx.play_file(ALARM_SOUND_FILE)
    else:
        # play a tone
        cpx.play_tone(800,0.5)

# return a smoothing of readings--highest/lowest readings ignored, remainder averaged
def smoothed_reading(values):
    min_idx=-1
    max_idx=-1
    min_value=1000
    max_value=-1000
    for i in range(len(values)):
        val=values[i]
        if val > max_value:
            max_value=val
            max_idx=i
        if val < min_value:
            min_value=val
            min_idx=i
    n=0
    acc=0.0
#    print ("(min,max) = "+str(min_value)+","+str(max_value)+")")
    for i in range(len(values)):
        if i==min_idx or i==max_idx:
#            print("ignoring "+str(values[i]))
            continue
        acc+=values[i]
        n+=1
    return acc/n

# get the angle from the current accelerometer reading
def get_angle():
    angle_reading = math.asin(-cpx.acceleration[2] / GRAVITY)
    return math.degrees(angle_reading)
        
# prime the accelerometer readings buffer
for i in range(NUM_READINGS):
    angle_readings[i] = get_angle()

# signal initialization is done    
cpx.play_tone(1000,0.2)
        
# Loop forever
while True:

    if not slouching:
        angle_reading = get_angle()
        angle_readings[reading_idx] = angle_reading
        reading_idx += 1
        if reading_idx >= NUM_READINGS:
            reading_idx = 0
    else:
        # sounds play synchronously so we need to take readings in rapid succession in this loop
        for i in range(NUM_READINGS):
            angle_readings[i] = get_angle()
        reading_idx = 0

    current_angle = smoothed_reading(angle_readings)
#    print(current_angle)
    
    # Set target angle on button press
    if cpx.button_a or cpx.button_b:
        target_angle = current_angle
        print("New target_angle: "+str(target_angle))
        cpx.play_tone(900, 0.1)
        time.sleep(0.1)
        cpx.play_tone(900, 0.1)
        time.sleep(0.1)
        
    # Check for slouching
    angle_diff = current_angle - target_angle
    if angle_diff > SLOUCH_ANGLE or angle_diff < -SLOUCH_ANGLE:
        if not slouching:
            slouch_start_time = time.monotonic()
        slouching = True
    else:
        slouching = False
        
    # If we are slouching
    if slouching:
        # Check how long we've been slouching
        if time.monotonic() - slouch_start_time > SLOUCH_TIME:
            sound_alarm()
            if not LOOP_ALARM:
                time.sleep(0.3)
