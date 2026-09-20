# CENG 487 Assignment4 by
# Timuçin Topcu
# StudentId:310201095
# 05 2025
import math

class vec3d(object):
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        #w=0 vector
        #w=1 point
    def applytransform(self, matrix_b):
        original_x = self.x
        original_y = self.y
        original_z = self.z

        self.x = original_x * matrix_b.data[0][0] + original_y * matrix_b.data[0][1] + original_z * matrix_b.data[0][2] + matrix_b.data[0][3]
        self.y = original_x * matrix_b.data[1][0] + original_y * matrix_b.data[1][1] + original_z * matrix_b.data[1][2] + matrix_b.data[1][3]
        self.z = original_x * matrix_b.data[2][0] + original_y * matrix_b.data[2][1] + original_z * matrix_b.data[2][2] + matrix_b.data[2][3]


    def dotprod(self,vecsec):
        if self.w == 0 and vecsec.w == 0:
            return vecsec.x*self.x + vecsec.y*self.y + vecsec.z*self.z
        else:
            return print("fail")

    def crossprod(self,vecsec):
        if self.w==0 and vecsec.w == 0:
            return vec3d(self.y*vecsec.z-self.z*vecsec.y,self.z*vecsec.x-self.x*vecsec.z,self.x*vecsec.y-self.y*vecsec.x,self.w)
        else:
            return print("fail")
    def lenscale(self):
        return (self.x**2+self.y**2+self.z**2)**0.5

    def scalerprod(self,num):
        return vec3d(self.x*num,self.y*num,self.z*num)

    def projtobasis(self,basis,angle):
        if self.w==0 and basis.w == 0:
            return  basis.scalerprod(self.dotprod(basis)/(basis.lenscale())**2)

    def anglewithvec(self,vecsec):
        return math.acos(self.dotprod(vecsec)/(vecsec.lenscale()*self.lenscale()))

    def cords(self):
        return(self.x,self.y,self.z)
