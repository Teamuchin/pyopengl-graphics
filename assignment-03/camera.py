# CENG 487 Assignment3 by
# Timuçin Topcu
# StudentId:310201095
# 05 2025

import mat3d
import vec3d

class camera(object):
    def __init__(self, position = vec3d.vec3d(0,0,0,0),direction = vec3d.vec3d(0,0,1,0),up = vec3d.vec3d(0,1,0,0)):
        self.position = position
        self.direction = direction
        self.up = up
        self.last_x = None
        self.last_y = None
        self.last_z = None
        self.turnsensitivity = 1
        self.movesensitivity = 0.01
        self.cammatr = mat3d.mat3d()
        self.max_delta = 20

    def _clamp_delta(self, delta, max_value):
        if abs(delta) > max_value:
            return max_value if delta > 0 else -max_value
        return delta

    def setposition(self,position):
        self.position = position
    def getposition(self):
        return self.position

    def turncamera(self, x, y,obj):
        if self.last_x is None or self.last_y is None:
            self.last_x = x
            self.last_y = y
            return
        dx = x - self.last_x
        dy = y - self.last_y
        dx = self._clamp_delta(dx, self.max_delta)
        dy = self._clamp_delta(dy, self.max_delta)
        self.cammatr= mat3d.mat3d()
        if abs(dx) < 10 and abs(dy) < 10:
            if dx != 0:
                self.cammatr.addrotation(-1*dx * self.turnsensitivity, "y")
            if dy != 0:
                self.cammatr.addrotation(dy * self.turnsensitivity, "x")
            self.position.applytransform(self.cammatr)
            for i in range(0,obj.getvertcount()):
                obj.getvert(i).applytransform(self.cammatr)
        self.last_x = x
        self.last_y = y
        self.cammatr = mat3d.mat3d()

    def movecamera(self, x, y,obj):
        if self.last_x is None or self.last_y is None:
            self.last_x = x
            self.last_y = y
            return
        dx = x - self.last_x
        dy = y - self.last_y
        dx = self._clamp_delta(dx, self.max_delta)
        dy = self._clamp_delta(dy, self.max_delta)
        self.cammatr= mat3d.mat3d()
        if abs(dx) < 10 and abs(dy) < 10:
            self.cammatr = mat3d.mat3d()
            if dx != 0:
                self.cammatr.addtranslat(dx * self.movesensitivity,0,0)
            if dy != 0:
                self.cammatr.addtranslat(0, -1*dy * self.movesensitivity,0)
            self.position.applytransform(self.cammatr)
            for i in range(0,obj.getvertcount()):
                obj.getvert(i).applytransform(self.cammatr)
        self.last_x = x
        self.last_y = y
        self.cammatr = mat3d.mat3d()


    def movecameradepth(self,z,obj):
        if self.last_z is None:
            self.last_z = z
            return
        dz = z - self.last_z
        dz = self._clamp_delta(dz, self.max_delta)
        self.cammatr= mat3d.mat3d()
        if abs(dz) < 10:
            self.cammatr = mat3d.mat3d()
            if dz != 0:
                self.cammatr.addtranslat(0,0,dz * self.movesensitivity)
            self.position.applytransform(self.cammatr)
            for i in range(0,obj.getvertcount()):
                obj.getvert(i).applytransform(self.cammatr)
        self.last_z = z
        self.cammatr = mat3d.mat3d()

    def setsensitivity(self,width,height):
        self.turnsensitivity = 1000000/(width*height)
        self.movesensitivity = 10000/(width*height)



