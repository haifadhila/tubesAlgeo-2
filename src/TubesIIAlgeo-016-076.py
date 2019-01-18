# TUGAS BESAR II IF2123 ALJABAR GEOMETRI
# Simulasi Transformasi Linier pada Bidang 2D Dengan Menggunakan OpenGL API
# NAMA / NIM :  ADYLAN ROAFFA ILMY / 13516016
#               HAIFA FADHILA ILMA / 13516076
# KELAS     :   K-01

import numpy as np
import time
import thread
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from copy import deepcopy

window = 0                                             # glut window number
width, height = 800, 600                               # window size
drawn = False
STEP = 50
DELAY = 0.02
DEGREE_TO_RAD = 0.0174533

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1*(width/2), width/2, -1*(height/2), height/2, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def idle_draw(points):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    glClearColor(1,1,1,0)
    glLoadIdentity()                                   # reset position
    refresh2d(width, height)                           # set mode to 2d
    glColor3f(1.0, 1.0, 1.0)
    draw_grids()
    draw_line()

    glColor3f(0.0, 0.0, 1.0)
    draw_shape(points)

    glutSwapBuffers()

def draw_shape(points):
    glBegin(GL_POLYGON)
    for vertex in points:
        glVertex2fv(vertex)
    glEnd()

def draw_line():
    glColor3f(0,0,0)
    glBegin(GL_LINES)                                  # start drawing a rectangle
    glVertex2f(0, height)                                   # bottom left point
    glVertex2f(0, -1*height)                           # bottom right point
    glVertex2f(width, 0)                  # top right point
    glVertex2f(-1 * width, 0)                          # top left point
    glEnd()

def draw_grids():
    glColor3f(0.9,0.9,0.9)
    glLineWidth(0.1)
    glBegin(GL_LINES)
    for i in range(-height,height,20):
        glVertex2f(width,i)
        glVertex2f(-width,i)
    for i in range(-width,width,20):
        glVertex2f(i,-height)
        glVertex2f(i,height)
    glEnd()

def input_vertices():
    global current_vertices
    global n
    global drawn
    global initial_vertices

    n = input()
    initial_vertices = []
    for i in range(n):
        p  = map(float,raw_input().split(","))
        initial_vertices = np.append(initial_vertices,p)
    initial_vertices.resize(n,2)
    current_vertices = np.array(initial_vertices)
    drawn = True

def animate_transformation(current_vertices,func, *args):
    if (func == rotate_vertices):
        degreeStep = args[0]/STEP
        for i_step in range(STEP):
            current_vertices = rotate_vertices(current_vertices,    degreeStep,args[1],args[2])
            time.sleep(DELAY)

    else:
        temp_vertices = deepcopy(current_vertices)
        result_vertices = np.array(func(temp_vertices,*args))
        diff_vertices = result_vertices - current_vertices

        diff_vertices /= STEP

        while (not np.allclose(result_vertices,current_vertices)) :
            current_vertices += diff_vertices
            time.sleep(DELAY)


# TRANSLATION
def translate_vertices(current_vertices,dx,dy):
    for vertex in current_vertices:
        vertex += [dx,dy]

    return current_vertices

# DILATION
def dilate_vertices(vertices,k):
    vertices*=k
    return vertices

# REFLECTION IN POINT
def reflectpoint_vertices(current_vertices, dx, dy):
    current_vertices[:,0] = 2*dx - current_vertices[:,0]
    current_vertices[:,1] = 2*dy - current_vertices[:,1]
    return current_vertices

# REFLECTION IN LINE (AXIS)
def reflectline_vertices(current_vertices, line):
    tempx = []
    tempy = []
    tempx = np.append(tempx,current_vertices[:,0])
    tempy = np.append(tempy,current_vertices[:,1])
    if (line=='y=x'):
        current_vertices[:,0] = tempy
        current_vertices[:,1] = tempx
    elif (line=='y=-x'):
        current_vertices[:,0] = -1*tempy
        current_vertices[:,1] = -1*tempx
    elif (line=='x'):
        current_vertices[:,1] *= -1
    elif (line=='y'):
        current_vertices[:,0] *= -1
    return current_vertices

