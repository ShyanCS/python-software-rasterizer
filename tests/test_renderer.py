from pathlib import Path

from renderer import render_scene
from scene import load_scene


def test_render_all_scenes(tmp_path):
    renderer_dir = Path(__file__).parent.parent / "src" / "renderer"
    scenes_dir = renderer_dir / "scenes"

    scene_files = list(scenes_dir.glob("*.json"))
    assert len(scene_files) > 0, "No scenes found"

    for scene_file in scene_files:
        scene_def = load_scene(str(scene_file))
        # render_scene should not raise any exceptions
        render_scene(scene_def, str(renderer_dir), str(tmp_path))

    png_files = list(tmp_path.glob("*.png"))
    assert len(png_files) == len(scene_files), "Expected one PNG per scene"
