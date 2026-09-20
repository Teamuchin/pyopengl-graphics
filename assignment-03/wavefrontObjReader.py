# CENG 487 Assignment3 by
# Timuçin Topcu
# StudentId:310201095
# 05 2025
import globj
import vec3d


class wavefrontObjReader(object):
    def __init__(self):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

    def readAllObj(self,filepath):
        objlist = []
        file = open(filepath, "r")
        for line in file:
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == 'o':
                objlist.append(globj.globj())
                objlist[len(objlist)-1].setname(values[1])
            if values[0] == 'v':
                vertex = list(map(float, values[1:4]))
                objlist[len(objlist)-1].addvert(vec3d.vec3d(vertex[0], vertex[1], vertex[2],1))
            if values[0] == "f":
                face = []
                for i in range(1,len(values)):
                    face.append(int(values[i])-1)
                objlist[len(objlist) - 1].addface(face)
        file.close()
        return objlist