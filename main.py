import os
import time
from pygame import mixer
from helpers.rotation import *
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from helpers.texture_loader import load_texture_pygame
from helpers.obj_loader import LoadMesh

from helpers.camera import Camera

cam = Camera()


def buffer_config(vao, vbo, buffer):
    glBindVertexArray(vao)
    # remember to change the method name in the documentation when name changes here

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)


    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(12))

def getFileContents(filename):
    p = os.path.join(os.getcwd(), "shaders", filename)
    return open(p, 'r').read()

def initialise_pygame():
    pygame.init()
    pygame.display.set_mode((1280 , 720), pygame.OPENGL | pygame.DOUBLEBUF)


    # mixer.music.load("images_and_sound/sound.mp3")
    # mixer.music.play(-1)
    # mixer.music.load("images_and_sound/sound2.mp3")
    # mixer.music.play(-1)
    mixer.Channel(0).play(mixer.Sound('images_and_sound/sound.mp3'), -1)
    mixer.Channel(1).play(mixer.Sound('images_and_sound/sound2.mp3'), -1)
initialise_pygame()


pendulum_indices, pendulum_buffer = LoadMesh.load_model("objs/ball minimal.obj")
background_indices, background_buffer = LoadMesh.load_model("objs/universe .obj")
grass_indices, grass_buffer = LoadMesh.load_model("objs/ground space.obj")
trunk_indices, trunk_buffer = LoadMesh.load_model("objs/trunk.obj")
tree_indices, tree_buffer = LoadMesh.load_model("objs/tree.obj") 
vertexShaderContent = getFileContents("object.vertex.shader")
fragmentShaderContent = getFileContents("object.fragment.shader")

vertexShader = compileShader(vertexShaderContent, GL_VERTEX_SHADER)
fragmentShader = compileShader(fragmentShaderContent, GL_FRAGMENT_SHADER)

program = glCreateProgram()
glAttachShader(program, vertexShader)
glAttachShader(program, fragmentShader)
glLinkProgram(program)


VAO = glGenVertexArrays(5)
VBO = glGenBuffers(5)


buffer_config(VAO[0], VBO[0], pendulum_buffer)
buffer_config(VAO[1], VBO[1], background_buffer)
buffer_config(VAO[2], VBO[2], grass_buffer)
buffer_config(VAO[3], VBO[3], trunk_buffer)
buffer_config(VAO[4], VBO[4], tree_buffer)


textures = glGenTextures(5)
load_texture("images_and_sound/ball.png", textures[0])
load_texture("images_and_sound/world.png", textures[1])
load_texture("images_and_sound/grass.jpg", textures[2])
load_texture("images_and_sound/trunk.jpg", textures[3])
load_texture("images_and_sound/tree.png", textures[4])



glUseProgram(program)
glClearColor(0.53, 0.82, 0.92, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


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



i=-40
angle =0
k =0
increasing =True
increasing2= 1 
projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
while True:
    if k >= 0.13 and increasing == False:
        k= 0.13
        increasing2 =0
    if k >= 0.13 and increasing == True:
        k= 0.13
        increasing2 =2
    if k<=0:
        k=0
        increasing2 =1
    if increasing2 == 1:
        k+=0.000345
    if increasing2== 0:
        k-=0.000345
    #print(i)
    if increasing == True and i>=40:
        if increasing2==2:
            increasing2=0
        increasing = False
    elif increasing == False and i<=-40:
        increasing = True
    elif increasing == True:
        i+=0.1
    elif increasing== False:
        i-=0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a]:
        cam.input_keyboard("LEFT", 0.08)
    if keys_pressed[pygame.K_d]:
        cam.input_keyboard("RIGHT", 0.08)
    if keys_pressed[pygame.K_w]:
        cam.input_keyboard("FORWARD", 0.08)
    if keys_pressed[pygame.K_s]:
        cam.input_keyboard("BACKWARD", 0.08)
    if keys_pressed[pygame.K_LEFT]:
        cam.input_keyboard("L_P", None)
    if keys_pressed[pygame.K_RIGHT]:
        cam.input_keyboard("R_P", None)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)



    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    rot_y = rotationMatrix(i)
    model = pyrr.matrix44.multiply(rot_y, pendulum_pos)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(pendulum_indices))

    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    rot_y = rotationMatrix90(90)
    model = pyrr.matrix44.multiply(rot_y, floor_pos)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(pendulum_indices))

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
    rot_y = pyrr.Matrix44.from_z_rotation(k)
    model = pyrr.matrix44.multiply(rot_y, tree_pos_2)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(tree_indices))


    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, trunk_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(trunk_indices))

    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, textures[4])
    rot_y = pyrr.Matrix44.from_z_rotation(k)
    model = pyrr.matrix44.multiply(rot_y, tree_pos)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(tree_indices))


    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, trunk_pos_3)
    glDrawArrays(GL_TRIANGLES, 0, len(trunk_indices))

    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, textures[4])
    rot_y = pyrr.Matrix44.from_z_rotation(k)
    model = pyrr.matrix44.multiply(rot_y, tree_pos_3)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(tree_indices))


    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, trunk_pos_4)
    glDrawArrays(GL_TRIANGLES, 0, len(trunk_indices))

    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, textures[4])
    rot_y = pyrr.Matrix44.from_z_rotation(k)
    model = pyrr.matrix44.multiply(rot_y, tree_pos_4)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(tree_indices))

    pygame.display.flip()
