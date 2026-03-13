#!/usr/bin/env python3
"""Step 5: Fix misplaced tracks found during audit."""

import json
import os
import re
import shutil
from pathlib import Path
from collections import defaultdict

GENRES_ROOT = Path("/Users/koryjcampbell/Music/CRATES/GENRES")
TOOLS_DIR = GENRES_ROOT / ".dj-crates-tools"

AUDIO_EXTENSIONS = {".mp3", ".m4a", ".flac", ".wav", ".aif", ".aiff", ".ogg"}


def get_decade(year_str: str) -> str | None:
    try:
        year = int(year_str)
        decade = (year // 10) * 10
        return f"{decade}s"
    except (ValueError, TypeError):
        return None


def get_year_from_path(filepath: Path) -> str | None:
    """Extract year from the file's current path."""
    for part in filepath.parts:
        if re.match(r"^\d{4}$", part):
            return part
    return None


def move_track(src: Path, new_genre: str, new_subgenre: str, year: str = None):
    """Move a track to new genre/subgenre, preserving decade/year structure."""
    if not src.exists():
        return False, f"Not found: {src}"

    if year is None:
        year = get_year_from_path(src)

    decade = get_decade(year) if year else None

    if year and decade:
        dest_dir = GENRES_ROOT / new_genre / new_subgenre / decade / year
    else:
        dest_dir = GENRES_ROOT / new_genre / new_subgenre / "Unknown Year"

    dest = dest_dir / src.name

    if src == dest:
        return True, "Already in place"

    # Handle collision
    if dest.exists():
        stem = dest.stem
        suffix = dest.suffix
        i = 1
        while dest.exists():
            dest = dest_dir / f"{stem} ({i}){suffix}"
            i += 1

    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))
    return True, f"Moved to {dest}"


def find_tracks_by_artist_in(genre: str, subgenre: str, artist_pattern: str) -> list[Path]:
    """Find all tracks matching an artist pattern in a genre/subgenre."""
    results = []
    base = GENRES_ROOT / genre / subgenre
    if not base.exists():
        return results
    pattern = re.compile(artist_pattern, re.IGNORECASE)
    for root, _, files in os.walk(base):
        for f in files:
            if Path(f).suffix.lower() in AUDIO_EXTENSIONS:
                # Check filename for artist
                if pattern.search(f):
                    results.append(Path(root) / f)
    return results


def find_all_tracks_in(genre: str, subgenre: str) -> list[Path]:
    """Find all tracks in a genre/subgenre."""
    results = []
    base = GENRES_ROOT / genre / subgenre
    if not base.exists():
        return results
    for root, _, files in os.walk(base):
        for f in files:
            if Path(f).suffix.lower() in AUDIO_EXTENSIONS:
                results.append(Path(root) / f)
    return results


