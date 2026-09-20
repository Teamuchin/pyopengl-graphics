# CENG 487 Assignment5 by
# Timuçin Topcu
# StudentId:310201095
# 06.2025
from OpenGL.GL import *
from OpenGL.GLUT import *
from matrix import *
from defs import *


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
        self.width = 0
        self.height = 0

    def draw(self):
        glClearColor(self.bgColor.r, self.bgColor.g, self.bgColor.b, self.bgColor.a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        aspect_ratio = self.width / self.height if self.height > 0 else 1.0
        projection_matrix = Matrix.perspective(self.camera.fov, aspect_ratio, self.camera.near, self.camera.far)
        view_matrix = self.camera.get_view_matrix()
        proj_list = projection_matrix.asList()
        view_list = view_matrix.asList()
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

        # get status of alt key
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
            self.camera.zoom(xOffset * 10)  # scaled for better feel
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
