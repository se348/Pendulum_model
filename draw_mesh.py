from OpenGL.GL import *
from Mesh import *
import pygame

class LoadMesh(Mesh):

    def __init__(self, filename, draw_type):
        self.vertices = []
        self.triangles =[]
        self.filename =filename
        self.draw_type =GL_TRIANGLE_STRIP
        self.load_drawing()
    def load_drawing(self):
        with open(self.filename) as fp:
            line =fp.readline()
            line2 =0
            while line:
                line2+=1
                print(line2)
                if line[:2] == "v ":
                    vx, vy, vz =[float(value) for value in line[2:].split()]
                    self.vertices.append((vx, vy, vz))
                if line[:2] == "f ":
                    t1, t2, t3= [value for value in line[2:].split()]
                    self.triangles.append([int(value) for value in t1.split('/')][0] - 1)
                    self.triangles.append([int(value) for value in t2.split('/')][0] - 1)
                    self.triangles.append([int(value) for value in t3.split('/')][0] - 1)
                line =fp.readline()
    def draw(self):
        for t in range(0, len(self.triangles) , 3):
            glBegin(self.draw_type)
            glVertex3fv(self.vertices[self.triangles[t]])
            glVertex3fv(self.vertices[self.triangles[t + 1]])
            glVertex3fv(self.vertices[self.triangles[t + 2]])
            glEnd()