"""Verifies the repaired renderer's output against a freshly computed reference.

The reference images are re-rendered at test time by a known-correct copy of
the pipeline shipped in tests/reference_renderer/ (never present during the
agent's run), using the same scene/asset files the agent had. This avoids
baking static reference PNGs into the verifier: the ground truth is always
recomputed from the same inputs the agent worked with.
"""

import os
import sys
import json
import glob

import numpy as np
import pytest
from PIL import Image

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENCE_DIR = os.path.join(TESTS_DIR, "reference_renderer")
RENDERER_DIR = "/app/renderer"
SCENES_DIR = os.path.join(RENDERER_DIR, "scenes")
OUTPUT_DIR = "/app/output"

# Pixel-value tolerance in [0, 1] normalized space. The pipeline is fully
# deterministic float64 arithmetic, so a correct fix reproduces the reference
# exactly; this margin only absorbs incidental uint8 rounding, not algorithmic
# error. Any of the three injected defects (coverage, perspective, depth)
# produces per-channel deviations far larger than this.
ATOL = 1.0 / 255.0 + 1e-4

sys.path.insert(0, REFERENCE_DIR)
from renderer import render_scene as reference_render_scene  # noqa: E402
from scene import load_scene as reference_load_scene  # noqa: E402


def _scene_files():
    return sorted(glob.glob(os.path.join(SCENES_DIR, "*.json")))


def _render_reference(scene_path, out_dir):
    scene_def = reference_load_scene(scene_path)
    reference_render_scene(scene_def, RENDERER_DIR, out_dir)
    return scene_def.output, scene_def.camera.width, scene_def.camera.height


@pytest.fixture(scope="module")
def reference_outputs(tmp_path_factory):
    """Render every scene with the known-correct reference pipeline."""
    out_dir = str(tmp_path_factory.mktemp("reference_output"))
    results = {}
    for scene_path in _scene_files():
        output_name, width, height = _render_reference(scene_path, out_dir)
        results[output_name] = {
            "path": os.path.join(out_dir, output_name),
            "width": width,
            "height": height,
        }
    return results


def test_scene_files_present():
    """Sanity check: the expected scene definitions exist in the environment."""
    scene_files = _scene_files()
    assert len(scene_files) == 4, (
        f"Expected 4 scene files in {SCENES_DIR}, found {len(scene_files)}"
    )


@pytest.mark.parametrize(
    "output_name",
    ["colored_cube.png", "textured_plane.png", "overlapping_meshes.png", "adjacent_triangles.png"],
)
def test_output_file_exists(output_name):
    """Each scene must produce its named PNG at the documented output path."""
    path = os.path.join(OUTPUT_DIR, output_name)
    assert os.path.isfile(path), f"Missing expected output file: {path}"


@pytest.mark.parametrize(
    "output_name",
    ["colored_cube.png", "textured_plane.png", "overlapping_meshes.png", "adjacent_triangles.png"],
)
def test_output_image_is_valid(output_name):
    """Each output must be a decodable RGB image with no NaN/Inf-derived artifacts."""
    path = os.path.join(OUTPUT_DIR, output_name)
    img = Image.open(path)
    assert img.mode == "RGB", f"{output_name} has unexpected mode {img.mode}, expected RGB"
    arr = np.array(img.convert("RGB"))
    assert np.isfinite(arr).all(), f"{output_name} contains non-finite pixel values"


def test_output_is_deterministic():
    """Instruction requires identical output across repeated executions;
    re-run the renderer and confirm byte-identical results."""
    import subprocess
    import tempfile
    rerun_dir = tempfile.mkdtemp()
    env = os.environ.copy()
    env["OUTPUT_DIR"] = rerun_dir
    subprocess.run([sys.executable, "main.py"], cwd=RENDERER_DIR, env=env, check=True)

    for name in ["colored_cube.png", "textured_plane.png", "overlapping_meshes.png", "adjacent_triangles.png"]:
        first = np.array(Image.open(os.path.join(OUTPUT_DIR, name)))
        second = np.array(Image.open(os.path.join(rerun_dir, name)))
        assert np.array_equal(first, second), f"{name}: output differs between repeated runs"


@pytest.mark.parametrize(
    "output_name",
    ["colored_cube.png", "textured_plane.png", "overlapping_meshes.png", "adjacent_triangles.png"],
)
def test_output_dimensions_match_scene(output_name, reference_outputs):
    """Output dimensions must match the camera width/height declared in the scene."""
    expected = reference_outputs[output_name]
    agent_img = Image.open(os.path.join(OUTPUT_DIR, output_name))
    assert agent_img.size == (expected["width"], expected["height"]), (
        f"{output_name}: expected {expected['width']}x{expected['height']}, "
        f"got {agent_img.size[0]}x{agent_img.size[1]}"
    )


@pytest.mark.parametrize(
    "output_name",
    ["colored_cube.png", "textured_plane.png", "overlapping_meshes.png", "adjacent_triangles.png"],
)
def test_output_matches_reference_pixels(output_name, reference_outputs):
    """Rendered pixels must match the freshly computed reference within tolerance.

    Catches all three known failure modes: incorrect coverage (bounding-box /
    edge-rule errors show up as missing or extra edge pixels), incorrect
    perspective interpolation (UV/color drift), and incorrect depth
    reconstruction (shifted occlusion boundaries on overlapping geometry).
    """
    ref_arr = np.array(Image.open(reference_outputs[output_name]["path"]).convert("RGB")).astype(np.float64) / 255.0
    agent_arr = np.array(Image.open(os.path.join(OUTPUT_DIR, output_name)).convert("RGB")).astype(np.float64) / 255.0

    assert ref_arr.shape == agent_arr.shape, (
        f"{output_name}: shape mismatch, reference {ref_arr.shape} vs agent {agent_arr.shape}"
    )

    diff = np.abs(ref_arr - agent_arr)
    max_diff = float(diff.max())
    mismatched_fraction = float((diff.max(axis=2) > ATOL).mean())

    assert max_diff <= ATOL, (
        f"{output_name}: pixel values diverge from reference "
        f"(max per-channel diff {max_diff:.6f} > tolerance {ATOL:.6f}, "
        f"{mismatched_fraction * 100:.3f}% of pixels affected)"
    )