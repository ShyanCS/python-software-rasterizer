import numpy as np
from geometry import edge_function, triangle_setup
from pipeline_types import Triangle, Vertex


def test_edge_function():
    a = np.array([0, 0])
    b = np.array([1, 0])
    c = np.array([0, 1])
    # Edge a->b is along x axis (y=0). Point c is at (0, 1).
    # edge_function(a, b, c) = (1-0)*(1-0) - (0-0)*(0-0) = 1
    val = edge_function(a, b, c)
    assert val == 1.0


def test_triangle_setup():
    v0 = Vertex(
        position=np.zeros(3), texcoord=np.zeros(2), color=np.zeros(3), clip_position=np.zeros(4)
    )
    v1 = Vertex(
        position=np.zeros(3), texcoord=np.zeros(2), color=np.zeros(3), clip_position=np.zeros(4)
    )
    v2 = Vertex(
        position=np.zeros(3), texcoord=np.zeros(2), color=np.zeros(3), clip_position=np.zeros(4)
    )

    v0.screen_position = np.array([10.0, 10.0, 0.0])
    v1.screen_position = np.array([20.0, 10.0, 0.0])
    v2.screen_position = np.array([10.0, 20.0, 0.0])

    t = Triangle(v0, v1, v2)
    bbox, area = triangle_setup(t, 100, 100)

    assert bbox == (10, 20, 10, 20)
    assert area == 100.0
