import numpy as np
from clipping import _clip_distance, clipping
from pipeline_types import Triangle, Vertex


def _make_vertex(x, y, z, w=1.0):
    clip = np.array([x, y, z, w], dtype=np.float64)
    return Vertex(
        position=np.zeros(3),
        texcoord=np.zeros(2),
        color=np.ones(3),
        clip_position=clip,
    )


def test_clip_distance_right_plane():
    # plane 0: x + w >= 0
    v = np.array([0.5, 0.0, 0.0, 1.0])
    assert _clip_distance(v, 0) == 1.5  # 0.5 + 1.0


def test_clip_distance_left_plane():
    # plane 1: w - x >= 0
    v = np.array([0.5, 0.0, 0.0, 1.0])
    assert _clip_distance(v, 1) == 0.5  # 1.0 - 0.5


def test_fully_inside_triangle_returns_one():
    v0 = _make_vertex(0.0, 0.0, 0.0)
    v1 = _make_vertex(0.5, 0.0, 0.0)
    v2 = _make_vertex(0.0, 0.5, 0.0)
    tri = Triangle(v0, v1, v2)
    result = clipping(tri)
    assert len(result) == 1


def test_fully_outside_triangle_returns_empty():
    # w=0 means vertex is at infinity; x=2, so x+w < 0 on all vertices
    v0 = _make_vertex(2.0, 0.0, 0.0, w=0.0)
    v1 = _make_vertex(3.0, 0.0, 0.0, w=0.0)
    v2 = _make_vertex(2.0, 1.0, 0.0, w=0.0)
    tri = Triangle(v0, v1, v2)
    result = clipping(tri)
    assert result == []
