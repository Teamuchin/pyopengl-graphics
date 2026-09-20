# CENG 487 Assignment6 by
# Timuçin Topcu
# StudentId:310201095
# 06.2025
from OpenGL.GL import *

class Shader:
    def __init__(self, vertex_path, fragment_path):
        self.programID = glCreateProgram()
        vertex_shader_id = self.load_and_compile_shader(vertex_path, GL_VERTEX_SHADER)
        fragment_shader_id = self.load_and_compile_shader(fragment_path, GL_FRAGMENT_SHADER)

        glAttachShader(self.programID, vertex_shader_id)
        glAttachShader(self.programID, fragment_shader_id)
        glLinkProgram(self.programID)

        # Check for linking errors
        if glGetProgramiv(self.programID, GL_LINK_STATUS) != GL_TRUE:
            info = glGetProgramInfoLog(self.programID)
            glDeleteProgram(self.programID)
            glDeleteShader(vertex_shader_id)
            glDeleteShader(fragment_shader_id)
            raise RuntimeError(f"Error linking shader program: {info}")

        glDeleteShader(vertex_shader_id)
        glDeleteShader(fragment_shader_id)

    def load_and_compile_shader(self, filepath, shader_type):
        try:
            with open(filepath, 'r') as f:
                shader_code = f.read()
        except IOError:
            print(f"Could not read shader file: {filepath}")

        shader_id = glCreateShader(shader_type)
        glShaderSource(shader_id, shader_code)
        glCompileShader(shader_id)

        if glGetShaderiv(shader_id, GL_COMPILE_STATUS) != GL_TRUE:
            info = glGetShaderInfoLog(shader_id)
            glDeleteShader(shader_id)
            raise RuntimeError(f"Error compiling shader: {info}")

        return shader_id

    def use(self):
        try:
            glUseProgram(self.programID)
        except OpenGL.error.GLError:
            print("Could not use shader program.")

    def set_uniform_mat4(self, name, matrix):
        loc = glGetUniformLocation(self.programID, name)
        glUniformMatrix4fv(loc, 1, GL_FALSE, matrix)

    def set_uniform_1i(self, name, value):
        loc = glGetUniformLocation(self.programID, name)
        glUniform1i(loc, value)

    def set_uniform_1f(self, name, value):
        loc = glGetUniformLocation(self.programID, name)
        glUniform1f(loc, value)