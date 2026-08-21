"""Fragment shaders for the software renderer."""

import numpy as np
from texture import Texture
from pipeline_types import Fragment

def fragment_shading(
    fragment: Fragment,
    texture: Texture = None
) -> np.ndarray:
    """Compute the final fragment color: texture × vertex color."""
    if texture is not None:
        texcoord = fragment.texcoord
        tex_color = texture.sample(texcoord[0], texcoord[1])
        return tex_color * fragment.color
    return fragment.color.copy()
