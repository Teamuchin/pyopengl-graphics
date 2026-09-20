# CENG 487 Assignment3 by
# Timuçin Topcu
# StudentId:310201095
# 05 2025
import math

class mat3d(object):
    def __init__(self):
        self.data = [[0 for _ in range(4)] for _ in range(4)]
        self.data[0][0] = 1
        self.data[1][1] = 1
        self.data[2][2] = 1
        self.data[3][3] = 1
        self.transhistory = ""

    def display(self):
        for row in self.data:
            print(row)
        print(self.transhistory)

    def update(self, row, col, value):
        # Update a specific element
        if 0 <= row < 4 and 0 <= col < 4:
            self.data[row][col] = value
        else:
            print("Invalid index")

    def matrmul(self, matrix_b):
        # Get dimensions
        rows_a = len(self.data)
        cols_a = len(self.data[0])
        cols_b = len(matrix_b[0])

        result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result[i][j] += self.data[i][k] * matrix_b[k][j]
        self.data = result



    def addtranslat(self,x,y,z):
        self.transhistory = "T" + self.transhistory
        arr2=[[0 for _ in range(4)] for _ in range(4)]
        arr2[0][0]=1
        arr2[1][1]=1
        arr2[2][2]=1
        arr2[3][3]=1
        arr2[0][3]=x
        arr2[1][3]=y
        arr2[2][3]=z
        self.matrmul(arr2)

    def addrotation(self, angle, axis):

        arr2 = [[0 for _ in range(4)] for _ in range(4)]

        angle = math.radians(angle)

        if axis == "x":
            # Rotation around X-axis
            arr2[0][0] = 1
            arr2[1][1] = math.cos(angle)
            arr2[1][2] = -math.sin(angle)
            arr2[2][1] = math.sin(angle)
            arr2[2][2] = math.cos(angle)
            arr2[3][3] = 1
            self.matrmul(arr2)
            self.transhistory = "RX" + self.transhistory
        elif axis == "y":
            # Rotation around Y-axis
            arr2[0][0] = math.cos(angle)
            arr2[0][2] = -math.sin(angle)
            arr2[1][1] = 1
            arr2[2][0] = math.sin(angle)
            arr2[2][2] = math.cos(angle)
            arr2[3][3] = 1
            self.matrmul(arr2)
            self.transhistory = "RY" + self.transhistory
        elif axis == "z":
            # Rotation around Z-axis
            arr2[0][0] = math.cos(angle)
            arr2[0][1] = -math.sin(angle)
            arr2[1][0] = math.sin(angle)
            arr2[1][1] = math.cos(angle)
            arr2[2][2] = 1
            arr2[3][3] = 1
            self.matrmul(arr2)
            self.transhistory = "RZ" + self.transhistory

    def addscale(self,x,y,z):
        self.transhistory = "S" + self.transhistory
        arr2=[[0 for _ in range(4)] for _ in range(4)]
        arr2[0][0]=x
        arr2[1][1]=y
        arr2[2][2]=z
        arr2[3][3]=1
        self.matrmul(arr2)