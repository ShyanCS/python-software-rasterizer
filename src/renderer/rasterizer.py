"""Triangle rasterizer.

The rasterization function accepts pluggable strategies for coverage,
depth reconstruction, and attribute interpolation. This allows each
stage to be independently replaced without modifying this module.
"""

import numpy as np
from pipeline_types import (
    Triangle, Fragment,
    CoverageStrategy, DepthStrategy, InterpolationStrategy,
)
from typing import Iterator


def rasterization(
    triangle: Triangle,
    bbox: tuple,
    area: float,
    coverage: CoverageStrategy,
    depth_reconstruct: DepthStrategy,
    interpolation: InterpolationStrategy,
) -> Iterator[Fragment]:
    """Rasterize a triangle and yield generated fragments.

    The three strategy arguments control which algorithms are used for
    sample coverage testing, depth reconstruction, and attribute
    interpolation.  The caller is responsible for supplying concrete
    implementations; the rasterizer itself is agnostic to the
    algorithms.
    """
    p0 = triangle.v0.screen_position
    p1 = triangle.v1.screen_position
    p2 = triangle.v2.screen_position

    for screen_x, screen_y, barycentric in coverage.covered_samples(
        p0, p1, p2, area, bbox
    ):
        depth_value = depth_reconstruct.reconstruct(
            p0[2], p1[2], p2[2], barycentric
        )

        texcoord = interpolation.interpolate(
            triangle.v0.texcoord, triangle.v1.texcoord, triangle.v2.texcoord,
            triangle.v0.clip_w, triangle.v1.clip_w, triangle.v2.clip_w,
            barycentric,
        )

        vertex_color = interpolation.interpolate(
            triangle.v0.color, triangle.v1.color, triangle.v2.color,
            triangle.v0.clip_w, triangle.v1.clip_w, triangle.v2.clip_w,
            barycentric,
        )

        yield Fragment(
            screen_x=screen_x,
            screen_y=screen_y,
            barycentric=barycentric,
            depth_value=depth_value,
            texcoord=texcoord,
            color=vertex_color,
        )
