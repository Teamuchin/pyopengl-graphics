# Attribution

## What I did not write

This course used an instructor-authored class repository providing a rendering framework and a
set of worked tutorial samples (immediate-mode drawing through shadow mapping), plus a `Core/`
helper package and shared texture assets.

> **IYTE CENG487 — Introduction to Computer Graphics, class repository.**
> İzmir Institute of Technology (IYTE), Department of Computer Engineering.
> Framework and tutorial samples are the work of the course instructor.

That material is **not included in this repository** and is not redistributed.

## What I did write

Everything under `assignment-01/` through `assignment-07/` is my own work.

| Folder | Files |
|---|---|
| `assignment-01/` | `assignment1.py`, `globj.py`, `mat3d.py`, `vec3d.py` — 4 |
| `assignment-02/` | adds `camera.py` — 5 |
| `assignment-03/` | adds Wavefront `.obj` loading and mesh handling, `ecube.obj`, `tori.obj` — 8 |
| `assignment-04/` | adds texturing — 8 |
| `assignment-05/` | adds GLSL shaders, bounding volumes, scene graph — 12 |
| `assignment-06/` | adds multi-texture and lighting — 17 |
| `assignment-07/` | adds depth-map shadows, `CornellManifold.obj` — 19 |

Each folder is self-contained and carries its own copy of the helper modules it needs, so none
of these assignments depends on the instructor's framework at run time.

## Verified

Every `.py` and `.glsl` file here was hashed against the instructor's framework files and
tutorial samples: **no file is a byte-identical copy.** The framework is genuinely absent, not
merely renamed.
