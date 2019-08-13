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
#from adafruit_circuitplayground.express import cpx
import audioio
import board
import digitalio
 
SLOUCH_ANGLE    = 7.0
SLOUCH_TIME     = 3
GRAVITY         = 9.80665

# if present, use this PCM file as the alarm sound
ALARM_SOUND_FILE = 'alarm.wav'
# set to True to immediately loop alarm sound without pausing
LOOP_ALARM = False

# Whether we're using the built-in tones (False) or a sound file (True)
alarm_wave = False

# Initialize target angle to zero
target_angle = 0
slouching = False


def init_audio():
    # make sure the speaker is enabled
    speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
    speaker_enable.switch_to_output(value=True)

def sound_alarm():
    global alarm_wave,audio,wave
    if alarm_wave:
        # play the pcm data
        print("Playing pcm alarm")
        audio.play(wave)
        while audio.playing:
            pass
        print("done")
    else:
        pass
        # Play a tone
        #cpx.play_tone(800, 0.5)


# prepare alarm sound file, if we have one
try:
    wave_file = open(ALARM_SOUND_FILE,"rb")
    wave = audioio.WaveFile(wave_file)
    audio = audioio.AudioOut(board.A0)
    alarm_wave = True
    print("Using wav file")
except:
    # couldn't open alarm file; fall back to built-in tones
    alarm_wave = False
    print("Using tone generator")
    

init_audio()
sound_alarm()
        
# Loop forever
while True:
    time.sleep(1)
    pass
'''
    # Compute current angle
    current_angle = math.asin(-cpx.acceleration[2] / GRAVITY)
    current_angle = math.degrees(current_angle)
    
    # Set target angle on button press
    if cpx.button_a or cpx.button_b:
        target_angle = current_angle
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
'''
