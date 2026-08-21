"""Attribute interpolation."""

import numpy as np


class DefaultInterpolationStrategy:
    """Default interpolation strategy implementation."""

    def interpolate(
        self,
        attr0: np.ndarray,
        attr1: np.ndarray,
        attr2: np.ndarray,
        w0: float,
        w1: float,
        w2: float,
        barycentric: np.ndarray,
    ) -> np.ndarray:
        reciprocal_w0, reciprocal_w1, reciprocal_w2 = self._compute_reciprocals(w0, w1, w2)
        numerator = self._compute_weighted_numerator(
            attr0,
            attr1,
            attr2,
            reciprocal_w0,
            reciprocal_w1,
            reciprocal_w2,
            barycentric,
        )
        denominator = self._compute_normalization(
            reciprocal_w0,
            reciprocal_w1,
            reciprocal_w2,
            barycentric,
        )
        return numerator / denominator

    def _compute_reciprocals(self, w0: float, w1: float, w2: float):
        """Compute per-vertex weight factors."""
        return 1.0 / w0, 1.0 / w1, 1.0 / w2

    def _compute_weighted_numerator(
        self,
        attr0: np.ndarray,
        attr1: np.ndarray,
        attr2: np.ndarray,
        reciprocal_w0: float,
        reciprocal_w1: float,
        reciprocal_w2: float,
        barycentric: np.ndarray,
    ) -> np.ndarray:
        """Compute the weighted attribute numerator."""
        return (
            barycentric[0] * attr0 * reciprocal_w0
            + barycentric[1] * attr1 * reciprocal_w1
            + barycentric[2] * attr2 * reciprocal_w2
        )

    def _compute_normalization(
        self,
        reciprocal_w0: float,
        reciprocal_w1: float,
        reciprocal_w2: float,
        barycentric: np.ndarray,
    ) -> float:
        """Compute the normalization denominator."""
        return (
            barycentric[0] * reciprocal_w0
            + barycentric[1] * reciprocal_w1
            + barycentric[2] * reciprocal_w2
        )
