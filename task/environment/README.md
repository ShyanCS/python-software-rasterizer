# CPU Software Renderer

A minimal, deterministic CPU software rasterizer written in Python that renders 3D scenes to PNG images. It implements a full 3D graphics pipeline without using any GPU APIs.

## Directory Structure

```text
task/environment/
├── Dockerfile              # Docker environment definition
├── requirements.txt        # Python dependencies (numpy, Pillow)
├── README.md               # This file
└── renderer/               # Renderer source code
    ├── main.py             # Entry point
    ├── renderer.py         # Pipeline orchestration
    ├── scene.py            # Scene loading
    ├── pipeline_types.py   # Explicit data structures
    ├── transform.py        # Model/viewport transforms
    ├── vertex.py           # Vertex processing
    ├── geometry.py         # Triangle setup and edge functions
    ├── clipping.py         # Homogeneous frustum clipping
    ├── rasterizer.py       # Triangle rasterization
    ├── shaders.py          # Fragment shading
    ├── depth.py            # Depth testing
    ├── interpolation.py    # Perspective-correct interpolation
    ├── math3d.py           # Vector and matrix math
    ├── camera.py           # Camera utilities
    ├── mesh.py             # OBJ loader
    ├── texture.py          # Texture sampling
    ├── utils.py            # Helper functions
    ├── assets/             # OBJ files and images
    └── scenes/             # Scene JSON definitions
```

## How to Run

### Locally

Ensure you have Python 3 installed.
```bash
cd task/environment/renderer
pip install numpy Pillow
OUTPUT_DIR=./output python main.py
```
Images will be generated in `task/environment/renderer/output`.

### Using Docker

```bash
cd task/environment
docker build -t software-renderer .
docker run -v $(pwd)/output:/app/output software-renderer
```

## Scene Format

Scenes are defined in JSON format. Example:
```json
{
    "camera": {
        "eye": [0.0, 0.0, 5.0],
        "target": [0.0, 0.0, 0.0],
        "up": [0.0, 1.0, 0.0],
        "fov": 45.0,
        "near": 0.1,
        "far": 100.0,
        "width": 512,
        "height": 512
    },
    "meshes": [
        {
            "obj_file": "assets/cube.obj",
            "transform": {
                "translate": [0.0, 0.0, 0.0],
                "rotate": [0.0, 45.0, 0.0],
                "scale": [1.0, 1.0, 1.0]
            },
            "default_color": [1.0, 0.0, 0.0]
        }
    ],
    "output": "rendered_cube.png",
    "background": [0.1, 0.1, 0.1]
}
```
