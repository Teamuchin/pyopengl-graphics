# CENG 487 Assignment7 by
# Timuçin Topcu
# StudentId:310201095
# 06.2025
from OpenGL.GL import *
from OpenGL.GLUT import *
import ctypes
import numpy

from boundingbox import *
from defs import DrawStyle
from PIL import Image
from wavefrontObjReader import *  # Assuming the filename is wavefrontObjReader.py
from matrix import *
from vector import *

__all__ = ['_Shape', 'MeshFromOBJ', 'DrawStyle']


class _Shape:
    def __init__(self, name, vertices, faces):
        self.vertices = numpy.array(vertices, dtype='float32')
        self.faces = numpy.array(faces, dtype='uint32')
        self.colors = numpy.array([], dtype='float32')
        self.uvs = numpy.array([], dtype='float32')
        self.normals = numpy.array([], dtype='float32')
        self.texture_id1 = None
        self.texture_id2 = None
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
        self.blend_factor = 0.5
        self.shininess = 32.0
        self.specular_strength = 0.5

        self.VAO = None
        self.VBO = None
        self.EBO = None
        self.shader = None

    def load_texture(self, texture_path, slot=1):
        try:
            image = Image.open(texture_path).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            img_data = numpy.frombuffer(image.tobytes(), numpy.uint8)
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            if image.mode == "RGBA":
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                             img_data)
            else:
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

            glGenerateMipmap(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, 0)

            if slot == 1:
                self.texture_id1 = texture_id
            elif slot == 2:
                self.texture_id2 = texture_id
        except FileNotFoundError:
            print(f"ERROR: Texture file not found at '{texture_path}'")

    def calcBboxObj(self):
        if self.vertices.size == 0: return
        for i in range(0, len(self.vertices), 4):
            point = Point3f(self.vertices[i], self.vertices[i + 1], self.vertices[i + 2])
            self.bboxObj.expand(point)

    def set_shader(self, shader):
        self.shader = shader

    def set_blend_factor(self, factor):
        self.blend_factor = max(0.0, min(1.0, factor))

    def init_buffers(self):
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        buffer_size = self.vertices.nbytes + self.colors.nbytes + self.uvs.nbytes + self.normals.nbytes
        glBufferData(GL_ARRAY_BUFFER, buffer_size, None, GL_STATIC_DRAW)
        offset = 0
        glBufferSubData(GL_ARRAY_BUFFER, offset, self.vertices.nbytes, self.vertices);
        offset += self.vertices.nbytes
        glBufferSubData(GL_ARRAY_BUFFER, offset, self.colors.nbytes, self.colors);
        offset += self.colors.nbytes
        glBufferSubData(GL_ARRAY_BUFFER, offset, self.uvs.nbytes, self.uvs);
        offset += self.uvs.nbytes
        glBufferSubData(GL_ARRAY_BUFFER, offset, self.normals.nbytes, self.normals)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.faces.nbytes, self.faces, GL_STATIC_DRAW)
        offset = 0
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(offset))
        offset += self.vertices.nbytes
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(offset))
        offset += self.colors.nbytes
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 2 * 4, ctypes.c_void_p(offset))
        offset += self.uvs.nbytes
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(3, 4, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(3)

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
            if self.texture_id1 is not None:
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, self.texture_id1)
                self.shader.set_uniform_1i("tex1", 0)

            if self.texture_id2 is not None:
                glActiveTexture(GL_TEXTURE1)
                glBindTexture(GL_TEXTURE_2D, self.texture_id2)
                self.shader.set_uniform_1i("tex2", 1)

            model_matrix = self.obj2World.asList()
            self.shader.set_uniform_mat4("proj", projection_matrix)
            self.shader.set_uniform_mat4("view", view_matrix)
            self.shader.set_uniform_mat4("model", model_matrix)
            self.shader.set_uniform_1f("blendFactor", self.blend_factor)
            self.shader.set_uniform_1f("materialShininess", self.shininess)
            self.shader.set_uniform_1f("materialSpecularStrength", self.specular_strength)

            glBindVertexArray(self.VAO)
            if self.drawStyle == DrawStyle.WIRE or self.wireOnShaded:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

            glDrawElements(GL_TRIANGLES, len(self.faces.flatten()), GL_UNSIGNED_INT, None)

            if self.drawStyle == DrawStyle.WIRE or self.wireOnShaded:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            glBindVertexArray(0)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, 0)

    def Translate(self, x, y, z):
        translate = Matrix.T(x, y, z)
        self.obj2World = translate.product(self.obj2World)


class MeshFromOBJ(_Shape):
    def __init__(self, name, filepath):
        loader = OBJLoader(filepath)
        vertices, uvs, normals, faces = loader.get_model_data()
        num_vertices = len(vertices) // 4
        colors = numpy.tile([1.0, 1.0, 1.0, 1.0], num_vertices).astype('float32')
        super().__init__(name, vertices, faces)
        self.uvs = uvs
        self.colors = colors
        self.drawStyle = DrawStyle.SMOOTH
        self.normals = normals