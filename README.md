# dj-crates-tools

Python tooling for organizing a large DJ music library by genre, subgenre, decade, and year — with automatic Serato DJ Pro crate sync and Billboard decade playlist generation.

## What It Does

1. **Scans** your music library and extracts ID3 metadata (artist, title, genre, BPM, key, year)
2. **Classifies** tracks into subgenres using artist mappings, ID3 tags, and decade-based defaults
3. **Reorganizes** files into a structured hierarchy: `Genre / Subgenre / Decade / Year / track.mp3`
4. **Audits & corrects** misplaced tracks across genres
5. **Generates Billboard decade playlists** (90s, 2000s, 2010s) using symlinks — no file duplication
6. **Syncs your folder structure into Serato DJ Pro** crates automatically

## Directory Structure

After running the tools, your library looks like:

```
CRATES/
├── GENRES/
│   ├── Hip-Hop:Rap/
│   │   ├── Boom Bap/
│   │   │   └── 1990s/
│   │   │       ├── 1993/
│   │   │       ├── 1994/
│   │   │       └── ...
│   │   ├── Drill/
│   │   ├── Trap/
│   │   └── ...
│   ├── R&B/
│   ├── House/
│   ├── Afrobeats/
│   └── ... (38 genres, 100+ subgenres)
└── PLAYLISTS/
    ├── 90s Hip-Hop & R&B Hits/
    ├── 2000s Hip-Hop & R&B Hits/
    └── 2010s Hip-Hop & R&B Hits/
```

## Scripts

### Core Pipeline

| Script | Purpose |
|--------|---------|
| `step1_inventory.py` | Scan library, extract ID3 metadata via `mutagen`, output `manifest.json` |
| `step2_classify.py` | Classify tracks into subgenres (500+ artist mappings across 11 genre maps) |
| `step4_reorganize.py` | Move files into `Genre/Subgenre/Decade/Year/` structure |
| `step5_corrections.py` | First-pass genre audit corrections (158 tracks) |
| `step6_deep_corrections.py` | Deep audit corrections from research (460 tracks) |

### Billboard Playlists

| Script | Purpose |
|--------|---------|
| `billboard_90s.py` | 90s Hip-Hop & R&B year-end hits → symlink playlist |
| `billboard_2000s.py` | 2000s Hip-Hop & R&B year-end hits → symlink playlist |
| `billboard_2010s.py` | 2010s Hip-Hop & R&B year-end hits → symlink playlist |

Playlists use **symlinks** pointing back to the original files in GENRES, so no disk space is wasted. Each script includes fuzzy matching (unicode normalization, punctuation stripping, substring artist/title matching) to find tracks in your library.

### Serato Sync

```bash
python3 serato_sync.py           # sync folder structure → Serato crates
python3 serato_sync.py --dry-run # preview without writing
python3 serato_sync.py --clean   # remove old synced crates first
```

Writes `.crate` files directly to Serato DJ Pro's `_Serato_/Subcrates/` directory using the native TLV binary format. Creates hierarchical subcrates using the `%%` delimiter convention. Restart Serato after syncing to see changes.

## Requirements

- Python 3.10+
- [`mutagen`](https://pypi.org/project/mutagen/) — for ID3 tag reading (`pip install mutagen`)

## Usage

Run the full pipeline:

```bash
# 1. Scan library
python3 step1_inventory.py

# 2. Classify into subgenres
python3 step2_classify.py

# 3. Reorganize files
python3 step4_reorganize.py

# 4. Generate playlists
python3 billboard_90s.py
python3 billboard_2000s.py
python3 billboard_2010s.py

# 5. Sync to Serato
python3 serato_sync.py --clean
```

Or just run `serato_sync.py` anytime you add/move music to update your Serato crates.

## License

MIT
