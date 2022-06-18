import os
import time
from turtle import back

from rotation import rotationMatrix, rotationMatrix90

import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from texture_loader import load_texture_pygame
from obj_loader import ObjLoader

from camera import Camera

cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True


def getFileContents(filename):
    p = os.path.join(os.getcwd(), "shaders", filename)
    return open(p, 'r').read()




pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF) # |pygame.FULLSCREEN
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# load here the 3d meshes
cube_indices, cube_buffer = ObjLoader.load_model("meshes/ball minimal.obj")
background_indices, background_buffer = ObjLoader.load_model("universe .obj")
grass_indices, grass_buffer = ObjLoader.load_model("ground space.obj")
trunk_indices, trunk_buffer = ObjLoader.load_model("trunk.obj")
tree_indices, tree_buffer = ObjLoader.load_model("tree.obj") 
vertexShaderContent = getFileContents("object.vertex.shader")
fragmentShaderContent = getFileContents("object.fragment.shader")

vertexShader = compileShader(vertexShaderContent, GL_VERTEX_SHADER)
fragmentShader = compileShader(fragmentShaderContent, GL_FRAGMENT_SHADER)

program = glCreateProgram()
glAttachShader(program, vertexShader)
glAttachShader(program, fragmentShader)
glLinkProgram(program)


# VAO and VBO
VAO = glGenVertexArrays(5)
VBO = glGenBuffers(5)

# cube VAO
glBindVertexArray(VAO[0])
# cube Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, cube_buffer.nbytes, cube_buffer, GL_STATIC_DRAW)

# cube vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(0))
# cube textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(12))
# cube normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

glBindVertexArray(VAO[1])
# cube Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, background_buffer.nbytes, background_buffer, GL_STATIC_DRAW)

# cube vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, background_buffer.itemsize * 8, ctypes.c_void_p(0))
# cube textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, background_buffer.itemsize * 8, ctypes.c_void_p(12))
# cube normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, background_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# grass plane
glBindVertexArray(VAO[2])
# cube Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, grass_buffer.nbytes, grass_buffer, GL_STATIC_DRAW)

# cube vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, grass_buffer.itemsize * 8, ctypes.c_void_p(0))
# cube textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, grass_buffer.itemsize * 8, ctypes.c_void_p(12))
# cube normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, grass_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# grass plane
glBindVertexArray(VAO[3])
# cube Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[3])
glBufferData(GL_ARRAY_BUFFER, trunk_buffer.nbytes, trunk_buffer, GL_STATIC_DRAW)

# cube vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, trunk_buffer.itemsize * 8, ctypes.c_void_p(0))
# cube textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, trunk_buffer.itemsize * 8, ctypes.c_void_p(12))
# cube normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, trunk_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# grass plane
glBindVertexArray(VAO[4])
# cube Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[4])
glBufferData(GL_ARRAY_BUFFER, tree_buffer.nbytes, tree_buffer, GL_STATIC_DRAW)

# cube vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, tree_buffer.itemsize * 8, ctypes.c_void_p(0))
# cube textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, tree_buffer.itemsize * 8, ctypes.c_void_p(12))
# cube normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, tree_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

textures = glGenTextures(5)
load_texture_pygame("ball.png", textures[0])
load_texture_pygame("world.png", textures[1])
load_texture_pygame("grass.jpg", textures[2])
load_texture_pygame("trunk.jpg", textures[3])
load_texture_pygame("tree.png", textures[4])



glUseProgram(program)
glClearColor(0.53, 0.82, 0.92, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
pendulum_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 11.47, 0]))
ground_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([5, 1, 2]))
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-0.3, 8, 0]))

trunk_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([18, 3, -25]))
tree_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([18,2.6,-25]))

trunk_pos_2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([28, 3, -25]))
tree_pos_2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([28,2.6,-25]))

trunk_pos_3 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-15, 3, -25]))
tree_pos_3 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-15,2.6,-25]))

trunk_pos_4 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-18, 3, -10]))
tree_pos_4 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-18,2.6,-10]))  

model_loc = glGetUniformLocation(program, "model")
proj_loc = glGetUniformLocation(program, "projection")
view_loc = glGetUniformLocation(program, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

running = True

i=-40
angle =0
increasing =True
while running:
    #print(i)
    if increasing == True and i>=40:
        increasing = False
    elif increasing == False and i<=-40:
        increasing = True
    elif increasing == True:
        i+=0.1
    elif increasing== False:
        i-=0.1
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        elif  event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.VIDEORESIZE:
            glViewport(0, 0, event.w, event.h)
            projection = pyrr.matrix44.create_perspective_projection_matrix(45, event.w / event.h, 0.1, 100)
            glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a]:
        cam.process_keyboard("LEFT", 0.08)
    if keys_pressed[pygame.K_d]:
        cam.process_keyboard("RIGHT", 0.08)
    if keys_pressed[pygame.K_w]:
        cam.process_keyboard("FORWARD", 0.08)
    if keys_pressed[pygame.K_s]:
        cam.process_keyboard("BACKWARD", 0.08)
    if keys_pressed[pygame.K_LEFT]:
        cam.process_keyboard("L_P", None,  angle + 0.174533)
    if keys_pressed[pygame.K_RIGHT]:
        cam.process_keyboard("R_P", None,  angle + 0.174533)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    

    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    rot_y = rotationMatrix(i)
    model = pyrr.matrix44.multiply(rot_y, pendulum_pos)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(cube_indices))

    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    rot_y = rotationMatrix90(90)
    model = pyrr.matrix44.multiply(rot_y, floor_pos)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(cube_indices))

    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, ground_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(grass_indices))

    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, trunk_pos_2)
    glDrawArrays(GL_TRIANGLES, 0, len(trunk_indices))

    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, tree_pos_2)
    glDrawArrays(GL_TRIANGLES, 0, len(tree_indices))


    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, trunk_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(trunk_indices))

    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, tree_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(tree_indices))


    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, trunk_pos_3)
    glDrawArrays(GL_TRIANGLES, 0, len(trunk_indices))

    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, tree_pos_3)
    glDrawArrays(GL_TRIANGLES, 0, len(tree_indices))


    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, trunk_pos_4)
    glDrawArrays(GL_TRIANGLES, 0, len(trunk_indices))

    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, tree_pos_4)
    glDrawArrays(GL_TRIANGLES, 0, len(tree_indices))

    pygame.display.flip()

pygame.quit()