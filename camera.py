import pygame
from OpenGL.GLU import *
from math import *

class Camera:
    #0 - Z-axis
    #1 - -Xaxis
    #2 - -Z-axis
    #3 - X-axis

    def __init__(self) -> None:
        self.orientation =0
        self.forward =30
        self.eye=(0,0,30)
        self.top_view =False
        self.bottom_view =False
    def update(self):
        print("orientation" + str(self.orientation))
        print("forward" + str(self.forward))
        print(self.top_view)
        print(self.bottom_view)
        keys =pygame.key.get_pressed()
        if self.top_view and self.bottom_view:
            self.top_view =False
            self.bottom_view= False
            return self.orientational_method()
        if keys[pygame.K_RIGHT]:
            self.top_view =False
            self.bottom_view= False
            if self.orientation==0:
                self.orientation =3 
            else:
                self.orientation -=1
            return self.orientational_method()
        if keys[pygame.K_LEFT]:
            self.top_view =False
            self.bottom_view= False
            if self.orientation==3:
                self.orientation =0 
            else:
                self.orientation +=1
            return self.orientational_method()
        if keys[pygame.K_UP] and self.top_view==False:
            self.top_view =True
            return self.orientational_method()
        elif keys[pygame.K_DOWN] and self.bottom_view ==False:
            self.bottom_view =True
            return self.orientational_method()
        elif keys[pygame.K_DOWN] and self.top_view==True:
            self.top_view =False
            return self.orientational_method()
        elif keys[pygame.K_UP] and self.bottom_view==True:
            self.bottom_view =False
            return self.orientational_method()
        if keys[pygame.K_w] and self.forward<50:
            self.forward +=1
            return self.orientational_method()
        if keys[pygame.K_x] and self.forward>10:
            self.forward -=1
            return self.orientational_method()
        return self.orientational_method()
    def orientational_method(self):
        if self.top_view and (self.orientation==0 or self.orientation==2):
            return gluLookAt(0, self.forward, 0,0,0,0,0,0,1)
        if self.bottom_view and (self.orientation==0 or self.orientation==2):
            return gluLookAt(0, -self.forward, 0,0,0,0,0,0,1)
        if self.top_view and (self.orientation==1 or self.orientation==3):
            return gluLookAt(0, self.forward, 0,0,0,0,1,0,0)
        if self.bottom_view and (self.orientation==1 or self.orientation==3):
            return gluLookAt(0, -self.forward, 0,0,0,0,1,0,0)
        elif self.orientation == 0 :
            return gluLookAt(0, 4, self.forward,0,0,0,0,1,0)
        elif self.orientation == 1:
            return gluLookAt(-self.forward, 4, 0,0,0,0,0,1,0)
        elif self.orientation == 2:
            return gluLookAt(0, 4, -self.forward,0,0,0,0,1,0)
        elif self.orientation == 3:
            return gluLookAt(self.forward, 4, 0,0,0,0,0,1,0)


















# def __init__(self):
#         self.eye =pygame.math.Vector3(0,0,-28)
#         self.up =pygame.math.Vector3(0,1,0)
#         self.right =pygame.math.Vector3(1,0,0)
#         self.forward =pygame.math.Vector3(0,0,1)
#         self.look =self.eye + self.forward
#     def update(self,):
#         keys =pygame.key.get_pressed()
#         if keys[pygame.K_DOWN]:
#             print(self.eye)
#             self.eye -= self.forward
#         if keys[pygame.K_UP]:
#             self.eye += self.forward
#         if keys[pygame.K_RIGHT]:
#             self.eye += self.right
#         if keys[pygame.K_LEFT]:
#             self.eye -= self.right
#         self.look =self.eye +self.forward
#         gluLookAt(
#             self.eye.x, self.eye.y,self.eye.z,
#             self.look.x,self.look.y,self.look.z,
#             self.up.x, self.up.y, self.up.z
#         )