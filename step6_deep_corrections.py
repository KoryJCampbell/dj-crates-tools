#!/usr/bin/env python3
"""Step 6: Execute deep audit corrections."""

import json
import os
import re
import shutil
from pathlib import Path
from collections import defaultdict

GENRES_ROOT = Path("/Users/koryjcampbell/Music/CRATES/GENRES")
TOOLS_DIR = GENRES_ROOT / ".dj-crates-tools"
AUDIO_EXTENSIONS = {".mp3", ".m4a", ".flac", ".wav", ".aif", ".aiff", ".ogg"}


def get_decade(year_str):
    try:
        y = int(year_str)
        return f"{(y // 10) * 10}s"
    except (ValueError, TypeError):
        return None


def get_year_from_path(filepath):
    for part in filepath.parts:
        if re.match(r"^\d{4}$", part):
            return part
    return None


def move_track(src, new_genre, new_subgenre):
    if not src.exists():
        return False
    year = get_year_from_path(src)
    decade = get_decade(year) if year else None
    if year and decade:
        dest_dir = GENRES_ROOT / new_genre / new_subgenre / decade / year
    else:
        dest_dir = GENRES_ROOT / new_genre / new_subgenre / "Unknown Year"
    dest = dest_dir / src.name
    if src == dest:
        return False
    if dest.exists():
        stem, suffix = dest.stem, dest.suffix
        i = 1
        while dest.exists():
            dest = dest_dir / f"{stem} ({i}){suffix}"
            i += 1
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))
    return True


# Default subgenre when None is specified
DEFAULT_SUBGENRES = {
    "Dancehall": "General Dancehall",
    "Reggaeton": "General Reggaeton",
    "Soca": "General Soca",
    "Dance": "General Dance",
    "Trance": "General Trance",
    "Disco": "General Disco",
    "Soul": "General Soul",
    "Christian": "General Christian",
}

