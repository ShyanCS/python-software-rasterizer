"""3D math utilities for the software renderer.

Provides vector and matrix operations for the graphics pipeline including
transformations (translation, rotation, scaling) and vector arithmetic.
All operations use float64 precision for deterministic results.
"""

import numpy as np


def vec3(x: float, y: float, z: float) -> np.ndarray:
    """Create a 3D vector."""
    return np.array([x, y, z], dtype=np.float64)


def vec4(x: float, y: float, z: float, w: float) -> np.ndarray:
    """Create a 4D homogeneous vector."""
    return np.array([x, y, z, w], dtype=np.float64)


def vec3_to_vec4(v: np.ndarray, w: float = 1.0) -> np.ndarray:
    """Extend a 3D vector to 4D homogeneous coordinates."""
    return np.array([v[0], v[1], v[2], w], dtype=np.float64)


def normalize(v: np.ndarray) -> np.ndarray:
    """Normalize a vector to unit length.

    Returns a zero vector if the input length is near zero.
    """
    length = np.linalg.norm(v)
    if length < 1e-10:
        return np.zeros_like(v)
    return v / length


def cross(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute the cross product of two 3D vectors."""
    return np.cross(a, b)


def dot(a: np.ndarray, b: np.ndarray) -> float:
    """Compute the dot product of two vectors."""
    return float(np.dot(a, b))


def mat4_identity() -> np.ndarray:
    """Create a 4x4 identity matrix."""
    return np.eye(4, dtype=np.float64)


def mat4_translation(tx: float, ty: float, tz: float) -> np.ndarray:
    """Create a 4x4 translation matrix."""
    m = np.eye(4, dtype=np.float64)
    m[0, 3] = tx
    m[1, 3] = ty
    m[2, 3] = tz
    return m


def mat4_scaling(sx: float, sy: float, sz: float) -> np.ndarray:
    """Create a 4x4 scaling matrix."""
    m = np.eye(4, dtype=np.float64)
    m[0, 0] = sx
    m[1, 1] = sy
    m[2, 2] = sz
    return m


def mat4_rotation_x(angle_rad: float) -> np.ndarray:
    """Create a 4x4 rotation matrix around the X axis."""
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    m = np.eye(4, dtype=np.float64)
    m[1, 1] = c
    m[1, 2] = -s
    m[2, 1] = s
    m[2, 2] = c
    return m


def mat4_rotation_y(angle_rad: float) -> np.ndarray:
    """Create a 4x4 rotation matrix around the Y axis."""
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    m = np.eye(4, dtype=np.float64)
    m[0, 0] = c
    m[0, 2] = s
    m[2, 0] = -s
    m[2, 2] = c
    return m


def mat4_rotation_z(angle_rad: float) -> np.ndarray:
    """Create a 4x4 rotation matrix around the Z axis."""
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    m = np.eye(4, dtype=np.float64)
    m[0, 0] = c
    m[0, 1] = -s
    m[1, 0] = s
    m[1, 1] = c
    return m


def mat4_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Multiply two 4x4 matrices: result = a @ b."""
    return a @ b


def mat4_transform_vec4(m: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Transform a 4D vector by a 4x4 matrix: result = m @ v."""
    return m @ v
