"""Explicit data structures for the graphics pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Optional, Protocol, Tuple, runtime_checkable

import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# Core data structures
# ---------------------------------------------------------------------------


@dataclass
class CameraParameters:
    """Camera configuration for a scene."""

    eye: np.ndarray
    target: np.ndarray
    up: np.ndarray
    fov: float
    near: float
    far: float
    width: int
    height: int


@dataclass
class Vertex:
    """Represents a vertex and its attributes as it flows through the pipeline."""

    position: np.ndarray  # Object or world space position (vec3 or vec4)
    texcoord: np.ndarray  # (u, v) texture coordinates
    color: np.ndarray  # (r, g, b) vertex color in [0, 1]

    # Set during vertex processing (clip space)
    clip_position: Optional[np.ndarray] = None

    # Set during perspective divide (NDC)
    ndc_position: Optional[np.ndarray] = None
    clip_w: Optional[float] = None

    # Set during viewport transform (screen space)
    screen_position: Optional[np.ndarray] = None


@dataclass
class Triangle:
    """Represents a triangle composed of three vertices."""

    v0: Vertex
    v1: Vertex
    v2: Vertex

    def as_list(self):
        return [self.v0, self.v1, self.v2]


@dataclass
class Fragment:
    """Represents a single pixel fragment during rasterization."""

    screen_x: int
    screen_y: int
    barycentric: np.ndarray
    depth_value: float
    texcoord: np.ndarray
    color: np.ndarray


class RenderTarget:
    """RGB color buffer paired with a float depth buffer."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.color = np.zeros((height, width, 3), dtype=np.float64)
        self.depth = np.full((height, width), np.inf, dtype=np.float64)

    def clear(self, color: tuple = (0.0, 0.0, 0.0)):
        self.color[:, :, 0] = color[0]
        self.color[:, :, 1] = color[1]
        self.color[:, :, 2] = color[2]
        self.depth[:, :] = np.inf

    def save_png(self, filepath: str):
        data = (np.clip(self.color, 0.0, 1.0) * 255).astype(np.uint8)
        img = Image.fromarray(data, "RGB")
        img.save(filepath)


# ---------------------------------------------------------------------------
# Pipeline stage protocols
# ---------------------------------------------------------------------------


@runtime_checkable
class CoverageStrategy(Protocol):
    """Determines which sample points are covered by a triangle.

    Given screen-space vertex positions, a signed triangle area, and a
    bounding box, yields ``(screen_x, screen_y, barycentric)`` tuples for
    every covered sample.
    """

    def covered_samples(
        self,
        p0: np.ndarray,
        p1: np.ndarray,
        p2: np.ndarray,
        area: float,
        bbox: Tuple[int, int, int, int],
    ) -> Iterator[Tuple[int, int, np.ndarray]]: ...


@runtime_checkable
class DepthStrategy(Protocol):
    """Reconstructs per-fragment depth from barycentric coordinates."""

    def reconstruct(
        self,
        z0: float,
        z1: float,
        z2: float,
        barycentric: np.ndarray,
    ) -> float: ...


@runtime_checkable
class InterpolationStrategy(Protocol):
    """Interpolates a vertex attribute across a triangle."""

    def interpolate(
        self,
        attr0: np.ndarray,
        attr1: np.ndarray,
        attr2: np.ndarray,
        w0: float,
        w1: float,
        w2: float,
        barycentric: np.ndarray,
    ) -> np.ndarray: ...
