# CENG 487 Assignment5 by
# Timuçin Topcu
# StudentId:310201095
# 06.2025
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
import ctypes

from boundingbox import *
from defs import DrawStyle

__all__ = ['_Shape', 'Cube', 'DrawStyle']


class _Shape:
    def __init__(self, name, vertices, faces):
        self.vertices = numpy.array(vertices, dtype='float32')
        self.faces = numpy.array(faces, dtype='uint32')
        self.colors = numpy.array([], dtype='float32')
        self.obj2World = Matrix()
        self.drawStyle = DrawStyle.NODRAW
        self.wireOnShaded = False
        self.wireWidth = 2
        self.name = name
        self.fixedDrawStyle = False
        self.wireColor = ColorRGBA(0.7, 1.0, 0.0, 1.0)
        self.wireOnShadedColor = ColorRGBA(1.0, 1.0, 1.0, 1.0)
        self.bboxObj = BoundingBox()
        self.calcBboxObj()

        self.VAO = None
        self.VBO = None
        self.EBO = None
        self.shader = None

    def calcBboxObj(self):
        if self.vertices.size == 0: return
        for i in range(0, len(self.vertices), 4):
            point = Point3f(self.vertices[i], self.vertices[i + 1], self.vertices[i + 2])
            self.bboxObj.expand(point)

    def set_shader(self, shader):
        self.shader = shader

    def init_buffers(self):
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes + self.colors.nbytes, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.vertices.nbytes, self.vertices)
        glBufferSubData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.colors.nbytes, self.colors)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.faces.nbytes, self.faces, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(self.vertices.nbytes))
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def setDrawStyle(self, style):
        self.drawStyle = style

    def setWireColor(self, r, g, b, a):
        self.wireColor = ColorRGBA(r, g, b, a)

    def setWireWidth(self, width):
        self.wireWidth = width

    def draw(self, projection_matrix, view_matrix):
        if self.shader and self.VAO is not None and self.faces.size > 0:
            self.shader.use()
            model_matrix = self.obj2World.asList()
            self.shader.set_uniform_mat4("proj", projection_matrix)
            self.shader.set_uniform_mat4("view", view_matrix)
            self.shader.set_uniform_mat4("model", model_matrix)

            glBindVertexArray(self.VAO)

            # Handle different drawing styles
            if self.drawStyle == DrawStyle.WIRE or self.wireOnShaded:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                glLineWidth(self.wireWidth)
            glDrawElements(GL_TRIANGLES, len(self.faces.flatten()), GL_UNSIGNED_INT, None)
            if self.drawStyle == DrawStyle.WIRE or self.wireOnShaded:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            glBindVertexArray(0)

    def Translate(self, x, y, z):
        translate = Matrix.T(x, y, z)
        self.obj2World = translate.product(self.obj2World)


class Cube(_Shape):
    def __init__(self, name, xSize, ySize, zSize, xDiv, yDiv, zDiv):
        halfX, halfY, halfZ = xSize / 2.0, ySize / 2.0, zSize / 2.0
        vertices = [
            # Bottom face
            -halfX, -halfY, -halfZ, 1.0,  # 0
            halfX, -halfY, -halfZ, 1.0,  # 1
            halfX, -halfY, halfZ, 1.0,  # 2
            -halfX, -halfY, halfZ, 1.0,  # 3
            # Top face
            -halfX, halfY, -halfZ, 1.0,  # 4
            halfX, halfY, -halfZ, 1.0,  # 5
            halfX, halfY, halfZ, 1.0,  # 6
            -halfX, halfY, halfZ, 1.0,  # 7
        ]

        faces = [
            0, 3, 2, 2, 1, 0,
            4, 5, 6, 6, 7, 4,
            3, 7, 6, 6, 2, 3,
            0, 1, 5, 5, 4, 0,
            0, 4, 7, 7, 3, 0,
            1, 2, 6, 6, 5, 1
        ]

        super().__init__(name, vertices, faces)
        self.drawStyle = DrawStyle.SMOOTH

        colors_list = []
        for _ in range(8):
            colors_list.extend([random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1.0])
        self.colors = numpy.array(colors_list, dtype='float32')