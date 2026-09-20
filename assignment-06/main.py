# CENG 487 Assignment6 by
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

    shape1 = MeshFromOBJ("cube1_from_obj", "cube.obj")
    shape1.Translate(2, 0.5, 0)
    shape1.set_shader(main_shader)
    shape1.load_texture("rubiks.png",slot=1)
    shape1.load_texture("texture1.png", slot=2)
    shape1.init_buffers()
    scene.add(shape1)

    shape2 = MeshFromOBJ("sphere1_from_obj", "sphere.obj")
    shape2.Translate(-2, 0.5, 0)
    shape2.set_shader(main_shader)
    shape2.load_texture("rubiks.png",slot=1)
    shape2.load_texture("texture1.png", slot=2)
    shape2.init_buffers()
    scene.add(shape2)

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