CORRECTIONS = [
    # HIP-HOP:RAP -> R&B
    ("Hip-Hop:Rap", None, r"Aaliyah - Miss You", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Alicia Keys - Karma", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Alicia Keys - You Don't Know My Name", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Ashanti - Foolish", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Ashanti - Happy", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Ashanti - I Just Wanna Love You Baby", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Ashanti - Only U", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Ashanti - Rock Wit U \(Awww Baby\)", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Ashanti - Baby \(Clean\)", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Beyonce - Irreplaceable", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Beyonce - Naughty Girl", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Beyonce - Ring The Alarm", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Beyonce - In Da Club", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Black Buddafly - Bad Girl", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Chris Brown - Gimme That \(Main\)", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Chris Brown - Run It \(Clean\)", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Chris Brown - Wall To Wall", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Chris Brown - With You", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Dave Hollister - Keep Lovin", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Destiny's Child - Independent Women", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Destiny's Child - Nasty Girl", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"En Vogue - Riddle", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Fantasia - When I See U", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Ginuwine - Hell Yeah", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Ginuwine - There It Is", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Jaheim - Just In Case \(Main\)", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Jaheim - Put That Woman First", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Jaheim - The Chosen One", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Monica - All Eyes On Me", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Nivea - Dont Mess With The Radio", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Omarion - Ice Box \(Clean\)", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Sean Kingston - Beautiful Girls", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Sean Kingston - Face Drop", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Sean Kingston - Lights", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Sean Kingston - Me Love", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Boyz II Men - Pass You By", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Pretty Ricky - Push It Baby", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Pretty Ricky - Yes Sir", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Next - Mamacita", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Next - Wifey", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Bell Biv Devoe - Da Hot Shit", "R&B", "New Jack Swing"),
    ("Hip-Hop:Rap", None, r"Blu Cantrell - Breathe \(No Rap", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Blu Cantrell - Hit Em Up Style \(Oops\) \(Radio", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Jamie Foxx - Extravaganza", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Lloyd - Get It Shawty", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Rihanna - Rehab \(Clean\)", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Rihanna - Ride", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Amerie - One Thing", "R&B", "Contemporary R&B"),
    ("Hip-Hop:Rap", None, r"Tainted Love ft Dwele", "R&B", "General R&B"),
    ("Hip-Hop:Rap", None, r"Eamon - \(How Could You\) Bring Him Home", "R&B", "General R&B"),

    # HIP-HOP:RAP -> POP
    ("Hip-Hop:Rap", None, r"Lady Gaga - Just Dance \(Clean\)", "Pop", "Dance Pop"),
    ("Hip-Hop:Rap", None, r"Nelly Furtado - Maneater", "Pop", "General Pop"),
    ("Hip-Hop:Rap", None, r"Shontelle - T-Shirt", "Pop", "General Pop"),
    ("Hip-Hop:Rap", None, r"Weird Al Yankovic", "Pop", "General Pop"),
    ("Hip-Hop:Rap", None, r"Brian Harvey Ft Wyclef Jean - Ole Ole Ole", "Pop", "General Pop"),
    ("Hip-Hop:Rap", None, r"Brooke Hogan.*About Us.*Pop Edit", "Pop", "General Pop"),

    # HIP-HOP:RAP -> DANCEHALL/REGGAE
    ("Hip-Hop:Rap", None, r"Aidonia - Yeah Yeah", "Dancehall", "General Dancehall"),
    ("Hip-Hop:Rap", None, r"Aidonia ft Chris Martin - Summer Girl", "Dancehall", "General Dancehall"),
    ("Hip-Hop:Rap", None, r"Baby Cham - (Groundsman|Heading To The Top|She's Crazy)", "Dancehall", "General Dancehall"),
    ("Hip-Hop:Rap", None, r"Beenie Man", "Dancehall", "General Dancehall"),
    ("Hip-Hop:Rap", None, r"Busy Signal - (Hustle|Smoke Some)", "Dancehall", "General Dancehall"),
    ("Hip-Hop:Rap", None, r"Cecile - Changes", "Dancehall", "General Dancehall"),
    ("Hip-Hop:Rap", None, r"Elephant Man - Dancing Gym", "Dancehall", "General Dancehall"),
    ("Hip-Hop:Rap", None, r"Harry Toddler - Soul Survivor", "Dancehall", "General Dancehall"),
    ("Hip-Hop:Rap", None, r"Ky-Mani Marley - One Time", "Reggae", "General Reggae"),
    ("Hip-Hop:Rap", None, r"Leftside & Esco - Tuck In", "Dancehall", "General Dancehall"),
    ("Hip-Hop:Rap", None, r"Macka Diamond - Bun Him", "Dancehall", "General Dancehall"),
    ("Hip-Hop:Rap", None, r"Munga", "Dancehall", "General Dancehall"),
    ("Hip-Hop:Rap", None, r"Rupee - (Hurricane|Tempted To Touch)", "Soca", "General Soca"),
    ("Hip-Hop:Rap", None, r"Shaggy", "Reggae", "General Reggae"),

    # R&B -> Correct genres
    ("R&B", None, r"Bon Jovi - Thank You For Loving Me", "Rock", "Pop Rock"),
    ("R&B", None, r"Chris Tomlin - I Lift My Hands", "Christian", "General Christian"),
    ("R&B", None, r"Enya - May It Be", "Pop", "General Pop"),
    ("R&B", None, r"Gloria Gaynor - I Never Knew", "Disco", "General Disco"),
    ("R&B", None, r"Hilary Duff - Stranger", "Pop", "General Pop"),
    ("R&B", None, r"Josh Groban - You Raise Me Up", "Pop", "Pop Ballad"),
    ("R&B", None, r"Backstreet Boys", "Pop", "General Pop"),
    ("R&B", None, r"Westlife", "Pop", "General Pop"),
    ("R&B", None, r"Bette Midler - In My Life", "Pop", "Pop Ballad"),
    ("R&B", None, r"Do \(DJ Sammy\) - Heaven", "Dance", "General Dance"),
    ("R&B", None, r"Annie Lennox - Sing", "Pop", "General Pop"),
    ("R&B", None, r"Codigo Fn - El Gallero", "Latin", "General Latin"),
    ("R&B", None, r"Duelo - A Punto De Empezar", "Latin", "General Latin"),
    ("R&B", None, r"Intocable - Nadie Es Indispensable", "Latin", "General Latin"),
    ("R&B", None, r"Irasema - Chiquitito", "Latin", "General Latin"),
    ("R&B", None, r"Los Tigres Del Norte", "Latin", "General Latin"),
    ("R&B", None, r"Pepe Tovar Y Sus Chacales", "Latin", "General Latin"),
    ("R&B", None, r"Joe Budden - Pump It Up", "Hip-Hop:Rap", "East Coast"),
    ("R&B", None, r"Lil Flip - Sunshine", "Hip-Hop:Rap", "Southern"),

    # POP -> Dance/Trance/Hip-Hop
    ("Pop", None, r"Darude - (Feel The Beat|Sandstorm)", "Dance", "EDM"),
    ("Pop", None, r"Daft Punk - One More Time", "Dance", "Electronica"),
    ("Pop", None, r"Deadmau5.*I Remember", "Dance", "EDM"),
    ("Pop", None, r"Deep Dish - Say Hello", "Dance", "General Dance"),
    ("Pop", None, r"Dj Tiesto - Adagio For Strings", "Trance", "General Trance"),
    ("Pop", None, r"Tiesto - Traffic", "Trance", "General Trance"),
    ("Pop", None, r"Eiffel 65 - Move Your Body", "Dance", "EDM"),
    ("Pop", None, r"Ferry Corsten - Rock Your Body Rock", "Trance", "General Trance"),
    ("Pop", None, r"Global Deejays - What A Feeling", "Dance", "General Dance"),
    ("Pop", None, r"Ian Van Dahl - (Reason|Will I|Castles)", "Trance", "General Trance"),
    ("Pop", None, r"Lasgo - (Alone|Something)", "Trance", "General Trance"),
    ("Pop", None, r"Safri Duo - Played Alive", "Dance", "General Dance"),
    ("Pop", None, r"Tomcraft - Loneliness", "Dance", "General Dance"),
    ("Pop", None, r"Warp Brothers Vs Aquagen - Phatt Bass", "Dance", "General Dance"),
    ("Pop", None, r"50 Cent - Disco Inferno", "Hip-Hop:Rap", "East Coast"),
    ("Pop", None, r"50 Cent - Window Shopper", "Hip-Hop:Rap", "East Coast"),
    ("Pop", None, r"Eminem - (Just Lose It|Lose Yourself|The Real Slim Shady|Without Me)", "Hip-Hop:Rap", "East Coast"),
    ("Pop", None, r"Dr Dre feat Snoop Dogg - Still D\.R\.E", "Hip-Hop:Rap", "West Coast"),
    ("Pop", None, r"D12 - My Band", "Hip-Hop:Rap", "East Coast"),
    ("Pop", None, r"Cypress Hill - \(Rock\) Superstar", "Hip-Hop:Rap", "West Coast"),
    ("Pop", None, r"Method Man.*Redman.*How High", "Hip-Hop:Rap", "East Coast"),
    ("Pop", None, r"Redman.*Method Man.*How High", "Hip-Hop:Rap", "East Coast"),
    ("Pop", None, r"Terror Squad.*Lean Back", "Hip-Hop:Rap", "East Coast"),
    ("Pop", None, r"Busta Rhymes feat Sean Paul - Make It Clap", "Hip-Hop:Rap", "East Coast"),
    ("Pop", None, r"Cassidy feat R Kelly - Hotel", "Hip-Hop:Rap", "East Coast"),

    # ROCK -> R&B / Hip-Hop
    ("Rock", "Pop Rock", r"Brandy - (Baby|I Wanna Be Down|Best Friend|Brokenhearted)", "R&B", "Contemporary R&B"),
    ("Rock", "Pop Rock", r"Mary J\. Blige - (MJB Da MVP|Ain't Really Love|Enough Cryin|Take Me As I Am|Be Without You)", "R&B", "Contemporary R&B"),
    ("Rock", None, r"Mustard - (Whole Lotta|Parking Lot|Pure Water)", "Hip-Hop:Rap", "West Coast"),
    ("Rock", "Alternative", r"Belly - (Consuela|Might Not|Trap Phone|Man Listen|Immigration|Lullaby|Alcantara|Papyrus|What You Want|All For Me)", "Hip-Hop:Rap", "East Coast"),
    ("Rock", None, r"Ahmir - Welcome To My Party", "R&B", "Contemporary R&B"),
    ("Rock", None, r"Labrinth - (Earthquake|Let the Sun Shine)", "Pop", "General Pop"),
    ("Rock", None, r"Swift - Pull Up", "Hip-Hop:Rap", "General Hip-Hop"),

    # DANCE -> R&B / Hip-Hop / Other
    ("Dance", None, r"Whitney Houston - My Love Is Your Love\.mp3", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Whitney Houston - I Learned From The Best", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Whitney Houston - Run to You", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Whitney Houston - I Will Always Love You", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Whitney Houston - Heartbreak Hotel", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Whitney Houston - I'm Every Woman \(Album", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Whitney Houston - Million Dollar Bill", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Destiny's Child - Bootylicious", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Destiny's Child - Independent Women", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Destiny's Child - Emotion", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Destiny's Child - Brown Eyes", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Destiny's Child - Nuclear", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Destiny's Child - No, No, No", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Jennifer Hudson - No One Gonna Love You", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Jennifer Hudson - Spotlight", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Jennifer Hudson - And I Am Telling You", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Jennifer Hudson - If This Isn't Love", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Jennifer Hudson - Giving Myself", "R&B", "Contemporary R&B"),
    ("Dance", None, r"USHER - Can U Help Me", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Melanie Fiona - (It Kills Me|Give It To Me Right)", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Des'ree - You Gotta Be", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Jeremih - Birthday Sex.*Album Version", "R&B", "Contemporary R&B"),
    ("Dance", None, r"Tony Touch - I Wonder Why", "Hip-Hop:Rap", "General Hip-Hop"),
    ("Dance", None, r"Mark Ronson - Ooh Wee.*Ghostface", "Hip-Hop:Rap", "General Hip-Hop"),
    ("Dance", None, r"Rapsody - Sojourner", "Hip-Hop:Rap", "Conscious"),
    ("Dance", None, r"Gucci Mane - Party Started", "Hip-Hop:Rap", "Trap"),
    ("Dance", None, r"Drake - Jimmy Cooks", "Hip-Hop:Rap", "Southern"),
    ("Dance", None, r"Kodak Black - Too Many Years", "Hip-Hop:Rap", "Trap"),
    ("Dance", None, r"Jacki-O - Pussy \(Real Good\)", "Hip-Hop:Rap", "Southern"),
    ("Dance", None, r"Frankee - F\.U\.R\.B", "Pop", "General Pop"),
    ("Dance", None, r"James Brown - Say It Loud", "Soul", "Classic Soul"),
    ("Dance", None, r"James Brown - Blind Man Can See It", "Soul", "Classic Soul"),
    ("Dance", None, r"Khia - My Neck, My Back", "Hip-Hop:Rap", "Southern"),
    ("Dance", None, r"Myles Smith - (Stargazing|Wait For You)", "Pop", "General Pop"),
    ("Dance", None, r"Gracie Abrams - Close To You", "Pop", "Indie Pop"),
    ("Dance", None, r"Mike Posner - Bow Chicka", "Pop", "Pop Rap"),
    ("Dance", None, r"Mike Posner - Smoke & Drive", "Hip-Hop:Rap", "General Hip-Hop"),
    ("Dance", None, r"Mike Posner - Still Not Over You", "Pop", "General Pop"),
    ("Dance", None, r"Kid Cudi - Pursuit Of Happiness", "Hip-Hop:Rap", "Conscious"),
    ("Dance", None, r"Trent Reznor and Atticus Ross - Yeah x10", "Rock", "Alternative"),
    ("Dance", None, r"Florence \+ The Machine - Seven Devils", "Rock", "Alternative"),
    ("Dance", None, r"Christina Aguilera - (Genie in a Bottle|What a Girl Wants)", "Pop", "Dance Pop"),
    ("Dance", None, r"Christina Aguilera.*Lady Marmalade", "Pop", "Dance Pop"),
    ("Dance", None, r"Christina Aguilera.*Dirrty", "Pop", "Dance Pop"),

    # REGGAE -> REGGAETON
    ("Reggae", None, r"Daddy Yankee", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"J\. Balvin", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Don Omar", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Nicky Jam", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Feid - (CHORRITO|CLASSY|Brickell|SORRY|LUNA)", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Wisin.*Yandel", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Héctor.*Father", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Plan B - (Es Un Secreto|Guatauba|She Said)", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Tego Calde", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Ivy Queen", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Angel Y Khriz", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"La Factoria - Perdóname", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"FloyyMenor", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Ryan Castro", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Cris MJ - SI NO ES CONTIGO", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Zion.*(Lennox|Zun Da Da|Alocate)", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Big Boy - Mis Ojos", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Justin Quiles - TU ROPA", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"J Alvarez - La Pregunta", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Alex Gargolas", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Blessed - (Mírame|SI SABE)", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Tainy - COLMILLO", "Reggaeton", "General Reggaeton"),
    ("Reggae", None, r"Tito El Bambino - Booty", "Reggaeton", "General Reggaeton"),
    # Reggae -> Hip-Hop
    ("Reggae", None, r"N\.O\.R\.E\. - (Nothin|Oye Mi Canto)", "Hip-Hop:Rap", "East Coast"),
    # Reggae -> Soca
    ("Reggae", None, r"KES - Savannah Grass", "Soca", "General Soca"),
    ("Reggae", None, r"Skinny Fabulous - Famalay", "Soca", "General Soca"),
    ("Reggae", None, r"Voice - Alive and Well", "Soca", "General Soca"),
    ("Reggae", None, r"Bunji Garlin - Badang", "Soca", "General Soca"),

    # JAZZ -> Soul / R&B / other
    ("Jazz", None, r"The Shields - You Cheated", "Soul", "Classic Soul"),
    ("Jazz", None, r"The Dells - (A Heart Is A House|The Love We Had|Oh, What A Night)", "Soul", "Classic Soul"),
    ("Jazz", None, r"Brenton Wood - (Darlin|Baby You Got|Me And You|I Like The Way|Catch You)", "Soul", "Classic Soul"),
    ("Jazz", None, r"The Mellow Kings - Tonite", "Soul", "Classic Soul"),
    ("Jazz", None, r"The Dubs - Could This Be Magic", "Soul", "Classic Soul"),
    ("Jazz", None, r"Natalie Cole - (Someone That I Used|Day Dreaming)", "R&B", "General R&B"),
    ("Jazz", None, r"Stella\. - more parties in LA", "Hip-Hop:Rap", "General Hip-Hop"),
    ("Jazz", None, r"Will Downing - A Million Ways", "R&B", "Quiet Storm"),
    ("Jazz", None, r"Ann Nesby - I Apologize", "R&B", "General R&B"),
    ("Jazz", None, r"Paul Hardcastle - 19", "Dance", "General Dance"),

    # SOUL -> R&B
    ("Soul", None, r"Olivia - Bizounce", "R&B", "Contemporary R&B"),

    # DISCO -> Hip-Hop
    ("Disco", None, r"Kash Doll - Buss It", "Hip-Hop:Rap", "General Hip-Hop"),

    # SOCA -> Hip-Hop / Reggaeton
    ("Soca", None, r"KILLY - (No Sad|Doomsday|Deadtalks)", "Hip-Hop:Rap", "General Hip-Hop"),
    ("Soca", None, r"Yaga & Mackie - Aparentemente", "Reggaeton", "General Reggaeton"),

    # LO-FI -> Hip-Hop / R&B
    ("Lo-Fi", None, r"Tyler.*Creator - (SORRY NOT SORRY|KEEP DA|IFHY|ARE WE STILL)", "Hip-Hop:Rap", "West Coast"),
    ("Lo-Fi", None, r"Red Cafe - I'm Ill", "Hip-Hop:Rap", "East Coast"),
    ("Lo-Fi", None, r"C-Side - Boyfriend.Girlfriend", "R&B", "Contemporary R&B"),

    # HOUSE -> R&B / Hip-Hop
    ("House", None, r"ATL - (Calling All Girls|Make It Up With Love)", "R&B", "Contemporary R&B"),
    ("House", None, r"Jungle Brothers - Jimbrowski", "Hip-Hop:Rap", "Golden Age"),
    ("House", None, r"Various Artists.*Youngbloodz", "Hip-Hop:Rap", "Southern"),

    # MOTOWN -> R&B
    ("Motown", None, r"Profyle - (Liar|Damn)", "R&B", "Contemporary R&B"),

    # GARAGE -> Hip-Hop
    ("Garage", None, r"Boxie.*Let Me Show You.*Juelz", "Hip-Hop:Rap", "East Coast"),
    ("Garage", None, r"Genius.*One Year Later.*K Camp", "Hip-Hop:Rap", "General Hip-Hop"),

    # CHRISTIAN -> R&B
    ("Christian", None, r"Coko.*Triflin.*Eve", "R&B", "Contemporary R&B"),
    ("Christian", None, r"Ruben Studdard - (Sorry 2004|What If|Don't Make)", "R&B", "Contemporary R&B"),
]


def main():
    moved = 0
    not_found = 0
    errors = []

    for correction in CORRECTIONS:
        src_genre, src_sub, pattern, dest_genre, dest_sub = correction
        pat = re.compile(pattern, re.IGNORECASE)

        # Search in the source genre folder (or specific subgenre)
        if src_sub:
            search_root = GENRES_ROOT / src_genre / src_sub
        else:
            search_root = GENRES_ROOT / src_genre

        if not search_root.exists():
            continue

        found_any = False
        for root, _, files in os.walk(search_root):
            for f in files:
                if Path(f).suffix.lower() not in AUDIO_EXTENSIONS:
                    continue
                if pat.search(f):
                    src = Path(root) / f
                    try:
                        if move_track(src, dest_genre, dest_sub):
                            moved += 1
                            found_any = True
                    except Exception as e:
                        errors.append(f"{src}: {e}")

        if not found_any:
            not_found += 1

    print(f"Moved: {moved}")
    print(f"Patterns with no matches: {not_found}")
    print(f"Errors: {len(errors)}")
    for e in errors:
        print(f"  {e}")

    # Clean up empty directories
    print("\nCleaning up empty directories...")
    total_removed = 0
    for _ in range(10):
        removed = 0
        for dirpath, dirnames, filenames in os.walk(GENRES_ROOT, topdown=False):
            p = Path(dirpath)
            if p == GENRES_ROOT or str(p).startswith(str(TOOLS_DIR)):
                continue
            real_files = [f for f in filenames if f != ".DS_Store"]
            remaining = [d for d in dirnames if (p / d).exists()]
            if not real_files and not remaining:
                for f in filenames:
                    (p / f).unlink()
                try:
                    p.rmdir()
                    removed += 1
                except OSError:
                    pass
        total_removed += removed
        if removed == 0:
            break
    print(f"Removed {total_removed} empty directories")

    # Final count
    total = 0
    for _, _, files in os.walk(GENRES_ROOT):
        for f in files:
            if Path(f).suffix.lower() in AUDIO_EXTENSIONS:
                total += 1
    print(f"\nTotal audio files: {total}")


if __name__ == "__main__":
    main()
