# CENG 487 Assignment3 by
# Timuçin Topcu
# StudentId:310201095
# 05 2025
import vec3d
import mat3d
from OpenGL.GL import *
import math


class globj(object):
    def __init__(self):
        self.vertcount = 0
        self.verts = []
        self.center = mat3d.mat3d()
        self.transhistory = ""
        self.drawtype = ""
        self.faces = []
        self.render_mode = "wireframe"  # Default to wireframe mode
        self.objname= ""
    def setname(self,name):
        self.objname=name
    def getname(self):
        return self.objname
    def getrender(self):
        return self.render_mode
    def set_render_mode(self, mode):
        """Set rendering mode: 'wireframe', 'filled', or 'both'"""
        if mode in ["wireframe", "filled", "both"]:
            self.render_mode = mode
            return True
        return False

    def toggle_render_mode(self):
        """Toggle between rendering modes"""
        if self.render_mode == "wireframe":
            self.render_mode = "filled"
        elif self.render_mode == "filled":
            self.render_mode = "both"
        else:  # "both"
            self.render_mode = "wireframe"
        return self.render_mode

    def setdrawtype(self, drawtype):
        self.drawtype = drawtype

    def getdrawtype(self):
        return self.drawtype

    def addvert(self, vert):
        self.verts.append(vert)
        self.vertcount += 1
        return self.vertcount - 1

    def getvertcount(self):
        return self.vertcount

    def setfaces(self, faces):
        self.faces = faces
    def addface(self,face):
        self.faces.append(face)
    def removeface(self, index):
        self.faces.pop(index)

    def getvert(self, index):
        return self.verts[index]

    def calculate_center(self):
        if self.vertcount == 0:
            return vec3d.vec3d(0, 0, 0, 1)

        x_sum = sum(v.x for v in self.verts)
        y_sum = sum(v.y for v in self.verts)
        z_sum = sum(v.z for v in self.verts)

        return vec3d.vec3d(
            x_sum / self.vertcount,
            y_sum / self.vertcount,
            z_sum / self.vertcount,
            1
        )

    def drawobj(self):
        # Draw wireframe if needed
        if self.render_mode in ["wireframe", "both"]:
            for face in self.faces:
                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                scale_factor = 1.0005
                glScalef(scale_factor, scale_factor, scale_factor)
                glLineWidth(2.0)
                glBegin(GL_LINE_LOOP)
                glColor3f(0.3, 0.5, 1.0)
                for vertex in face:
                    if 0 <= vertex < self.vertcount:
                        objcords = self.verts[vertex].cords()
                        glVertex3f(objcords[0], objcords[1], objcords[2])
                glEnd()
                glPopMatrix()


        # Draw filled polygons if needed
        if self.render_mode in ["filled", "both"]:
            for face in self.faces:
                glLineWidth(1.0)
                if len(face) == 3:
                    glBegin(GL_TRIANGLES)
                elif len(face) == 4:
                    glBegin(GL_QUADS)
                else:
                    glBegin(GL_POLYGON)

                glColor3f(0.4, 0.4, 0.4)
                for vertex in face:
                    if 0 <= vertex < self.vertcount:
                        objcords = self.verts[vertex].cords()
                        glVertex3f(objcords[0], objcords[1], objcords[2])
                glEnd()

    def applyobjtransform(self, matrix_b):
        if not self.center:
            self.center = self.calculate_center()
        else:
            self.center = self.calculate_center()

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



    def simple_subdivision(self):
        # Store original faces and vertex count
        original_faces = self.faces.copy()
        original_vertex_count = self.vertcount

        # Dictionary to store midpoints of edges
        # Key: tuple of (vertex1_idx, vertex2_idx) - sorted to ensure uniqueness
        # Value: index of the midpoint vertex
        edge_midpoints = {}

        # Dictionary to store center points for each face
        face_centers = {}

        # Process each face
        for face_idx, face in enumerate(original_faces):
            face_vertex_count = len(face)

            # Calculate face center point
            center_x = sum(self.getvert(v_idx).x for v_idx in face) / face_vertex_count
            center_y = sum(self.getvert(v_idx).y for v_idx in face) / face_vertex_count
            center_z = sum(self.getvert(v_idx).z for v_idx in face) / face_vertex_count

            # Add face center point
            center_idx = self.addvert(vec3d.vec3d(center_x, center_y, center_z, 1))
            face_centers[face_idx] = center_idx

            # For each edge in the face, find or create midpoint
            face_midpoints = []
            for i in range(face_vertex_count):
                # Get vertices of the edge
                v1_idx = face[i]
                v2_idx = face[(i + 1) % face_vertex_count]

                # Create a unique key for this edge (ensure v1_idx < v2_idx)
                edge_key = tuple(sorted([v1_idx, v2_idx]))

                # Check if we already created a midpoint for this edge
                if edge_key in edge_midpoints:
                    face_midpoints.append(edge_midpoints[edge_key])
                else:
                    # Get vertex positions
                    v1 = self.getvert(v1_idx)
                    v2 = self.getvert(v2_idx)

                    # Calculate midpoint
                    midpoint_x = (v1.x + v2.x) / 2
                    midpoint_y = (v1.y + v2.y) / 2
                    midpoint_z = (v1.z + v2.z) / 2

                    # Add new vertex
                    midpoint_idx = self.addvert(vec3d.vec3d(midpoint_x, midpoint_y, midpoint_z, 1))

                    # Store midpoint index
                    edge_midpoints[edge_key] = midpoint_idx
                    face_midpoints.append(midpoint_idx)

        # Remove all original faces
        self.faces = []

        # Create new faces
        for face_idx, face in enumerate(original_faces):
            face_vertex_count = len(face)
            center_idx = face_centers[face_idx]

            if face_vertex_count == 3:  # Triangle face
                # Get the three original vertices
                v0, v1, v2 = face

                # Get the three midpoints (in order)
                e0 = edge_midpoints[tuple(sorted([v0, v1]))]
                e1 = edge_midpoints[tuple(sorted([v1, v2]))]
                e2 = edge_midpoints[tuple(sorted([v2, v0]))]

                # Create four equal triangles - one for each original vertex and one in the middle
                self.faces.append([v0, e0, e2])  # Triangle using vertex 0
                self.faces.append([v1, e1, e0])  # Triangle using vertex 1
                self.faces.append([v2, e2, e1])  # Triangle using vertex 2
                self.faces.append([e0, e1, e2])  # Center triangle

            elif face_vertex_count == 4:  # Quad face
                # Get the four original vertices
                v0, v1, v2, v3 = face

                # Get the four midpoints (in order)
                e0 = edge_midpoints[tuple(sorted([v0, v1]))]
                e1 = edge_midpoints[tuple(sorted([v1, v2]))]
                e2 = edge_midpoints[tuple(sorted([v2, v3]))]
                e3 = edge_midpoints[tuple(sorted([v3, v0]))]

                # Create four quads connecting vertices, midpoints and center
                self.faces.append([v0, e0, center_idx, e3])
                self.faces.append([v1, e1, center_idx, e0])
                self.faces.append([v2, e2, center_idx, e1])
                self.faces.append([v3, e3, center_idx, e2])

            else:  # n-gon face where n > 4
                # For each vertex in the face, create a quad connecting:
                # - The vertex
                # - The midpoint to the next vertex
                # - The center point
                # - The midpoint to the previous vertex
                for i in range(face_vertex_count):
                    vertex_idx = face[i]

                    # Get indices of adjacent vertices
                    prev_vertex_idx = face[(i - 1) % face_vertex_count]
                    next_vertex_idx = face[(i + 1) % face_vertex_count]

                    # Get midpoint indices
                    prev_mid_idx = edge_midpoints[tuple(sorted([vertex_idx, prev_vertex_idx]))]
                    next_mid_idx = edge_midpoints[tuple(sorted([vertex_idx, next_vertex_idx]))]

                    # Create a quad face
                    self.faces.append([vertex_idx, next_mid_idx, center_idx, prev_mid_idx])
