import numpy as np
from camera import look_at, perspective


def test_look_at_produces_4x4_matrix():
    eye = np.array([0.0, 0.0, 5.0])
    target = np.array([0.0, 0.0, 0.0])
    up = np.array([0.0, 1.0, 0.0])
    m = look_at(eye, target, up)
    assert m.shape == (4, 4)


def test_look_at_identity_when_on_axis():
    eye = np.array([0.0, 0.0, 1.0])
    target = np.array([0.0, 0.0, 0.0])
    up = np.array([0.0, 1.0, 0.0])
    m = look_at(eye, target, up)
    # Camera should look down -Z: right is +X, up is +Y
    np.testing.assert_almost_equal(m[0, :3], [1.0, 0.0, 0.0])
    np.testing.assert_almost_equal(m[1, :3], [0.0, 1.0, 0.0])


def test_perspective_produces_4x4_matrix():
    m = perspective(60.0, 16 / 9, 0.1, 100.0)
    assert m.shape == (4, 4)


def test_perspective_w_row():
    # OpenGL perspective: m[3, 2] == -1 (w gets -z)
    m = perspective(60.0, 1.0, 0.1, 100.0)
    assert m[3, 2] == -1.0
    assert m[3, 3] == 0.0


def test_perspective_near_far_clipping():
    near, far = 1.0, 10.0
    m = perspective(90.0, 1.0, near, far)
    # A point at (0, 0, -near, 1) in view space should map to z_clip = -near after projection
    v = np.array([0.0, 0.0, -near, 1.0])
    clip = m @ v
    # Normalized z should be -1 after perspective divide
    ndc_z = clip[2] / clip[3]
    np.testing.assert_almost_equal(ndc_z, -1.0)
