#!/usr/bin/env python3
"""Build 90s Hip-Hop & R&B Hits playlist from Billboard year-end charts."""

import os
import re
import unicodedata
from pathlib import Path

GENRES_ROOT = Path("/Users/koryjcampbell/Music/CRATES/GENRES")
PLAYLIST_DIR = Path("/Users/koryjcampbell/Music/CRATES/PLAYLISTS/90s Hip-Hop & R&B Hits")
AUDIO_EXTENSIONS = {".mp3", ".m4a", ".flac", ".wav", ".aif", ".aiff", ".ogg"}

BILLBOARD_HITS = {
    1990: [
        ("U Can't Touch This", "MC Hammer", "Hammer"),
        ("Ice Ice Baby", "Vanilla Ice"),
        ("Hold On", "En Vogue"),
        ("Poison", "Bell Biv DeVoe"),
        ("Rub You the Right Way", "Johnny Gill"),
        ("My, My, My", "Johnny Gill"),
        ("Do Me!", "Bell Biv DeVoe"),
        ("Gonna Make You Sweat", "C+C Music Factory"),
        ("Sensitivity", "Ralph Tresvant"),
        ("Feels Good", "Tony! Toni! Toné!"),
        ("All Around the World", "Lisa Stansfield"),
        ("I'll Be Good to You", "Quincy Jones"),
        ("Knockin' Boots", "Candyman"),
        ("Can't Stop", "After 7"),
        ("Have You Seen Her", "MC Hammer", "Hammer"),
        ("Funky Cold Medina", "Tone Loc"),
        ("It Takes Two", "Rob Base"),
        ("Whip Appeal", "Babyface"),
        ("Make You Sweat", "Keith Sweat"),
        ("I Wanna Be Rich", "Calloway"),
        ("Come Back to Me", "Janet Jackson"),
        ("Alright", "Janet Jackson"),
        ("Ready or Not", "After 7"),
        ("Giving You the Benefit", "Pebbles"),
        ("Pray", "MC Hammer", "Hammer"),
        ("Don't Wanna Fall in Love", "Jane Child"),
        ("Groove Is in the Heart", "Deee-Lite"),
        ("Love Will Never Do", "Janet Jackson"),
        ("Where Do We Go from Here", "Stacy Lattisaw"),
        ("The Humpty Dance", "Digital Underground"),
    ],
    1991: [
        ("I Wanna Sex You Up", "Color Me Badd"),
        ("Gonna Make You Sweat", "C+C Music Factory"),
        ("O.P.P.", "Naughty by Nature"),
        ("Emotions", "Mariah Carey"),
        ("Cream", "Prince"),
        ("I Like the Way (The Kissing Game)", "Hi-Five"),
        ("Here We Go (Let's Rock and Roll)", "C+C Music Factory"),
        ("Summertime", "DJ Jazzy Jeff & The Fresh Prince", "DJ Jazzy Jeff"),
        ("All the Man That I Need", "Whitney Houston"),
        ("Do Anything", "Natural Selection"),
        ("Good Vibrations", "Marky Mark", "Marky Mark and the Funky Bunch"),
        ("It Ain't Over 'til It's Over", "Lenny Kravitz"),
        ("I Adore Mi Amor", "Color Me Badd"),
        ("Romantic", "Karyn White"),
        ("Ring My Bell", "DJ Jazzy Jeff"),
        ("Set Adrift on Memory Bliss", "PM Dawn"),
        ("You're in Love", "Wilson Phillips"),
        ("Iesha", "Another Bad Creation"),
        ("Written All Over Your Face", "Rude Boys"),
        ("Motownphilly", "Boyz II Men"),
        ("It's So Hard to Say Goodbye", "Boyz II Men"),
        ("Every Heartbeat", "Amy Grant"),
        ("Unforgettable", "Natalie Cole"),
        ("Don't Let the Sun Go Down on Me", "George Michael"),
        ("3 A.M. Eternal", "The KLF"),
        ("I Don't Wanna Cry", "Mariah Carey"),
        ("Someday", "Mariah Carey"),
        ("Do Me Right", "Guy"),
        ("Coming Out of the Dark", "Gloria Estefan"),
    ],
    1992: [
        ("End of the Road", "Boyz II Men"),
        ("Baby Got Back", "Sir Mix-a-Lot"),
        ("Jump Around", "House of Pain"),
        ("Rump Shaker", "Wreckx-N-Effect"),
        ("Baby-Baby-Baby", "TLC"),
        ("Ain't 2 Proud 2 Beg", "TLC"),
        ("I Love Your Smile", "Shanice"),
        ("Stay", "Jodeci"),
        ("Come & Talk to Me", "Jodeci"),
        ("Tears of a Clown", "After 7"),
        ("I'm Too Sexy", "Right Said Fred"),
        ("Nuthin' but a 'G' Thang", "Dr. Dre"),
        ("Warm It Up", "Kris Kross"),
        ("Jump", "Kris Kross"),
        ("My Lovin' (You're Never Gonna Get It)", "En Vogue"),
        ("Free Your Mind", "En Vogue"),
        ("Giving Him Something He Can Feel", "En Vogue"),
        ("Real Love", "Mary J. Blige"),
        ("You Remind Me", "Mary J. Blige"),
        ("Damn I Wish I Was Your Lover", "Sophie B. Hawkins"),
        ("If I Ever Fall in Love", "Shai"),
        ("Tennessee", "Arrested Development"),
        ("Mr. Wendal", "Arrested Development"),
        ("I'll Be There", "Mariah Carey"),
        ("Make It Happen", "Mariah Carey"),
        ("The Best Things in Life Are Free", "Luther Vandross"),
        ("Sometimes Love Just Ain't Enough", "Patty Smyth"),
        ("To Be with You", "Mr. Big"),
        ("Masterpiece", "Atlantic Starr"),
        ("Humpin' Around", "Bobby Brown"),
    ],
    1993: [
        ("That's the Way Love Goes", "Janet Jackson"),
        ("Weak", "SWV"),
        ("Right Here", "SWV"),
        ("Nuthin' but a 'G' Thang", "Dr. Dre"),
        ("Let Me Ride", "Dr. Dre"),
        ("Dre Day", "Dr. Dre"),
        ("Whoomp! (There It Is)", "Tag Team"),
        ("Slam", "Onyx"),
        ("Informer", "Snow"),
        ("Freak Like Me", "Adina Howard"),
        ("I'm Gonna Be (500 Miles)", "The Proclaimers"),
        ("Show Me Love", "Robin S"),
        ("Rebirth of Slick", "Digable Planets"),
        ("Hip Hop Hooray", "Naughty by Nature"),
        ("Runaway Train", "Soul Asylum"),
        ("Knockin' Da Boots", "H-Town"),
        ("Don't Walk Away", "Jade"),
        ("Lately", "Jodeci"),
        ("Cry for You", "Jodeci"),
        ("If", "Janet Jackson"),
        ("Again", "Janet Jackson"),
        ("Dreamlover", "Mariah Carey"),
        ("Hero", "Mariah Carey"),
        ("I'm So into You", "SWV"),
        ("Shoop", "Salt-N-Pepa"),
        ("Whatta Man", "Salt-N-Pepa"),
        ("Gangsta Lean", "DRS"),
        ("Never Keeping Secrets", "Babyface"),
        ("I Got a Man", "Positive K"),
        ("One More Chance", "Notorious B.I.G.", "The Notorious B.I.G."),
        ("Juicy", "Notorious B.I.G.", "The Notorious B.I.G."),
        ("They Want EFX", "Das EFX"),
        ("C.R.E.A.M.", "Wu-Tang Clan"),
        ("Gin and Juice", "Snoop Dogg", "Snoop Doggy Dogg"),
        ("Who Am I", "Snoop Dogg", "Snoop Doggy Dogg"),
        ("Runnin'", "Pharcyde", "The Pharcyde"),
        ("Check Yo Self", "Ice Cube"),
        ("Electric Slide", "Marcia Griffiths"),
        ("Come Inside", "Intro"),
        ("Comforter", "Shai"),
    ],
    1994: [
        ("I'll Make Love to You", "Boyz II Men"),
        ("On Bended Knee", "Boyz II Men"),
        ("Bump N' Grind", "R. Kelly"),
        ("Your Body's Callin'", "R. Kelly"),
        ("Regulate", "Warren G"),
        ("Stay", "Jodeci"),
        ("Fantastic Voyage", "Coolio"),
        ("I Wanna Be Down", "Brandy"),
        ("Baby I Love Your Way", "Big Mountain"),
        ("Whatta Man", "Salt-N-Pepa"),
        ("Any Time, Any Place", "Janet Jackson"),
        ("Back & Forth", "Aaliyah"),
        ("At Your Best", "Aaliyah"),
        ("Juicy", "Notorious B.I.G.", "The Notorious B.I.G."),
        ("Big Poppa", "Notorious B.I.G.", "The Notorious B.I.G."),
        ("Flava in Ya Ear", "Craig Mack"),
        ("Gin and Juice", "Snoop Dogg", "Snoop Doggy Dogg"),
        ("Funkdafied", "Da Brat"),
        ("You Want This", "Janet Jackson"),
        ("Understanding", "Xscape"),
        ("Secret", "Madonna"),
        ("Another Night", "Real McCoy"),
        ("Always in My Heart", "Tevin Campbell"),
        ("I Miss You", "Aaron Hall"),
        ("Never Lie", "Immature"),
        ("Tootsee Roll", "69 Boyz"),
        ("I Wanna Love You", "Jade"),
        ("Anything", "SWV"),
        ("U.N.I.T.Y.", "Queen Latifah"),
        ("Player's Ball", "Outkast", "OutKast"),
        ("Southernplayalisticadillacmuzik", "Outkast", "OutKast"),
        ("93 'til Infinity", "Souls of Mischief"),
        ("Mass Appeal", "Gang Starr"),
        ("Everyday Thang", "Bone Thugs-N-Harmony"),
        ("Thuggish Ruggish Bone", "Bone Thugs-N-Harmony"),
        ("Luchini AKA This Is It", "Camp Lo"),
    ],
    1995: [
        ("Gangsta's Paradise", "Coolio"),
        ("Waterfalls", "TLC"),
        ("Creep", "TLC"),
        ("Red Light Special", "TLC"),
        ("On Bended Knee", "Boyz II Men"),
        ("Water Runs Dry", "Boyz II Men"),
        ("This Is How We Do It", "Montell Jordan"),
        ("Fantasy", "Mariah Carey"),
        ("One Sweet Day", "Mariah Carey"),
        ("Always Be My Baby", "Mariah Carey"),
        ("I Know", "Dionne Farris"),
        ("Ask of You", "Raphael Saadiq"),
        ("Dear Mama", "2Pac", "Tupac"),
        ("Keep Their Heads Ringin'", "Dr. Dre"),
        ("I Got 5 on It", "Luniz"),
        ("Player's Anthem", "Junior M.A.F.I.A."),
        ("Big Poppa", "Notorious B.I.G.", "The Notorious B.I.G."),
        ("One More Chance", "Notorious B.I.G.", "The Notorious B.I.G."),
        ("I Wish", "Skee-Lo"),
        ("Freek'n You", "Jodeci"),
        ("Shy Guy", "Diana King"),
        ("Gold", "Spandau Ballet"),
        ("Brown Sugar", "D'Angelo"),
        ("Candy Rain", "Soul for Real"),
        ("Tell Me", "Groove Theory"),
        ("You Used to Love Me", "Faith Evans"),
        ("Before I Let You Go", "Blackstreet"),
        ("Boombastic", "Shaggy"),
        ("Renee", "Lost Boyz"),
        ("I'll Be There for You/You're All I Need", "Method Man"),
        ("Don't Take It Personal", "Monica"),
        ("Feels So Good", "Xscape"),
        ("He's Mine", "Mokenstef"),
        ("Sukiyaki", "4 P.M."),
        ("Freak Like Me", "Adina Howard"),
    ],
    1996: [
        ("No Diggity", "Blackstreet"),
        ("Tha Crossroads", "Bone Thugs-N-Harmony"),
        ("1st of tha Month", "Bone Thugs-N-Harmony"),
        ("Twisted", "Keith Sweat"),
        ("Nobody Knows", "Tony Rich Project", "Tony Rich"),
        ("Sittin' Up in My Room", "Brandy"),
        ("How Do U Want It", "2Pac", "Tupac"),
        ("California Love", "2Pac", "Tupac"),
        ("Hit 'Em Up", "2Pac", "Tupac"),
        ("I Ain't Mad at Cha", "2Pac", "Tupac"),
        ("It Was a Good Day", "Ice Cube"),
        ("Only You", "112"),
        ("Peaches & Cream", "112"),
        ("You're Makin' Me High", "Toni Braxton"),
        ("Un-Break My Heart", "Toni Braxton"),
        ("Pony", "Ginuwine"),
        ("Hey Lover", "LL Cool J"),
        ("Doin' It", "LL Cool J"),
        ("Ain't Nobody", "LL Cool J"),
        ("Always Be My Baby", "Mariah Carey"),
        ("One Sweet Day", "Mariah Carey"),
        ("Killing Me Softly", "Fugees"),
        ("Ready or Not", "Fugees"),
        ("Fu-Gee-La", "Fugees"),
        ("C'mon N' Ride It (The Train)", "Quad City DJ's"),
        ("Who Will Save Your Soul", "Jewel"),
        ("Touch Me Tease Me", "Case"),
        ("Lady", "D'Angelo"),
        ("You Make Me Wanna...", "Usher", "USHER"),
        ("Nice & Slow", "Usher", "USHER"),
        ("You Remind Me of Something", "R. Kelly"),
        ("Down Low (Nobody Has to Know)", "R. Kelly"),
        ("I Believe I Can Fly", "R. Kelly"),
        ("I Can't Sleep Baby", "R. Kelly"),
        ("Elevators", "Outkast", "OutKast"),
        ("Rosa Parks", "Outkast", "OutKast"),
        ("Set It Off", "Queen Latifah"),
        ("The Rain (Supa Dupa Fly)", "Missy Elliott"),
        ("Sock It 2 Me", "Missy Elliott"),
        ("It's All About the Benjamins", "Puff Daddy", "Diddy"),
        ("Return of the Mack", "Mark Morrison"),
        ("Macarena", "Los Del Rio"),
        ("Thinkin' Bout It", "Gerald Levert"),
        ("Count on Me", "Whitney Houston"),
        ("Exhale (Shoop Shoop)", "Whitney Houston"),
        ("Who Do U Love", "Deborah Cox"),
    ],
    1997: [
        ("Hypnotize", "Notorious B.I.G.", "The Notorious B.I.G."),
        ("Mo Money Mo Problems", "Notorious B.I.G.", "The Notorious B.I.G."),
        ("I'll Be Missing You", "Puff Daddy", "Diddy", "P. Diddy"),
        ("Can't Nobody Hold Me Down", "Puff Daddy", "Diddy"),
        ("Honey", "Mariah Carey"),
        ("Return of the Mack", "Mark Morrison"),
        ("You Make Me Wanna...", "Usher", "USHER"),
        ("Nice & Slow", "Usher", "USHER"),
        ("No Diggity", "Blackstreet"),
        ("For You I Will", "Monica"),
        ("Not Tonight", "Lil' Kim"),
        ("Crush on You", "Lil' Kim"),
        ("The Rain (Supa Dupa Fly)", "Missy Elliott"),
        ("Sock It 2 Me", "Missy Elliott"),
        ("I Believe I Can Fly", "R. Kelly"),
        ("Bitch Better Have My Money", "AMG"),
        ("4 Seasons of Loneliness", "Boyz II Men"),
        ("I Don't Ever Wanna See You Again", "Uncle Sam"),
        ("Quit Playing Games", "Backstreet Boys"),
        ("Hard Knock Life", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Sunshine", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Who You Wit", "Jay-Z", "Jay Z", "JAY-Z"),
        ("It's All About the Benjamins", "Puff Daddy", "Diddy"),
        ("Been Around the World", "Puff Daddy", "Diddy"),
        ("Feels So Good", "Mase"),
        ("What You Want", "Mase"),
        ("Lookout Weekend", "Debbie Deb"),
        ("Gettin' Jiggy wit It", "Will Smith"),
        ("Men in Black", "Will Smith"),
        ("The Boy Is Mine", "Brandy"),
        ("Butta Love", "Next"),
        ("Too Close", "Next"),
        ("In My Bed", "Dru Hill"),
        ("5 Steps", "Dru Hill"),
        ("How Do I Live", "LeAnn Rimes"),
        ("Foolish", "Ashanti"),
        ("Semi-Charmed Life", "Third Eye Blind"),
        ("Ghetto Supastar", "Pras Michel"),
        ("No No No", "Destiny's Child"),
        ("Rosa Parks", "Outkast", "OutKast"),
    ],
    1998: [
        ("The Boy Is Mine", "Brandy"),
        ("Too Close", "Next"),
        ("Nice & Slow", "Usher", "USHER"),
        ("My Way", "Usher", "USHER"),
        ("Doo Wop (That Thing)", "Lauryn Hill"),
        ("Everything Is Everything", "Lauryn Hill"),
        ("Ghetto Supastar", "Pras Michel"),
        ("Are You That Somebody?", "Aaliyah"),
        ("Gettin' Jiggy wit It", "Will Smith"),
        ("Hard Knock Life", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Can I Get A...", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Money, Cash, Hoes", "Jay-Z", "Jay Z", "JAY-Z"),
        ("I Don't Ever Wanna See You Again", "Uncle Sam"),
        ("Gone Till November", "Wyclef Jean"),
        ("Make It Hot", "Nicole Wray"),
        ("Uh Oh", "Trina"),
        ("My Body", "LSG"),
        ("How Deep Is Your Love", "Dru Hill"),
        ("No, No, No Part 2", "Destiny's Child"),
        ("Crush on You", "Lil' Kim"),
        ("Been Around the World", "Puff Daddy", "Diddy"),
        ("Come with Me", "Puff Daddy", "Diddy"),
        ("It's Not Right but It's Okay", "Whitney Houston"),
        ("Heartbreak Hotel", "Whitney Houston"),
        ("My Love Is Your Love", "Whitney Houston"),
        ("You're Still the One", "Shania Twain"),
        ("Thank God I Found You", "Mariah Carey"),
        ("My All", "Mariah Carey"),
        ("When You Believe", "Whitney Houston"),
        ("Nobody's Supposed to Be Here", "Deborah Cox"),
        ("Feel So Good", "Mase"),
        ("Lookin' at Me", "Mase"),
        ("What You Want", "Mase"),
        ("I'll Be", "Edwin McCain"),
        ("How's It Goin' Down", "DMX"),
        ("Ruff Ryders' Anthem", "DMX"),
        ("Get at Me Dog", "DMX"),
        ("Party Up", "DMX"),
        ("Intergalactic", "Beastie Boys"),
        ("Rosa Parks", "Outkast", "OutKast"),
        ("Aquemini", "Outkast", "OutKast"),
        ("Still Not a Player", "Big Pun"),
        ("Twinz (Deep Cover '98)", "Big Pun"),
    ],
    1999: [
        ("No Scrubs", "TLC"),
        ("Unpretty", "TLC"),
        ("Heartbreaker", "Mariah Carey"),
        ("Bills, Bills, Bills", "Destiny's Child"),
        ("Bug a Boo", "Destiny's Child"),
        ("Jumpin' Jumpin'", "Destiny's Child"),
        ("If You Had My Love", "Jennifer Lopez"),
        ("Waiting for Tonight", "Jennifer Lopez"),
        ("Satisfy You", "Puff Daddy", "Diddy", "P. Diddy"),
        ("Hot Boyz", "Missy Elliott"),
        ("She's All I Got", "Juvenile"),
        ("Back That Azz Up", "Juvenile"),
        ("Ha", "Juvenile"),
        ("Bling Bling", "B.G."),
        ("Big Pimpin'", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Hard Knock Life", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Vivrant Thing", "Q-Tip"),
        ("Wild Wild West", "Will Smith"),
        ("I Need to Know", "Marc Anthony"),
        ("No Limit", "Master P"),
        ("Somebody's Watching Me", "Beatnuts"),
        ("Anywhere", "112"),
        ("Kiss Me", "Sixpence None the Richer"),
        ("Angel of Mine", "Monica"),
        ("My Name Is", "Eminem"),
        ("Guilty Conscience", "Eminem"),
        ("It's Not Right but It's Okay", "Whitney Houston"),
        ("What's It Gonna Be?!", "Busta Rhymes"),
        ("Gimme Some More", "Busta Rhymes"),
        ("You Don't Know Me", "Jagged Edge"),
        ("Gotta Man", "Eve"),
        ("Thong Song", "Sisqo", "Sisqó"),
        ("Incomplete", "Sisqo", "Sisqó"),
        ("Can I Get A...", "Jay-Z", "Jay Z", "JAY-Z"),
        ("Ride wit Me", "Nelly"),
        ("Country Grammar", "Nelly"),
        ("Girl on TV", "LFO"),
        ("Summer Girls", "LFO"),
        ("Fortunate", "Maxwell"),
        ("Tell Me It's Real", "K-Ci & JoJo"),
        ("All My Life", "K-Ci & JoJo"),
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
        GENRES_ROOT / "Disco",
    ]

    total_hits = 0
    total_found = 0
    all_missing = []

    for year in range(1990, 2000):
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

    print(f"\nTotal: {total_found}/{total_hits} matched ({total_found/total_hits*100:.1f}%)")
    print(f"Missing: {len(all_missing)}")
    if all_missing:
        print("\nMissing tracks:")
        for year, m in all_missing:
            print(f"  [{year}] {m}")


if __name__ == "__main__":
    main()
