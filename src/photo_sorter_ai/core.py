from __future__ import annotations

import hashlib
import json
import os
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps, UnidentifiedImageError

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


class SorterError(RuntimeError):
    """Expected, user-facing sorter error."""


@dataclass(frozen=True)
class Photo:
    path: str
    sha256: str
    phash: str
    width: int
    height: int
    taken: str

    @property
    def orientation(self) -> str:
        if self.width == self.height:
            return "square"
        return "landscape" if self.width > self.height else "portrait"


@dataclass(frozen=True)
class PlanItem:
    source: str
    destination: str
    sha256: str
    action: str = "copy"


def sha256(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def perceptual_hash(image: Image.Image, size: int = 8) -> str:
    """Return a compact average perceptual hash; close images have small Hamming distance."""
    gray = ImageOps.grayscale(ImageOps.exif_transpose(image)).resize((size, size))
    pixels = list(gray.getdata())
    mean = sum(pixels) / len(pixels)
    bits = "".join("1" if value >= mean else "0" for value in pixels)
    return f"{int(bits, 2):0{size * size // 4}x}"


def hamming(a: str, b: str) -> int:
    return (int(a, 16) ^ int(b, 16)).bit_count()


def _taken(image: Image.Image, path: Path) -> str:
    try:
        raw = image.getexif().get(36867)  # DateTimeOriginal
        if raw:
            return datetime.strptime(str(raw), "%Y:%m:%d %H:%M:%S").isoformat()
    except (ValueError, TypeError, OverflowError):
        pass
    return datetime.fromtimestamp(path.stat().st_mtime).isoformat()


def analyze(path: Path) -> Photo:
    path = path.resolve()
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            width, height = ImageOps.exif_transpose(image).size
            return Photo(str(path), sha256(path), perceptual_hash(image), width, height, _taken(image, path))
    except (OSError, UnidentifiedImageError) as exc:
        raise SorterError(f"Cannot read image: {path}") from exc


def discover(root: Path, recursive: bool = True, include_hidden: bool = False) -> list[Path]:
    root = root.resolve()
    if not root.is_dir():
        raise SorterError(f"Not a directory: {root}")
    iterator: Iterable[Path] = root.rglob("*") if recursive else root.iterdir()
    result = []
    for p in iterator:
        try:
            rel = p.relative_to(root)
            hidden = any(part.startswith(".") for part in rel.parts)
            if p.is_file() and not p.is_symlink() and p.suffix.lower() in SUPPORTED and (include_hidden or not hidden):
                result.append(p)
        except OSError:
            continue
    return sorted(result, key=lambda p: str(p).casefold())


def cluster(photos: list[Photo], threshold: int = 8) -> list[list[Photo]]:
    """Greedy perceptual-similarity clusters. threshold is Hamming distance (0..64)."""
    if not 0 <= threshold <= 64:
        raise ValueError("threshold must be between 0 and 64")
    groups: list[list[Photo]] = []
    for photo in photos:
        for group in groups:
            if hamming(photo.phash, group[0].phash) <= threshold:
                group.append(photo)
                break
        else:
            groups.append([photo])
    return groups


def build_plan(photos: list[Photo], destination: Path, mode: str = "date") -> list[PlanItem]:
    destination = destination.resolve()
    if mode not in {"date", "orientation"}:
        raise SorterError("mode must be 'date' or 'orientation'")
    used: set[Path] = set()
    plan = []
    for photo in photos:
        src = Path(photo.path)
        folder = photo.taken[:7] if mode == "date" else photo.orientation
        target = destination / folder / src.name
        counter = 1
        while target in used or target.exists():
            target = destination / folder / f"{src.stem} ({counter}){src.suffix}"
            counter += 1
        used.add(target)
        plan.append(PlanItem(str(src), str(target), photo.sha256))
    return plan


def apply_plan(plan: list[PlanItem], manifest: Path, move: bool = False) -> None:
    """Execute a precomputed plan after re-checking every source digest."""
    manifest = manifest.resolve()
    if manifest.exists():
        raise SorterError(f"Manifest already exists: {manifest}")
    completed: list[dict[str, str]] = []
    for item in plan:
        src, dst = Path(item.source), Path(item.destination)
        if not src.is_file() or sha256(src) != item.sha256:
            raise SorterError(f"Source changed since preview: {src}")
        if dst.exists():
            raise SorterError(f"Destination exists: {dst}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        temp = dst.with_name(f".{dst.name}.photo-sorter.tmp")
        try:
            shutil.copy2(src, temp)
            if sha256(temp) != item.sha256:
                raise SorterError(f"Copy verification failed: {src}")
            os.replace(temp, dst)
            if move:
                src.unlink()
            completed.append({"source": str(src), "destination": str(dst), "sha256": item.sha256})
        finally:
            temp.unlink(missing_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": 1, "mode": "move" if move else "copy", "files": completed}
    manifest.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def plan_as_json(plan: list[PlanItem]) -> str:
    return json.dumps([asdict(item) for item in plan], indent=2, ensure_ascii=False)
