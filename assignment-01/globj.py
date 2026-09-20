# CENG 487 Assignment1 by
# Timuçin Topcu
# StudentId:310201095
# 03 2025
import vec3d
import mat3d

class globj(object):
    def __init__(self):
        self.vertcount = 0
        self.verts = []
        self.center =mat3d.mat3d()
        self.transhistory = ""

    def addvert(self,vert):
        self.verts.append(vert)
        self.vertcount+=1



    def applyobjtransform(self, matrix_b):
        self.center = vec3d.vec3d(self.verts[0].x, self.verts[0].y, self.verts[0].z, 1)

        original_positions = []
        for vector in self.verts:
            original_positions.append((vector.x, vector.y, vector.z))

        for vector in self.verts:
            # Translate to origin
            vector.x -= self.center.x
            vector.y -= self.center.y
            vector.z -= self.center.z

            # Apply transformation
            vector.applytransform(matrix_b)

            # Translate back
            vector.x += self.center.x
            vector.y += self.center.y
            vector.z += self.center.z
        self.transhistory = matrix_b.transhistory + self.transhistory
