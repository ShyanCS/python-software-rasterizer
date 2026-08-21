"""Main rendering pipeline.

Orchestrates the full graphics pipeline.
"""

import os
import numpy as np

from math3d import mat4_multiply
from camera import look_at, perspective
from mesh import Mesh
from texture import Texture
from scene import SceneDefinition, SceneMeshEntry
from pipeline_types import RenderTarget
from transform import build_model_matrix, viewport_transform
from vertex import vertex_processing, perspective_divide
from clipping import clipping
from geometry import triangle_setup, EdgeFunctionCoverage
from rasterizer import rasterization
from shaders import fragment_shading
from depth import depth_test, framebuffer_write, DefaultDepthStrategy
from interpolation import DefaultInterpolationStrategy

# Default pipeline strategies — replace these to swap algorithms.
_default_coverage = EdgeFunctionCoverage()
_default_depth = DefaultDepthStrategy()
_default_interpolation = DefaultInterpolationStrategy()


def render_scene(
    scene: SceneDefinition,
    base_path: str,
    output_dir: str,
    coverage=None,
    depth_reconstruct=None,
    interpolation=None,
):
    """Render a complete scene to a PNG file.

    The optional *coverage*, *depth_reconstruct*, and *interpolation*
    parameters accept strategy objects that satisfy the corresponding
    protocols defined in ``pipeline_types``.  When ``None`` (the
    default), the built-in default strategies are used.
    """
    coverage = coverage or _default_coverage
    depth_reconstruct = depth_reconstruct or _default_depth
    interpolation = interpolation or _default_interpolation

    cam = scene.camera
    aspect = cam.width / cam.height

    view_matrix = look_at(cam.eye, cam.target, cam.up)
    proj_matrix = perspective(cam.fov, aspect, cam.near, cam.far)
    view_proj = mat4_multiply(proj_matrix, view_matrix)

    render_target = RenderTarget(cam.width, cam.height)
    render_target.clear(tuple(scene.background))

    for mesh_entry in scene.meshes:
        _render_mesh(
            mesh_entry, view_proj, render_target, base_path,
            coverage, depth_reconstruct, interpolation,
        )

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, scene.output)
    render_target.save_png(output_path)
    print(f"  Saved: {output_path}")


def _render_mesh(
    mesh_entry: SceneMeshEntry,
    view_proj: np.ndarray,
    render_target: RenderTarget,
    base_path: str,
    coverage,
    depth_reconstruct,
    interpolation,
):
    """Render a single mesh entry from the scene definition."""
    obj_path = os.path.join(base_path, mesh_entry.obj_file)
    mesh = Mesh.load_obj(obj_path)

    model_matrix = build_model_matrix(mesh_entry.transform)
    mvp = mat4_multiply(view_proj, model_matrix)

    texture = None
    if mesh_entry.texture_file:
        tex_path = os.path.join(base_path, mesh_entry.texture_file)
        texture = Texture.load(tex_path)
    elif mesh_entry.generate_texture == 'checkerboard':
        texture = Texture.generate_checkerboard()

    num_vertices = len(mesh.positions)
    if mesh_entry.vertex_colors:
        vertex_colors = [np.array(c, dtype=np.float64) for c in mesh_entry.vertex_colors]
    elif mesh_entry.default_color:
        default = np.array(mesh_entry.default_color, dtype=np.float64)
        vertex_colors = [default.copy() for _ in range(num_vertices)]
    else:
        vertex_colors = [np.array([1.0, 1.0, 1.0], dtype=np.float64) for _ in range(num_vertices)]

    for v_indices, vt_indices in mesh.faces:
        # 1. Vertex Processing
        triangle = vertex_processing(
            mesh.positions,
            mesh.texcoords,
            vertex_colors,
            v_indices,
            vt_indices,
            mvp
        )

        # 2. Clipping
        clipped_triangles = clipping(triangle)

        for tri in clipped_triangles:
            # 3. Perspective Divide
            perspective_divide(tri)

            # 4. Viewport Transform
            viewport_transform(tri, render_target.width, render_target.height)

            # 5. Triangle Setup
            bbox, area = triangle_setup(tri, render_target.width, render_target.height)

            if bbox is not None:
                # 6. Rasterization (coverage + depth + interpolation)
                for fragment in rasterization(
                    tri, bbox, area,
                    coverage, depth_reconstruct, interpolation,
                ):
                    # 7. Fragment Shading
                    color = fragment_shading(fragment, texture)

                    # 8. Depth Test
                    if depth_test(render_target, fragment):

                        # 9. Framebuffer Write
                        framebuffer_write(render_target, fragment, color)
