from pynput.keyboard import Key, Listener
from pynput.mouse import Controller
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel
import vgamepad as vg
import openvr
import ctypes

import sys
import time
import openvr

#openvr.init(openvr.VRApplication_Scene)
openvr.init(openvr.VRApplication_Overlay)

poses = []  # Let waitGetPoses populate the poses structure the first time

for i in range(10):
    #	virtual bool GetControllerStateWithPose( ETrackingUniverseOrigin eOrigin, \
    #       vr::TrackedDeviceIndex_t unControllerDeviceIndex, vr::VRControllerState_t *pControllerState, \
    #       uint32_t unControllerStateSize, TrackedDevicePose_t *pTrackedDevicePose ) = 0;
    #poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)
    #hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
    res, state, devposes = openvr.VRSystem().getControllerStateWithPose(0,openvr.k_unTrackedDeviceIndex_Hmd)
    hmd_pose = devposes.mDeviceToAbsoluteTracking
    hmd_angular_velocity = devposes.vAngularVelocity
    #print(hmd_angular_velocity)
    print(hmd_pose)
    print(hmd_pose[0][0])
    print(hmd_angular_velocity[0])
    #print(hmd_pose[0])
    sys.stdout.flush()
    input("Press enter to continue...")

openvr.shutdown()