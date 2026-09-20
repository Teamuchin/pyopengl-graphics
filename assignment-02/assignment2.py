# CENG 487 Assignment2 by
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

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

# Global objects and variables
currentobj = None
current_obj_index = 1  # Track which object is currently displayed
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
nums = ['3', '4', '5', '6', '7', '8', '9']


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


# Initialize our objects
def req_object(objnum, vertnum=4):
    global currentobj, subdindex, subdmode, current_subdivisions, current_obj_default_pos
    currentobj = globj.globj()
    current_subdivisions = []
    subdindex = 0
    match objnum:
        case 1:
            # Create polyhedron
            currentobj.create_polyhedron_plane(vertnum)
            currentobj.setdrawtype("quad")
        case 2:
            # Create box
            currentobj.create_platonic_solid("hexahedron")
            currentobj.setdrawtype("quad")
        case 3:
            # Create pyramid
            currentobj.addvert(vec3d.vec3d(1, 0, 1, 1))
            currentobj.addvert(vec3d.vec3d(1, 0, -1, 1))
            currentobj.addvert(vec3d.vec3d(-1, 0, 1, 1))
            currentobj.addvert(vec3d.vec3d(-1, 0, -1, 1))
            currentobj.addvert(vec3d.vec3d(0, 2, 0, 1))
            currentobj.setfaces([
                [0, 2, 3, 1],
                [0, 1, 4],
                [0, 2, 4],
                [1, 3, 4],
                [2, 3, 4]
            ])
            currentobj.calculate_center()
            currentobj.setdrawtype("triangle")
        case 4:
            # Create torus
            currentobj.create_torus(major_radius=1.0, minor_radius=0.3,
                                    major_segments=20, minor_segments=10)
        case 5:
            # Create cylinder
            currentobj.create_cylinder(radius=0.8, height=2.0, segments=20)
        case 6:
            # Create sphere
            currentobj.create_sphere(radius=1.0, slices=12, stacks=12)
        case 7:
            # Create tetrahedron
            currentobj.create_platonic_solid("tetrahedron")
        case 8:
            # Create octahedron
            currentobj.create_platonic_solid("octahedron")
        case 9:
            # Create icosahedron
            currentobj.create_platonic_solid("icosahedron")
    current_obj_default_pos = copy.deepcopy(currentobj)
    currentobj.drawobj()


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

    draw_text("CENG 487 Assignment 2 by: Timuçin TOPCU", 10, height - 20, GLUT_BITMAP_HELVETICA_18, (1.0, 1.0, 0.0))

    # Display current object name and controls
    if currentobj:
        current_obj_name = f"Current Object: {current_obj_index}"
        draw_text(current_obj_name, 10, height - 40, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
        draw_text("Controls:", 10, height - 60, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
        draw_text("  ESC: Quit", 10, height - 80, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
        draw_text("  m: Switch view mode", 10, height - 100, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
        draw_text("  n: Switch to next object", 10, height - 120, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
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
        if current_obj_index == 1:
            draw_text("Use 3-9 to change side count", 10, 40, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))
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
        if subdindex < len(current_subdivisions) - 1:
            subdindex += 1
            currentobj = copy.deepcopy(current_subdivisions[subdindex])
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
            subdindex -= 1
            currentobj = copy.deepcopy(current_subdivisions[subdindex])
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
    elif key == 'n':
        current_obj_index += 1
        if current_obj_index > 9:
            current_obj_index = 1
        req_object(current_obj_index)
        current_obj_default_pos = copy.deepcopy(currentobj)
        DrawGLScene()
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
    elif key in nums:
        if current_obj_index == 1:
            req_object(1, int(key))
    elif key == 'f':
        currentobj = copy.deepcopy(current_obj_default_pos)

        # Reset subdivisions while maintaining the appropriate level
        stored_level = subdindex
        subdindex = 0
        current_subdivisions = []

        # Store the base object as the level 0
        if stored_level > 0:
            current_subdivisions.append(copy.deepcopy(currentobj))

            # Apply subdivisions up to the stored level
            for _ in range(stored_level):
                new_obj = copy.deepcopy(current_subdivisions[-1])
                new_obj.simple_subdivision()
                current_subdivisions.append(new_obj)

            # Set to the appropriate level
            currentobj = copy.deepcopy(current_subdivisions[stored_level])
            subdindex = stored_level


def main():
    global window

    # Initialize GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow(b"CENG487 Transformation Demo")
    glutFullScreen()
    # Start with the first object (polyhedron)
    req_object(1)

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