# ROTATE
def rotate_vertices(current_vertices, angle, pointA, pointB):

    tempx = []
    tempy = []
    tempx = np.append(tempx,current_vertices[:,0])
    tempy = np.append(tempy,current_vertices[:,1])
    angle *= DEGREE_TO_RAD
    current_vertices[:,0] = ((tempx-pointA)*math.cos(angle))-((tempy-pointB)*math.sin(angle)) + pointA
    current_vertices[:,1] = ((tempx-pointA)*math.sin(angle))+((tempy-pointB)*math.cos(angle)) + pointB
    return current_vertices

# SHEAR
def shear_vertices(current_vertices, param, k):
    if (param == 'x'):
        current_vertices[:,0] += k*current_vertices[:,1];
    elif (param == 'y'):
        current_vertices[:,1] += k*current_vertices[:,0];
    return current_vertices

# STRETCH
def stretch_vertices(current_vertices, param, k):
    if (param == 'x'):
        current_vertices[:,0] *= k
    elif (param == 'y'):
        current_vertices[:,1] *= k
    return current_vertices

# CUSTOM TRANSFORMATION
def custom_transform_vertices(current_vertices,command):
    matrix = []
    for i in range(1,len(command)):
        p  = float(command[i])
        matrix = np.append(matrix,p)
    matrix.resize(2,2)

    current_vertices = np.dot(current_vertices,matrix)
    return current_vertices

# MULTIPLE COMMANDS
def multiple_commands(current_vertices,n):
    command_list=[]
    i=0
    while (i<n):
        current_command = raw_input().split(" ")
        if (not (current_command[0] == 'multiple' or current_command[0] == 'reset' or current_command[0] == 'exit')):
            command_list.append(current_command)
            i+=1
        else :
            print "Ulangi input"

    for command in command_list:
        try:
            command_action(current_vertices, command)
            # print command
        except ValueError as e:
            print "\nInput salah\n"

# RESET VERTICES
def reset_vertices(current_vertices):
    current_vertices = deepcopy(initial_vertices)
    return current_vertices


def command_action(current_vertices,command):

    try :

        if (command[0]=='translate'):
                dx = float(command[1])
                dy = float(command[2])
                animate_transformation(current_vertices,translate_vertices,dx,dy)

        elif (command[0] =='dilate'):
            k = float(command[1])
            animate_transformation(current_vertices,dilate_vertices,k)

        elif (command[0] == 'reflect'):
            if (command[1] == 'y=x' or command[1] == 'y=-x' or command[1] == 'x' or command[1] == 'y'):
                line = command[1]
                animate_transformation(current_vertices,reflectline_vertices, line)

            else:
                point = command[1].split(",")
                dx = float(point[0].replace('(', ''))
                dy = float(point[1].replace(')', ''))
                animate_transformation(current_vertices,reflectpoint_vertices,dx,dy)

        elif (command[0] == 'rotate'):
            angle = float(command[1])
            a = float(command[2])
            b = float(command[3])
            animate_transformation(current_vertices,rotate_vertices,angle,a,b)

        elif (command[0] == 'shear'):
            param = command[1]
            k = float(command[2])
            animate_transformation(current_vertices,shear_vertices,param,k)

        elif (command[0] == 'stretch'):
            param = command[1]
            k = float(command[2])
            animate_transformation(current_vertices,stretch_vertices,param,k)

        elif (command[0] =='custom' and not len(command[1])==0):
            animate_transformation(current_vertices,custom_transform_vertices,command)

        elif (command[0] =='reset'):
            animate_transformation(current_vertices,reset_vertices)

        elif (command[0] =='multiple'):
            n = int(command[1])
            multiple_commands(current_vertices,n)

        elif (command[0] =='exit'):
            glutLeaveMainLoop()

        else :
            print "Wrong input"

    except IndexError as e:
        print "\nInput salah\n"

def get_command():
    if (drawn):
        global current_vertices
        command = raw_input().split(" ")

        try:
            command_action(current_vertices,command)
        except ValueError as e:
            print "\nInput salah\n"

        get_command()

def draw():
    idle_draw(current_vertices)


# initialization
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(500, 100)
    thread.start_new_thread(get_command,())
    window = glutCreateWindow("Tugas Besar Aljabar Geometri - 2EZ4ANH")
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutMainLoop()

def start():
    while (not drawn):
        print "Enter the vertices"
        try:
            input_vertices()
        except ValueError as e:
            print "Input salah, mohon ulangi"

    main()


start()
