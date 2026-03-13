#!/usr/bin/env python3
"""Step 4: Reorganize files into Genre/Subgenre/Decade/Year/ structure."""

import json
import os
import shutil
from pathlib import Path

GENRES_ROOT = Path("/Users/koryjcampbell/Music/CRATES/GENRES")
TOOLS_DIR = GENRES_ROOT / ".dj-crates-tools"
CLASSIFICATION = TOOLS_DIR / "classification.json"
MOVE_LOG = TOOLS_DIR / "move_log.json"

DECADES = ["1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]


def get_decade(year_str: str) -> str | None:
    try:
        year = int(year_str)
        decade = (year // 10) * 10
        return f"{decade}s"
    except (ValueError, TypeError):
        return None


def count_audio_files(root: Path) -> int:
    """Count audio files under a directory."""
    count = 0
    for _, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith((".mp3", ".m4a", ".flac", ".wav", ".aif", ".aiff", ".ogg", ".MP3")):
                count += 1
    return count


def main():
    print("Loading classification...")
    with open(CLASSIFICATION) as f:
        tracks = json.load(f)

    # Pre-move file count
    pre_count = count_audio_files(GENRES_ROOT)
    print(f"Pre-move audio file count: {pre_count}")
    print(f"Tracks in classification: {len(tracks)}")

    moved = 0
    skipped = 0
    errors = []
    already_in_place = 0
    move_log = []

    for track in tracks:
        src = Path(track["file_path"])

        if not src.exists():
            errors.append({"file": str(src), "error": "Source file not found"})
            continue

        genre = track["current_genre"]
        subgenre = track["proposed_subgenre"]
        year = track.get("year_from_path")
        decade = get_decade(year) if year else None

        # Build destination path
        # Genre / Subgenre / Decade / Year / filename
        # If no year: Genre / Subgenre / Unknown Year / filename
        if year and decade:
            dest_dir = GENRES_ROOT / genre / subgenre / decade / year
        else:
            dest_dir = GENRES_ROOT / genre / subgenre / "Unknown Year"

        dest = dest_dir / src.name

        # Skip if already in the right place
        if src == dest:
            already_in_place += 1
            continue

        # Handle filename collision
        if dest.exists():
            stem = dest.stem
            suffix = dest.suffix
            i = 1
            while dest.exists():
                dest = dest_dir / f"{stem} ({i}){suffix}"
                i += 1

        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dest))
            move_log.append({"from": str(src), "to": str(dest)})
            moved += 1
        except Exception as e:
            errors.append({"file": str(src), "error": str(e)})

    print(f"\n--- Move Results ---")
    print(f"Moved: {moved}")
    print(f"Already in place: {already_in_place}")
    print(f"Errors: {len(errors)}")

    if errors:
        print("\nErrors:")
        for e in errors[:20]:
            print(f"  {e['file']}: {e['error']}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")

    # Save move log
    with open(MOVE_LOG, "w") as f:
        json.dump({"moved": moved, "errors": errors, "log": move_log}, f, indent=2)
    print(f"\nMove log saved to: {MOVE_LOG}")

    # Clean up empty directories
    print("\nCleaning up empty directories...")
    empty_removed = 0
    for dirpath, dirnames, filenames in os.walk(GENRES_ROOT, topdown=False):
        p = Path(dirpath)
        if p == GENRES_ROOT or p == TOOLS_DIR or str(p).startswith(str(TOOLS_DIR)):
            continue
        # Remove .DS_Store files in otherwise empty dirs
        if set(filenames) <= {".DS_Store"} and not dirnames:
            for f in filenames:
                (p / f).unlink()
            try:
                p.rmdir()
                empty_removed += 1
            except OSError:
                pass
        elif not filenames and not dirnames:
            try:
                p.rmdir()
                empty_removed += 1
            except OSError:
                pass

    print(f"Removed {empty_removed} empty directories")

    # Post-move file count
    post_count = count_audio_files(GENRES_ROOT)
    print(f"\n--- Verification ---")
    print(f"Pre-move count:  {pre_count}")
    print(f"Post-move count: {post_count}")
    if pre_count == post_count:
        print("✓ File counts match — no files lost!")
    else:
        diff = pre_count - post_count
        print(f"⚠ MISMATCH: {diff} files differ. Check move log.")

    # Print final structure summary
    print(f"\n--- Final Structure ---")
    for genre_dir in sorted(GENRES_ROOT.iterdir()):
        if not genre_dir.is_dir() or genre_dir.name.startswith("."):
            continue
        genre_count = count_audio_files(genre_dir)
        print(f"\n{genre_dir.name} ({genre_count} tracks):")
        for sub_dir in sorted(genre_dir.iterdir()):
            if not sub_dir.is_dir():
                continue
            sub_count = count_audio_files(sub_dir)
            decades = []
            for d in sorted(sub_dir.iterdir()):
                if d.is_dir():
                    decades.append(d.name)
            decade_str = ", ".join(decades[:5])
            if len(decades) > 5:
                decade_str += f" +{len(decades)-5} more"
            print(f"  {sub_dir.name} ({sub_count}) [{decade_str}]")


if __name__ == "__main__":
    main()
