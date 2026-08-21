import numpy as np
from texture import Texture


def test_checkerboard_shape():
    tex = Texture.generate_checkerboard(width=64, height=64, cell_size=8)
    assert tex.data.shape == (64, 64, 3)
    assert tex.width == 64
    assert tex.height == 64


def test_checkerboard_colors():
    color_a = (200, 200, 200)
    color_b = (50, 50, 50)
    tex = Texture.generate_checkerboard(
        width=16, height=16, cell_size=8, color_a=color_a, color_b=color_b
    )
    # (0,0) is cell (0,0) -> even -> color_a
    np.testing.assert_almost_equal(tex.data[0, 0], [c / 255.0 for c in color_a])
    # (8,0) is cell (1,0) -> odd -> color_b
    np.testing.assert_almost_equal(tex.data[0, 8], [c / 255.0 for c in color_b])


def test_sample_clamps_to_range():
    tex = Texture.generate_checkerboard(width=8, height=8)
    color = tex.sample(0.5, 0.5)
    assert color.shape == (3,)
    assert all(0.0 <= c <= 1.0 for c in color)


def test_sample_wraps_uv():
    tex = Texture.generate_checkerboard(width=8, height=8)
    # Sampling at u=0.1 and u=1.1 should give same result (wrap)
    c1 = tex.sample(0.1, 0.1)
    c2 = tex.sample(1.1, 1.1)
    np.testing.assert_array_equal(c1, c2)


def test_texture_from_array():
    data = np.full((4, 4, 3), 128, dtype=np.uint8)
    tex = Texture(data)
    assert tex.width == 4
    assert tex.height == 4
    np.testing.assert_almost_equal(tex.sample(0.5, 0.5), [128 / 255.0] * 3)
