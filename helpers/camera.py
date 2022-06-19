import math
import numpy as np
import time
from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians

class Camera:
    #status
        #0 =front
        #1 =right
        #2 = back
        #3 =left
        #4 = orginal
    def __init__(self):
        self.camera_pos = Vector3([0.0, 5.0, 25.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])
        self.i =0
        self.status= 4

    def get_view_matrix(self):
        #print(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)
        # print(self.camera_front)
        # print(self.camera_pos)
        if self.status==1:
            return matrix44.create_look_at(np.array([25.6, 4.79, 9.8]),np.array([24.72, 4.8, 9.3]), np.array([0,1,0]) )
        if self.status==3:
            return matrix44.create_look_at(np.array([-27.14, 12.23, -16.19]),np.array([-26.25 , 12.09, -15.76]), np.array([0,1,0]) )
        if self.status ==2:
            return matrix44.create_look_at(np.array([17.14, 13.06, -33.763]),np.array([16.63, 12.95, -32.89]), np.array([0,1,0]))
        if self.status ==0:
            return matrix44.create_look_at(np.array([-14.33, 4.84, 22.99]),np.array([-13.83, 4.83, 22.1351 ]), np.array([0,1,0]))
        
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    

    def input_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            if self.status==4:
                self.camera_pos += self.camera_front * velocity
            else:
                self.i -= 0.8
        if direction == "BACKWARD":
            if self.status ==4:
                self.camera_pos -= self.camera_front * velocity
            else:
                self.i +=0.8
        if direction == "LEFT":
            self.camera_pos -= self.camera_right * velocity
        if direction == "RIGHT":
            self.camera_pos += self.camera_right * velocity
        if direction == "L_P":
            self.i=0
            if self.status ==0:
                self.status =4
            else:
                self.status -=1
            time.sleep(0.2)
        if direction == "R_P":
            self.i=0
            if self.status ==4:
                self.status =0
            else:
                self.status +=1
            time.sleep(0.2)
        