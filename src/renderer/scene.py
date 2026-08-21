"""Scene definition loading from JSON files."""

import json
from typing import List, Optional

import numpy as np
from pipeline_types import CameraParameters


class SceneMeshEntry:
    def __init__(
        self,
        obj_file: str,
        transform: dict,
        vertex_colors: Optional[List[List[float]]] = None,
        default_color: Optional[List[float]] = None,
        texture_file: Optional[str] = None,
        generate_texture: Optional[str] = None,
    ):
        self.obj_file = obj_file
        self.transform = transform
        self.vertex_colors = vertex_colors
        self.default_color = default_color
        self.texture_file = texture_file
        self.generate_texture = generate_texture


class SceneDefinition:
    def __init__(
        self,
        camera: CameraParameters,
        meshes: List[SceneMeshEntry],
        output: str,
        background: List[float],
    ):
        self.camera = camera
        self.meshes = meshes
        self.output = output
        self.background = background


def load_scene(filepath: str) -> SceneDefinition:
    """Load a scene definition from a JSON file."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON scene file '{filepath}': {e}")
    except FileNotFoundError:
        raise ValueError(f"Scene file not found: '{filepath}'")

    if "camera" not in data:
        raise ValueError("Scene file missing required 'camera' configuration.")
    if "meshes" not in data or not isinstance(data["meshes"], list):
        raise ValueError("Scene file missing required 'meshes' array.")
    if "output" not in data:
        raise ValueError("Scene file missing required 'output' filename.")

    cam_data = data["camera"]
    required_cam_keys = ["eye", "target", "up", "fov", "near", "far", "width", "height"]
    for key in required_cam_keys:
        if key not in cam_data:
            raise ValueError(f"Camera configuration missing required key: '{key}'")

    camera = CameraParameters(
        eye=np.array(cam_data["eye"], dtype=np.float64),
        target=np.array(cam_data["target"], dtype=np.float64),
        up=np.array(cam_data["up"], dtype=np.float64),
        fov=float(cam_data["fov"]),
        near=float(cam_data["near"]),
        far=float(cam_data["far"]),
        width=int(cam_data["width"]),
        height=int(cam_data["height"]),
    )

    meshes = []
    for i, mesh_data in enumerate(data["meshes"]):
        if "obj_file" not in mesh_data:
            raise ValueError(f"Mesh entry {i} missing required 'obj_file' path.")

        entry = SceneMeshEntry(
            obj_file=mesh_data["obj_file"],
            transform=mesh_data.get("transform", {}),
            vertex_colors=mesh_data.get("vertex_colors"),
            default_color=mesh_data.get("default_color"),
            texture_file=mesh_data.get("texture_file"),
            generate_texture=mesh_data.get("generate_texture"),
        )
        meshes.append(entry)

    background = data.get("background", [0.1, 0.1, 0.1])

    return SceneDefinition(
        camera=camera, meshes=meshes, output=data["output"], background=background
    )
