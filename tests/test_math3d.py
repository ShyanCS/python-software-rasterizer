import numpy as np
from math3d import (
    cross,
    mat4_multiply,
    mat4_rotation_x,
    mat4_rotation_y,
    mat4_rotation_z,
    normalize,
)


def test_mat4_multiply():
    a = np.eye(4)
    b = np.eye(4)
    b[0, 3] = 5.0
    c = mat4_multiply(a, b)
    np.testing.assert_array_equal(c, b)


def test_mat4_rotation_x():
    rot = mat4_rotation_x(np.pi / 2)
    vec = np.array([0, 1, 0, 1])
    res = rot @ vec
    np.testing.assert_almost_equal(res, [0, 0, 1, 1])


def test_mat4_rotation_y():
    rot = mat4_rotation_y(np.pi / 2)
    vec = np.array([1, 0, 0, 1])
    res = rot @ vec
    np.testing.assert_almost_equal(res, [0, 0, -1, 1])


def test_mat4_rotation_z():
    rot = mat4_rotation_z(np.pi / 2)
    vec = np.array([1, 0, 0, 1])
    res = rot @ vec
    np.testing.assert_almost_equal(res, [0, 1, 0, 1])


def test_normalize():
    v = np.array([3.0, 4.0, 0.0])
    n = normalize(v)
    np.testing.assert_almost_equal(n, [0.6, 0.8, 0.0])


def test_cross():
    v1 = np.array([1, 0, 0], dtype=np.float64)
    v2 = np.array([0, 1, 0], dtype=np.float64)
    res = cross(v1, v2)
    np.testing.assert_array_equal(res, [0, 0, 1])
