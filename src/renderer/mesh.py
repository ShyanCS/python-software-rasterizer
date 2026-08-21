"""Wavefront OBJ mesh loader.

Supports loading triangulated meshes with vertex positions (v),
texture coordinates (vt), and triangular faces (f). Materials and
normals are not supported.
"""

import numpy as np
from typing import List, Tuple


class Mesh:
    """A triangle mesh with positions and optional texture coordinates.

    Attributes:
        positions: List of vertex positions as 3D numpy arrays.
        texcoords: List of texture coordinates as 2D numpy arrays.
        faces: List of face tuples (position_indices, texcoord_indices).
               Indices are 0-based.
    """

    def __init__(self):
        self.positions: List[np.ndarray] = []
        self.texcoords: List[np.ndarray] = []
        self.faces: List[Tuple[List[int], List[int]]] = []

    @staticmethod
    def load_obj(filepath: str) -> 'Mesh':
        """Load a mesh from a Wavefront OBJ file.

        Parses vertex positions (v), texture coordinates (vt), and
        triangular faces (f). Face vertex indices may include position
        and texture coordinate references separated by slashes
        (e.g., "f 1/1 2/2 3/3").

        OBJ indices are 1-based and converted to 0-based internally.

        Args:
            filepath: Path to the .obj file.

        Returns:
            A Mesh instance populated with the parsed data.
        """
        mesh = Mesh()

        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split()
                prefix = parts[0]

                if prefix == 'v' and len(parts) >= 4:
                    x = float(parts[1])
                    y = float(parts[2])
                    z = float(parts[3])
                    mesh.positions.append(
                        np.array([x, y, z], dtype=np.float64)
                    )

                elif prefix == 'vt' and len(parts) >= 3:
                    u = float(parts[1])
                    v = float(parts[2])
                    mesh.texcoords.append(
                        np.array([u, v], dtype=np.float64)
                    )

                elif prefix == 'f':
                    v_indices = []
                    vt_indices = []
                    for vert_str in parts[1:]:
                        components = vert_str.split('/')
                        v_idx = int(components[0]) - 1
                        v_indices.append(v_idx)
                        if len(components) > 1 and components[1]:
                            vt_idx = int(components[1]) - 1
                            vt_indices.append(vt_idx)

                    mesh.faces.append((v_indices, vt_indices))

        return mesh
