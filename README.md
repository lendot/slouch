# slouch
Slouch detector for Circuit Playground Express

Based off of this [Adafruit tutorial](https://learn.adafruit.com/circuit-playground-slouch-detector).

To use, copy `main.py` to the device. It will beep once when initialized. To set the target posture angle, sit in that position and
press either of the buttons on the CPX. An alarm will sound if you lean more than `SLOUCH_ANGLE` degrees forward or backward.

If you want to play a custom sound for the alarm, create a file called `alarm.wav` and copy it to the device. It must be a 22kHz
or lowe 16-bit mono file. Sample sounds are in the [sounds](sounds) directory.
