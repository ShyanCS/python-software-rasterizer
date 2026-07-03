"""Vertex processing and projection transformations."""

import numpy as np
from math3d import vec3_to_vec4, mat4_transform_vec4
from pipeline_types import Triangle, Vertex
from typing import List

def vertex_processing(
    positions: List[np.ndarray],
    texcoords: List[np.ndarray],
    vertex_colors: List[np.ndarray],
    v_indices: list,
    vt_indices: list,
    mvp: np.ndarray
) -> Triangle:
    """Transform vertices to clip space and construct a Triangle."""
    vertices = []
    for i in range(3):
        vi = v_indices[i]
        pos = positions[vi]
        clip_pos = mat4_transform_vec4(mvp, vec3_to_vec4(pos))

        if vt_indices and i < len(vt_indices):
            tc = texcoords[vt_indices[i]].copy()
        else:
            tc = np.array([0.0, 0.0], dtype=np.float64)

        color = vertex_colors[vi].copy()

        vertex = Vertex(
            position=pos.copy(),
            texcoord=tc,
            color=color,
            clip_position=clip_pos
        )
        vertices.append(vertex)
        
    return Triangle(vertices[0], vertices[1], vertices[2])

def perspective_divide(triangle: Triangle):
    """Convert clip space coordinates to normalized device coordinates in-place."""
    for vertex in triangle.as_list():
        cp = vertex.clip_position
        w = cp[3]
        vertex.clip_w = w
        vertex.ndc_position = np.array([cp[0] / w, cp[1] / w, cp[2] / w], dtype=np.float64)
