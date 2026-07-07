"""Transform operations for the graphics pipeline."""

import numpy as np
from math3d import (
    mat4_identity, mat4_translation, mat4_scaling,
    mat4_rotation_x, mat4_rotation_y, mat4_rotation_z,
    mat4_multiply
)
from utils import degrees_to_radians
from pipeline_types import Triangle

def build_model_matrix(transform: dict) -> np.ndarray:
    """Build a 4x4 model matrix from a transform specification."""
    model = mat4_identity()

    if 'scale' in transform:
        s = transform['scale']
        model = mat4_multiply(mat4_scaling(s[0], s[1], s[2]), model)

    if 'rotate' in transform:
        r = transform['rotate']
        rx = degrees_to_radians(r[0])
        ry = degrees_to_radians(r[1])
        rz = degrees_to_radians(r[2])
        model = mat4_multiply(mat4_rotation_x(rx), model)
        model = mat4_multiply(mat4_rotation_y(ry), model)
        model = mat4_multiply(mat4_rotation_z(rz), model)

    if 'translate' in transform:
        t = transform['translate']
        model = mat4_multiply(mat4_translation(t[0], t[1], t[2]), model)

    return model

def viewport_transform(triangle: Triangle, width: int, height: int):
    """Transform normalized device coordinates to screen coordinates in-place."""
    for vertex in triangle.as_list():
        ndc = vertex.ndc_position
        sx = (ndc[0] + 1.0) * 0.5 * width
        sy = (1.0 - ndc[1]) * 0.5 * height
        sz = (ndc[2] + 1.0) * 0.5
        vertex.screen_position = np.array([sx, sy, sz], dtype=np.float64)
