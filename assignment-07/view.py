# CENG 487 Assignment7 by
# Timuçin Topcu
# StudentId:310201095
# 06.2025
from OpenGL.GL import *
from OpenGL.GLUT import *
from matrix import *
from defs import *
import math


class Event:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.button = -1
        self.state = -1
        self.altPressed = False


class View:
    def __init__(self, camera, grid, scene=None):
        self.camera = camera
        self.grid = grid
        self.scene = scene
        self.bgColor = ColorRGBA(0.15, 0.15, 0.15, 1.0)
        self.cameraIsMoving = False
        self.objectAnimOn = False
        self.event = Event()
        self.mouseX = -1
        self.mouseY = -1
        self.width = 1920
        self.height = 1080
        self.specularOn = True

    def draw(self):
        glClearColor(self.bgColor.r, self.bgColor.g, self.bgColor.b, self.bgColor.a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        aspect_ratio = self.width / self.height if self.height > 0 else 1.0
        projection_matrix = Matrix.perspective(self.camera.fov, aspect_ratio, self.camera.near, self.camera.far)
        view_matrix = self.camera.get_view_matrix()
        proj_list = projection_matrix.asList()
        view_list = view_matrix.asList()

        if self.scene.lights and self.scene.nodes:
            shader = self.scene.nodes[0].shader
            if shader:
                shader.use()
                shader.set_uniform_3f("viewPos", self.camera.eye.x, self.camera.eye.y, self.camera.eye.z)
                shader.set_uniform_1i("specularOn", 1 if self.specularOn else 0)

                for i, light in enumerate(self.scene.lights):
                    prefix = f"lights[{i}]"
                    if light.enabled:
                        shader.set_uniform_1i(f"{prefix}.type", light.type)
                        shader.set_uniform_3f(f"{prefix}.position", *light.position)
                        shader.set_uniform_3f(f"{prefix}.direction", *light.direction)
                        shader.set_uniform_3f(f"{prefix}.color", *light.color)
                        shader.set_uniform_1f(f"{prefix}.intensity", light.intensity)
                        shader.set_uniform_1f(f"{prefix}.constant", 1.0)
                        shader.set_uniform_1f(f"{prefix}.linear", 0.09)
                        shader.set_uniform_1f(f"{prefix}.quadratic", 0.032)
                        shader.set_uniform_1f(f"{prefix}.coneAngle", math.cos(math.radians(light.cone_angles[0])))
                        shader.set_uniform_1f(f"{prefix}.penumbraAngle", math.cos(math.radians(light.cone_angles[1])))
                    else:
                        shader.set_uniform_1i(f"{prefix}.type", 0)  # Type 0 is disabled

        for node in self.scene.nodes:
            node.draw(proj_list, view_list)

        glutSwapBuffers()

    def setScene(self, scene):
        self.scene = scene

    def setObjectAnim(self, onOff):
        self.objectAnimOn = onOff

    def isObjectAnim(self):
        return self.objectAnimOn

    def setCameraIsMoving(self, onOff):
        self.cameraIsMoving = onOff

    def isCameraMoving(self):
        return self.cameraIsMoving

    def keyPressed(self, key, x, y):
        if ord(key) == 27:
            glutLeaveMainLoop()
            return
        if key == b'b':
            self.specularOn = not self.specularOn
            print(f"Specular Lighting: {'ON' if self.specularOn else 'OFF'}")

        if key == b'f':
            self.camera.reset()

        if key == b'4':
            for node in self.scene.nodes:
                if not node.fixedDrawStyle:
                    node.drawStyle = DrawStyle.WIRE
                    node.wireOnShaded = False

        if key == b'5':
            for node in self.scene.nodes:
                if not node.fixedDrawStyle:
                    node.drawStyle = DrawStyle.SMOOTH
                    node.wireOnShaded = False

        if key == b'6':
            for node in self.scene.nodes:
                if not node.fixedDrawStyle and node.drawStyle != DrawStyle.WIRE:
                    node.wireOnShaded = True
        if key == b'+':
            for node in self.scene.nodes:
                if hasattr(node, 'set_blend_factor'):
                    node.set_blend_factor(node.blend_factor + 0.05)
        if key == b'-':
            for node in self.scene.nodes:
                if hasattr(node, 'set_blend_factor'):
                    node.set_blend_factor(node.blend_factor - 0.05)
        if b'1' <= key <= b'3':
            light_index = int(key) - 1
            if light_index < len(self.scene.lights):
                self.scene.lights[light_index].toggle()
                print(f"Toggled light {light_index + 1}. Enabled: {self.scene.lights[light_index].enabled}")

        glutPostRedisplay()

    def resizeView(self, width, height):
        self.width = width
        self.height = height
        if height == 0:
            height = 1
        glViewport(0, 0, width, height)

    def specialKeyPressed(self, *args):
        if args[0] == GLUT_KEY_LEFT:
            self.camera.pan(-0.1)

        if args[0] == GLUT_KEY_RIGHT:
            self.camera.pan(0.1)

        glutPostRedisplay()

    def mousePressed(self, button, state, x, y):
        self.event.x = x
        self.event.y = y
        self.event.state = state
        self.event.button = button

        m = glutGetModifiers()
        self.event.altPressed = m & GLUT_ACTIVE_ALT

        self.mouseX = x
        self.mouseY = y

        if state == 0:
            if self.event.altPressed > 0:
                self.setCameraIsMoving(True)
        else:
            self.setCameraIsMoving(False)

    def mouseMove(self, x, y):
        if self.event.altPressed == False:
            return

        xSpeed = 0.02
        ySpeed = 0.02
        xOffset = (x - self.mouseX) * xSpeed
        yOffset = (y - self.mouseY) * ySpeed

        if (self.event.button == GLUT_RIGHT_BUTTON):
            self.camera.zoom(xOffset * 10)
        elif (self.event.button == GLUT_MIDDLE_BUTTON):
            self.camera.dolly(-xOffset, yOffset, 0)
        elif (self.event.button == GLUT_LEFT_BUTTON):
            self.camera.yaw(xOffset)
            self.camera.pitch(yOffset)

        self.mouseX = x
        self.mouseY = y

        self.event.x = x
        self.event.y = y

    def idleFunction(self):
        if self.isObjectAnim() or self.isCameraMoving():
            glutPostRedisplay()