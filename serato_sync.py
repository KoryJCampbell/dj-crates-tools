#!/usr/bin/env python3
"""
serato_sync.py - Sync CRATES folder structure into Serato DJ Pro crates.

Scans /Users/koryjcampbell/Music/CRATES/ (GENRES + PLAYLISTS) and creates
matching .crate files in Serato's Subcrates directory with proper hierarchy.

Directory structure:
  CRATES/GENRES/Genre/Subgenre/Decade/Year/track.mp3
  CRATES/PLAYLISTS/PlaylistName/Year/track.mp3

Produces Serato crates like:
  GENRES%%Hip-Hop:Rap.crate                          (all tracks in genre)
  GENRES%%Hip-Hop:Rap%%Drill.crate                   (all tracks in subgenre)
  GENRES%%Hip-Hop:Rap%%Drill%%2020s.crate            (all tracks in decade)
  GENRES%%Hip-Hop:Rap%%Drill%%2020s%%2024.crate      (all tracks in year)
  PLAYLISTS%%90s Hip-Hop & R&B Hits.crate            (playlist)
  PLAYLISTS%%90s Hip-Hop & R&B Hits%%1993.crate      (playlist year)

Usage:
  python3 serato_sync.py              # sync all
  python3 serato_sync.py --dry-run    # preview without writing
  python3 serato_sync.py --clean      # remove synced crates before writing
"""

import os
import struct
import sys
from collections import defaultdict
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────
CRATES_ROOT = Path("/Users/koryjcampbell/Music/CRATES")
SERATO_SUBCRATES = Path("/Users/koryjcampbell/Music/_Serato_/Subcrates")
SERATO_ROOT = Path("/Users/koryjcampbell/Music/_Serato_")

AUDIO_EXTENSIONS = {".mp3", ".flac", ".wav", ".ogg", ".aif", ".aiff", ".aac", ".m4a", ".alac"}

# Prefix for all crates we create (so we can identify/clean them)
SYNC_MARKER = "%%"  # crates with %% in name are ours (subcrates)

# Column definitions that Serato expects
DEFAULT_COLUMNS = [
    ("song", "250"),
    ("artist", "250"),
    ("bpm", "30"),
    ("key", "30"),
    ("album", "250"),
    ("length", "250"),
    ("comment", "250"),
]


# ── Serato Binary Format ───────────────────────────────────────────────────

def encode_utf16be(text: str) -> bytes:
    """Encode string as UTF-16 Big Endian (no BOM)."""
    return text.encode("utf-16-be")


def make_tlv(tag: str, data: bytes) -> bytes:
    """Create a TLV record: 4-byte tag + 4-byte BE length + data."""
    return tag.encode("ascii") + struct.pack(">I", len(data)) + data


def build_crate_bytes(track_paths: list[str]) -> bytes:
    """
    Build a complete .crate file as bytes.

    track_paths: list of paths relative to drive root (no leading /)
                 e.g. "Users/koryjcampbell/Music/CRATES/GENRES/..."
    """
    parts = []

    # Version header
    version_str = "1.0/Serato ScratchLive Crate"
    parts.append(make_tlv("vrsn", encode_utf16be(version_str)))

    # Column definitions
    for col_name, col_width in DEFAULT_COLUMNS:
        col_data = make_tlv("tvcn", encode_utf16be(col_name))
        col_data += make_tlv("tvcw", encode_utf16be(col_width))
        parts.append(make_tlv("ovct", col_data))

    # Track entries
    for path in sorted(track_paths):
        ptrk_data = make_tlv("ptrk", encode_utf16be(path))
        parts.append(make_tlv("otrk", ptrk_data))

    return b"".join(parts)


def write_crate(crate_name: str, track_paths: list[str], dry_run: bool = False) -> int:
    """
    Write a .crate file to Serato's Subcrates directory.
    Returns number of tracks written.
    """
    if not track_paths:
        return 0

    crate_file = SERATO_SUBCRATES / f"{crate_name}.crate"
    data = build_crate_bytes(track_paths)

    if dry_run:
        print(f"  [DRY RUN] {crate_name}.crate ({len(track_paths)} tracks)")
    else:
        crate_file.parent.mkdir(parents=True, exist_ok=True)
        with open(crate_file, "wb") as f:
            f.write(data)

    return len(track_paths)


# ── Directory Scanning ──────────────────────────────────────────────────────

def get_relative_path(filepath: Path) -> str:
    """
    Convert absolute path to Serato-style relative path (no leading /).
    Serato paths are relative to the drive root.
    """
    # /Users/koryjcampbell/Music/... -> Users/koryjcampbell/Music/...
    return str(filepath).lstrip("/")


def is_audio_file(filepath: Path) -> bool:
    """Check if file is a supported audio format."""
    return filepath.suffix.lower() in AUDIO_EXTENSIONS


