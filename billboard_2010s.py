#!/usr/bin/env python3
"""Build 2010s Hip-Hop & R&B Hits playlist from Billboard year-end charts."""

import os
import re
import unicodedata
from pathlib import Path

GENRES_ROOT = Path("/Users/koryjcampbell/Music/CRATES/GENRES")
PLAYLIST_DIR = Path("/Users/koryjcampbell/Music/CRATES/PLAYLISTS/2010s Hip-Hop & R&B Hits")
AUDIO_EXTENSIONS = {".mp3", ".m4a", ".flac", ".wav", ".aif", ".aiff", ".ogg"}

# Billboard Year-End Hot R&B/Hip-Hop Songs + Hot 100 crossover hits 2010-2019
BILLBOARD_HITS = {
    2010: [
        ("Nothin' on You", "B.o.B", "B.o.B."),
        ("Airplanes", "B.o.B", "B.o.B."),
        ("Love the Way You Lie", "Eminem"),
        ("Not Afraid", "Eminem"),
        ("OMG", "Usher", "USHER"),
        ("There Goes My Baby", "Usher", "USHER"),
        ("DJ Got Us Fallin' in Love", "Usher", "USHER"),
        ("More", "Usher", "USHER"),
        ("Find Your Love", "Drake"),
        ("Over", "Drake"),
        ("Miss Me", "Drake"),
        ("Fancy", "Drake"),
        ("BedRock", "Young Money"),
        ("Roger That", "Young Money"),
        ("Break Your Heart", "Taio Cruz"),
        ("Dynamite", "Taio Cruz"),
        ("Rude Boy", "Rihanna"),
        ("Only Girl (In the World)", "Rihanna"),
        ("What's My Name?", "Rihanna"),
        ("Bottoms Up", "Trey Songz"),
        ("Say Aah", "Trey Songz"),
        ("Neighbors Know My Name", "Trey Songz"),
        ("Already Taken", "Trey Songz"),
        ("Your Love", "Nicki Minaj"),
        ("Right Thru Me", "Nicki Minaj"),
        ("Massive Attack", "Nicki Minaj"),
        ("Un-Thinkable (I'm Ready)", "Alicia Keys"),
        ("Empire State of Mind", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Young Forever", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Imma Be", "Black Eyed Peas"),
        ("I Gotta Feeling", "Black Eyed Peas"),
        ("Teach Me How to Dougie", "Cali Swag District"),
        ("My Chick Bad", "Ludacris"),
        ("Baby", "Justin Bieber"),
        ("Eenie Meenie", "Sean Kingston"),
        ("I Invented Sex", "Trey Songz"),
        ("Pyramid", "Charice"),
        ("Ridin' Solo", "Jason Derulo"),
        ("In My Head", "Jason Derulo"),
        ("Whatcha Say", "Jason Derulo"),
        ("Lil Freak", "Usher", "USHER"),
        ("Hey Daddy (Daddy's Home)", "Usher", "USHER"),
        ("All I Do Is Win", "DJ Khaled"),
        ("Lay It Down", "Lloyd"),
        ("How Low", "Ludacris"),
        ("Deuces", "Chris Brown"),
        ("I Can Transform Ya", "Chris Brown"),
        ("Crawl", "Chris Brown"),
    ],
    2011: [
        ("Rolling in the Deep", "Adele"),
        ("Someone Like You", "Adele"),
        ("We Found Love", "Rihanna"),
        ("S&M", "Rihanna"),
        ("Man Down", "Rihanna"),
        ("What's My Name?", "Rihanna"),
        ("Look at Me Now", "Chris Brown"),
        ("Yeah 3x", "Chris Brown"),
        ("Beautiful People", "Chris Brown"),
        ("She Ain't You", "Chris Brown"),
        ("Black and Yellow", "Wiz Khalifa"),
        ("Roll Up", "Wiz Khalifa"),
        ("No Hands", "Waka Flocka Flame"),
        ("Hard in da Paint", "Waka Flocka Flame"),
        ("Headlines", "Drake"),
        ("Marvin's Room", "Drake"),
        ("The Motto", "Drake"),
        ("I'm On One", "DJ Khaled"),
        ("6 Foot 7 Foot", "Lil Wayne"),
        ("She Will", "Lil Wayne"),
        ("How to Love", "Lil Wayne"),
        ("John", "Lil Wayne"),
        ("Moment 4 Life", "Nicki Minaj"),
        ("Super Bass", "Nicki Minaj"),
        ("Fly", "Nicki Minaj"),
        ("Party Rock Anthem", "LMFAO"),
        ("Sexy and I Know It", "LMFAO"),
        ("Otis", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Niggas in Paris", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Watch the Throne", "Jay-Z", "Jay Z", "JAY-Z"),
        ("All of the Lights", "Kanye West"),
        ("H*A*M", "Kanye West"),
        ("Motivation", "Kelly Rowland"),
        ("Written in the Stars", "Tinie Tempah"),
        ("Best Thing I Never Had", "Beyoncé", "Beyonce"),
        ("Countdown", "Beyoncé", "Beyonce"),
        ("Love on Top", "Beyoncé", "Beyonce"),
        ("Run the World (Girls)", "Beyoncé", "Beyonce"),
        ("Lay It Down", "Lloyd"),
        ("Lotus Flower Bomb", "Wale"),
        ("Rack City", "Tyga"),
        ("Who Gon Stop Me", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Lighters", "Bad Meets Evil", "Eminem"),
        ("I Need a Doctor", "Dr. Dre"),
        ("Wet the Bed", "Chris Brown"),
        ("No Sleep", "Wiz Khalifa"),
        ("Take Care", "Drake"),
    ],
    2012: [
        ("We Are Young", "fun."),
        ("Somebody That I Used to Know", "Gotye"),
        ("Whistle", "Flo Rida"),
        ("Wild Ones", "Flo Rida"),
        ("Climax", "Usher", "USHER"),
        ("Scream", "Usher", "USHER"),
        ("Numb", "Usher", "USHER"),
        ("Mercy", "Kanye West"),
        ("Clique", "Kanye West"),
        ("Take Care", "Drake"),
        ("Headlines", "Drake"),
        ("The Motto", "Drake"),
        ("HYFR", "Drake"),
        ("Make Me Proud", "Drake"),
        ("Rack City", "Tyga"),
        ("Faded", "Tyga"),
        ("Adorn", "Miguel"),
        ("Do You...", "Miguel"),
        ("Birthday Song", "2 Chainz"),
        ("No Lie", "2 Chainz"),
        ("I'm Different", "2 Chainz"),
        ("Spend It", "2 Chainz"),
        ("Bandz a Make Her Dance", "Juicy J"),
        ("Niggas in Paris", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Turn Up the Music", "Chris Brown"),
        ("Don't Wake Me Up", "Chris Brown"),
        ("Don't Judge Me", "Chris Brown"),
        ("Beez in the Trap", "Nicki Minaj"),
        ("Pound the Alarm", "Nicki Minaj"),
        ("Starships", "Nicki Minaj"),
        ("Drank in My Cup", "Kirko Bangz"),
        ("Pop That", "French Montana"),
        ("Poetic Justice", "Kendrick Lamar"),
        ("Swimming Pools (Drank)", "Kendrick Lamar"),
        ("Backseat Freestyle", "Kendrick Lamar"),
        ("Lotus Flower Bomb", "Wale"),
        ("Bag of Money", "Wale"),
        ("Let Me Love You", "Ne-Yo"),
        ("Miss Me", "Drake"),
        ("Diamonds", "Rihanna"),
        ("Where Have You Been", "Rihanna"),
        ("Cockiness", "Rihanna"),
        ("Love Me", "Lil Wayne"),
        ("Love Sosa", "Chief Keef"),
        ("I Don't Like", "Chief Keef"),
        ("R.I.P.", "Young Jeezy"),
        ("Fuckin' Problems", "A$AP Rocky", "ASAP Rocky"),
        ("Goldie", "A$AP Rocky", "ASAP Rocky"),
    ],
    2013: [
        ("Thrift Shop", "Macklemore", "Macklemore & Ryan Lewis"),
        ("Can't Hold Us", "Macklemore", "Macklemore & Ryan Lewis"),
        ("Blurred Lines", "Robin Thicke"),
        ("Started from the Bottom", "Drake"),
        ("Hold On, We're Going Home", "Drake"),
        ("All Me", "Drake"),
        ("Worst Behavior", "Drake"),
        ("Holy Grail", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Tom Ford", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Fuckin' Problems", "A$AP Rocky", "ASAP Rocky"),
        ("Just Give Me a Reason", "Pink", "P!nk"),
        ("Suit & Tie", "Justin Timberlake"),
        ("Mirrors", "Justin Timberlake"),
        ("TKO", "Justin Timberlake"),
        ("Poetic Justice", "Kendrick Lamar"),
        ("Swimming Pools (Drank)", "Kendrick Lamar"),
        ("Bitch, Don't Kill My Vibe", "Kendrick Lamar"),
        ("Love Sosa", "Chief Keef"),
        ("Bugatti", "Ace Hood"),
        ("No New Friends", "DJ Khaled"),
        ("Power Trip", "J. Cole"),
        ("Crooked Smile", "J. Cole"),
        ("Fine China", "Chris Brown"),
        ("Loyal", "Chris Brown"),
        ("Beat It", "Sean Kingston"),
        ("Gas Pedal", "Sage the Gemini"),
        ("Bandz a Make Her Dance", "Juicy J"),
        ("Body Party", "Ciara"),
        ("Adorn", "Miguel"),
        ("How Many Drinks?", "Miguel"),
        ("Bad", "Wale"),
        ("Love Me", "Lil Wayne"),
        ("Tapout", "Rich Gang"),
        ("23", "Mike WiLL Made-It"),
        ("Versace", "Migos"),
        ("My Hitta", "YG"),
        ("Drunk in Love", "Beyoncé", "Beyonce"),
        ("XO", "Beyoncé", "Beyonce"),
        ("No Worries", "Lil Wayne"),
        ("Pour It Up", "Rihanna"),
        ("Stay", "Rihanna"),
        ("The Monster", "Eminem"),
        ("Berzerk", "Eminem"),
        ("Rap God", "Eminem"),
        ("Treasure", "Bruno Mars"),
        ("Locked Out of Heaven", "Bruno Mars"),
        ("When I Was Your Man", "Bruno Mars"),
    ],
    2014: [
        ("Happy", "Pharrell", "Pharrell Williams"),
        ("All of Me", "John Legend"),
        ("Fancy", "Iggy Azalea"),
        ("Problem", "Ariana Grande"),
        ("Stay with Me", "Sam Smith"),
        ("Turn Down for What", "DJ Snake"),
        ("Talk Dirty", "Jason Derulo"),
        ("Trumpets", "Jason Derulo"),
        ("Wiggle", "Jason Derulo"),
        ("Loyal", "Chris Brown"),
        ("New Flame", "Chris Brown"),
        ("Drunk in Love", "Beyoncé", "Beyonce"),
        ("Partition", "Beyoncé", "Beyonce"),
        ("Studio", "Schoolboy Q", "ScHoolboy Q"),
        ("Man of the Year", "Schoolboy Q", "ScHoolboy Q"),
        ("No Type", "Rae Sremmurd"),
        ("No Flex Zone", "Rae Sremmurd"),
        ("0 to 100", "Drake"),
        ("Trophies", "Drake"),
        ("Hold On, We're Going Home", "Drake"),
        ("Wet Dreamz", "J. Cole"),
        ("A Tale of 2 Citiez", "J. Cole"),
        ("My Nigga", "YG"),
        ("Who Do You Love?", "YG"),
        ("Left Hand Free", "alt-J"),
        ("Move That Dope", "Future"),
        ("Honest", "Future"),
        ("Lifestyle", "Rich Gang"),
        ("Hot Nigga", "Bobby Shmurda"),
        ("About the Money", "T.I."),
        ("Or Nah", "Ty Dolla Sign", "Ty Dolla $ign"),
        ("Paranoid", "Ty Dolla Sign", "Ty Dolla $ign"),
        ("The Worst", "Jhene Aiko", "Jhené Aiko"),
        ("2 On", "Tinashe"),
        ("Anaconda", "Nicki Minaj"),
        ("Pills N Potions", "Nicki Minaj"),
        ("Only", "Nicki Minaj"),
        ("Don't Tell 'Em", "Jeremih"),
        ("She Came to Give It to You", "Usher", "USHER"),
        ("I Don't Fuck with You", "Big Sean"),
        ("IDFWU", "Big Sean"),
        ("Blessings", "Big Sean"),
        ("Tuesday", "ILoveMakonnen", "iLoveMakonnen"),
        ("CoCo", "O.T. Genasis"),
        ("Post to Be", "Omarion"),
        ("Na Na", "Trey Songz"),
        ("We Dem Boyz", "Wiz Khalifa"),
    ],
    2015: [
        ("Hotline Bling", "Drake"),
        ("Back to Back", "Drake"),
        ("Energy", "Drake"),
        ("Know Yourself", "Drake"),
        ("10 Bands", "Drake"),
        ("Used To", "Drake"),
        ("Can't Feel My Face", "The Weeknd", "Weeknd"),
        ("The Hills", "The Weeknd", "Weeknd"),
        ("Earned It", "The Weeknd", "Weeknd"),
        ("Often", "The Weeknd", "Weeknd"),
        ("Trap Queen", "Fetty Wap"),
        ("679", "Fetty Wap"),
        ("My Way", "Fetty Wap"),
        ("Watch Me", "Silento"),
        ("March Madness", "Future"),
        ("Fuck Up Some Commas", "Future"),
        ("Where Ya At", "Future"),
        ("Commas", "Future"),
        ("Alright", "Kendrick Lamar"),
        ("King Kunta", "Kendrick Lamar"),
        ("These Walls", "Kendrick Lamar"),
        ("i", "Kendrick Lamar"),
        ("Cheerleader", "OMI"),
        ("Flex (Ooh Ooh Ooh)", "Rich Homie Quan"),
        ("Hit the Quan", "iHeart Memphis", "iHeartMemphis"),
        ("Post to Be", "Omarion"),
        ("Blessings", "Big Sean"),
        ("I Don't Fuck with You", "Big Sean"),
        ("IDFWU", "Big Sean"),
        ("Throw Sum Mo", "Rae Sremmurd"),
        ("No Type", "Rae Sremmurd"),
        ("No Flex Zone", "Rae Sremmurd"),
        ("My Way", "Fetty Wap"),
        ("CoCo", "O.T. Genasis"),
        ("Lean On", "Major Lazer"),
        ("Worth It", "Fifth Harmony"),
        ("G.D.F.R.", "Flo Rida"),
        ("Only", "Nicki Minaj"),
        ("Truffle Butter", "Nicki Minaj"),
        ("The Night Is Still Young", "Nicki Minaj"),
        ("Feeling Myself", "Nicki Minaj"),
        ("Wet Dreamz", "J. Cole"),
        ("No Role Modelz", "J. Cole"),
        ("Apparently", "J. Cole"),
        ("Wicked", "Future"),
        ("Like I'm Gonna Lose You", "Meghan Trainor"),
        ("Antidote", "Travis Scott"),
    ],
    2016: [
        ("One Dance", "Drake"),
        ("Hotline Bling", "Drake"),
        ("Pop Style", "Drake"),
        ("Controlla", "Drake"),
        ("Too Good", "Drake"),
        ("Summer Sixteen", "Drake"),
        ("Work", "Rihanna"),
        ("Needed Me", "Rihanna"),
        ("Kiss It Better", "Rihanna"),
        ("Formation", "Beyoncé", "Beyonce"),
        ("Hold Up", "Beyoncé", "Beyonce"),
        ("Sorry", "Beyoncé", "Beyonce"),
        ("Freedom", "Beyoncé", "Beyonce"),
        ("Panda", "Desiigner"),
        ("No Problem", "Chance the Rapper"),
        ("Angels", "Chance the Rapper"),
        ("Broccoli", "D.R.A.M.", "DRAM"),
        ("Low Life", "Future"),
        ("Wicked", "Future"),
        ("Jumpman", "Drake"),
        ("Pick Up the Phone", "Young Thug"),
        ("Best Friend", "Young Thug"),
        ("Black Beatles", "Rae Sremmurd"),
        ("By Chance", "Rae Sremmurd"),
        ("My Way", "Fetty Wap"),
        ("Famous", "Kanye West"),
        ("Ultralight Beam", "Kanye West"),
        ("Father Stretch My Hands", "Kanye West"),
        ("Gold", "Kiiara"),
        ("All the Way Up", "Fat Joe"),
        ("Tiimmy Turner", "Desiigner"),
        ("You Was Right", "Lil Uzi Vert"),
        ("Money Longer", "Lil Uzi Vert"),
        ("Caroline", "Aminé", "Amine"),
        ("Come and See Me", "PartyNextDoor", "PARTYNEXTDOOR"),
        ("Don't", "Bryson Tiller"),
        ("Exchange", "Bryson Tiller"),
        ("Sorry", "Bryson Tiller"),
        ("Real Friends", "Kanye West"),
        ("Really Really", "Kevin Gates"),
        ("2 Phones", "Kevin Gates"),
        ("Luv", "Tory Lanez"),
        ("Starboy", "The Weeknd", "Weeknd"),
        ("False Alarm", "The Weeknd", "Weeknd"),
        ("Fade", "Kanye West"),
        ("This Is What You Came For", "Calvin Harris"),
    ],
    2017: [
        ("Bodak Yellow", "Cardi B"),
        ("Rockstar", "Post Malone"),
        ("Congratulations", "Post Malone"),
        ("HUMBLE.", "Kendrick Lamar", "Kendrick"),
        ("LOYALTY.", "Kendrick Lamar", "Kendrick"),
        ("DNA.", "Kendrick Lamar", "Kendrick"),
        ("ELEMENT.", "Kendrick Lamar", "Kendrick"),
        ("Bad and Boujee", "Migos"),
        ("T-Shirt", "Migos"),
        ("Slippery", "Migos"),
        ("Love Galore", "SZA"),
        ("The Weekend", "SZA"),
        ("XO TOUR Llif3", "Lil Uzi Vert"),
        ("Unforgettable", "French Montana"),
        ("Mask Off", "Future"),
        ("Bank Account", "21 Savage"),
        ("Bounce Back", "Big Sean"),
        ("Moves", "Big Sean"),
        ("Portland", "Drake"),
        ("Passionfruit", "Drake"),
        ("Signs", "Drake"),
        ("Fake Love", "Drake"),
        ("I'm the One", "DJ Khaled"),
        ("Wild Thoughts", "DJ Khaled"),
        ("Shining", "DJ Khaled"),
        ("That's What I Like", "Bruno Mars"),
        ("24K Magic", "Bruno Mars"),
        ("1-800-273-8255", "Logic"),
        ("iSpy", "Kyle", "KYLE"),
        ("Broccoli", "D.R.A.M.", "DRAM"),
        ("Tunnel Vision", "Kodak Black"),
        ("Location", "Khalid"),
        ("Young Dumb & Broke", "Khalid"),
        ("Loyal", "PartyNextDoor", "PARTYNEXTDOOR"),
        ("Plain Jane", "A$AP Ferg", "ASAP Ferg"),
        ("4 4 4", "Jay-Z", "Jay Z", "JAY-Z"),
        ("The Story of O.J.", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Gucci Gang", "Lil Pump"),
        ("I Fall Apart", "Post Malone"),
        ("Motorsport", "Migos"),
        ("MotorSport", "Migos"),
        ("No Limit", "G-Eazy"),
        ("Starboy", "The Weeknd", "Weeknd"),
        ("Reminder", "The Weeknd", "Weeknd"),
        ("Party Monster", "The Weeknd", "Weeknd"),
        ("Havana", "Camila Cabello"),
    ],
    2018: [
        ("God's Plan", "Drake"),
        ("Nice for What", "Drake"),
        ("In My Feelings", "Drake"),
        ("Nonstop", "Drake"),
        ("I'm Upset", "Drake"),
        ("Mob Ties", "Drake"),
        ("Psycho", "Post Malone"),
        ("Better Now", "Post Malone"),
        ("Rockstar", "Post Malone"),
        ("I Like It", "Cardi B"),
        ("Bodak Yellow", "Cardi B"),
        ("Be Careful", "Cardi B"),
        ("Money", "Cardi B"),
        ("SICKO MODE", "Travis Scott"),
        ("Stargazing", "Travis Scott"),
        ("Butterfly Effect", "Travis Scott"),
        ("Lucid Dreams", "Juice WRLD", "Juice Wrld"),
        ("All Girls Are the Same", "Juice WRLD", "Juice Wrld"),
        ("Sad!", "XXXTentacion", "XXXTENTACION"),
        ("Moonlight", "XXXTentacion", "XXXTENTACION"),
        ("Changes", "XXXTentacion", "XXXTENTACION"),
        ("Yes Indeed", "Lil Baby"),
        ("Drip Too Hard", "Lil Baby"),
        ("Racks on Racks", "Lil Pump"),
        ("Walk It Talk It", "Migos"),
        ("Stir Fry", "Migos"),
        ("Narcos", "Migos"),
        ("Mine", "Bazzi"),
        ("This Is America", "Childish Gambino"),
        ("Taste", "Tyga"),
        ("Love Lies", "Khalid"),
        ("Young Dumb & Broke", "Khalid"),
        ("Praise the Lord", "A$AP Rocky", "ASAP Rocky"),
        ("Mo Bamba", "Sheck Wes"),
        ("Plug Walk", "Rich the Kid"),
        ("FEFE", "6ix9ine"),
        ("Gummo", "6ix9ine"),
        ("Freaky Friday", "Lil Dicky"),
        ("Ric Flair Drip", "Offset"),
        ("Trip", "Ella Mai"),
        ("Boo'd Up", "Ella Mai"),
        ("Best Part", "Daniel Caesar"),
        ("Finesse", "Bruno Mars"),
        ("Girls Like You", "Maroon 5"),
        ("The London", "Young Thug"),
        ("Wow.", "Post Malone"),
    ],
    2019: [
        ("Old Town Road", "Lil Nas X"),
        ("Panini", "Lil Nas X"),
        ("Truth Hurts", "Lizzo"),
        ("Good as Hell", "Lizzo"),
        ("Juice", "Lizzo"),
        ("Suge", "DaBaby"),
        ("Intro", "DaBaby"),
        ("Baby Sitter", "DaBaby"),
        ("Bop", "DaBaby"),
        ("Circles", "Post Malone"),
        ("Wow.", "Post Malone"),
        ("Sunflower", "Post Malone"),
        ("Goodbyes", "Post Malone"),
        ("Money in the Grave", "Drake"),
        ("Going Bad", "Meek Mill"),
        ("Dreams and Nightmares", "Meek Mill"),
        ("Middle Child", "J. Cole"),
        ("Drip Too Hard", "Lil Baby"),
        ("Close Friends", "Lil Baby"),
        ("Woah", "Lil Baby"),
        ("Mo Bamba", "Sheck Wes"),
        ("SICKO MODE", "Travis Scott"),
        ("Highest in the Room", "Travis Scott"),
        ("Wake Up in the Sky", "Gucci Mane"),
        ("Robbery", "Juice WRLD", "Juice Wrld"),
        ("Lucid Dreams", "Juice WRLD", "Juice Wrld"),
        ("Bandit", "Juice WRLD", "Juice Wrld"),
        ("Racks in the Middle", "Nipsey Hussle"),
        ("7 Rings", "Ariana Grande"),
        ("Thank U, Next", "Ariana Grande"),
        ("Break Up with Your Girlfriend", "Ariana Grande"),
        ("Bad Guy", "Billie Eilish"),
        ("Swervin", "A Boogie wit da Hoodie", "A Boogie Wit da Hoodie"),
        ("Ballin'", "Mustard"),
        ("Pop Out", "Polo G"),
        ("Mia", "Bad Bunny"),
        ("Talk", "Khalid"),
        ("My Bad", "Khalid"),
        ("Pure Water", "Mustard"),
        ("No Guidance", "Chris Brown"),
        ("Baby", "DaBaby"),
        ("Mixed Personalities", "YNW Melly"),
        ("Murder on My Mind", "YNW Melly"),
        ("Shotta Flow", "NLE Choppa"),
        ("Act Up", "City Girls"),
        ("Money", "Cardi B"),
        ("Press", "Cardi B"),
    ],
}


def normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"['\"\-\.\,\!\?\(\)\[\]\{\}]", "", s)
    s = re.sub(r"\s*(feat|ft|featuring|f/).*$", "", s)
    s = re.sub(r"\s+", " ", s)
    return s


def title_match(filename, title):
    fn = normalize(filename)
    t = normalize(title)
    if not t:
        return False
    if t in fn:
        return True
    t2 = re.sub(r"^the ", "", t)
    if t2 != t and t2 in fn:
        return True
    return False


def artist_match(filename, *artists):
    fn = normalize(filename)
    for artist in artists:
        a = normalize(artist)
        if not a:
            continue
        if a in fn:
            return True
        parts = a.split()
        if len(parts) > 1 and parts[-1] in fn and len(parts[-1]) > 3:
            return True
    return False


def find_track(year, title, artists, search_dirs):
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
                if title_match(f, title) and artist_match(f, *artists):
                    in_year = year_str in str(filepath)
                    candidates.append((filepath, in_year))
    if not candidates:
        return None
    year_matches = [c for c in candidates if c[1]]
    if year_matches:
        return year_matches[0][0]
    return candidates[0][0]


def main():
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
    all_missing = []

    for year in range(2010, 2020):
        hits = BILLBOARD_HITS.get(year, [])
        year_dir = PLAYLIST_DIR / str(year)
        year_dir.mkdir(parents=True, exist_ok=True)
        found = 0
        for entry in hits:
            title = entry[0]
            artists = entry[1:]
            track = find_track(year, title, artists, search_dirs)
            if track:
                link_path = year_dir / track.name
                if not link_path.exists() and not link_path.is_symlink():
                    try:
                        os.symlink(track, link_path)
                        found += 1
                    except:
                        pass
            else:
                all_missing.append((year, f"{artists[0]} - {title}"))
        total_hits += len(hits)
        total_found += found
        print(f"{year}: {found}/{len(hits)} hits found")

    print(f"\n{'='*50}")
    print(f"Total: {total_found}/{total_hits} matched ({total_found/total_hits*100:.1f}%)")
    print(f"Missing: {len(all_missing)}")
    if all_missing:
        print("\nMissing tracks:")
        for year, m in all_missing:
            print(f"  [{year}] {m}")

    # Count symlinks created
    link_count = 0
    for year_dir in PLAYLIST_DIR.iterdir():
        if year_dir.is_dir():
            for f in year_dir.iterdir():
                if f.is_symlink():
                    link_count += 1
    print(f"\nTotal symlinks in playlist: {link_count}")
    print(f"Playlist location: {PLAYLIST_DIR}")


if __name__ == "__main__":
    main()
