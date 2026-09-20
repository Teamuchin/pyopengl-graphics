# CENG 487 Assignment3 by
# Timuçin Topcu
# StudentId:310201095
# 05 2025

# Note:
# -----
# This Uses PyOpenGL and PyOpenGL_accelerate packages.  It also uses GLUT for UI.
# To get proper GLUT support on linux don't forget to install python-opengl package using apt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import vec3d
import globj
import time
import copy
import camera
import wavefrontObjReader

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

# Global objects and variables
currentobj = None
current_subdivisions = []
current_obj_default_pos = globj.globj()
subdindex = 0
render_in_progress = False
subdivision_timestamp = 0  # Track when the last subdivision occurred
subdivision_cooldown = 1  # Cooldown time in seconds
width, height = 1920, 1080
scenecamera = camera.camera()
scenecamera.setsensitivity(width, height)
left_mouse_down = False
right_mouse_down = False
objreader = wavefrontObjReader.wavefrontObjReader()


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):  # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)  # This Will Clear The Background Color To Black
    glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
    glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reset The Projection Matrix
    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


def draw_text(text, x, y, font=GLUT_BITMAP_HELVETICA_18, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(font, ord(character))


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    scenecamera.setsensitivity(Width, Height)


def readObj():
    global currentobj
    currentobj = objreader.readAllObj(sys.argv[1])[0]
    currentobj.calculate_center()


def detect_mouse_click(button, state, x, y):
    global left_mouse_down, right_mouse_down
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            left_mouse_down = True
        elif state == GLUT_UP:
            left_mouse_down = False
    elif button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            right_mouse_down = True
        elif state == GLUT_UP:
            right_mouse_down = False


def detect_mouse_motion(x, y):
    if left_mouse_down:
        mods = glutGetModifiers()
        if mods & GLUT_ACTIVE_ALT:
            scenecamera.turncamera(x, y, currentobj)
        else:
            scenecamera.movecamera(x, y, currentobj)
    if right_mouse_down:
        mods = glutGetModifiers()
        if mods & GLUT_ACTIVE_ALT:
            scenecamera.movecameradepth(y, currentobj)


# The main drawing function.
def DrawGLScene():
    global currentobj

    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset The View

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    draw_text("CENG 487 Assignment 3 by: Timuçin TOPCU", 10, height - 20, GLUT_BITMAP_HELVETICA_18, (1.0, 1.0, 0.0))

    # Display current object name and controls
    if currentobj:
        draw_text(f"Object: {currentobj.getname()}", 10, height - 40, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
        draw_text("Controls:", 10, height - 60, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
        draw_text("  ESC: Quit", 10, height - 80, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
        draw_text("  m: Switch view mode", 10, height - 100, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
        draw_text("  +/-: Increase/decrease subdivision level", 10, height - 140, GLUT_BITMAP_HELVETICA_12,
                  (0.7, 0.7, 1.0))
        draw_text("  Drag Mouse While Pressing Left Click to Move Camera", 10, height - 160, GLUT_BITMAP_HELVETICA_12,
                  (0.7, 0.7, 1.0))
        draw_text("  Drag Mouse While Pressing Left Click + Alt to Turn Camera", 10, height - 180,
                  GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
        draw_text("  Drag Mouse On Y Axis While Pressing Right Click + Alt to Move Camera Depth", 10, height - 200,
                  GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
        draw_text("  f: Reset Camera", 10, height - 220, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))

        if len(current_subdivisions) > 0:
            draw_text(f"Subdivision Level: {subdindex}", 10, 60, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
        draw_text(f"Render Mode: {currentobj.getrender()}", 10, 20, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glLoadIdentity()

    # Move into the screen 6.0 units.
    glTranslatef(0, 0.0, -6.0)

    if currentobj:
        currentobj.drawobj()

    # Swap the buffers to display the scene
    glutSwapBuffers()


def NextSubdivison():
    global currentobj, subdindex, current_subdivisions, render_in_progress
    try:
        current_render_mode = currentobj.getrender()  # Get current render mode

        if subdindex < len(current_subdivisions) - 1:
            subdindex += 1
            currentobj = copy.deepcopy(current_subdivisions[subdindex])
            # Set the render mode to match the previous object
            while currentobj.getrender() != current_render_mode:
                currentobj.toggle_render_mode()
        else:
            current_subdivisions.append(copy.deepcopy(currentobj))
            currentobj.simple_subdivision()
            subdindex += 1
    finally:
        render_in_progress = False


def PrevSubdivision():
    global currentobj, subdindex, current_subdivisions, render_in_progress
    try:
        if subdindex > 0:
            current_render_mode = currentobj.getrender()  # Get current render mode
            subdindex -= 1
            currentobj = copy.deepcopy(current_subdivisions[subdindex])
            # Set the render mode to match the previous object
            while currentobj.getrender() != current_render_mode:
                currentobj.toggle_render_mode()
    finally:
        render_in_progress = False


# The function called whenever a key is pressed
def keyPressed(*args):
    global current_transform, subdindex, render_in_progress, current_subdivisions
    global current_obj_default_pos, current_obj_index, currentobj, subdivision_timestamp, subdivision_cooldown

    key = args[0].decode('utf-8') if isinstance(args[0], bytes) else args[0]
    x, y = args[1], args[2]

    current_time = time.time()

    if key == ESCAPE:
        glutLeaveMainLoop()
    elif key == 'm':
        mode = currentobj.toggle_render_mode()
        print(f"Render mode: {mode.upper()}")
    elif key == '+':
        if not render_in_progress and (current_time - subdivision_timestamp) >= subdivision_cooldown:
            render_in_progress = True
            subdivision_timestamp = current_time
            NextSubdivison()
    elif key == '-':
        if not render_in_progress and (current_time - subdivision_timestamp) >= subdivision_cooldown:
            render_in_progress = True
            subdivision_timestamp = current_time
            PrevSubdivision()
    elif key == 'f':
        current_render_mode = currentobj.getrender()  # Save the current render mode
        stored_level = subdindex  # Store the current subdivision level

        # Reset the camera by loading the default position object
        currentobj = copy.deepcopy(current_obj_default_pos)

        # Set the render mode to match the previous state
        while currentobj.getrender() != current_render_mode:
            currentobj.toggle_render_mode()

        # Reset subdivisions while maintaining the appropriate level
        subdindex = 0
        current_subdivisions = []

        # Store the base object as the level 0
        current_subdivisions.append(copy.deepcopy(currentobj))

        # Apply subdivisions up to the stored level
        for _ in range(stored_level):
            new_obj = copy.deepcopy(current_subdivisions[-1])
            new_obj.simple_subdivision()
            # Maintain the same render mode for the new subdivision
            while new_obj.getrender() != current_render_mode:
                new_obj.toggle_render_mode()
            current_subdivisions.append(new_obj)

        # Set to the appropriate level
        if stored_level > 0:
            currentobj = copy.deepcopy(current_subdivisions[stored_level])
            subdindex = stored_level


def main():
    global window, current_obj_default_pos, currentobj

    # Initialize GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow(b"CENG487 Transformation Demo")
    glutFullScreen()
    # Start with the first object (polyhedron)
    readObj()

    # Save the initial object as the default position
    current_obj_default_pos = copy.deepcopy(currentobj)

    # Initialize the subdivision array with the base object
    current_subdivisions.append(copy.deepcopy(currentobj))

    # Register callbacks
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutMotionFunc(detect_mouse_motion)
    glutMouseFunc(detect_mouse_click)
    # Initialize OpenGL
    InitGL(width, height)

    # Start the main loop
    glutMainLoop()


# Print message and start the program
print("Hit ESC key to quit.")
main()