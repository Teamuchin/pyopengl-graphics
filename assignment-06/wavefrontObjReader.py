# CENG 487 Assignment6 by
# Timuçin Topcu
# StudentId:310201095
# 06.2025
import numpy


class OBJLoader:
    def __init__(self, filepath):
        self.vertices = []
        self.uvs = []
        self.faces = []
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    self.parse_line(line)
        except FileNotFoundError:
            print(f"ERROR: OBJ file not found at '{filepath}'")

    def parse_line(self, line):
        if line.startswith('#') or not line.strip():
            return
        parts = line.strip().split()
        if not parts:
            return

        line_type = parts[0]
        values = parts[1:]

        if line_type == 'v':
            self.vertices.append([float(v) for v in values])
        elif line_type == 'vt':
            self.uvs.append([float(v) for v in values])
        elif line_type == 'f':
            self.parse_face(values)

    def parse_face(self, values):
        face_vertices = []
        for val in values:
            v_vt_vn = val.split('/')
            v_idx = int(v_vt_vn[0]) - 1
            vt_idx = int(v_vt_vn[1]) - 1 if len(v_vt_vn) > 1 and v_vt_vn[1] else -1
            face_vertices.append((v_idx, vt_idx))
        for i in range(1, len(face_vertices) - 1):
            self.faces.append([face_vertices[0], face_vertices[i], face_vertices[i + 1]])

    def get_model_data(self):
        final_vertices = []
        final_uvs = []
        final_faces = []

        vertex_cache = {}

        for face in self.faces:
            face_indices = []
            for v_idx, vt_idx in face:
                cache_key = (v_idx, vt_idx)
                if cache_key in vertex_cache:
                    final_index = vertex_cache[cache_key]
                else:
                    final_index = len(final_vertices) // 4
                    vertex_cache[cache_key] = final_index
                    pos = self.vertices[v_idx]
                    final_vertices.extend([pos[0], pos[1], pos[2], 1.0])
                    if vt_idx != -1 and self.uvs:
                        uv = self.uvs[vt_idx]
                        final_uvs.extend([uv[0], uv[1]])
                    else:
                        final_uvs.extend([0.0, 0.0])
                face_indices.append(final_index)
            final_faces.append(face_indices)
        return (
            numpy.array(final_vertices, dtype='float32'),
            numpy.array(final_uvs, dtype='float32'),
            numpy.array(final_faces, dtype='uint32')
        )