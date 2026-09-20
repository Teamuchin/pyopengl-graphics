# CENG 487 Assignment2 by
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
                glBegin(GL_LINE_LOOP)
                glColor3f(0.3, 0.5, 1.0)  # Blue for wireframe
                for vertex in face:
                    if 0 <= vertex < self.vertcount:
                        objcords = self.verts[vertex].cords()
                        glVertex3f(objcords[0], objcords[1], objcords[2])
                glEnd()

        # Draw filled polygons if needed
        if self.render_mode in ["filled", "both"]:
            for face in self.faces:
                if len(face) == 3:
                    glBegin(GL_TRIANGLES)
                elif len(face) == 4:
                    glBegin(GL_QUADS)
                else:
                    glBegin(GL_POLYGON)

                glColor3f(1.0, 0.5, 0.0)  # Orange for filled faces
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

    def create_torus(self, major_radius=1.0, minor_radius=0.3, major_segments=20, minor_segments=10):
        # Clear existing geometry
        self.verts = []
        self.faces = []
        self.vertcount = 0

        # Generate vertices
        for i in range(major_segments):
            major_angle = 2 * math.pi * i / major_segments
            major_x = math.cos(major_angle)
            major_y = math.sin(major_angle)

            for j in range(minor_segments):
                minor_angle = 2 * math.pi * j / minor_segments
                minor_x = math.cos(minor_angle)
                minor_y = math.sin(minor_angle)

                # Calculate the point on the torus
                x = (major_radius + minor_radius * minor_x) * major_x
                y = (major_radius + minor_radius * minor_x) * major_y
                z = minor_radius * minor_y

                self.addvert(vec3d.vec3d(x, y, z, 1))

        # Generate faces
        for i in range(major_segments):
            for j in range(minor_segments):
                # Calculate the indices of the four vertices for this face
                v1 = i * minor_segments + j
                v2 = i * minor_segments + (j + 1) % minor_segments
                v3 = ((i + 1) % major_segments) * minor_segments + (j + 1) % minor_segments
                v4 = ((i + 1) % major_segments) * minor_segments + j

                # Add the face
                self.faces.append([v1, v2, v3, v4])

        self.setdrawtype("quad")
        return self

    def create_cylinder(self, radius=1.0, height=2.0, segments=20):
        # Clear existing geometry
        self.verts = []
        self.faces = []
        self.vertcount = 0

        half_height = height / 2.0

        # Generate vertices for top and bottom circles
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)

            # Top circle vertex
            self.addvert(vec3d.vec3d(x, half_height, y, 1))
            # Bottom circle vertex
            self.addvert(vec3d.vec3d(x, -half_height, y, 1))

        # Add center points for top and bottom faces
        top_center_idx = self.vertcount
        self.addvert(vec3d.vec3d(0, half_height, 0, 1))

        bottom_center_idx = self.vertcount
        self.addvert(vec3d.vec3d(0, -half_height, 0, 1))

        # Generate side faces (quads)
        for i in range(segments):
            v1 = i * 2  # Top vertex of current segment
            v2 = (i * 2 + 2) % (segments * 2)  # Top vertex of next segment
            v3 = (i * 2 + 3) % (segments * 2)  # Bottom vertex of next segment
            v4 = i * 2 + 1  # Bottom vertex of current segment

            self.faces.append([v1, v2, v3, v4])

        # Generate top and bottom faces (triangles)
        for i in range(segments):
            v1 = i * 2  # Top vertex of current segment
            v2 = (i * 2 + 2) % (segments * 2)  # Top vertex of next segment

            # Top face triangle
            self.faces.append([v1, v2, top_center_idx])

            v3 = i * 2 + 1  # Bottom vertex of current segment
            v4 = (i * 2 + 3) % (segments * 2)  # Bottom vertex of next segment

            # Bottom face triangle
            self.faces.append([v3, v4, bottom_center_idx])

        self.setdrawtype("triangle")
        return self

    def create_sphere(self, radius=1.0, slices=12, stacks=12):
        # Clear existing geometry
        self.verts = []
        self.faces = []
        self.vertcount = 0

        # Add top vertex
        top_idx = self.vertcount
        self.addvert(vec3d.vec3d(0, radius, 0, 1))

        # Generate vertices for the body
        for i in range(1, stacks):
            phi = math.pi * i / stacks
            y = radius * math.cos(phi)
            slice_radius = radius * math.sin(phi)

            for j in range(slices):
                theta = 2 * math.pi * j / slices
                x = slice_radius * math.cos(theta)
                z = slice_radius * math.sin(theta)

                self.addvert(vec3d.vec3d(x, y, z, 1))

        # Add bottom vertex
        bottom_idx = self.vertcount
        self.addvert(vec3d.vec3d(0, -radius, 0, 1))

        # Generate top cap triangles
        for i in range(slices):
            v1 = top_idx
            v2 = 1 + i
            v3 = 1 + (i + 1) % slices

            self.faces.append([v1, v2, v3])

        # Generate body quads
        for i in range(1, stacks - 1):
            row1_start = 1 + (i - 1) * slices
            row2_start = 1 + i * slices

            for j in range(slices):
                v1 = row1_start + j
                v2 = row1_start + (j + 1) % slices
                v3 = row2_start + (j + 1) % slices
                v4 = row2_start + j

                self.faces.append([v1, v2, v3, v4])

        # Generate bottom cap triangles
        bottom_row_start = 1 + (stacks - 2) * slices
        for i in range(slices):
            v1 = bottom_idx
            v2 = bottom_row_start + i
            v3 = bottom_row_start + (i + 1) % slices

            self.faces.append([v1, v3, v2])  # Note the order change to maintain proper winding

        self.setdrawtype("triangle")
        return self

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

    def create_polyhedron_plane(self, edge_count):
        self.verts = []
        polyhedron_faces = [[]]
        self.vertcount = 0
        for i in range(edge_count):
            angle = 2 * math.pi * i / edge_count
            x = 1 * math.cos(angle)
            y = 1 * math.sin(angle)
            vertind = self.addvert(vec3d.vec3d(x, y, 0, 1))
            polyhedron_faces[0].append(vertind)
        self.setfaces(polyhedron_faces)
        fixinitrotation = mat3d.mat3d()
        fixinitrotation.addrotation(270 - (180 / edge_count), "z")
        self.applyobjtransform(fixinitrotation)

    def create_platonic_solid(self, solid_type):
        # Clear existing geometry
        self.verts = []
        self.faces = []
        self.vertcount = 0

        solid_type = solid_type.lower()

        if solid_type == "tetrahedron":
            # Regular tetrahedron with equal edge lengths
            # The coordinates are calculated to place vertices on a unit sphere
            a = 1.0 / math.sqrt(2)  # Distance from origin to vertices

            # Add vertices
            self.addvert(vec3d.vec3d(a, 0, -a / 2, 1))
            self.addvert(vec3d.vec3d(-a, 0, -a / 2, 1))
            self.addvert(vec3d.vec3d(0, a, a / 2, 1))
            self.addvert(vec3d.vec3d(0, -a, a / 2, 1))

            # Add faces with proper winding order
            self.faces.append([0, 2, 1])
            self.faces.append([0, 1, 3])
            self.faces.append([0, 3, 2])
            self.faces.append([1, 2, 3])

        elif solid_type == "hexahedron" or solid_type == "cube":
            # Hexahedron (cube) - 6 square faces
            s = 1 / math.sqrt(3)  # Scaling to place on unit sphere

            # Add vertices
            self.addvert(vec3d.vec3d(-s, s, s, 1))  # 0: Front top left
            self.addvert(vec3d.vec3d(s, s, s, 1))  # 1: Front top right
            self.addvert(vec3d.vec3d(s, -s, s, 1))  # 2: Front bottom right
            self.addvert(vec3d.vec3d(-s, -s, s, 1))  # 3: Front bottom left
            self.addvert(vec3d.vec3d(-s, s, -s, 1))  # 4: Back top left
            self.addvert(vec3d.vec3d(s, s, -s, 1))  # 5: Back top right
            self.addvert(vec3d.vec3d(s, -s, -s, 1))  # 6: Back bottom right
            self.addvert(vec3d.vec3d(-s, -s, -s, 1))  # 7: Back bottom left

            # Add faces with consistent winding
            self.faces.append([0, 1, 2, 3])  # Front face
            self.faces.append([5, 4, 7, 6])  # Back face
            self.faces.append([4, 0, 3, 7])  # Left face
            self.faces.append([1, 5, 6, 2])  # Right face
            self.faces.append([4, 5, 1, 0])  # Top face
            self.faces.append([3, 2, 6, 7])  # Bottom face

        elif solid_type == "octahedron":
            # Octahedron - 8 triangular faces
            s = 1.0  # Distance from origin to vertices

            # Add vertices - 6 vertices at unit distance along each axis
            self.addvert(vec3d.vec3d(0, 0, s, 1))  # Top
            self.addvert(vec3d.vec3d(s, 0, 0, 1))  # Right
            self.addvert(vec3d.vec3d(0, 0, -s, 1))  # Bottom
            self.addvert(vec3d.vec3d(-s, 0, 0, 1))  # Left
            self.addvert(vec3d.vec3d(0, s, 0, 1))  # Front
            self.addvert(vec3d.vec3d(0, -s, 0, 1))  # Back

            # Add faces with consistent winding order
            self.faces.append([0, 1, 4])
            self.faces.append([0, 4, 3])
            self.faces.append([0, 3, 5])
            self.faces.append([0, 5, 1])
            self.faces.append([2, 4, 1])
            self.faces.append([2, 3, 4])
            self.faces.append([2, 5, 3])
            self.faces.append([2, 1, 5])


        elif solid_type == "icosahedron":
            # Icosahedron - 20 triangular faces
            phi = (1 + math.sqrt(5)) / 2  # Golden ratio
            norm = math.sqrt(phi * phi + 1)  # Normalization factor

            # The coordinates are normalized to place vertices on a unit sphere
            a = 1.0 / norm
            b = phi / norm

            # Define 12 vertices of the icosahedron
            vertices = [
                (-a, 0, b), (a, 0, b), (-a, 0, -b), (a, 0, -b),
                (0, b, a), (0, b, -a), (0, -b, a), (0, -b, -a),
                (b, a, 0), (-b, a, 0), (b, -a, 0), (-b, -a, 0)
            ]

            # Add all vertices
            for v in vertices:
                self.addvert(vec3d.vec3d(v[0], v[1], v[2], 1))

            # Define the 20 triangular faces with correct winding order
            faces = [
                [0, 4, 1], [0, 9, 4], [9, 5, 4], [4, 5, 8], [4, 8, 1],
                [8, 10, 1], [8, 3, 10], [5, 3, 8], [5, 2, 3], [2, 7, 3],
                [7, 10, 3], [7, 6, 10], [7, 11, 6], [11, 0, 6], [0, 1, 6],
                [6, 1, 10], [9, 0, 11], [9, 11, 2], [9, 2, 5], [7, 2, 11]
            ]

            # Add all faces
            for face in faces:
                self.faces.append(face)

        else:
            print(f"Unknown solid type: {solid_type}")
            print("Available types: tetrahedron, hexahedron, octahedron, icosahedron")
            return self

        # Set draw type based on the solid
        if solid_type == "hexahedron" or solid_type == "cube":
            self.setdrawtype("quad")
        else:
            self.setdrawtype("triangle")

        # Center the solid at the origin
        self.center = self.calculate_center()

        return self