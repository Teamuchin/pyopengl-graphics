# Setup

Each `assignment-NN/` folder is standalone — the course framework is not needed to run them.

## Requirements

```bash
pip install PyOpenGL PyOpenGL-accelerate numpy Pillow
```

The course pinned **PyOpenGL 3.1.9** and **numpy 1.26.4**; numpy 2.x breaks PyOpenGL
compatibility, so those are the safe versions. GLUT is used for windowing and mouse input, so
a system GLUT library is required (`freeglut` / `libglut`).

## Run

```bash
cd assignment-07
python main.py
```

Assignments 1-4 use `assignmentN.py` as the entry point; 5-7 use `main.py`.

## About the missing framework

The instructor's class framework and the worked tutorial samples
(`01-HelloOpenGL.py` ... `11-HelloModernOpenGLDepthMapShadow.py`, `Core/`) are deliberately not
included. Obtain them from the course repository if you want to compare against them — they are
not redistributed here.
