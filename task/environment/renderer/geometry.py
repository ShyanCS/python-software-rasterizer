"""Geometry setup and default coverage strategy for rasterization."""

import numpy as np
from typing import Tuple, Iterator
from pipeline_types import Triangle


def edge_function(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """Compute the edge function value for point c relative to edge a->b."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def triangle_setup(triangle: Triangle, width: int, height: int):
    """Compute the bounding box and signed area for a triangle.

    Returns:
        tuple: (min_x, max_x, min_y, max_y), area
        If area is near zero, returns None, 0.0
    """
    p0 = triangle.v0.screen_position
    p1 = triangle.v1.screen_position
    p2 = triangle.v2.screen_position

    # Signed area of the full triangle (twice the area)
    area = edge_function(p0[:2], p1[:2], p2[:2])

    # Skip degenerate (zero-area) triangles
    if abs(area) < 1e-10:
        return None, 0.0

    # Compute bounding box, clamped to framebuffer bounds
    min_x = max(0, int(np.floor(min(p0[0], p1[0], p2[0]))))
    max_x = min(width - 1, int(np.floor(max(p0[0], p1[0], p2[0]))))
    min_y = max(0, int(np.floor(min(p0[1], p1[1], p2[1]))))
    max_y = min(height - 1, int(np.floor(max(p0[1], p1[1], p2[1]))))


    return (min_x, max_x, min_y, max_y), area


class EdgeFunctionCoverage:
    """Default CoverageStrategy using edge-function inside testing."""

    def covered_samples(
        self,
        p0: np.ndarray,
        p1: np.ndarray,
        p2: np.ndarray,
        area: float,
        bbox: Tuple[int, int, int, int],
    ) -> Iterator[Tuple[int, int, np.ndarray]]:
        inv_area = 1.0 / area

        for screen_x, screen_y, sample_point in self._generate_sample_points(bbox):
            edge_weights = self._compute_edge_values(p0, p1, p2, sample_point)

            if not self._is_inside_triangle(edge_weights, area):
                continue

            barycentric = self._compute_barycentrics(edge_weights, inv_area)
            yield screen_x, screen_y, barycentric

    def _generate_sample_points(
        self, bbox: Tuple[int, int, int, int]
    ) -> Iterator[Tuple[int, int, np.ndarray]]:
        """Yield (pixel_x, pixel_y, sample_point) for every pixel in the bounding box."""
        min_x, max_x, min_y, max_y = bbox
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                sample_point = np.array([x + 0.5, y + 0.5])
                yield x, y, sample_point

    def _compute_edge_values(
        self,
        p0: np.ndarray,
        p1: np.ndarray,
        p2: np.ndarray,
        sample_point: np.ndarray,
    ) -> Tuple[float, float, float]:
        """Evaluate the three edge functions at the sample point."""
        w0 = edge_function(p1[:2], p2[:2], sample_point)
        w1 = edge_function(p2[:2], p0[:2], sample_point)
        w2 = edge_function(p0[:2], p1[:2], sample_point)
        return w0, w1, w2

    def _is_inside_triangle(
        self,
        edge_weights: Tuple[float, float, float],
        area: float,
    ) -> bool:
        """Return True if the edge weights indicate the sample is inside the triangle."""
        w0, w1, w2 = edge_weights
        if area > 0:
            return w0 >= 0 and w1 >= 0 and w2 >= 0
        else:
            return w0 <= 0 and w1 <= 0 and w2 <= 0

    def _compute_barycentrics(
        self,
        edge_weights: Tuple[float, float, float],
        inv_area: float,
    ) -> np.ndarray:
        """Normalize edge weights into barycentric coordinates."""
        return np.array(edge_weights) * inv_area
