# AutoFisher
# An autoclicker designed to help you autofish
# (c) 2024 - Mitchell Case
# v. 0.1.0
# 
# Requirements:
# This works due to the subtitling accessibility feature. In order for it to
# work properly, subtitles must be enabled and the background set to completely 
# black (for consistency).

import mss
import mss.tools
import pynput.keyboard, pynput.mouse
import time
import os


# Global variables
autoclicker_enabled = False
null_string = 0x000000
catch_reference = 0x000000


def on_press(key):
    global autoclicker_enabled
    global null_string
    global catch_reference

    if key == pynput.keyboard.Key.ctrl_r:

        if (autoclicker_enabled == True):
            # Reset the control values, just in case the player has moved since 
            # the last time they went fishing
            autoclicker_enabled = False
            null_string = 0x000000
            catch_reference = 0x000000
            print("Autofisher disabled.")

        else:
            autoclicker_enabled = True
            calibrate()
            time.sleep(2)


def on_release(key):
    global autoclicker_enabled

    if key == pynput.keyboard.Key.alt_gr:
        autoclicker_enabled = False
        print("Exiting...")
        keyboard_listener.stop()
        os._exit(0)         # This is the only way to permanently drop back to a 
                            # python console at the moment, so this stays
        return False


# Helper function designed to manipulate hexadecimal string values in Python, 
# since this isn't a low-level language by default (damn you untyped languages!)
# Returns as a tuple in format (R, G, B)
def split_hex(value):
    value = int(str(value), 16)
    return hex(value >> 16), hex((value & 0xFF00) >> 8), hex(value & 0xFF)


# Evaluates whether the current value should be considered a false positive 
# (significant change in value compared to the calibration pixel)
def evaluate(reference, current):
    global catch_reference

    reference_tuple = split_hex(reference)
    current_tuple = split_hex(current)

    false_positive = True
    for i in range(0, 3):
        difference = abs(int(str(reference_tuple[i]), 16) - int(str(current_tuple[i]), 16))
        if difference > 3:
            false_positive = False
            break
        
    if not false_positive:
        # On the first go around after calibration, set the catch-reference value
        if catch_reference == 0x000000:
            catch_reference = current

        # Otherwise, see if what we currently have is actually a catch
        else:
            known_catch_tuple = split_hex(catch_reference)
            for i in range(0, 3):
                difference = abs(int(str(known_catch_tuple[i]), 16) - int(str(current_tuple[i]), 16))
                # Unlike the first test, however, the difference should be somewhat the same
                if difference > 5:
                    false_positive = True
                    break

        return not false_positive 

    else:
        return False
    
    # Hedge bets here just in case we get something that doesn't go through 
    # the for loop
    return False


def calibrate():
    global null_string
    calibration_picture = mss.mss().grab(monitor)
    null_string = calibration_picture.rgb.hex()
    print("Calibrated null string to [{0}]".format(null_string))
    print("Autofisher enabled.")
    mss.tools.to_png(calibration_picture.rgb, calibration_picture.size, output="cal.png")
    print("cal.png")



### TUNING FACTORS ###

top = 115           # From the bottom-most pixel on monitor, top of the image
left = 265          # From the right-most pixel on monitor, left of the image

width = 1           # Image pixel width
height = 1          # Image pixel height

main_monitor = 2    # Source monitor to use. Reference your system settings.

use_button = pynput.mouse.Button.right      # Typical use button in Minecraft.
                                            # Alter if necessary: see pynput.

### END TUNING FACTORS ###

mouse_control = pynput.mouse.Controller()


keyboard_controller = pynput.keyboard.Controller()
monitor = {
    "top": mss.mss().monitors[main_monitor]["height"] - top,
    "left": mss.mss().monitors[main_monitor]["width"] - left,
    "width": width,
    "height": height,
    "mon": main_monitor
}


print("When ready, press Right Ctrl...")
keyboard_listener = pynput.keyboard.Listener(on_press=on_press,
                                             on_release=on_release)
keyboard_listener.start()



while True:

    with mss.mss() as screen_capture:

        if autoclicker_enabled == True:

            raw_capture = screen_capture.grab(monitor)
            rgb_values = raw_capture.rgb.hex()

            # First make sure that we actually see something different compared 
            # to the calibration picture
            if evaluate(null_string, rgb_values):
                print("I caught something! [{0}]".format(rgb_values))
                # Reel it in!
                mouse_control.click(use_button, count=1)
                time.sleep(2)       # Trying to time it so the captions go away
                                    # before we cast

                print("Casting...")
                mouse_control.click(use_button, count=1)
                time.sleep(1)
            
            time.sleep(0.5)
