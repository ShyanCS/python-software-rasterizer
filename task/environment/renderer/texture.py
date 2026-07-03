"""Texture loading and sampling.

Supports loading textures from image files and procedural generation
of checkerboard patterns. Sampling uses nearest-neighbor filtering only.
"""

import numpy as np
from PIL import Image


class Texture:
    """A 2D texture with nearest-neighbor sampling.

    Internally stores pixel data as float64 values in the range [0, 1].

    Attributes:
        data: Texture pixel data as (height, width, 3) float64 array.
        width: Texture width in pixels.
        height: Texture height in pixels.
    """

    def __init__(self, data: np.ndarray):
        """Initialize a texture from raw pixel data.

        Args:
            data: RGB image data with shape (height, width, 3),
                  values in [0, 255] (uint8).
        """
        self.data = data.astype(np.float64) / 255.0
        self.height, self.width = data.shape[:2]

    @staticmethod
    def load(filepath: str) -> 'Texture':
        """Load a texture from an image file (PNG, JPEG, etc.).

        Args:
            filepath: Path to the image file.

        Returns:
            A Texture instance with the loaded image data.
        """
        img = Image.open(filepath).convert('RGB')
        data = np.array(img)
        return Texture(data)

    @staticmethod
    def generate_checkerboard(
        width: int = 64, height: int = 64,
        cell_size: int = 8,
        color_a: tuple = (200, 200, 200),
        color_b: tuple = (50, 50, 50)
    ) -> 'Texture':
        """Generate a deterministic checkerboard pattern texture.

        Creates an alternating grid of two colors. The pattern is fully
        deterministic given the same parameters.

        Args:
            width: Texture width in pixels.
            height: Texture height in pixels.
            cell_size: Size of each checker cell in pixels.
            color_a: RGB color for even cells (0-255).
            color_b: RGB color for odd cells (0-255).

        Returns:
            A Texture instance containing the checkerboard pattern.
        """
        data = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                cell_x = x // cell_size
                cell_y = y // cell_size
                if (cell_x + cell_y) % 2 == 0:
                    data[y, x] = color_a
                else:
                    data[y, x] = color_b
        return Texture(data)

    def sample(self, u: float, v: float) -> np.ndarray:
        """Sample the texture at the given UV coordinates.

        Uses nearest-neighbor filtering. UV coordinates are wrapped
        to [0, 1) using modular arithmetic. The V axis is flipped
        so that (0, 0) corresponds to the bottom-left of the image
        (standard texture convention).

        Args:
            u: Horizontal texture coordinate.
            v: Vertical texture coordinate.

        Returns:
            RGB color as a float64 array with values in [0, 1].
        """
        u_wrapped = u % 1.0
        v_wrapped = v % 1.0

        px = int(u_wrapped * self.width) % self.width
        py = int((1.0 - v_wrapped) * self.height) % self.height

        return self.data[py, px].copy()
