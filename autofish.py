# AutoFisher
# An autoclicker designed to help you autofish
# (c) 2024 - Mitchell Case
# v. 0.0.1
# 
# Requirements:
# This works due to the subtitling accessibility feature. In order for it to
# work properly, subtitles must be enabled and the background set to completely 
# black (for consistency).

import mss
import mss.tools
import pynput.keyboard, pynput.mouse
import time


# Global variables
autoclicker_enabled = False
null_string = 0x000000


def on_press(key):
    global autoclicker_enabled
    global null_string

    if key == pynput.keyboard.Key.ctrl_r:

        if (autoclicker_enabled == True):
            autoclicker_enabled = False
            null_string = 0x000000
            print("Autofisher disabled.")

        else:
            autoclicker_enabled = True
            calibration_picture = mss.mss().grab(monitor)
            null_string = calibration_picture.rgb.hex()
            print("Calibrated null string to [{0}]".format(null_string))
            print("Autofisher enabled.")
            mss.tools.to_png(calibration_picture.rgb, calibration_picture.size, output="cal.png")
            print("cal.png")
            time.sleep(2)


def on_release(key):
    global autoclicker_enabled

    if key == pynput.keyboard.Key.alt_gr:
        print("Autofisher disabled this run. Press [CTRL]+c to exit...")
        autoclicker_enabled = False
        return False


def split_hex(value):
    value = int(str(value), 16)
    return hex(value >> 16), hex((value & 0xFF00) >> 8), hex(value & 0xFF)


def evaluate(reference, current):

    reference_tuple = split_hex(reference)
    current_tuple = split_hex(current)

    # print(reference_tuple)
    # print(current_tuple)

    false_positive = True
    exact_same = False
    for i in range(0, 3):
        difference = int(str(reference_tuple[i]), 16) - int(str(current_tuple[i]), 16)
        if difference > 1:
            false_positive = False
            break
        
        if difference == 0:
            exact_same = True;
            break

    if not false_positive:
        print("Actual catch detected!")
        return True

    else:
        if not exact_same:
            print("False positive detected; likely either nighttime or rain")
            
        return False
    
    # Hedge bets here just in case we get something that doesn't go through 
    # the for loop
    return False



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
