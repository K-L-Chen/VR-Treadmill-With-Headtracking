import time
from pynput.keyboard import Key, Listener
from pynput.mouse import Controller, Button, Listener as mouse_listener
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel
import vgamepad as vg
from math import cos, sin
import openvr
import ctypes

gamepad = vg.VX360Gamepad()
mouse = Controller()
enabled = True
keyToggle = False
clickToggle = False
clickStop = False
# -------------------------------------------------------------------
sensitivity = 75 # How sensitive the joystick will be
pollRate = 30 # How many times per second the mouse will be checked
quitKey = Key.ctrl_r # Which key will stop the program
mouseX = 700 #reset x position for mouse
mouseY = 500 #reset y position for mouse
base_hmd_pose = None
# -------------------------------------------------------------------

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        global base_hmd_pose

        self.setWindowTitle("Maratron")
        
        startJoy = QPushButton("Start")
        startJoy.clicked.connect(self.run)
        
        self.setKeyButton = QPushButton("Set Stop Key")
        self.setKeyButton.clicked.connect(self.setKey)
        
        pollLabel = QLabel("Polling Rate (/sec):")
        
        senseLabel = QLabel("Sensitivity:")
        
        self.keyLabel = QLabel("Stop Key: " + str(quitKey))
        
        pollRateLine = QLineEdit(str(pollRate))
        pollRateLine.textChanged.connect(self.setPollingRate)
        
        senseLine = QLineEdit(str(sensitivity))
        senseLine.textChanged.connect(self.setSensitivity)
        
        layout = QVBoxLayout()
        
        layout.addWidget(startJoy)
        layout.addWidget(senseLabel)
        layout.addWidget(senseLine)
        layout.addWidget(pollLabel)
        layout.addWidget(pollRateLine)
        layout.addWidget(self.keyLabel)
        layout.addWidget(self.setKeyButton)
        
        self.setLayout(layout)
        self.show()
        #vr_system = openvr.init(openvr.VRApplication_Scene)
        openvr.init(openvr.VRApplication_Overlay)
        _, _, devposes = openvr.VRSystem().getControllerStateWithPose(1,openvr.k_unTrackedDeviceIndex_Hmd)
        base_hmd_pose = devposes.mDeviceToAbsoluteTracking

        
    def setPollingRate(a, b):
        global pollRate
        if b != "":
            pollRate = int(b)
            print("Poll rate:", b)
    
    def setSensitivity(a, b):
        global sensitivity
        if b != "":
            sensitivity = int(b)
            print("Sensitivity:", b)
            
    def setKey(a, b):
        global quitKey
        global keyToggle
        if not keyToggle:
            a.keyLabel.setText("PRESS ANY KEY")
            a.setKeyButton.setText("Confirm?")
            print("Listening...")
            keyToggle = True
        else:
            a.keyLabel.setText("Stop Key: " + str(quitKey))
            a.setKeyButton.setText("Set Stop Key")
            print("Confirmed")
            keyToggle = False
        
    def run(a, b):
        global enabled
        global keyToggle
        global mouseX
        global mouseY

        #Rotate the forward movement vector by the gyro status of the headset using pyopenvr
        #This way, we can go and look around without having the legs follow where we're facing.
        #TODO implement a way to stop this function
        #@return tuple, x_value and y_value
        def rotate(mousey:int):
            global vr_system
            global base_hmd_pose
            global clickToggle

            if not clickToggle:
                #TODO calculate theta from HMD reading, last position
                _, _, devposes = openvr.VRSystem().getControllerStateWithPose(1,openvr.k_unTrackedDeviceIndex_Hmd)
                if base_hmd_pose != None:
                    hmd_pose = devposes.mDeviceToAbsoluteTracking
                    hmd_ang_vel = devposes.vAngularVelocity[0] #we only care about X rotation
                    #if the change is not significant from a physical distance standpoint,
                    #we don't care either
                    if abs(hmd_pose[0][3] - base_hmd_pose[0][3]) > 0.1:
                        #calculate theta from the angular rate of change * time elaped since
                        #last poll (i.e. 1 / pollRate)
                        #only calc if change is significant (> 1 deg, ~ 0.0175 rad)
                        change = hmd_ang_vel * (1 / pollRate)
                        if (change * change > 0.0003):
                            theta += change
                else:
                    theta = 0

                cost = cos(theta)
                sint = sin(theta)
                if theta < 0:
                    return (int(mousey * sint), int(mousey * cost))
                else:
                    return (int((-1) * mousey * sint), int(mousey * cost))
            else:
                return (0, mousey)

        enabled = True
        mousey = 0
        mousey1 = 0
        mousey2 = 0
        while enabled and not keyToggle:
            mousey2 = mousey1
            mousey1 = 0
            
            mousey1 = (mouse.position[1] - mouseY) * -(sensitivity) # convert mouse position to joystick value
            
            mousey = max(-32768, min(32767, int((mousey1 + mousey2)/2))) # average and clamp
            mouse.position = (mouseX, mouseY)
            print("Joystick y:", mousey)
            
            xval, yval = rotate(mousey)
            gamepad.left_joystick(xval, yval)  # values between -32768 and 32767
            
            gamepad.update()
            
            time.sleep(1 / pollRate)
        
def onPress(key):
    global enabled
    global keyToggle
    global quitKey

    if keyToggle:
        print("Stop key will be", str(key))
        quitKey = key
    elif key == quitKey:
        enabled = False 
        print("Stopped with", quitKey)

def onClick(x, y, button, pressed):
    global clickToggle
    global clickStop
    
    if button == Button.left:
        clickToggle = True

    elif button == Button.right:
        clickStop = True
        return False

def main():            
    listener = Listener(onPress)
    mlistener = mouse_listener(on_click=onClick)
    listener.start()
    mlistener.start()
            
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
    return

if __name__ == "__main__":
    main()
