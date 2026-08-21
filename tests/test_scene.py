import json

import pytest
from scene import SceneDefinition, SceneLoadError, load_scene


def _write_scene(tmp_path, data):
    p = tmp_path / "scene.json"
    p.write_text(json.dumps(data))
    return str(p)


BASE_SCENE = {
    "camera": {
        "eye": [0, 0, 5],
        "target": [0, 0, 0],
        "up": [0, 1, 0],
        "fov": 60,
        "near": 0.1,
        "far": 100,
        "width": 64,
        "height": 64,
    },
    "meshes": [{"obj_file": "models/cube.obj"}],
    "output": "out.png",
}


def test_load_scene_missing_file():
    with pytest.raises(SceneLoadError, match="not found"):
        load_scene("/nonexistent/path/scene.json")


def test_load_scene_invalid_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("not: valid json {{{")
    with pytest.raises(SceneLoadError, match="Failed to parse"):
        load_scene(str(p))


def test_load_scene_missing_camera(tmp_path):
    data = {k: v for k, v in BASE_SCENE.items() if k != "camera"}
    with pytest.raises(SceneLoadError, match="camera"):
        load_scene(_write_scene(tmp_path, data))


def test_load_scene_missing_meshes(tmp_path):
    data = {k: v for k, v in BASE_SCENE.items() if k != "meshes"}
    with pytest.raises(SceneLoadError, match="meshes"):
        load_scene(_write_scene(tmp_path, data))


def test_load_scene_missing_output(tmp_path):
    data = {k: v for k, v in BASE_SCENE.items() if k != "output"}
    with pytest.raises(SceneLoadError, match="output"):
        load_scene(_write_scene(tmp_path, data))


def test_load_scene_missing_camera_key(tmp_path):
    data = {**BASE_SCENE, "camera": {"eye": [0, 0, 5]}}
    with pytest.raises(SceneLoadError, match="missing required key"):
        load_scene(_write_scene(tmp_path, data))


def test_load_scene_success(tmp_path):
    scene = load_scene(_write_scene(tmp_path, BASE_SCENE))
    assert isinstance(scene, SceneDefinition)
    assert scene.output == "out.png"
    assert len(scene.meshes) == 1
