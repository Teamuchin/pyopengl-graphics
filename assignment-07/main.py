# CENG 487 Assignment7 by
# Timuçin Topcu
# StudentId:310201095
# 06.2025
import sys

from camera import *
from view import *
from shader import Shader
from scene import *
from shapes import *
from light import *

camera = Camera()
camera.createView(Point3f(0.0, 20.0, 55.0),
                  Point3f(0.0, 20.0, 0.0),
                  Vector3f(0.0, 1.0, 0.0))

camera.setNear(0.1)
camera.setFar(1000)
view = View(camera, None)
scene = Scene()
view.setScene(scene)

# Light 1: Directional
dir_light = Light(light_type="directional", direction=(0.5, -1.0, -0.5), color=(0.8, 0.8, 0.8), intensity=0.6)
scene.add_light(dir_light)


# Light 2: Point
point_light = Light(light_type="point", position=(0, 40, 0), color=(1.0, 0.7, 0.7), intensity=100.0)
scene.add_light(point_light)

# Light 3: Spotlight
spot_light = Light(light_type="spot", position=(-15, 40, -5), direction=(0.5, -1, 0.5), color=(0.5, 0.5, 1.0),
                   intensity=50.0, cone_angles=(12.5, 17.5))
scene.add_light(spot_light)


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

    cornell_box = MeshFromOBJ("cornell_box", "CornellManifold.obj")
    cornell_box.set_shader(main_shader)
    cornell_box.load_texture("texture4.png")
    cornell_box.init_buffers()
    scene.add(cornell_box)

    glutDisplayFunc(view.draw)
    glutIdleFunc(view.idleFunction)
    glutReshapeFunc(view.resizeView)
    glutKeyboardFunc(view.keyPressed)
    glutSpecialFunc(view.specialKeyPressed)
    glutMouseFunc(view.mousePressed)
    glutMotionFunc(view.mouseMove)

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glutMainLoop()


print("Hit ESC key to quit.")
main()