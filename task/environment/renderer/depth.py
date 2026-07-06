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
        w0: float = 1.0,
        w1: float = 1.0,
        w2: float = 1.0,
    ) -> float:
        self._validate_barycentrics(barycentric)
        return self._interpolate_depth(z0, z1, z2, barycentric, w0, w1, w2)

    def _validate_barycentrics(self, barycentric: np.ndarray):
        """Verify that barycentric coordinates have the expected shape."""
        if barycentric.shape != (3,):
            raise ValueError(
                f"Expected barycentric shape (3,), got {barycentric.shape}"
            )

    def _interpolate_depth(
        self,
        z0: float, z1: float, z2: float,
        barycentric: np.ndarray,
        w0: float, w1: float, w2: float,
    ) -> float:
        """Compute the weighted depth value from vertex depths and barycentrics."""
        eps = 1e-12
        rw0, rw1, rw2 = 1.0 / max(w0, eps), 1.0 / max(w1, eps), 1.0 / max(w2, eps)
        numerator = (barycentric[0] * z0 * rw0 +
                     barycentric[1] * z1 * rw1 +
                     barycentric[2] * z2 * rw2)
        denominator = (barycentric[0] * rw0 +
                        barycentric[1] * rw1 +
                        barycentric[2] * rw2)
        return float(numerator / max(denominator, eps))

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
    """Write the fragment color and depth to the render target."""
    x, y = fragment.screen_x, fragment.screen_y
    render_target.depth[y, x] = fragment.depth_value
    render_target.color[y, x] = np.clip(color, 0.0, 1.0)