def scan_directory_tree(root: Path) -> dict[str, list[str]]:
    """
    Scan a directory tree and build a mapping of crate hierarchy -> track paths.

    For a file at: GENRES/Hip-Hop:Rap/Drill/2020s/2024/track.mp3
    Creates entries in:
      GENRES%%Hip-Hop:Rap
      GENRES%%Hip-Hop:Rap%%Drill
      GENRES%%Hip-Hop:Rap%%Drill%%2020s
      GENRES%%Hip-Hop:Rap%%Drill%%2020s%%2024
    """
    crates = defaultdict(list)

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden directories
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]

        current = Path(dirpath)
        audio_files = [current / f for f in filenames if is_audio_file(current / f)]

        if not audio_files:
            continue

        # Build the hierarchy relative to CRATES_ROOT
        rel = current.relative_to(CRATES_ROOT)
        parts = list(rel.parts)  # e.g. ["GENRES", "Hip-Hop:Rap", "Drill", "2020s", "2024"]

        # Add tracks to every level of the hierarchy
        for i in range(1, len(parts) + 1):
            crate_name = "%%".join(parts[:i])
            for audio_file in audio_files:
                serato_path = get_relative_path(audio_file)
                crates[crate_name].append(serato_path)

    return crates


def update_neworder(crate_names: list[str], dry_run: bool = False):
    """
    Update Serato's neworder.pref to include our crates.
    Preserves existing manually-created crates.
    """
    neworder_file = SERATO_ROOT / "neworder.pref"

    # Read existing entries
    existing_crates = []
    if neworder_file.exists():
        with open(neworder_file, "rb") as f:
            content = f.read()
        # Parse the UTF-16-ish format
        text = content.decode("utf-16-be", errors="ignore")
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("[crate]"):
                name = line[len("[crate]"):].strip()
                if name:
                    existing_crates.append(name)

    # Build new order: existing non-synced crates first, then our synced crates sorted
    manual_crates = [c for c in existing_crates if "%%" not in c and c not in ("", " ")]
    synced_top_level = sorted(set(crate_names))

    # Combine: manual crates + our top-level crates
    all_crates = manual_crates + [c for c in synced_top_level if c not in manual_crates]

    if dry_run:
        print(f"\n  [DRY RUN] Would update neworder.pref with {len(all_crates)} crates")
        return

    # Write in Serato's format (UTF-16 BE with their record markers)
    lines = [" [ b e g i n   r e c o r d ] "]
    for crate in all_crates:
        # Space-separate each character for Serato's format
        spaced = " ".join(crate)
        lines.append(f" [ c r a t e ] {spaced} ")
    lines.append(" [ e n d   r e c o r d ] ")

    with open(neworder_file, "w") as f:
        f.write("\n".join(lines) + "\n")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    dry_run = "--dry-run" in sys.argv
    clean = "--clean" in sys.argv

    print("=" * 60)
    print("  Serato Crate Sync")
    print("=" * 60)
    print(f"  Source:  {CRATES_ROOT}")
    print(f"  Target:  {SERATO_SUBCRATES}")
    if dry_run:
        print("  Mode:    DRY RUN (no files will be written)")
    print()

    # Step 1: Clean existing synced crates if requested
    if clean and not dry_run:
        removed = 0
        for f in SERATO_SUBCRATES.glob("*.crate"):
            if "%%" in f.stem:
                f.unlink()
                removed += 1
        print(f"Cleaned {removed} existing synced crates\n")

    # Step 2: Scan GENRES and PLAYLISTS
    all_crates = {}

    genres_dir = CRATES_ROOT / "GENRES"
    playlists_dir = CRATES_ROOT / "PLAYLISTS"

    if genres_dir.exists():
        print("Scanning GENRES...")
        genre_crates = scan_directory_tree(genres_dir)
        all_crates.update(genre_crates)
        print(f"  Found {len(genre_crates)} crate levels\n")

    if playlists_dir.exists():
        print("Scanning PLAYLISTS...")
        playlist_crates = scan_directory_tree(playlists_dir)
        all_crates.update(playlist_crates)
        print(f"  Found {len(playlist_crates)} crate levels\n")

    # Step 3: Write crate files
    print("Writing crates...")
    total_crates = 0
    total_tracks = 0

    # Sort by hierarchy depth so parents are created before children
    for crate_name in sorted(all_crates.keys(), key=lambda x: x.count("%%")):
        tracks = all_crates[crate_name]
        count = write_crate(crate_name, tracks, dry_run=dry_run)
        if count > 0:
            total_crates += 1
            total_tracks += count

    # Step 4: Summary
    print(f"\n{'=' * 60}")
    print(f"  Crates written:  {total_crates}")
    print(f"  Total track entries: {total_tracks}")
    print(f"{'=' * 60}")

    # Show top-level crate breakdown
    print("\nTop-level crates:")
    top_level = {}
    for name, tracks in all_crates.items():
        top = name.split("%%")[0]
        if top not in top_level:
            top_level[top] = 0
        if name.count("%%") == 0:
            top_level[top] = len(tracks)

    for name in sorted(top_level.keys()):
        depth_count = sum(1 for k in all_crates if k.startswith(name + "%%"))
        print(f"  {name}: {top_level[name]} tracks, {depth_count} subcrates")

    # Remind user to rescan
    if not dry_run:
        print("\n  ** Restart Serato DJ Pro or rescan library to see changes **")


if __name__ == "__main__":
    main()
