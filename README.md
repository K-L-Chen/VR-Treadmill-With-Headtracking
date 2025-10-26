# VR-Treadmill

Below is the README from the original repository.

script that converts mouse movement into joystick movement for a VR treadmill.
(requires Python3)


to bind the virtual gamepad using steam input, open the script in a text editor and comment out the indicated line. when the bind is set up, uncomment the line and restart the script.


REQUIRED: 

pip install pynput

pip install vgamepad

pip install PyQt6

To permanently change settings, edit treadmill.py and change the vaules between the dashes near the top.

# Additions

In an attempt to add additional functionality to the base source code, this fork's purpose is to try and decouple the movement on the treadmill from the rotation of the user's head.

This is done by multiplying the vector of movement (i.e. walking on the treadmill) by the angle between the direction the user's head is facing and the vector of movement.

NEW REQUIREMENTS:

pip install openvr

