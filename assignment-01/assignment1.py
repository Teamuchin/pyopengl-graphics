# CENG 487 Assignment1 by
# Timuçin Topcu
# StudentId:310201095
# 03 2025

# Note:
# -----
# This Uses PyOpenGL and PyOpenGL_accelerate packages.  It also uses GLUT for UI.
# To get proper GLUT support on linux don't forget to install python-opengl package using apt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import mat3d
import vec3d
import globj
import time

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

# Global objects and variables
triangleobj = None
squareobj = None
last_update_time = 0
transform_speed = 100
animate = False
current_transform = "rotate"  # Current transformation mode: "rotate", "translate", "scale"
current_axis = "z"  # Current rotation axis


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


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# Initialize our objects
def init_objects():
    global triangleobj, squareobj

    # Create triangle
    triangleobj = globj.globj()
    triangleobj.addvert(vec3d.vec3d(0, 1.0, 0, 1))
    triangleobj.addvert(vec3d.vec3d(1, -1, 0, 1))
    triangleobj.addvert(vec3d.vec3d(-1, -1.0, 0, 1))

    # Create square
    squareobj = globj.globj()
    squareobj.addvert(vec3d.vec3d(-1.0, 1.0, 0.0, 1))
    squareobj.addvert(vec3d.vec3d(1.0, 1.0, 0.0, 1))
    squareobj.addvert(vec3d.vec3d(1.0, -1.0, 0.0, 1))
    squareobj.addvert(vec3d.vec3d(-1.0, -1.0, 0.0, 1))


# Draw the triangle
def draw_triangle():
    glBegin(GL_POLYGON)  # Start drawing a polygon
    glColor3f(1.0, 0.0, 0.0)  # Red
    trianglecords = triangleobj.verts[0].cords()
    glVertex3f(trianglecords[0], trianglecords[1], trianglecords[2])  # Top
    glColor3f(0.0, 1.0, 0.0)  # Green
    trianglecords = triangleobj.verts[1].cords()
    glVertex3f(trianglecords[0], trianglecords[1], trianglecords[2])  # Bottom Right
    glColor3f(0.0, 0.0, 1.0)  # Blue
    trianglecords = triangleobj.verts[2].cords()
    glVertex3f(trianglecords[0], trianglecords[1], trianglecords[2])  # Bottom Left
    glEnd()  # We are done with the polygon


# Draw the square
def draw_square():
    glBegin(GL_QUADS)  # Start drawing a 4 sided polygon
    glColor3f(0.3, 0.5, 1.0)  # Bluish shade
    for i in range(4):
        squarecords = squareobj.verts[i].cords()
        glVertex3f(squarecords[0], squarecords[1], squarecords[2])
    glEnd()  # We are done with the polygon


# Apply time-based transformations
def apply_time_transform():
    global last_update_time, triangleobj, squareobj

    current_time = time.time()
    elapsed_time = current_time - last_update_time
    # Concept I use here is similar to delta time in game engines. With this I ensure movement is scalable to any frames per second we want
    # Only update if animation is on and enough time has passed
    if animate and elapsed_time > 0.016:  # ~60 FPS
        triangle_transform = mat3d.mat3d()
        square_transform = mat3d.mat3d()


        if current_transform == "rotate":
            # Rotation amount based on elapsed time
            angle_increment = math.radians(transform_speed) * elapsed_time
            triangle_transform.addrotation(angle_increment,current_axis)
            square_transform.addrotation(angle_increment,current_axis)
        elif current_transform == "translate":
            # Translation based on elapsed time
            move_amount = (transform_speed/100) * elapsed_time
            if current_axis == "x":
                triangle_transform.addtranslat(move_amount, 0, 0)
                square_transform.addtranslat(move_amount, 0, 0)
            elif current_axis == "y":
                triangle_transform.addtranslat(0, move_amount, 0)
                square_transform.addtranslat(0, move_amount, 0)
            elif current_axis == "z":
                triangle_transform.addtranslat(0, 0, move_amount)
                square_transform.addtranslat(0, 0, move_amount)
        elif current_transform == "scale":
            # Scale based on elapsed time
            scale_factor = 1.0 + ((transform_speed/100) * elapsed_time)
            triangle_transform.addscale(scale_factor, scale_factor, scale_factor)
            square_transform.addscale(scale_factor, scale_factor, scale_factor)

        # Apply transformations
        triangleobj.applyobjtransform(triangle_transform)
        squareobj.applyobjtransform(square_transform)

        # Update time
        last_update_time = current_time


# The main drawing function.
def DrawGLScene():
    global triangleobj, squareobj

    # Apply time-based transformations
    apply_time_transform()

    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset The View

    # Move Left 1.5 units and into the screen 6.0 units.
    glTranslatef(-1.5, 0.0, -6.0)

    # Draw the triangle
    draw_triangle()

    # Move Right 3.0 units
    glTranslatef(3.0, 0.0, 0.0)

    # Draw the square
    draw_square()

    # Swap the buffers to display the scene
    glutSwapBuffers()


# The function called whenever a key is pressed
def keyPressed(*args):
    global animate, current_transform, current_axis, transform_speed, last_update_time

    key = args[0].decode('utf-8') if isinstance(args[0], bytes) else args[0]

    if key == ESCAPE:
        sys.exit()

    elif key == ' ':
        animate = not animate
        if animate:
            last_update_time = time.time()
        print(f"Animation: {'ON' if animate else 'OFF'}")

    elif key == 'r':
        current_transform = "rotate"
        print("Mode: Rotation")
    elif key == 't':
        current_transform = "translate"
        print("Mode: Translation")
    elif key == 's':
        current_transform = "scale"
        print("Mode: Scaling")

    elif key == 'x':
        current_axis = "x"
        print(f"Axis: X")
    elif key == 'y':
        current_axis = "y"
        print(f"Axis: Y")
    elif key == 'z':
        current_axis = "z"
        print(f"Axis: Z")

    elif key == '+' or key == '=':
        transform_speed += 20
        print(f"Speed: {transform_speed}")
    elif key == '-':
        transform_speed = transform_speed - 20
        print(f"Speed: {transform_speed}")


def main():
    global window, last_update_time

    # Initialize GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow(b"CENG487 Transformation Demo")

    # Initialize objects
    init_objects()

    # Set up the starting time
    last_update_time = time.time()

    # Register callbacks
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)

    # Initialize OpenGL
    InitGL(640, 480)

    # Print instructions
    print("Controls:")
    print("  ESC: Quit")
    print("  SPACE: Toggle animation on/off")
    print("  r: Switch to rotation mode")
    print("  t: Switch to translation mode")
    print("  s: Switch to scaling mode")
    print("  x/y/z: Switch to x/y/z axis")
    print("  +/-: Increase/decrease animation speed")

    # Start the main loop
    glutMainLoop()


# Print message and start the program
print("Hit ESC key to quit.")
main()