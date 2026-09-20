# PyOpenGL Graphics Assignments

Seven computer-graphics assignments in Python with PyOpenGL, building a rendering pipeline from immediate-mode drawing up to shadow-mapped scenes.

**Course:** CENG487 — Introduction to Computer Graphics  
**Institution:** İzmir Institute of Technology (IYTE) — İzmir, Türkiye

## Assignments

| Folder | What it implements |
|---|---|
| `assignment-01` | Matrix stack and object hierarchy — `mat3d.py` / `vec3d.py` provide 4x4 transform matrices and vector maths, composed into a drawn cube |
| `assignment-02` | Camera — a view matrix built from eye / target / up, with the scene orbiting the camera |
| `assignment-03` | Wavefront `.obj` loader (`wavefrontObjReader.py`) reading `ecube.obj` and `tori.obj` into vertex buffers |
| `assignment-04` | Texture mapping onto the imported meshes |
| `assignment-05` | GLSL pipeline (`vertex_shader.glsl`, `fragment_shader.glsl`), axis-aligned bounding boxes, scene/view separation |
| `assignment-06` | Two-slot multi-texturing — a Rubik's-cube texture blended against a checker — plus lighting |
| `assignment-07` | Shadow mapping: a depth pass from the light's point of view applied to a Cornell box (`CornellManifold.obj`, `light.py`) |

## Running

```bash
pip install PyOpenGL PyOpenGL-accelerate numpy Pillow
cd assignment-07 && python main.py
```

Keep **PyOpenGL 3.1.9** and **numpy 1.26.x** — numpy 2.x breaks PyOpenGL compatibility.
GLUT is used for windowing, so `freeglut` is required.

Assignments 1-4 run from `assignmentN.py`; 5-7 from `main.py`. Each folder is
self-contained and carries its own copy of the helper modules it needs.

## Third-party components

The course's rendering framework and worked tutorial samples are not redistributed here — see `ATTRIBUTION.md`.

---

Submitted reports, worksheets and lecture material are archived outside this
repository rather than committed, so the repo stays code-only.
