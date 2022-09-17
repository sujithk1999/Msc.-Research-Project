# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 13:04:50 2022

@author: Admin
"""

### Importing the libraries that are required for the development and runnung the code##

import sys
import math
import numpy as np
import time
import cv2
import imutils

# These lines of the code is used to start the V-rep simulation 
try:
    import vrep
except:
    print("vrep module cannot be imported properly so please check the files.")
    print("Please be sure that vrep.py file together with remoteApi.dll file is are located in the current path.")



print ('The Program has started to run')
vrep.simxFinish(-1) 


### client ID is required for interfacing the code and the platform ####

clientID = vrep.simxStart('127.0.0.1',19999,True,True,5000,5) 


if clientID != -1:
    print ('The program has Connected to remote API server')
else:
    print("The program has Failed to connect to remote API Server")
   

#### This line of code is used for getting the motor handles ###

errorCode, left_Motor_handle = vrep.simxGetObjectHandle(clientID, 
                                            "Pioneer_p3dx_leftMotor",vrep.simx_opmode_oneshot_wait)
errorCode, right_Motor_handle = vrep.simxGetObjectHandle(clientID, 
                                            "Pioneer_p3dx_rightMotor",vrep.simx_opmode_oneshot_wait)

#this line of the code is to get the sensor values 

sensor_handles = np.zeros(16)
sensor_read_values = np.zeros(16)


detection_Status = np.zeros(16)

#### This line of the code is used for getting the sensor handles ####

for i in range(1, 17):
    errorCode, sensor_handle = vrep.simxGetObjectHandle(clientID, 
                                            "Pioneer_p3dx_ultrasonicSensor" + str(i), vrep.simx_opmode_oneshot_wait)
    sensor_handles[i-1] = sensor_handle
    
    
    errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, sensor_handle, vrep.simx_opmode_streaming)
    
# the motor speed values
v0 = 1.5
v_l = 0
v_r = 0

#### Setting the minimum and the maxumum distance for the detetion and avoiding the obstacle ###

maxDetectionRadius = 0.5 
minSafetyDist = 0.2
braitenbergL = np.array([-0.2,-0.4,-0.6,-0.8,-1,-1.2,-1.4,-1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
braitenbergR = np.array([-1.6,-1.4,-1.2,-1,-0.8,-0.6,-0.4,-0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])


simStatusCheck = vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

## For getting the sensor handles ## 
while True:
    for i in range(1,17):
        # Keep reading data from sensors
        returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, int(sensor_handles[i-1]), vrep.simx_opmode_buffer)
        distToObject = math.sqrt(math.pow(detectedPoint[0], 2) + math.pow(detectedPoint[1], 2) + math.pow(detectedPoint[2], 2)) # Calculate distance to obstacle relative to each sensor 
		
        if (detectionState == True) and (distToObject < maxDetectionRadius):
            if (distToObject < minSafetyDist): 
                distToObject = minSafetyDist
            detection_Status[i-1] = 1-((distToObject - minSafetyDist)/(maxDetectionRadius - minSafetyDist))
        else:
            detection_Status[i-1] = 0
			
    v_l = v0
    v_r = v0
	
    for i in range(1,17):
        v_l = v_l + braitenbergL[i-1] * detection_Status[i-1]
        v_r = v_r + braitenbergR[i-1] * detection_Status[i-1]
		
		
    errorCode = vrep.simxSetJointTargetVelocity(clientID, left_Motor_handle, v_l, vrep.simx_opmode_oneshot)
    errorCode = vrep.simxSetJointTargetVelocity(clientID, right_Motor_handle, v_r, vrep.simx_opmode_oneshot)
print(" The sensor values are:", sensor_read_values)    