def main():
    moves = []
    errors = []

    def do_move(src, new_genre, new_subgenre, year=None, reason=""):
        ok, msg = move_track(src, new_genre, new_subgenre, year)
        if ok:
            moves.append({"from": str(src), "to_genre": new_genre, "to_sub": new_subgenre, "reason": reason})
        else:
            errors.append({"file": str(src), "error": msg, "reason": reason})

    # ================================================================
    # AMAPIANO - Everything misplaced
    # ================================================================
    print("Fixing Amapiano...")
    for t in find_tracks_by_artist_in("Amapiano", "General Amapiano", r"Sly.*Family Stone"):
        do_move(t, "Soul", "Psychedelic Soul", reason="Sly & The Family Stone → Soul")
    for t in find_tracks_by_artist_in("Amapiano", "General Amapiano", r"Tracy T"):
        do_move(t, "Hip-Hop:Rap", "Trap", reason="Tracy T → Hip-Hop:Rap/Trap")

    # ================================================================
    # BHANGRA - Ghetto Supastar is not Bhangra
    # ================================================================
    print("Fixing Bhangra...")
    for t in find_tracks_by_artist_in("Bhangra", "General Bhangra", r"Pras|Dirty Bastard|Mya"):
        do_move(t, "Hip-Hop:Rap", "East Coast", reason="Ghetto Supastar → Hip-Hop")

    # ================================================================
    # BOLLYWOOD
    # ================================================================
    print("Fixing Bollywood...")
    for t in find_all_tracks_in("Bollywood", "General Bollywood"):
        do_move(t, "Hip-Hop:Rap", "General Hip-Hop", reason="KK track → Hip-Hop")

    # ================================================================
    # CHRISTMAS - Most tracks aren't Christmas songs
    # ================================================================
    print("Fixing Christmas...")
    for t in find_tracks_by_artist_in("Christmas", "General Christmas", r"69 Boyz"):
        do_move(t, "Hip-Hop:Rap", "Southern", reason="69 Boyz → Hip-Hop/Southern")
    for t in find_tracks_by_artist_in("Christmas", "General Christmas", r"Brenda.*Tabulations"):
        do_move(t, "Soul", "Classic Soul", reason="Brenda & Tabulations → Soul")
    for t in find_tracks_by_artist_in("Christmas", "General Christmas", r"Dean Martin"):
        do_move(t, "Jazz", "General Jazz", reason="Dean Martin → Jazz")
    for t in find_tracks_by_artist_in("Christmas", "General Christmas", r"Kelly Clarkson"):
        do_move(t, "Pop", "Pop Rock", reason="Kelly Clarkson → Pop/Pop Rock")
    # Mariah non-Christmas tracks
    for t in find_tracks_by_artist_in("Christmas", "General Christmas", r"Mariah Carey"):
        fname = t.name.lower()
        if "christmas" not in fname and "holiday" not in fname and "santa" not in fname:
            do_move(t, "Pop", "Pop R&B", reason="Mariah Carey non-Christmas → Pop/Pop R&B")
    for t in find_tracks_by_artist_in("Christmas", "General Christmas", r"Moonglows"):
        do_move(t, "Soul", "Classic Soul", reason="Moonglows → Soul/Classic Soul")
    for t in find_tracks_by_artist_in("Christmas", "General Christmas", r"Ronettes"):
        do_move(t, "Pop", "Dance Pop", reason="Ronettes → Pop/Dance Pop")

    # ================================================================
    # CLASSICAL - Elvis doesn't belong
    # ================================================================
    print("Fixing Classical...")
    for t in find_tracks_by_artist_in("Classical", "General Classical", r"Elvis Presley"):
        do_move(t, "Rock", "Classic Rock", reason="Elvis → Rock/Classic Rock")

    # ================================================================
    # COUNTRY - Non-country tracks
    # ================================================================
    print("Fixing Country...")
    for t in find_tracks_by_artist_in("Country", "General Country", r"Bryan J|Travis Porter"):
        do_move(t, "Hip-Hop:Rap", "Southern", reason="Bryan J/Travis Porter → Hip-Hop")
    for t in find_tracks_by_artist_in("Country", "General Country", r"Mason.*Princess Superstar|Perfect.*Exceeder"):
        do_move(t, "Dance", "EDM", reason="Mason/Princess Superstar → Dance/EDM")

    # ================================================================
    # BASSLINE - Cha Cha Slide isn't Bassline
    # ================================================================
    print("Fixing Bassline...")
    for t in find_tracks_by_artist_in("Bassline", "General Bassline", r"Mr\. C|Cha Cha Slide"):
        do_move(t, "Dance", "General Dance", reason="Cha Cha Slide → Dance")

    # ================================================================
    # BREAKBEAT - Ike & Tina aren't Breakbeat
    # ================================================================
    print("Fixing Breakbeat...")
    for t in find_tracks_by_artist_in("Breakbeat", "General Breakbeat", r"Ike.*Tina"):
        do_move(t, "Soul", "Classic Soul", reason="Ike & Tina → Soul/Classic Soul")

    # ================================================================
    # DUBSTEP - These aren't dubstep
    # ================================================================
    print("Fixing Dubstep...")
    for t in find_tracks_by_artist_in("Dubstep", "General Dubstep", r"M'Black"):
        do_move(t, "Dance", "General Dance", reason="M'Black → Dance")
    for t in find_tracks_by_artist_in("Dubstep", "General Dubstep", r"Pix'L"):
        do_move(t, "Dance", "General Dance", reason="Pix'L → Dance")

    # ================================================================
    # DRUM & BASS - Belly/French Montana isn't DnB
    # ================================================================
    print("Fixing Drum & Bass...")
    for t in find_tracks_by_artist_in("Drum & Bass", "General Drum & Bass", r"Belly|French Montana"):
        do_move(t, "Hip-Hop:Rap", "East Coast", reason="Belly/French Montana → Hip-Hop")

    # ================================================================
    # BAILE FUNK - New Orleans Bounce isn't Baile Funk
    # ================================================================
    print("Fixing Baile Funk...")
    for t in find_tracks_by_artist_in("Baile Funk", "General Baile Funk", r"DJ Poppa|Blaza"):
        do_move(t, "Dance", "General Dance", reason="New Orleans Bounce → Dance")

    # ================================================================
    # AFROBEATS/General - Non-Afrobeats artists
    # ================================================================
    print("Fixing Afrobeats misplacements...")
    for t in find_tracks_by_artist_in("Afrobeats", "General Afrobeats", r"Tyler.*Creator"):
        do_move(t, "Hip-Hop:Rap", "West Coast", reason="Tyler the Creator → Hip-Hop/West Coast")
    for t in find_tracks_by_artist_in("Afrobeats", "General Afrobeats", r"Gucci Mane"):
        do_move(t, "Hip-Hop:Rap", "Trap", reason="Gucci Mane → Hip-Hop/Trap")
    for t in find_tracks_by_artist_in("Afrobeats", "General Afrobeats", r"^Doss\b"):
        do_move(t, "Dance", "Electronica", reason="Doss → Dance/Electronica")
    for t in find_tracks_by_artist_in("Afrobeats", "General Afrobeats", r"Byron Messia"):
        do_move(t, "Dancehall", "General Dancehall", reason="Byron Messia → Dancehall")

    # ================================================================
    # POP/Pop R&B - Davido and Busta Rhymes don't belong
    # ================================================================
    print("Fixing Pop/Pop R&B...")
    for t in find_tracks_by_artist_in("Pop", "Pop R&B", r"Davido"):
        do_move(t, "Afrobeats", "Afropop", reason="Davido → Afrobeats/Afropop")
    for t in find_tracks_by_artist_in("Pop", "Pop R&B", r"Busta Rhymes"):
        do_move(t, "Hip-Hop:Rap", "East Coast", reason="Busta Rhymes → Hip-Hop/East Coast")

    # ================================================================
    # HOUSE/General House - Non-house tracks
    # ================================================================
    print("Fixing House misplacements...")
    for t in find_tracks_by_artist_in("House", "General House", r"^ATL\b"):
        # Check if it's the R&B group ATL not an artist alias
        do_move(t, "R&B", "Contemporary R&B", reason="ATL → R&B")
    for t in find_tracks_by_artist_in("House", "General House", r"03 Greedo"):
        do_move(t, "Hip-Hop:Rap", "West Coast", reason="03 Greedo → Hip-Hop/West Coast")
    for t in find_tracks_by_artist_in("House", "General House", r"Mike Stud"):
        do_move(t, "Hip-Hop:Rap", "East Coast", reason="Mike Stud → Hip-Hop/East Coast")
    for t in find_tracks_by_artist_in("House", "General House", r"F\.L\.Y\.|Fast Life Yungstaz"):
        do_move(t, "Hip-Hop:Rap", "Southern", reason="F.L.Y. → Hip-Hop/Southern")
    for t in find_tracks_by_artist_in("House", "General House", r"Question Mark.*Mysterians"):
        do_move(t, "Rock", "Classic Rock", reason="Question Mark & Mysterians → Rock")
    for t in find_tracks_by_artist_in("House", "General House", r"Magic System"):
        do_move(t, "Afrobeats", "General Afrobeats", reason="Magic System → Afrobeats")
    for t in find_tracks_by_artist_in("House", "General House", r"Steve Aoki"):
        do_move(t, "Dance", "EDM", reason="Steve Aoki → Dance/EDM")

    # ================================================================
    # ROCK/General Rock - Many misplacements
    # ================================================================
    print("Fixing Rock/General Rock misplacements...")

    rock_fixes = {
        r"\bEve\b": ("Hip-Hop:Rap", "East Coast", "Eve → Hip-Hop/East Coast"),
        r"Tamia": ("R&B", "Contemporary R&B", "Tamia → R&B"),
        r"Dwele": ("R&B", "Neo-Soul", "Dwele → R&B/Neo-Soul"),
        r"Kylie Minogue": ("Pop", "Dance Pop", "Kylie Minogue → Pop/Dance Pop"),
        r"Spice Girls": ("Pop", "Dance Pop", "Spice Girls → Pop/Dance Pop"),
        r"Sam.*Dave": ("Soul", "Classic Soul", "Sam & Dave → Soul/Classic Soul"),
        r"Big Joe Turner": ("Jazz", "General Jazz", "Big Joe Turner → Jazz"),
        r"Michael McDonald": ("Soul", "General Soul", "Michael McDonald → Soul"),
        r"Donny Hathaway": ("Soul", "Classic Soul", "Donny Hathaway → Soul/Classic Soul"),
        r"Danity Kane": ("Pop", "Dance Pop", "Danity Kane → Pop/Dance Pop"),
        r"Jesse McCartney": ("Pop", "Dance Pop", "Jesse McCartney → Pop/Dance Pop"),
        r"Emma Bunton": ("Pop", "Dance Pop", "Emma Bunton → Pop/Dance Pop"),
        r"Earth.*Wind.*Fire": ("Soul", "Classic Soul", "Earth Wind & Fire → Soul/Classic Soul"),
        r"Ike.*Tina Turner": ("Soul", "Classic Soul", "Ike & Tina → Soul/Classic Soul"),
        r"Culture Club": ("Pop", "Synth Pop", "Culture Club → Pop/Synth Pop"),
        r"Kane.*Abel": ("Hip-Hop:Rap", "Southern", "Kane & Abel → Hip-Hop/Southern"),
        r"Violator": ("Hip-Hop:Rap", "East Coast", "Violator → Hip-Hop/East Coast"),
        r"Sean Paul": ("Dancehall", "General Dancehall", "Sean Paul → Dancehall"),
        r"Benzino": ("Hip-Hop:Rap", "East Coast", "Benzino → Hip-Hop/East Coast"),
        r"Choppa Style": ("Hip-Hop:Rap", "Southern", "Choppa Style → Hip-Hop/Southern"),
        r"Atomic Kitten": ("Pop", "Dance Pop", "Atomic Kitten → Pop/Dance Pop"),
        r"Jennifer.*Hewitt": ("Pop", "Dance Pop", "J Love Hewitt → Pop/Dance Pop"),
        r"Jennifer Paige": ("Pop", "Dance Pop", "Jennifer Paige → Pop/Dance Pop"),
        r"Ecstasy.*Passion": ("Disco", "General Disco", "Ecstasy Passion & Pain → Disco"),
        r"\bChange\b": ("Disco", "General Disco", "Change → Disco"),
        r"Graham Central": ("Soul", "Funk", "Graham Central Station → Soul/Funk"),
        r"The Impressions": ("Soul", "Classic Soul", "The Impressions → Soul/Classic Soul"),
        r"Wild Cherry": ("Soul", "Funk", "Wild Cherry → Soul/Funk"),
        r"Average White Band": ("Soul", "Funk", "Average White Band → Soul/Funk"),
        r"Ruth Brown": ("Jazz", "General Jazz", "Ruth Brown → Jazz"),
        r"Eddie Kendricks": ("Soul", "Classic Soul", "Eddie Kendricks → Soul"),
        r"Talking Heads": ("Rock", "Alternative", None),  # Keep in Rock but fix subgenre
        r"Carla Thomas": ("Soul", "Classic Soul", "Carla Thomas → Soul/Classic Soul"),
        r"Tina Turner": ("Pop", "Dance Pop", "Tina Turner → Pop"),
        r"Phil Collins": ("Pop", "Dance Pop", "Phil Collins → Pop/Dance Pop"),
        r"Robbie Williams": ("Pop", "Dance Pop", "Robbie Williams → Pop/Dance Pop"),
        r"BBMak": ("Pop", "Dance Pop", "BBMak → Pop"),
        r"Bobby Darin": ("Jazz", "General Jazz", "Bobby Darin → Jazz"),
        r"All Star Tribute": ("Pop", "Dance Pop", "All Star Tribute → Pop"),
        r"The Pack": ("Hip-Hop:Rap", "West Coast", "The Pack → Hip-Hop/West Coast"),
        r"Smitty": ("Hip-Hop:Rap", "Southern", "Smitty → Hip-Hop/Southern"),
        r"Gnarls Barkley": ("Soul", "Neo-Soul", "Gnarls Barkley → Soul/Neo-Soul"),
        r"Don Julian.*Larks": ("Soul", "Classic Soul", "Don Julian → Soul"),
        r"Neil Sedaka": ("Pop", "Dance Pop", "Neil Sedaka → Pop"),
        r"Bobby Day": ("Soul", "Classic Soul", "Bobby Day → Soul"),
        r"Bobby Moore": ("Soul", "Classic Soul", "Bobby Moore → Soul"),
        r"The Coasters": ("Soul", "Classic Soul", "Coasters → Soul"),
        r"Chuck Berry": ("Rock", "Classic Rock", None),
        r"Ricky Nelson": ("Rock", "Classic Rock", None),
        r"The Shirelles": ("Soul", "Classic Soul", "Shirelles → Soul"),
        r"The Penguins": ("Soul", "Classic Soul", "Penguins → Soul"),
        r"The Five Satins": ("Soul", "Classic Soul", "Five Satins → Soul"),
        r"The Chantels": ("Soul", "Classic Soul", "Chantels → Soul"),
        r"Barbara Lewis": ("Soul", "Classic Soul", "Barbara Lewis → Soul"),
        r"Bertha Tillman": ("Soul", "Classic Soul", "Bertha Tillman → Soul"),
        r"Varetta Dillard": ("Soul", "Classic Soul", "Varetta Dillard → Soul"),
        r"The Nutmegs": ("Soul", "Classic Soul", "Nutmegs → Soul"),
        r"The Swallows": ("Soul", "Classic Soul", "Swallows → Soul"),
        r"The Dells": ("Soul", "Classic Soul", "Dells → Soul"),
        r"Dion.*Belmonts": ("Rock", "Classic Rock", None),
        r"Everly Brothers": ("Rock", "Classic Rock", None),
        r"The Tymes": ("Soul", "Classic Soul", "Tymes → Soul"),
        r"The Sapphires": ("Soul", "Classic Soul", "Sapphires → Soul"),
        r"Tommy McLain": ("Soul", "General Soul", "Tommy McLain → Soul"),
        r"Rosco Gordon": ("Jazz", "General Jazz", "Rosco Gordon → Blues/Jazz"),
        r"Eugene McDaniels": ("Soul", "Classic Soul", "Eugene McDaniels → Soul"),
        r"The Foundations": ("Soul", "Classic Soul", "Foundations → Soul"),
        r"Was.*Not Was": ("Pop", "Dance Pop", "Was (Not Was) → Pop"),
        r"Nicolette Larson": ("Pop", "General Pop", "Nicolette Larson → Pop"),
        r"Brenda Russell": ("R&B", "Contemporary R&B", "Brenda Russell → R&B"),
        r"Katy Perry": ("Pop", "Dance Pop", "Katy Perry → Pop"),
        r"Taylor Swift": ("Pop", "Synth Pop", "Taylor Swift → Pop"),
        r"Olivia Rodrigo": ("Pop", "Pop Rock", "Olivia Rodrigo → Pop"),
        r"100 Gecs": ("Dance", "Electropop", "100 Gecs → Dance/Electropop"),
        r"Peaches\b": ("Dance", "Electronica", "Peaches → Dance"),
    }

    for pattern, (new_g, new_s, reason) in rock_fixes.items():
        if reason is None:
            continue  # Keep in Rock
        for t in find_tracks_by_artist_in("Rock", "General Rock", pattern):
            do_move(t, new_g, new_s, reason=reason)

    # ================================================================
    # SOUL/General Soul - Fix misplacements
    # ================================================================
    print("Fixing Soul/General Soul misplacements...")
    for t in find_tracks_by_artist_in("Soul", "General Soul", r"Gabriel.*Dresden"):
        do_move(t, "Dance", "Electronica", reason="Gabriel & Dresden → Dance")
    for t in find_tracks_by_artist_in("Soul", "General Soul", r"Rüfüs|RÜFÜS"):
        do_move(t, "Dance", "Electronica", reason="Rüfüs → Dance/Electronica")
    for t in find_tracks_by_artist_in("Soul", "General Soul", r"^Olivia\b"):
        do_move(t, "R&B", "Contemporary R&B", reason="Olivia → R&B")

    # ================================================================
    # DANCEHALL - Non-dancehall
    # ================================================================
    print("Fixing Dancehall misplacements...")
    for t in find_tracks_by_artist_in("Dancehall", "General Dancehall", r"Gucci Mane"):
        do_move(t, "Hip-Hop:Rap", "Trap", reason="Gucci Mane → Hip-Hop/Trap")

    # ================================================================
    # HIP-HOP GOLDEN AGE - Non-hip-hop artists
    # ================================================================
    print("Fixing Hip-Hop/Golden Age misplacements...")
    for t in find_tracks_by_artist_in("Hip-Hop:Rap", "Golden Age", r"Jennifer Lopez"):
        do_move(t, "Pop", "Dance Pop", reason="J.Lo → Pop/Dance Pop")
    for t in find_tracks_by_artist_in("Hip-Hop:Rap", "Golden Age", r"\bTLC\b"):
        do_move(t, "Pop", "Pop R&B", reason="TLC → Pop/Pop R&B")
    for t in find_tracks_by_artist_in("Hip-Hop:Rap", "Golden Age", r"Destiny.*Child"):
        do_move(t, "Pop", "Pop R&B", reason="Destiny's Child → Pop/Pop R&B")
    for t in find_tracks_by_artist_in("Hip-Hop:Rap", "Golden Age", r"Erykah Badu"):
        do_move(t, "R&B", "Neo-Soul", reason="Erykah Badu → R&B/Neo-Soul")
    for t in find_tracks_by_artist_in("Hip-Hop:Rap", "Golden Age", r"Nicole Wray"):
        do_move(t, "R&B", "Contemporary R&B", reason="Nicole Wray → R&B")
    for t in find_tracks_by_artist_in("Hip-Hop:Rap", "Golden Age", r"Hil St Soul"):
        do_move(t, "R&B", "Neo-Soul", reason="Hil St Soul → R&B/Neo-Soul")
    for t in find_tracks_by_artist_in("Hip-Hop:Rap", "Golden Age", r"Toni Estes"):
        do_move(t, "R&B", "Contemporary R&B", reason="Toni Estes → R&B")

    # ================================================================
    # HIP-HOP BLING ERA - R&B/Pop artists with hip-hop collabs stay,
    # but pure R&B/Pop tracks should move
    # ================================================================
    print("Fixing Hip-Hop/Bling Era misplacements...")
    for t in find_tracks_by_artist_in("Hip-Hop:Rap", "Bling Era", r"Jill Scott"):
        do_move(t, "R&B", "Neo-Soul", reason="Jill Scott → R&B/Neo-Soul")
    for t in find_tracks_by_artist_in("Hip-Hop:Rap", "Bling Era", r"Musiq Soulchild|Musiq\b"):
        do_move(t, "R&B", "Neo-Soul", reason="Musiq Soulchild → R&B/Neo-Soul")

    # ================================================================
    # Print summary
    # ================================================================
    print(f"\n{'='*60}")
    print(f"CORRECTIONS COMPLETE")
    print(f"{'='*60}")
    print(f"Total moves: {len(moves)}")
    print(f"Errors: {len(errors)}")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  {e['file']}: {e['error']}")

    # Group by reason
    by_reason = defaultdict(int)
    for m in moves:
        by_reason[m["reason"]] += 1
    print("\nMoves by reason:")
    for reason, count in sorted(by_reason.items(), key=lambda x: -x[1]):
        print(f"  {count:3d}  {reason}")

    # Save correction log
    log = {"moves": moves, "errors": errors}
    with open(TOOLS_DIR / "correction_log.json", "w") as f:
        json.dump(log, f, indent=2)

    # Clean up empty directories
    print("\nCleaning up empty directories...")
    empty_removed = 0
    for _ in range(10):
        removed = 0
        for dirpath, dirnames, filenames in os.walk(GENRES_ROOT, topdown=False):
            p = Path(dirpath)
            if p == GENRES_ROOT or str(p).startswith(str(TOOLS_DIR)):
                continue
            real_files = [f for f in filenames if f != ".DS_Store"]
            remaining_dirs = [d for d in dirnames if (p / d).exists()]
            if not real_files and not remaining_dirs:
                for f in filenames:
                    (p / f).unlink()
                try:
                    p.rmdir()
                    removed += 1
                except OSError:
                    pass
        empty_removed += removed
        if removed == 0:
            break
    print(f"Removed {empty_removed} empty directories")


if __name__ == "__main__":
    main()
