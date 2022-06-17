import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from camera import Camera

from cube import Cube
from draw_mesh import LoadMesh
from draw_mesh2 import LoadMesh2

pygame.init()
eye=[0,0,0]
# project settings
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OpenGL in Python')
cube = LoadMesh("teapot.obj",GL_LINE_LOOP)
camera =Camera()

def initialise():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (screen_width / screen_height), 0.1, 300.0)

def initcamera():
    # modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    camera.update()
    glMatrixMode(GL_PROJECTION)
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    initcamera()    
    glPushMatrix()
    cube.draw()
    glPopMatrix()

done = False
initialise()
glClearColor(0.3,0.1,0.3,1)
while not done:
    glClear(GL_COLOR_BUFFER_BIT)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    display()
    pygame.display.flip()
    #pygame.time.wait(60)
pygame.quit()