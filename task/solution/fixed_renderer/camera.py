"""Camera and projection matrix construction.

Provides look-at view matrix and perspective projection matrix
following OpenGL-style conventions (right-handed coordinate system,
NDC z in [-1, 1], camera looks down -Z).
"""

import numpy as np
from math3d import normalize, cross, dot


def look_at(eye: np.ndarray, target: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Create a look-at view matrix.

    Constructs a view matrix that transforms world-space coordinates into
    camera/eye-space coordinates. The camera is positioned at 'eye', looking
    toward 'target', with the given 'up' direction.

    Convention: camera looks down -Z in view space, +X is right, +Y is up.

    Args:
        eye: Camera position in world space (3D vector).
        target: Point the camera looks at in world space (3D vector).
        up: World-space up direction (3D vector).

    Returns:
        4x4 view matrix as a numpy array.
    """
    forward = normalize(target - eye)
    right = normalize(cross(forward, up))
    cam_up = cross(right, forward)

    m = np.eye(4, dtype=np.float64)
    m[0, 0] = right[0]
    m[0, 1] = right[1]
    m[0, 2] = right[2]
    m[0, 3] = -dot(right, eye)
    m[1, 0] = cam_up[0]
    m[1, 1] = cam_up[1]
    m[1, 2] = cam_up[2]
    m[1, 3] = -dot(cam_up, eye)
    m[2, 0] = -forward[0]
    m[2, 1] = -forward[1]
    m[2, 2] = -forward[2]
    m[2, 3] = dot(forward, eye)
    return m


def perspective(fov_y_deg: float, aspect: float,
                near: float, far: float) -> np.ndarray:
    """Create a perspective projection matrix.

    Uses OpenGL-style conventions: NDC z ranges from -1 to 1,
    near and far are positive distances from the camera.

    The resulting matrix transforms view-space coordinates (where the
    camera looks down -Z) into clip-space coordinates suitable for
    homogeneous clipping and perspective divide.

    Args:
        fov_y_deg: Vertical field of view in degrees.
        aspect: Viewport width divided by height.
        near: Distance to the near clipping plane (positive).
        far: Distance to the far clipping plane (positive).

    Returns:
        4x4 perspective projection matrix as a numpy array.
    """
    fov_y_rad = np.radians(fov_y_deg)
    f = 1.0 / np.tan(fov_y_rad / 2.0)

    m = np.zeros((4, 4), dtype=np.float64)
    m[0, 0] = f / aspect
    m[1, 1] = f
    m[2, 2] = -(far + near) / (far - near)
    m[2, 3] = -(2.0 * far * near) / (far - near)
    m[3, 2] = -1.0
    return m
