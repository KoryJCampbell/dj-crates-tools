#!/usr/bin/env python3
"""Step 1: Scan all tracks and extract metadata into a JSON manifest."""

import json
import os
import re
import sys
from pathlib import Path

import mutagen
from mutagen.id3 import ID3

GENRES_ROOT = Path("/Users/koryjcampbell/Music/CRATES/GENRES")
OUTPUT_FILE = GENRES_ROOT / ".dj-crates-tools" / "manifest.json"

AUDIO_EXTENSIONS = {".mp3", ".m4a", ".flac", ".wav", ".aif", ".aiff", ".ogg"}
SKIP_EXTENSIONS = {".asd", ".ds_store", ".jpg", ".png"}

YEAR_PATTERN = re.compile(r"^\d{4}$")


def get_decade(year_str: str) -> str | None:
    """Convert a year string to a decade label like '2010s'."""
    try:
        year = int(year_str)
        decade = (year // 10) * 10
        return f"{decade}s"
    except (ValueError, TypeError):
        return None


def extract_metadata(filepath: Path) -> dict:
    """Extract ID3 metadata from an audio file."""
    meta = {
        "artist": None,
        "album_artist": None,
        "title": None,
        "album": None,
        "genre_tag": None,
        "year_tag": None,
        "bpm": None,
        "key": None,
    }
    try:
        f = mutagen.File(str(filepath))
        if f is None:
            return meta
        tags = f.tags
        if tags is None:
            return meta

        # Handle ID3 tags (mp3)
        if hasattr(tags, "getall"):
            meta["artist"] = str(tags.get("TPE1", [""])).strip() or None
            meta["album_artist"] = str(tags.get("TPE2", [""])).strip() or None
            meta["title"] = str(tags.get("TIT2", [""])).strip() or None
            meta["album"] = str(tags.get("TALB", [""])).strip() or None
            meta["genre_tag"] = str(tags.get("TCON", [""])).strip() or None
            meta["year_tag"] = str(tags.get("TDRC", [""])).strip() or None
            meta["bpm"] = str(tags.get("TBPM", [""])).strip() or None
            meta["key"] = str(tags.get("TKEY", [""])).strip() or None
        # Handle MP4/M4A tags
        elif hasattr(tags, "items"):
            for k, v in tags.items():
                val = v[0] if isinstance(v, list) and v else v
                if k == "\xa9ART":
                    meta["artist"] = str(val)
                elif k == "aART":
                    meta["album_artist"] = str(val)
                elif k == "\xa9nam":
                    meta["title"] = str(val)
                elif k == "\xa9alb":
                    meta["album"] = str(val)
                elif k == "\xa9gen":
                    meta["genre_tag"] = str(val)
                elif k == "\xa9day":
                    meta["year_tag"] = str(val)
    except Exception as e:
        meta["_error"] = str(e)

    return meta


def scan_library() -> list[dict]:
    """Walk the GENRES directory and build inventory."""
    tracks = []
    skipped = 0

    for genre_dir in sorted(GENRES_ROOT.iterdir()):
        if not genre_dir.is_dir() or genre_dir.name.startswith("."):
            continue

        genre_name = genre_dir.name

        for root, dirs, files in os.walk(genre_dir):
            root_path = Path(root)
            # Determine the relative path components after the genre folder
            rel = root_path.relative_to(genre_dir)
            parts = list(rel.parts)

            # Figure out year from path
            year_from_path = None
            subgenre_from_path = None

            for part in parts:
                if YEAR_PATTERN.match(part):
                    year_from_path = part
                elif part != "Unknown Year":
                    subgenre_from_path = part

            for fname in sorted(files):
                ext = Path(fname).suffix.lower()
                if ext in SKIP_EXTENSIONS or ext not in AUDIO_EXTENSIONS:
                    skipped += 1
                    continue

                filepath = root_path / fname
                meta = extract_metadata(filepath)

                decade = get_decade(year_from_path) if year_from_path else None

                track = {
                    "file_path": str(filepath),
                    "filename": fname,
                    "current_genre": genre_name,
                    "year_from_path": year_from_path,
                    "decade": decade,
                    "subgenre_from_path": subgenre_from_path,
                    "artist": meta["artist"],
                    "album_artist": meta["album_artist"],
                    "title": meta["title"],
                    "album": meta["album"],
                    "genre_tag": meta["genre_tag"],
                    "year_tag": meta["year_tag"],
                    "bpm": meta["bpm"],
                    "key": meta["key"],
                }

                if "_error" in meta:
                    track["metadata_error"] = meta["_error"]

                tracks.append(track)

    print(f"Scanned {len(tracks)} tracks, skipped {skipped} non-audio files")
    return tracks


def main():
    print("Scanning library...")
    tracks = scan_library()

    # Summary stats
    genres = {}
    no_artist = 0
    no_title = 0
    has_subgenre_tag = 0
    has_subgenre_path = 0

    for t in tracks:
        g = t["current_genre"]
        genres[g] = genres.get(g, 0) + 1
        if not t["artist"]:
            no_artist += 1
        if not t["title"]:
            no_title += 1
        # Check if genre_tag contains a subgenre hint (slash, semicolon, etc.)
        gt = t.get("genre_tag") or ""
        if "/" in gt or ";" in gt or "," in gt:
            has_subgenre_tag += 1
        if t["subgenre_from_path"]:
            has_subgenre_path += 1

    print(f"\n--- Summary ---")
    print(f"Total tracks: {len(tracks)}")
    print(f"Tracks missing artist: {no_artist}")
    print(f"Tracks missing title: {no_title}")
    print(f"Tracks with subgenre in ID3 tag: {has_subgenre_tag}")
    print(f"Tracks already in subgenre folder: {has_subgenre_path}")
    print(f"\nGenre distribution:")
    for g, count in sorted(genres.items(), key=lambda x: -x[1]):
        print(f"  {g}: {count}")

    # Save manifest
    with open(OUTPUT_FILE, "w") as f:
        json.dump(tracks, f, indent=2, ensure_ascii=False)
    print(f"\nManifest saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
