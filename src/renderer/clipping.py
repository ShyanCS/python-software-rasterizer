"""Homogeneous triangle clipping against the view frustum."""

from typing import List

import numpy as np
from pipeline_types import Triangle, Vertex


def _clip_distance(vertex_clip: np.ndarray, plane_index: int) -> float:
    """Compute the signed distance from a clip-space point to a frustum plane."""
    x, y, z, w = vertex_clip
    if plane_index == 0:
        return x + w
    elif plane_index == 1:
        return w - x
    elif plane_index == 2:
        return y + w
    elif plane_index == 3:
        return w - y
    elif plane_index == 4:
        return z + w
    elif plane_index == 5:
        return w - z
    return 0.0


def _lerp_vertex(va: Vertex, vb: Vertex, t: float) -> Vertex:
    """Linearly interpolate all attributes between two vertices."""
    return Vertex(
        position=va.position * (1.0 - t) + vb.position * t,
        texcoord=va.texcoord * (1.0 - t) + vb.texcoord * t,
        color=va.color * (1.0 - t) + vb.color * t,
        clip_position=va.clip_position * (1.0 - t) + vb.clip_position * t,
    )


def _clip_polygon_against_plane(vertices: List[Vertex], plane_index: int) -> List[Vertex]:
    """Clip a convex polygon against a single frustum plane."""
    if not vertices:
        return []

    output = []
    n = len(vertices)

    for i in range(n):
        current = vertices[i]
        next_v = vertices[(i + 1) % n]

        d_current = _clip_distance(current.clip_position, plane_index)
        d_next = _clip_distance(next_v.clip_position, plane_index)

        current_inside = d_current >= 0
        next_inside = d_next >= 0

        if current_inside:
            output.append(current)
            if not next_inside:
                t = d_current / (d_current - d_next)
                output.append(_lerp_vertex(current, next_v, t))
        elif next_inside:
            t = d_current / (d_current - d_next)
            output.append(_lerp_vertex(current, next_v, t))

    return output


def clipping(triangle: Triangle) -> List[Triangle]:
    """Clip a triangle against all six frustum planes."""
    polygon = triangle.as_list()

    for plane_idx in range(6):
        polygon = _clip_polygon_against_plane(polygon, plane_idx)
        if not polygon:
            return []

    triangles = []
    for i in range(1, len(polygon) - 1):
        triangles.append(Triangle(polygon[0], polygon[i], polygon[i + 1]))

    return triangles
