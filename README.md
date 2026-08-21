# Python CPU Software Rasterizer

A standalone, from-scratch 3D software rasterizer written entirely in Python. This project demonstrates the core mathematics and pipeline stages of modern graphics rendering without relying on any external graphics libraries (like OpenGL, Vulkan, or DirectX).

## Features

- **Vertex Processing**: Transformations (Model, View, Projection) using custom 4x4 matrix math.
- **Perspective-Correct Interpolation**: Accurately interpolates vertex attributes (like texture coordinates and colors) across triangles using barycentric coordinates and the reciprocal of the homogeneous `W` coordinate.
- **Rasterization**: Triangle traversal and edge function evaluation.
- **Z-Buffering**: Depth testing for correct visibility ordering of overlapping geometry.
- **Texture Mapping**: Basic nearest-neighbor texture sampling.

## Project Structure

- `src/renderer/`: The core rendering engine.
  - `main.py`: CLI entrypoint.
  - `math3d.py`, `geometry.py`: Core math types and transformations.
  - `vertex.py`, `transform.py`: Vertex processing and viewport mapping.
  - `rasterizer.py`, `interpolation.py`: Triangle traversal and attribute interpolation.
  - `depth.py`, `clipping.py`: Depth testing and near-plane clipping.
  - `texture.py`: Texture loading and sampling.
- `src/renderer/scenes/`: Example JSON scenes describing camera parameters, objects, and materials.
- `src/renderer/assets/`: Obj models and PNG textures used by the scenes.
- `tests/`: Basic validation test suite.

## Installation

This project requires Python 3.9+ and very few dependencies.

```bash
# Clone the repository
git clone https://github.com/ShyanCS/python-software-rasterizer.git
cd python-software-rasterizer

# Install dependencies (only numpy and Pillow for image I/O)
pip install -r requirements.txt
```

## Usage

You can render a specific scene or all available scenes using the CLI:

```bash
# Render all scenes to the default 'output/' directory
python src/renderer/main.py

# Render a specific scene to a custom directory
python src/renderer/main.py --scene src/renderer/scenes/01_colored_cube.json --outdir my_renders
```

## Docker

You can also run the renderer in an isolated container using Docker Compose. The `output/` directory will be mounted automatically:

```bash
# Build and run the renderer to process all scenes
docker compose up
```

## Testing and CI

This repository uses GitHub Actions for continuous integration. The CI pipeline checks code formatting (using `black` and `ruff`) and runs the test suite.

To run tests locally with coverage:
```bash
pytest --cov=src/renderer --cov-report=term-missing tests/
```
