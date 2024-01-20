# Minecraft Autofisher Script

This is a simple script written in Python that autofishes for you. That's all 
it does --- nothing else. Set up your character in prime fishing location, then 
run `python autofish.py` in a terminal window and follow the instructions.

The script defaults to using Right [CTRL] as the on/off key. When the script is 
disabled, you can just leave it running in the background while you go and do 
other things. When you're ready, press [CTRL] again to re-enable the script.
Close via [CTRL]+C in the terminal window.

If you don't have python installed, I recommend grabbing 
[Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) as it's a 
reasonably small python distribution for most use cases. The other two packages 
you will need at a minimum are `pynput` and `mss`. Those can be installed with 
`pip install pynput mss` -- it should pull in all relevant dependencies if it 
needs anything else.

## Caveats

This script takes advantage of the subtitling system built into Minecraft, so 
you'll need to turn on subtitles.

In addition, the script needs to be "calibrated" in a sense, so you'll need to 
play with the script settings a little bit to find the optimum settings for your 
AFK use case. 

This script does not work when Minecraft is full screened; the script will just 
see the pause screen instead of the pixels that you see.

If a wandering trader comes within the vicinity, it will fuck up the script since 
the length of their subtitles is about the length of the subtitles that this 
script is looking for. Them basterds.