from pathlib import Path

import pytest
from PIL import Image

from photo_sorter_ai.core import SorterError, analyze, apply_plan, build_plan, cluster, discover, hamming


def make(path: Path, color=(20, 40, 60), size=(40, 30)) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, color).save(path)
    return path


def test_analyze_and_orientation(tmp_path):
    photo = analyze(make(tmp_path / "a.jpg", size=(80, 40)))
    assert photo.width == 80 and photo.height == 40
    assert photo.orientation == "landscape"
    assert len(photo.sha256) == 64 and len(photo.phash) == 16


def test_discover_recursive_hidden_and_non_images(tmp_path):
    make(tmp_path / "a.jpg")
    make(tmp_path / "nested" / "b.png")
    make(tmp_path / ".hidden" / "c.jpg")
    (tmp_path / "notes.txt").write_text("not an image")
    assert len(discover(tmp_path)) == 2
    assert len(discover(tmp_path, recursive=False)) == 1
    assert len(discover(tmp_path, include_hidden=True)) == 3


def test_cluster_identical_visuals(tmp_path):
    a = analyze(make(tmp_path / "a.png", (100, 100, 100)))
    b = analyze(make(tmp_path / "b.png", (100, 100, 100)))
    groups = cluster([a, b], threshold=0)
    assert len(groups) == 1 and len(groups[0]) == 2
    assert hamming(a.phash, b.phash) == 0


def test_orientation_plan_avoids_existing_destination(tmp_path):
    src = make(tmp_path / "src" / "a.jpg", size=(60, 30))
    out = tmp_path / "out"
    make(out / "landscape" / "a.jpg")
    plan = build_plan([analyze(src)], out, "orientation")
    assert Path(plan[0].destination).name == "a (1).jpg"


def test_apply_copy_and_manifest(tmp_path):
    src = make(tmp_path / "src" / "a.jpg")
    out = tmp_path / "out"
    plan = build_plan([analyze(src)], out, "orientation")
    manifest = tmp_path / "manifest.json"
    apply_plan(plan, manifest)
    assert src.exists()
    assert Path(plan[0].destination).exists()
    assert manifest.exists()


def test_apply_rejects_changed_source(tmp_path):
    src = make(tmp_path / "src" / "a.jpg")
    plan = build_plan([analyze(src)], tmp_path / "out", "orientation")
    make(src, color=(200, 0, 0))
    with pytest.raises(SorterError, match="changed"):
        apply_plan(plan, tmp_path / "manifest.json")


def test_invalid_threshold(tmp_path):
    with pytest.raises(ValueError):
        cluster([], 65)
