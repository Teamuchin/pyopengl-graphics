# CENG 487 Assignment4 by
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
        self.edge_connections = [] #first element is the edge
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
    def setedgeconnections(self):
        for face in self.faces:
            for i in face:
                if face[(i+1)%len(face)] not in self.edge_connections[face[i]]:
                    self.edge_connections[face[i]].append(face[(i+1)%len(face)])
                if face[(i-1)%len(face)] not in self.edge_connections[face[i]]:
                    self.edge_connections[face[i]].append(face[(i-1)%len(face)])
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

    def catmull_clark_subdivision(self):
        original_faces = self.faces.copy()
        original_vertex_count = self.vertcount
        face_centers = {}
        for face_idx, face in enumerate(original_faces):
            center_x = sum(self.getvert(v_idx).x for v_idx in face) / len(face)
            center_y = sum(self.getvert(v_idx).y for v_idx in face) / len(face)
            center_z = sum(self.getvert(v_idx).z for v_idx in face) / len(face)
            center_idx = self.addvert(vec3d.vec3d(center_x, center_y, center_z, 1))
            face_centers[face_idx] = center_idx

        # Step 2: Calculate edge points
        edge_points = {}
        # Process each edge once
        for face_idx, face in enumerate(original_faces):
            for i in range(len(face)):
                v1_idx = face[i]
                v2_idx = face[(i + 1) % len(face)]
                edge_key = tuple(sorted([v1_idx, v2_idx]))
                if edge_key in edge_points:
                    continue
                v1 = self.getvert(v1_idx)
                v2 = self.getvert(v2_idx)
                shared_faces = []
                for j in range(len(original_faces)):
                    face_j = original_faces[j]
                    if v1_idx in face_j and v2_idx in face_j:
                        for k in range(len(face_j)):
                            if (face_j[k] == v1_idx and face_j[(k + 1) % len(face_j)] == v2_idx) or \
                                    (face_j[k] == v2_idx and face_j[(k + 1) % len(face_j)] == v1_idx):
                                shared_faces.append(j)
                                break

                if len(shared_faces) == 1:
                    midpoint_x = (v1.x + v2.x) / 2
                    midpoint_y = (v1.y + v2.y) / 2
                    midpoint_z = (v1.z + v2.z) / 2
                else:
                    midpoint_x = (v1.x + v2.x + self.verts[face_centers[shared_faces[0]]].x + self.verts[face_centers[shared_faces[1]]].x) / 4
                    midpoint_y = (v1.y + v2.y + self.verts[face_centers[shared_faces[0]]].y + self.verts[face_centers[shared_faces[1]]].y) / 4
                    midpoint_z = (v1.z + v2.z + self.verts[face_centers[shared_faces[0]]].z + self.verts[face_centers[shared_faces[1]]].z) / 4
                edge_point_idx = self.addvert(vec3d.vec3d(midpoint_x, midpoint_y, midpoint_z, 1))
                edge_points[edge_key] = edge_point_idx

        # Step 3: Calculate new positions for original vertices
        new_vertex_positions = {}
        for vertex_idx in range(original_vertex_count):
            original_vertex = self.getvert(vertex_idx)

            # Find all faces containing this vertex
            adjacent_faces = []
            for face_idx, face in enumerate(original_faces):
                if vertex_idx in face:
                    adjacent_faces.append(face_idx)
            adjacent_edges = []
            for face_idx in adjacent_faces:
                face = original_faces[face_idx]
                vertex_index_in_face = face.index(vertex_idx)
                prev_vertex = face[(vertex_index_in_face - 1) % len(face)]
                next_vertex = face[(vertex_index_in_face + 1) % len(face)]
                adjacent_edges.append(tuple(sorted([vertex_idx, prev_vertex])))
                adjacent_edges.append(tuple(sorted([vertex_idx, next_vertex])))
            adjacent_edges = list(set(adjacent_edges))
            f_x = sum(self.getvert(face_centers[face_idx]).x for face_idx in adjacent_faces) / len(adjacent_faces)
            f_y = sum(self.getvert(face_centers[face_idx]).y for face_idx in adjacent_faces) / len(adjacent_faces)
            f_z = sum(self.getvert(face_centers[face_idx]).z for face_idx in adjacent_faces) / len(adjacent_faces)
            edge_midpoint_sum_x = 0
            edge_midpoint_sum_y = 0
            edge_midpoint_sum_z = 0

            for edge in adjacent_edges:
                v1 = self.getvert(edge[0])
                v2 = self.getvert(edge[1])
                edge_midpoint_sum_x += (v1.x + v2.x) / 2
                edge_midpoint_sum_y += (v1.y + v2.y) / 2
                edge_midpoint_sum_z += (v1.z + v2.z) / 2

            r_x = edge_midpoint_sum_x / len(adjacent_edges)
            r_y = edge_midpoint_sum_y / len(adjacent_edges)
            r_z = edge_midpoint_sum_z / len(adjacent_edges)
            n = len(adjacent_faces)
            new_x = (f_x + 2 * r_x + (n - 3) * original_vertex.x) / n
            new_y = (f_y + 2 * r_y + (n - 3) * original_vertex.y) / n
            new_z = (f_z + 2 * r_z + (n - 3) * original_vertex.z) / n
            new_vertex_positions[vertex_idx] = vec3d.vec3d(new_x, new_y, new_z, 1)
        for vertex_idx, new_position in new_vertex_positions.items():
            self.verts[vertex_idx] = new_position
        new_faces = []
        for face_idx, face in enumerate(original_faces):
            face_point_idx = face_centers[face_idx]
            for i in range(len(face)):
                vertex_idx = face[i]
                next_vertex_idx = face[(i + 1) % len(face)]
                current_edge_key = tuple(sorted([vertex_idx, next_vertex_idx]))
                prev_i = (i - 1) % len(face)
                prev_vertex_idx = face[prev_i]
                prev_edge_key = tuple(sorted([vertex_idx, prev_vertex_idx]))
                current_edge_point_idx = edge_points[current_edge_key]
                prev_edge_point_idx = edge_points[prev_edge_key]
                new_quad = [vertex_idx, current_edge_point_idx, face_point_idx, prev_edge_point_idx]
                new_faces.append(new_quad)
        self.faces = new_faces
