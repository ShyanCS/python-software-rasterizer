from mesh import Mesh


def test_mesh_load(tmp_path):
    obj_content = """
v 1.0 1.0 1.0
v -1.0 -1.0 -1.0
v 1.0 -1.0 1.0
vt 0.0 0.0
vt 1.0 1.0
vt 0.5 0.5
f 1/1 2/2 3/3
"""
    file_path = tmp_path / "test.obj"
    file_path.write_text(obj_content)

    mesh = Mesh.load_obj(str(file_path))
    assert len(mesh.positions) == 3
    assert len(mesh.texcoords) == 3
    assert len(mesh.faces) == 1

    v_indices, vt_indices = mesh.faces[0]
    assert v_indices == [0, 1, 2]
    assert vt_indices == [0, 1, 2]
