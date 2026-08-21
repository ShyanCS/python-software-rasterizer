"""Depth reconstruction, testing, and framebuffer write."""

import numpy as np
from pipeline_types import Fragment, RenderTarget


class DefaultDepthStrategy:
    """Default depth reconstruction strategy."""

    def reconstruct(
        self,
        z0: float,
        z1: float,
        z2: float,
        barycentric: np.ndarray,
    ) -> float:
        self._validate_barycentrics(barycentric)
        return self._interpolate_depth(z0, z1, z2, barycentric)

    def _validate_barycentrics(self, barycentric: np.ndarray):
        """Verify that barycentric coordinates have the expected shape."""
        if barycentric.shape != (3,):
            raise ValueError(f"Expected barycentric shape (3,), got {barycentric.shape}")

    def _interpolate_depth(
        self,
        z0: float,
        z1: float,
        z2: float,
        barycentric: np.ndarray,
    ) -> float:
        """Compute the weighted depth value from vertex depths and barycentrics."""
        return float(barycentric[0] * z0 + barycentric[1] * z1 + barycentric[2] * z2)


def depth_test(render_target: RenderTarget, fragment: Fragment) -> bool:
    """Check if the fragment passes the depth test.

    Returns:
        bool: True if the fragment is closer than the current depth buffer value.
    """
    x, y = fragment.screen_x, fragment.screen_y
    if x < 0 or x >= render_target.width or y < 0 or y >= render_target.height:
        return False

    return fragment.depth_value < render_target.depth[y, x]


def framebuffer_write(render_target: RenderTarget, fragment: Fragment, color: np.ndarray):
    """Write the fragment color and depth to the render target with atmospheric fog."""
    x, y = fragment.screen_x, fragment.screen_y

    fog_factor = np.clip(fragment.depth_value, 0.0, 1.0)
    fog_color = np.array([0.8, 0.8, 0.9], dtype=np.float64)
    final_color = color * (1.0 - fog_factor) + fog_color * fog_factor

    render_target.depth[y, x] = fragment.depth_value
    render_target.color[y, x] = np.clip(final_color, 0.0, 1.0)
