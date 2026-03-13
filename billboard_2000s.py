#!/usr/bin/env python3
"""Build 2000s Hip-Hop & R&B Hits playlist from Billboard year-end charts knowledge."""

import os
import re
import unicodedata
from pathlib import Path

GENRES_ROOT = Path("/Users/koryjcampbell/Music/CRATES/GENRES")
PLAYLIST_DIR = Path("/Users/koryjcampbell/Music/CRATES/PLAYLISTS/2000s Hip-Hop & R&B Hits")
AUDIO_EXTENSIONS = {".mp3", ".m4a", ".flac", ".wav", ".aif", ".aiff", ".ogg"}

# Billboard Year-End Hot R&B/Hip-Hop Songs + Hot 100 crossover hits
# Top ~50-75 per year, comprehensive from memory of Billboard charts
BILLBOARD_HITS = {
    2000: [
        ("Maria Maria", "Santana", "Carlos Santana"),
        ("Say My Name", "Destiny's Child"),
        ("I Knew I Loved You", "Savage Garden"),
        ("Jumpin' Jumpin'", "Destiny's Child"),
        ("Hot Boyz", "Missy Elliott"),
        ("Try Again", "Aaliyah"),
        ("He Wasn't Man Enough", "Toni Braxton"),
        ("No More", "Ruff Endz"),
        ("Incomplete", "Sisqo", "Sisqó"),
        ("Thong Song", "Sisqo", "Sisqó"),
        ("I Wanna Know", "Joe"),
        ("Big Pimpin'", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Party Up (Up in Here)", "DMX"),
        ("Wobble Wobble", "504 Boyz"),
        ("The Next Episode", "Dr. Dre"),
        ("Country Grammar", "Nelly"),
        ("Shake Ya Ass", "Mystikal"),
        ("Danger (Been So Long)", "Mystikal"),
        ("Who Dat", "JT Money"),
        ("Separated", "Avant"),
        ("Got Your Money", "Ol' Dirty Bastard", "ODB"),
        ("Forgot About Dre", "Dr. Dre"),
        ("Bag Lady", "Erykah Badu"),
        ("Give Me You", "Mary J. Blige"),
        ("From the Bottom of My Broken Heart", "Britney Spears"),
        ("How Deep Is Your Love", "Dru Hill"),
        ("Feelin' So Good", "Jennifer Lopez"),
        ("Shorty (You Keep Playin' with My Mind)", "Imajin"),
        ("You Got It (Donut)", "Profyle"),
        ("Wifey", "Next"),
        ("Best of Me", "Mya"),
        ("Ride wit Me", "Nelly"),
        ("Case of the Ex", "Mya", "Mýa"),
        ("My First Night with You", "Mya"),
        ("Breathe and Stop", "Q-Tip"),
        ("Let's Get Married", "Jagged Edge"),
        ("Where I Wanna Be", "Donell Jones"),
        ("Satisfy You", "Puff Daddy", "Diddy", "P. Diddy"),
        ("Come On Over Baby", "Christina Aguilera"),
        ("I Try", "Macy Gray"),
        ("The Real Slim Shady", "Eminem"),
        ("Stan", "Eminem"),
        ("Still D.R.E.", "Dr. Dre"),
        ("U Know What's Up", "Donell Jones"),
        ("Alive", "Edwin McCain"),
        ("Gotta Tell You", "Samantha Mumba"),
        ("Back That Azz Up", "Juvenile"),
        ("All Good?", "De La Soul"),
        ("Promise", "Jagged Edge"),
        ("Beautiful Ones", "Prince"),
    ],
    2001: [
        ("Fallin'", "Alicia Keys"),
        ("Crazy in Love", "Beyoncé", "Beyonce"),
        ("U Remind Me", "Usher", "USHER"),
        ("Fiesta", "R. Kelly"),
        ("Izzo (H.O.V.A.)", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Differences", "Ginuwine"),
        ("Put It on Me", "Ja Rule"),
        ("I'm Real", "Jennifer Lopez"),
        ("It's Over Now", "112"),
        ("Stutter", "Joe"),
        ("One Minute Man", "Missy Elliott"),
        ("Ms. Jackson", "Outkast", "OutKast"),
        ("Peaches & Cream", "112"),
        ("Contagious", "The Isley Brothers", "Isley Brothers"),
        ("Family Affair", "Mary J. Blige"),
        ("What Would You Do?", "City High"),
        ("Free", "Mya"),
        ("Who We Be", "DMX"),
        ("Hit 'Em Up Style", "Blu Cantrell"),
        ("Let Me Blow Ya Mind", "Eve"),
        ("Area Codes", "Ludacris"),
        ("I'm a Thug", "Trick Daddy"),
        ("Ugly", "Bubba Sparxxx"),
        ("Ride wit Me", "Nelly"),
        ("Where the Party At", "Jagged Edge"),
        ("Bootylicious", "Destiny's Child"),
        ("Survivor", "Destiny's Child"),
        ("Always on Time", "Ja Rule"),
        ("Girl Talk", "TLC"),
        ("U Got It Bad", "Usher", "USHER"),
        ("I Wanna Talk About Me", "Toby Keith"),
        ("Livin' It Up", "Ja Rule"),
        ("How You Remind Me", "Nickelback"),
        ("What's Your Fantasy", "Ludacris"),
        ("Southern Hospitality", "Ludacris"),
        ("Superwoman Part II", "Lil' Mo"),
        ("Can't Deny It", "Fabolous"),
        ("My Baby", "Lil' Romeo"),
        ("I Just Wanna Love U", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Take You Out", "Luther Vandross"),
        ("You Makes Me Wanna", "Usher", "USHER"),
        ("Video", "India.Arie", "India Arie"),
        ("Raise Up", "Petey Pablo"),
        ("I'm a Slave 4 U", "Britney Spears"),
        ("Thank God I Found You", "Mariah Carey"),
        ("Heartbreaker", "Mariah Carey"),
        ("Where I Wanna Be", "Donell Jones"),
        ("Just in Case", "Jaheim"),
        ("No More (Baby I'ma Do Right)", "3LW"),
    ],
    2002: [
        ("Hot in Herre", "Nelly"),
        ("Dilemma", "Nelly"),
        ("Foolish", "Ashanti"),
        ("Ain't It Funny", "Jennifer Lopez"),
        ("U Don't Have to Call", "Usher", "USHER"),
        ("Gangsta Lovin'", "Eve"),
        ("Oh Boy", "Cam'ron", "Camron"),
        ("Cleanin' Out My Closet", "Eminem"),
        ("Lose Yourself", "Eminem"),
        ("Without Me", "Eminem"),
        ("Happy", "Ashanti"),
        ("Pass the Courvoisier", "Busta Rhymes"),
        ("What's Luv?", "Fat Joe"),
        ("Luv U Better", "LL Cool J"),
        ("Oops (Oh My)", "Tweet"),
        ("I Need a Girl (Part One)", "P. Diddy", "Diddy"),
        ("I Need a Girl (Part Two)", "P. Diddy", "Diddy"),
        ("Rainy Dayz", "Mary J. Blige"),
        ("Full Moon", "Brandy"),
        ("Down 4 U", "Irv Gotti"),
        ("Work It", "Missy Elliott"),
        ("Just a Friend 2002", "Mario"),
        ("A Woman's Worth", "Alicia Keys"),
        ("Girlfriend", "NSYNC", "*NSYNC", "N'Sync"),
        ("Half Crazy", "Musiq Soulchild", "Musiq"),
        ("Love", "Musiq Soulchild", "Musiq"),
        ("I Care 4 U", "Aaliyah"),
        ("Rock the Boat", "Aaliyah"),
        ("No One", "Alicia Keys"),
        ("Don't Let Me Get Me", "Pink", "P!nk"),
        ("I'm Gonna Be Alright", "Jennifer Lopez"),
        ("Nothin'", "N.O.R.E."),
        ("Roll Out (My Business)", "Ludacris"),
        ("Welcome to Atlanta", "Jermaine Dupri"),
        ("I Love You", "Faith Evans"),
        ("Satisfaction", "Eve"),
        ("Beautiful", "Snoop Dogg"),
        ("I Need a Girl", "Trey Songz"),
        ("Can't Stop Won't Stop", "Young Gunz"),
        ("Saturday (Oooh! Ooooh!)", "Ludacris"),
        ("Heaven", "DJ Sammy"),
        ("Move Bitch", "Ludacris"),
        ("In Da Club", "50 Cent"),
    ],
    2003: [
        ("In Da Club", "50 Cent"),
        ("Crazy in Love", "Beyoncé", "Beyonce"),
        ("Baby Boy", "Beyoncé", "Beyonce"),
        ("21 Questions", "50 Cent"),
        ("Right Thurr", "Chingy"),
        ("Rock Wit U (Awww Baby)", "Ashanti"),
        ("Into You", "Fabolous"),
        ("Frontin'", "Pharrell"),
        ("Excuse Me Miss", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Stand Up", "Ludacris"),
        ("P.I.M.P.", "50 Cent"),
        ("Get Low", "Lil Jon"),
        ("So Gone", "Monica"),
        ("Rain on Me", "Ashanti"),
        ("Mesmerize", "Ja Rule"),
        ("Ignition (Remix)", "R. Kelly"),
        ("Thoia Thoing", "R. Kelly"),
        ("Step in the Name of Love", "R. Kelly"),
        ("Magic Stick", "Lil' Kim"),
        ("Dip It Low", "Christina Milian"),
        ("Superstar", "Lupe Fiasco"),
        ("Overnight Celebrity", "Twista"),
        ("Holidae In", "Chingy"),
        ("Damn!", "YoungBloodZ"),
        ("Wanksta", "50 Cent"),
        ("Can't Let You Go", "Fabolous"),
        ("Put That Woman First", "Jaheim"),
        ("Miss You", "Aaliyah"),
        ("All I Have", "Jennifer Lopez"),
        ("Gossip Folks", "Missy Elliott"),
        ("When I See U", "Fantasia"),
        ("Like Glue", "Sean Paul"),
        ("Get Busy", "Sean Paul"),
        ("Gimme the Light", "Sean Paul"),
        ("Where Is the Love?", "Black Eyed Peas"),
        ("I Know What You Want", "Busta Rhymes"),
        ("I Can", "Nas"),
        ("Shake Ya Tailfeather", "Nelly"),
        ("Air Force Ones", "Nelly"),
        ("Beautiful", "Snoop Dogg"),
        ("Tipsy", "J-Kwon"),
        ("Hey Ya!", "Outkast", "OutKast"),
        ("The Way You Move", "Outkast", "OutKast"),
        ("Roses", "Outkast", "OutKast"),
        ("Never Leave You", "Lumidee"),
        ("Chicken Noodle Soup", "Webstar"),
        ("Slow Jamz", "Twista"),
        ("Through the Wire", "Kanye West"),
    ],
    2004: [
        ("Yeah!", "Usher", "USHER"),
        ("Burn", "Usher", "USHER"),
        ("Confessions Part II", "Usher", "USHER"),
        ("Goodies", "Ciara"),
        ("My Boo", "Usher", "USHER"),
        ("Lean Back", "Terror Squad"),
        ("Tipsy", "J-Kwon"),
        ("Dip It Low", "Christina Milian"),
        ("Slow Motion", "Juvenile"),
        ("Turn Me On", "Kevin Lyttle"),
        ("If I Ain't Got You", "Alicia Keys"),
        ("My Place", "Nelly"),
        ("Hotel", "Cassidy"),
        ("Overnight Celebrity", "Twista"),
        ("Sunshine", "Lil' Flip"),
        ("Diary", "Alicia Keys"),
        ("Through the Wire", "Kanye West"),
        ("Jesus Walks", "Kanye West"),
        ("All Falls Down", "Kanye West"),
        ("Splash Waterfalls", "Ludacris"),
        ("Freek-a-Leek", "Petey Pablo"),
        ("I Don't Wanna Know", "Mario Winans"),
        ("One Call Away", "Chingy"),
        ("Caught Up", "Usher", "USHER"),
        ("Let Me Love You", "Mario"),
        ("Naughty Girl", "Beyoncé", "Beyonce"),
        ("Me, Myself and I", "Beyoncé", "Beyonce"),
        ("Lose My Breath", "Destiny's Child"),
        ("Soldier", "Destiny's Child"),
        ("1 Thing", "Amerie"),
        ("How We Do", "The Game", "Game"),
        ("Drop It Like It's Hot", "Snoop Dogg"),
        ("Just Lose It", "Eminem"),
        ("Encore", "Eminem"),
        ("Get Right", "Jennifer Lopez"),
        ("I Like That", "Houston"),
        ("Lovers and Friends", "Lil Jon"),
        ("Salt Shaker", "Ying Yang Twins"),
        ("Toxic", "Britney Spears"),
        ("Locked Up", "Akon"),
        ("So Sick", "Ne-Yo"),
        ("What You Know", "T.I."),
        ("U Don't Know Me", "T.I."),
        ("Bringing Sexy Back", "Justin Timberlake"),
        ("Breathe", "Fabolous"),
        ("Girl Tonite", "Twista"),
        ("Wonderful", "Ja Rule"),
    ],
    2005: [
        ("We Belong Together", "Mariah Carey"),
        ("Let Me Hold You", "Bow Wow"),
        ("Gold Digger", "Kanye West"),
        ("Run It!", "Chris Brown"),
        ("Candy Shop", "50 Cent"),
        ("Lose Control", "Missy Elliott"),
        ("1, 2 Step", "Ciara"),
        ("Oh", "Ciara"),
        ("Caught Up", "Usher", "USHER"),
        ("Don't Cha", "Pussycat Dolls", "The Pussycat Dolls"),
        ("Sugar, We're Goin Down", "Fall Out Boy"),
        ("Disco Inferno", "50 Cent"),
        ("So Sick", "Ne-Yo"),
        ("Get Right", "Jennifer Lopez"),
        ("Soldier", "Destiny's Child"),
        ("Switch", "Will Smith"),
        ("Behind Those Hazel Eyes", "Kelly Clarkson"),
        ("Since U Been Gone", "Kelly Clarkson"),
        ("Hate It or Love It", "The Game", "Game"),
        ("How We Do", "The Game", "Game"),
        ("Just a Lil Bit", "50 Cent"),
        ("Shake It Off", "Mariah Carey"),
        ("Don't Forget About Us", "Mariah Carey"),
        ("Pon de Replay", "Rihanna"),
        ("Grillz", "Nelly"),
        ("My Humps", "Black Eyed Peas"),
        ("I'm Sprung", "T-Pain"),
        ("Hustler's Ambition", "50 Cent"),
        ("Be Without You", "Mary J. Blige"),
        ("Enough Cryin", "Mary J. Blige"),
        ("Soul Survivor", "Young Jeezy"),
        ("Go Crazy", "Young Jeezy"),
        ("Gimme That", "Chris Brown"),
        ("Yo (Excuse Me Miss)", "Chris Brown"),
        ("Like You", "Bow Wow"),
        ("Let Me Hold You", "Bow Wow"),
        ("Welcome to Atlanta (Remix)", "Ludacris"),
        ("Number One Spot", "Ludacris"),
        ("Reggaeton", "Don Omar"),
        ("President", "YoungBloodZ"),
        ("Lovers and Friends", "Lil Jon"),
        ("I'm N Luv (Wit a Stripper)", "T-Pain"),
        ("Wait (The Whisper Song)", "Ying Yang Twins"),
        ("Laffy Taffy", "D4L"),
        ("We Be Burnin'", "Sean Paul"),
        ("Back Then", "Mike Jones"),
        ("Still Tippin'", "Mike Jones"),
        ("Diamonds", "Rihanna"),
        ("My Hood", "Young Jeezy"),
        ("Poppin'", "Chris Brown"),
    ],
    2006: [
        ("Bad Day", "Daniel Powter"),
        ("Temperature", "Sean Paul"),
        ("Promiscuous", "Nelly Furtado"),
        ("Hips Don't Lie", "Shakira"),
        ("SOS", "Rihanna"),
        ("Unfaithful", "Rihanna"),
        ("Check on It", "Beyoncé", "Beyonce"),
        ("Deja Vu", "Beyoncé", "Beyonce"),
        ("Ring the Alarm", "Beyoncé", "Beyonce"),
        ("Grillz", "Nelly"),
        ("Ridin'", "Chamillionaire"),
        ("Hustlin'", "Rick Ross"),
        ("What You Know", "T.I."),
        ("Why You Wanna", "T.I."),
        ("Shoulder Lean", "Young Dro"),
        ("It's Goin' Down", "Yung Joc"),
        ("I Think They Like Me", "Dem Franchize Boyz"),
        ("Lean wit It, Rock wit It", "Dem Franchize Boyz"),
        ("So Sick", "Ne-Yo"),
        ("When You're Mad", "Ne-Yo"),
        ("Sexy Back", "Justin Timberlake"),
        ("My Love", "Justin Timberlake"),
        ("Money Maker", "Ludacris"),
        ("Runaway Love", "Ludacris"),
        ("You Don't Know Me", "T.I."),
        ("We Fly High", "Jim Jones"),
        ("Pop, Lock & Drop It", "Huey"),
        ("Touch It", "Busta Rhymes"),
        ("I Wanna Love You", "Akon"),
        ("Smack That", "Akon"),
        ("Me & U", "Cassie"),
        ("Pullin' Me Back", "Chingy"),
        ("U and Dat", "E-40"),
        ("Tell Me", "Bobby Valentino", "Bobby V"),
        ("It's Over", "112"),
        ("Be Without You", "Mary J. Blige"),
        ("One", "Mary J. Blige"),
        ("Ice Box", "Omarion"),
        ("Entourage", "Omarion"),
        ("Ain't No Other Man", "Christina Aguilera"),
        ("Unpredictable", "Jamie Foxx"),
        ("Get Up", "Ciara"),
        ("Promise", "Ciara"),
        ("Hate It or Love It", "The Game", "Game"),
        ("Candy Rain", "Soul for Real"),
        ("Chain Hang Low", "Jibbs"),
        ("Snap Yo Fingers", "Lil Jon"),
        ("Laffy Taffy", "D4L"),
        ("Stay Fly", "Three 6 Mafia"),
        ("Walk It Out", "Unk"),
    ],
    2007: [
        ("Irreplaceable", "Beyoncé", "Beyonce"),
        ("Beautiful Liar", "Beyoncé", "Beyonce"),
        ("Umbrella", "Rihanna"),
        ("Don't Matter", "Akon"),
        ("Buy U a Drank", "T-Pain"),
        ("Bartender", "T-Pain"),
        ("Big Things Poppin'", "T.I."),
        ("Crank That", "Soulja Boy"),
        ("The Way I Are", "Timbaland"),
        ("Give It to Me", "Timbaland"),
        ("Ice Box", "Omarion"),
        ("Wall to Wall", "Chris Brown"),
        ("Kiss Kiss", "Chris Brown"),
        ("With You", "Chris Brown"),
        ("Throw Some D's", "Rich Boy"),
        ("Party Like a Rockstar", "Shop Boyz"),
        ("Pop, Lock & Drop It", "Huey"),
        ("Make Me Better", "Fabolous"),
        ("Ay Bay Bay", "Hurricane Chris"),
        ("Can't Tell Me Nothing", "Kanye West"),
        ("Stronger", "Kanye West"),
        ("Good Life", "Kanye West"),
        ("I'm a Flirt", "R. Kelly"),
        ("Same Girl", "R. Kelly"),
        ("International Players Anthem", "UGK"),
        ("This Is Why I'm Hot", "Mims"),
        ("A Milli", "Lil Wayne"),
        ("Lollipop", "Lil Wayne"),
        ("We Takin' Over", "DJ Khaled"),
        ("I'm So Hood", "DJ Khaled"),
        ("Wipe Me Down", "Lil Boosie"),
        ("Because of You", "Ne-Yo"),
        ("Do You", "Ne-Yo"),
        ("Girlfriend", "Avril Lavigne"),
        ("No One", "Alicia Keys"),
        ("Like a Boy", "Ciara"),
        ("Last Night", "Diddy"),
        ("Get It Shawty", "Lloyd"),
        ("You", "Lloyd"),
        ("Lost Without U", "Robin Thicke"),
        ("Go Getta", "Young Jeezy"),
        ("Shawty", "Plies"),
        ("Got Money", "Lil Wayne"),
        ("I'm N Luv (Wit a Stripper)", "T-Pain"),
        ("Walk It Out", "Unk"),
        ("We Fly High", "Jim Jones"),
        ("Chain Hang Low", "Jibbs"),
        ("Bed", "J. Holiday"),
        ("Suffocate", "J. Holiday"),
        ("I Luv It", "Young Jeezy"),
    ],
    2008: [
        ("Lollipop", "Lil Wayne"),
        ("Low", "Flo Rida"),
        ("Bleeding Love", "Leona Lewis"),
        ("A Milli", "Lil Wayne"),
        ("Mrs. Officer", "Lil Wayne"),
        ("Got Money", "Lil Wayne"),
        ("Love in This Club", "Usher", "USHER"),
        ("Love in This Club Part II", "Usher", "USHER"),
        ("No Air", "Jordin Sparks"),
        ("Closer", "Ne-Yo"),
        ("Bust It Baby Part 2", "Plies"),
        ("Put On", "Young Jeezy"),
        ("Whatever You Like", "T.I."),
        ("Live Your Life", "T.I."),
        ("Shawty Get Loose", "Lil Mama"),
        ("Independent", "Webbie"),
        ("Sensual Seduction", "Snoop Dogg"),
        ("Superstar", "Lupe Fiasco"),
        ("Like a Boy", "Ciara"),
        ("Go Girl", "Ciara"),
        ("Sweetest Girl (Dollar Bill)", "Wyclef Jean"),
        ("Take You Down", "Chris Brown"),
        ("Forever", "Chris Brown"),
        ("With You", "Chris Brown"),
        ("Touch My Body", "Mariah Carey"),
        ("Can't Believe It", "T-Pain"),
        ("Flashing Lights", "Kanye West"),
        ("Love Lockdown", "Kanye West"),
        ("Heartless", "Kanye West"),
        ("Paper Planes", "M.I.A."),
        ("Right Round", "Flo Rida"),
        ("In the Ayer", "Flo Rida"),
        ("Leavin'", "Jesse McCartney"),
        ("Bust It Baby", "Plies"),
        ("Pop Champagne", "Jim Jones"),
        ("Spotlight", "Jennifer Hudson"),
        ("I'm So Paid", "Akon"),
        ("Sexy Can I", "Ray J"),
        ("Birthday Sex", "Jeremih"),
        ("Turnin Me On", "Keri Hilson"),
        ("Knock You Down", "Keri Hilson"),
        ("Superwoman", "Alicia Keys"),
        ("Like I'll Never See You Again", "Alicia Keys"),
        ("Swagga Like Us", "T.I."),
        ("Dangerous", "Kardinal Offishall"),
        ("Just Fine", "Mary J. Blige"),
        ("Good Girl Gone Bad", "Rihanna"),
        ("Disturbia", "Rihanna"),
        ("Don't Stop the Music", "Rihanna"),
        ("Rehab", "Rihanna"),
    ],
    2009: [
        ("Boom Boom Pow", "Black Eyed Peas"),
        ("Right Round", "Flo Rida"),
        ("Single Ladies", "Beyoncé", "Beyonce"),
        ("Halo", "Beyoncé", "Beyonce"),
        ("Best I Ever Had", "Drake"),
        ("Every Girl", "Young Money"),
        ("Blame It", "Jamie Foxx"),
        ("Knock You Down", "Keri Hilson"),
        ("Turnin Me On", "Keri Hilson"),
        ("Birthday Sex", "Jeremih"),
        ("Dead and Gone", "T.I."),
        ("Whatever You Like", "T.I."),
        ("Live Your Life", "T.I."),
        ("Day 'n' Nite", "Kid Cudi"),
        ("Heartless", "Kanye West"),
        ("Love Lockdown", "Kanye West"),
        ("Amazing", "Kanye West"),
        ("Kiss Me Thru the Phone", "Soulja Boy"),
        ("Successful", "Drake"),
        ("Thriller", "Michael Jackson"),
        ("Run This Town", "Jay-Z", "Jay Z", "JAY-Z"),
        ("D.O.A. (Death of Auto-Tune)", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Empire State of Mind", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Rockin' That Thang", "The-Dream"),
        ("Wetter", "Twista"),
        ("Pretty Wings", "Maxwell"),
        ("I Invented Sex", "Trey Songz"),
        ("Say Aah", "Trey Songz"),
        ("LOL Smiley Face", "Trey Songz"),
        ("I Can Transform Ya", "Chris Brown"),
        ("Crawl", "Chris Brown"),
        ("Beautiful", "Akon"),
        ("Teach Me How to Dougie", "Cali Swag District"),
        ("I'm Different", "2 Chainz"),
        ("Throw It in the Bag", "Fabolous"),
        ("Money Goes Honey Stay", "Fabolous"),
        ("Diva", "Beyoncé", "Beyonce"),
        ("Sweet Dreams", "Beyoncé", "Beyonce"),
        ("Ego", "Beyoncé", "Beyonce"),
        ("Solja Girl", "Destiny's Child"),
        ("Fire Burning", "Sean Kingston"),
        ("Break Up", "Mario"),
        ("Mad", "Ne-Yo"),
        ("Miss Independent", "Ne-Yo"),
        ("Closer", "Ne-Yo"),
        ("I'm in Miami Bitch", "LMFAO"),
        ("BedRock", "Young Money"),
        ("On to the Next One", "Jay-Z", "Jay Z", "JAY-Z"),
        ("I Need a Girl", "Trey Songz"),
        ("Neighbors Know My Name", "Trey Songz"),
    ],
}


def normalize(s):
    """Normalize a string for fuzzy matching."""
    if not s:
        return ""
    # Remove accents
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    # Remove common punctuation
    s = re.sub(r"['\"\-\.\,\!\?\(\)\[\]\{\}]", "", s)
    # Remove "feat" and everything after
    s = re.sub(r"\s*(feat|ft|featuring|f/).*$", "", s)
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s)
    return s


def title_match(filename, title):
    """Check if a filename contains the song title."""
    fn = normalize(filename)
    t = normalize(title)
    if not t:
        return False
    # Direct substring
    if t in fn:
        return True
    # Try without "the"
    t2 = re.sub(r"^the ", "", t)
    if t2 != t and t2 in fn:
        return True
    return False


def artist_match(filename, *artists):
    """Check if a filename contains any of the artist name variants."""
    fn = normalize(filename)
    for artist in artists:
        a = normalize(artist)
        if not a:
            continue
        if a in fn:
            return True
        # Try last name only for multi-word artists
        parts = a.split()
        if len(parts) > 1 and parts[-1] in fn and len(parts[-1]) > 3:
            return True
    return False


def find_track(year, title, artists, search_dirs):
    """Find a matching track in the library."""
    year_str = str(year)
    candidates = []

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for root, _, files in os.walk(search_dir):
            for f in files:
                if Path(f).suffix.lower() not in AUDIO_EXTENSIONS:
                    continue
                filepath = Path(root) / f
                fn = f

                # Must match both artist and title
                if title_match(fn, title) and artist_match(fn, *artists):
                    # Prefer same year
                    in_year = year_str in str(filepath)
                    candidates.append((filepath, in_year))

    if not candidates:
        return None

    # Prefer tracks from the correct year
    year_matches = [c for c in candidates if c[1]]
    if year_matches:
        return year_matches[0][0]
    return candidates[0][0]


def main():
    # Search directories
    search_dirs = [
        GENRES_ROOT / "Hip-Hop:Rap",
        GENRES_ROOT / "R&B",
        GENRES_ROOT / "Pop",
        GENRES_ROOT / "Dance",
        GENRES_ROOT / "Soul",
        GENRES_ROOT / "Dancehall",
        GENRES_ROOT / "Reggae",
    ]

    total_hits = 0
    total_found = 0
    total_missing = 0

    all_missing = []

    for year in range(2000, 2010):
        hits = BILLBOARD_HITS.get(year, [])
        year_dir = PLAYLIST_DIR / str(year)
        year_dir.mkdir(parents=True, exist_ok=True)

        found = 0
        missing = []

        for entry in hits:
            title = entry[0]
            artists = entry[1:]

            track = find_track(year, title, artists, search_dirs)

            if track:
                # Create symlink
                link_name = track.name
                link_path = year_dir / link_name
                if link_path.exists() or link_path.is_symlink():
                    continue  # Skip duplicates
                try:
                    os.symlink(track, link_path)
                    found += 1
                except Exception as e:
                    print(f"  Error linking {track.name}: {e}")
            else:
                missing.append(f"{artists[0]} - {title}")

        total_hits += len(hits)
        total_found += found
        total_missing += len(missing)
        all_missing.extend([(year, m) for m in missing])

        print(f"{year}: {found}/{len(hits)} hits found")

    print(f"\n{'='*50}")
    print(f"Total: {total_found}/{total_hits} Billboard hits matched ({total_found/total_hits*100:.1f}%)")
    print(f"Missing: {total_missing}")

    if all_missing:
        print(f"\nMissing tracks:")
        for year, m in all_missing:
            print(f"  [{year}] {m}")

    # Count symlinks created
    link_count = 0
    for year_dir in PLAYLIST_DIR.iterdir():
        if year_dir.is_dir():
            for f in year_dir.iterdir():
                if f.is_symlink():
                    link_count += 1
    print(f"\nTotal symlinks created: {link_count}")
    print(f"Playlist location: {PLAYLIST_DIR}")


if __name__ == "__main__":
    main()
