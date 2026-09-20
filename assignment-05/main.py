# CENG 487 Assignment5 by
# Timuçin Topcu
# StudentId:310201095
# 06.2025
from camera import *
from view import *
from shader import Shader
from scene import *
from shapes import *
camera = Camera()
camera.createView( Point3f(0.0, 2.0, 10.0),
                      Point3f(0.0, 0.0, 0.0),
                      Vector3f(0.0, 1.0, 0.0) )

camera.setNear(0.1)
camera.setFar(1000)
view = View(camera, None)
scene = Scene()
view.setScene(scene)

def main():
    global view
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow(b"CENG487 Modern OpenGL")
    try:
        main_shader = Shader("vertex_shader.glsl", "fragment_shader.glsl")
    except RuntimeError as e:
        print(f"Shader compilation error: {e}")
        sys.exit(1)

    cube1 = Cube("cube1", 1, 1, 1, 1, 1, 1)
    cube1.Translate( 2, 0.5, 0)
    cube1.set_shader(main_shader)
    cube1.init_buffers()
    scene.add(cube1)

    cube2 = Cube("cube2", 1.5, 1.5, 1.5, 1, 1, 1)
    cube2.Translate( -2, 0, 0)
    cube2.set_shader(main_shader)
    cube2.init_buffers()
    scene.add(cube2)

    glutDisplayFunc( view.draw )
    glutIdleFunc( view.idleFunction )
    glutReshapeFunc( view.resizeView )
    glutKeyboardFunc( view.keyPressed )
    glutSpecialFunc( view.specialKeyPressed )
    glutMouseFunc( view.mousePressed )
    glutMotionFunc( view.mouseMove )

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glutMainLoop()

print("Hit ESC key to quit.")
main()