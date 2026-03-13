#!/usr/bin/env python3
"""Step 2: Classify tracks into subgenres using ID3 tags + artist knowledge."""

import csv
import json
import re
from pathlib import Path

TOOLS_DIR = Path("/Users/koryjcampbell/Music/CRATES/GENRES/.dj-crates-tools")
MANIFEST = TOOLS_DIR / "manifest.json"
OUTPUT_JSON = TOOLS_DIR / "classification.json"
OUTPUT_CSV = TOOLS_DIR / "classification_review.csv"

# ============================================================
# SUBGENRE MAPPINGS PER GENRE
# ============================================================

# Artist name → subgenre (case-insensitive lookup)
# We normalize artist names to lowercase for matching.

HIPHOP_ARTIST_MAP = {
    # Boom Bap / East Coast
    "nas": "Boom Bap",
    "jay z": "East Coast",
    "jay-z": "East Coast",
    "the notorious b.i.g.": "East Coast",
    "notorious b.i.g.": "East Coast",
    "biggie smalls": "East Coast",
    "wu-tang clan": "Boom Bap",
    "method man": "Boom Bap",
    "raekwon": "Boom Bap",
    "ghostface killah": "Boom Bap",
    "mobb deep": "Boom Bap",
    "a tribe called quest": "Boom Bap",
    "de la soul": "Boom Bap",
    "gang starr": "Boom Bap",
    "dj premier": "Boom Bap",
    "pete rock": "Boom Bap",
    "big l": "Boom Bap",
    "big pun": "Boom Bap",
    "krs-one": "Boom Bap",
    "black moon": "Boom Bap",
    "smif-n-wessun": "Boom Bap",
    "boot camp clik": "Boom Bap",
    "fat joe": "East Coast",
    "fabolous": "East Coast",
    "jadakiss": "East Coast",
    "the lox": "East Coast",
    "styles p": "East Coast",
    "sheek louch": "East Coast",
    "dipset": "East Coast",
    "cam'ron": "East Coast",
    "juelz santana": "East Coast",
    "jim jones": "East Coast",
    "50 cent": "East Coast",
    "g-unit": "East Coast",
    "lloyd banks": "East Coast",
    "tony yayo": "East Coast",
    "young buck": "East Coast",
    "dmx": "East Coast",
    "busta rhymes": "East Coast",
    "ll cool j": "East Coast",
    "french montana": "East Coast",
    "a$ap rocky": "East Coast",
    "asap rocky": "East Coast",
    "a$ap ferg": "East Coast",
    "a$ap mob": "East Coast",
    "joey bada$$": "Boom Bap",
    "joey badass": "Boom Bap",
    "action bronson": "Boom Bap",
    "roc marciano": "Boom Bap",
    "griselda": "Boom Bap",
    "westside gunn": "Boom Bap",
    "conway the machine": "Boom Bap",
    "benny the butcher": "Boom Bap",
    "freddie gibbs": "Boom Bap",
    "pusha t": "East Coast",
    "clipse": "East Coast",
    "the diplomats": "East Coast",
    "ma$e": "East Coast",
    "mase": "East Coast",
    "diddy": "East Coast",
    "puff daddy": "East Coast",
    "p. diddy": "East Coast",
    "sean combs": "East Coast",
    "junior m.a.f.i.a.": "East Coast",
    "lil' kim": "East Coast",
    "lil kim": "East Coast",
    "missy elliott": "East Coast",
    "eve": "East Coast",
    "ja rule": "East Coast",
    "swizz beatz": "East Coast",

    # West Coast
    "dr. dre": "West Coast",
    "snoop dogg": "West Coast",
    "snoop doggy dogg": "West Coast",
    "ice cube": "West Coast",
    "the game": "West Coast",
    "game": "West Coast",
    "kendrick lamar": "West Coast",
    "tupac": "West Coast",
    "2pac": "West Coast",
    "warren g": "West Coast",
    "nate dogg": "West Coast",
    "xzibit": "West Coast",
    "kurupt": "West Coast",
    "daz dillinger": "West Coast",
    "tha dogg pound": "West Coast",
    "e-40": "West Coast",
    "too $hort": "West Coast",
    "too short": "West Coast",
    "mac dre": "West Coast",
    "dj quik": "West Coast",
    "yg": "West Coast",
    "dom kennedy": "West Coast",
    "nipsey hussle": "West Coast",
    "schoolboy q": "West Coast",
    "ab-soul": "West Coast",
    "jay rock": "West Coast",
    "tyler, the creator": "West Coast",
    "tyler the creator": "West Coast",
    "vince staples": "West Coast",
    "anderson .paak": "West Coast",
    "the pharcyde": "West Coast",
    "cypress hill": "West Coast",
    "n.w.a": "West Coast",
    "n.w.a.": "West Coast",
    "eazy-e": "West Coast",
    "mc ren": "West Coast",
    "dj mustard": "West Coast",
    "mustard": "West Coast",

    # G-Funk
    "tha eastsidaz": "G-Funk",
    "213": "G-Funk",
    "domino": "G-Funk",
    "above the law": "G-Funk",

    # Southern / Dirty South
    "outkast": "Southern",
    "andre 3000": "Southern",
    "big boi": "Southern",
    "goodie mob": "Southern",
    "cee lo green": "Southern",
    "t.i.": "Southern",
    "ludacris": "Southern",
    "jeezy": "Southern",
    "young jeezy": "Southern",
    "lil wayne": "Southern",
    "lil' wayne": "Southern",
    "birdman": "Southern",
    "juvenile": "Southern",
    "cash money millionaires": "Southern",
    "hot boys": "Southern",
    "b.g.": "Southern",
    "mannie fresh": "Southern",
    "master p": "Southern",
    "mystikal": "Southern",
    "no limit": "Southern",
    "trick daddy": "Southern",
    "trina": "Southern",
    "rick ross": "Southern",
    "ace hood": "Southern",
    "dj khaled": "Southern",
    "plies": "Southern",
    "pitbull": "Southern",
    "flo rida": "Southern",
    "2 chainz": "Southern",
    "big k.r.i.t.": "Southern",
    "big krit": "Southern",
    "gucci mane": "Trap",
    "waka flocka flame": "Trap",
    "waka flocka": "Trap",
    "oj da juiceman": "Trap",
    "mike jones": "Southern",
    "paul wall": "Southern",
    "slim thug": "Southern",
    "chamillionaire": "Southern",
    "scarface": "Southern",
    "ugk": "Southern",
    "bun b": "Southern",
    "pimp c": "Southern",
    "8ball & mjg": "Southern",
    "three 6 mafia": "Southern",
    "project pat": "Southern",
    "yo gotti": "Southern",
    "moneybagg yo": "Southern",
    "big sean": "Southern",
    "meek mill": "East Coast",
    "nicki minaj": "East Coast",

    # Trap
    "future": "Trap",
    "young thug": "Trap",
    "migos": "Trap",
    "quavo": "Trap",
    "offset": "Trap",
    "takeoff": "Trap",
    "21 savage": "Trap",
    "metro boomin": "Trap",
    "lil baby": "Trap",
    "gunna": "Trap",
    "lil uzi vert": "Trap",
    "playboi carti": "Trap",
    "travis scott": "Trap",
    "lil yachty": "Trap",
    "kodak black": "Trap",
    "nba youngboy": "Trap",
    "youngboy never broke again": "Trap",
    "dababy": "Trap",
    "lil durk": "Trap",
    "polo g": "Trap",
    "rod wave": "Trap",
    "lil tecca": "Trap",
    "don toliver": "Trap",
    "jackboy": "Trap",
    "moneybagg yo": "Trap",
    "key glock": "Trap",
    "young dolph": "Trap",
    "rae sremmurd": "Trap",
    "swae lee": "Trap",
    "slim jxmmi": "Trap",
    "2 chainz": "Trap",
    "juicy j": "Trap",

    # Crunk
    "lil jon": "Crunk",
    "lil jon & the east side boyz": "Crunk",
    "ying yang twins": "Crunk",
    "crime mob": "Crunk",
    "trillville": "Crunk",
    "david banner": "Crunk",
    "pastor troy": "Crunk",
    "bonecrusher": "Crunk",

    # Drill
    "chief keef": "Drill",
    "lil reese": "Drill",
    "lil herb": "Drill",
    "g herbo": "Drill",
    "king von": "Drill",
    "pop smoke": "Drill",
    "fivio foreign": "Drill",
    "sheff g": "Drill",
    "sleepy hallow": "Drill",
    "22gz": "Drill",
    "central cee": "Drill",

    # Conscious / Alternative
    "common": "Conscious",
    "mos def": "Conscious",
    "talib kweli": "Conscious",
    "black star": "Conscious",
    "the roots": "Conscious",
    "j. cole": "Conscious",
    "j cole": "Conscious",
    "childish gambino": "Conscious",
    "chance the rapper": "Conscious",
    "logic": "Conscious",
    "kid cudi": "Conscious",
    "lupe fiasco": "Conscious",
    "immortal technique": "Conscious",
    "dead prez": "Conscious",
    "brother ali": "Conscious",
    "atmosphere": "Conscious",
    "aesop rock": "Conscious",
    "run the jewels": "Conscious",
    "killer mike": "Conscious",
    "el-p": "Conscious",
    "noname": "Conscious",
    "saba": "Conscious",
    "smino": "Conscious",
    "earthgang": "Conscious",
    "jid": "Conscious",
    "denzel curry": "Conscious",
    "little simz": "Conscious",
    "jpegmafia": "Conscious",
    "open mike eagle": "Conscious",

    # Kanye - spans eras but iconic enough for own mapping
    "kanye west": "East Coast",
    "ye": "East Coast",

    # Gangsta
    "the notorious b.i.g.": "East Coast",

    # Cloud Rap
    "lil b": "Cloud Rap",
    "clams casino": "Cloud Rap",
    "main attrakionz": "Cloud Rap",
    "a$ap rocky": "Cloud Rap",  # arguably

    # Eminem - East Coast (Detroit)
    "eminem": "East Coast",
    "d12": "East Coast",
    "royce da 5'9\"": "East Coast",
    "royce da 5'9": "East Coast",

    # Nelly - Southern pop-rap
    "nelly": "Southern",
    "st. lunatics": "Southern",
    "chingy": "Southern",
    "murphy lee": "Southern",

    # Drake - Toronto but stylistically versatile
    "drake": "Southern",
    "partynextdoor": "Southern",

    # Misc well-known
    "kanye west": "East Coast",
    "lil nas x": "Southern",
    "jack harlow": "Southern",
    "post malone": "Southern",
    "cardi b": "East Coast",
    "megan thee stallion": "Southern",
    "doja cat": "West Coast",
    "saweetie": "West Coast",
    "ice spice": "Drill",
    "glorilla": "Southern",
    "sexyy red": "Southern",

    # Bow Wow, Soulja Boy
    "bow wow": "Southern",
    "lil bow wow": "Southern",
    "soulja boy": "Southern",
    "soulja boy tell 'em": "Southern",

    # Philadelphia
    "beanie sigel": "East Coast",
    "state property": "East Coast",
    "freeway": "East Coast",
    "cassidy": "East Coast",

    # More Southern
    "webbie": "Southern",
    "boosie badazz": "Southern",
    "lil boosie": "Southern",
    "rich homie quan": "Trap",
    "fetty wap": "East Coast",
    "desiigner": "Trap",
    "blocboy jb": "Trap",
    "blueface": "West Coast",
    "roddy ricch": "West Coast",
    "baby keem": "West Coast",

    # Tech N9ne etc
    "tech n9ne": "Midwest",
    "bone thugs-n-harmony": "Midwest",
    "twista": "Midwest",
    "do or die": "Midwest",
    "crucial conflict": "Midwest",

    # More artists
    "wiz khalifa": "East Coast",
    "mac miller": "East Coast",
    "asap ferg": "East Coast",
    "tyler the creator": "West Coast",
    "earl sweatshirt": "West Coast",
    "odd future": "West Coast",
    "frank ocean": "West Coast",

    # Lex Luger era
    "waka flocka flame": "Trap",

    # More recent
    "j.i.d": "Conscious",
    "bas": "Conscious",
    "dreamville": "Conscious",
    "cordae": "Conscious",
    "isaiah rashad": "Southern",
    "rico nasty": "East Coast",
    "tierra whack": "East Coast",

    # Additional unmapped artists
    "akon": "Southern",
    "big tymers": "Southern",
    "dilated peoples": "Boom Bap",
    "az": "Boom Bap",
    "ashanti": "East Coast",
    "beenie man": "Southern",
    "504 boyz": "Southern",
    "black eyed peas": "East Coast",
    "bubba sparxxx": "Southern",
    "black rob": "East Coast",
    "c murder": "Southern",
    "c-murder": "Southern",
    "beastie boys": "East Coast",
    "camron": "East Coast",
    "cam'ron": "East Coast",
    "d4l": "Southern",
    "big shug": "Boom Bap",
    "blaq poet": "Boom Bap",
    "boyz n da hood": "Southern",
    "bumpy knuckles": "Boom Bap",
    "cnn": "East Coast",
    "capone-n-noreaga": "East Coast",
    "n.o.r.e.": "East Coast",
    "noreaga": "East Coast",
    "sean kingston": "Southern",
    "shawty lo": "Southern",
    "rich boy": "Southern",
    "lil scrappy": "Crunk",
    "lil flip": "Southern",
    "lil mama": "East Coast",
    "silkk the shocker": "Southern",
    "baby bash": "West Coast",
    "b-real": "West Coast",
    "xzibit": "West Coast",
    "talib kweli": "Boom Bap",
    "rakim": "Boom Bap",
    "eric b. & rakim": "Boom Bap",
    "eric b": "Boom Bap",
    "slick rick": "East Coast",
    "epmd": "Boom Bap",
    "erick sermon": "Boom Bap",
    "redman": "East Coast",
    "redman & method man": "East Coast",
    "method man & redman": "East Coast",
    "run-d.m.c.": "Old School",
    "run dmc": "Old School",
    "salt-n-pepa": "Old School",
    "mc lyte": "Old School",
    "queen latifah": "East Coast",
    "the sugarhill gang": "Old School",
    "grandmaster flash": "Old School",
    "kurtis blow": "Old School",
    "big daddy kane": "Boom Bap",
    "rakim": "Boom Bap",
    "public enemy": "Boom Bap",
    "n.w.a.": "West Coast",
    "digital underground": "West Coast",
    "shock g": "West Coast",
    "too $hort": "West Coast",
    "mc hammer": "West Coast",
    "hammer": "West Coast",
    "snow tha product": "West Coast",
    "tyga": "West Coast",
    "kid ink": "West Coast",
    "problem": "West Coast",
    "dom kennedy": "West Coast",
    "russ": "East Coast",
    "dave east": "East Coast",
    "don q": "East Coast",
    "young m.a": "East Coast",
    "bobby shmurda": "East Coast",
    "rowdy rebel": "East Coast",
    "max b": "East Coast",
    "lil tjay": "Drill",
    "a boogie wit da hoodie": "East Coast",
    "a boogie": "East Coast",
    "lil mosey": "Trap",
    "nle choppa": "Trap",
    "42 dugg": "Trap",
    "est gee": "Trap",
    "latto": "Trap",
    "city girls": "Trap",
    "jt": "Trap",
    "yung miami": "Trap",
    "trippie redd": "Trap",
    "ski mask the slump god": "Trap",
    "xxxtentacion": "Trap",
    "juice wrld": "Trap",
    "tee grizzley": "Trap",
    "42 dugg": "Trap",
    "big30": "Trap",
    "pooh shiesty": "Trap",
    "morray": "Southern",
    "toosii": "Southern",
    "yung bleu": "Southern",
    "jacquees": "Southern",
    "k camp": "Southern",
    "yfn lucci": "Trap",
    "young scooter": "Trap",
    "peewee longway": "Trap",
    "migos": "Trap",
    "offset": "Trap",
    "quavo": "Trap",
    "takeoff": "Trap",
    "2 chainz": "Trap",
    "ti": "Southern",
    "lil keed": "Trap",
    "lil gotit": "Trap",
    "sahbabii": "Trap",
    "young nudy": "Trap",
    "key!": "Trap",
    "j.i.d.": "Conscious",
    "earthgang": "Conscious",
    "6lack": "Southern",
    "t-pain": "Southern",
    "r. kelly": "Southern",
    "kevin gates": "Southern",
    "boosie": "Southern",
    "the-dream": "Southern",
    "haystack": "Southern",
    "david banner": "Crunk",
    "lil' flip": "Southern",
    "youngbloodz": "Crunk",
}

RNB_ARTIST_MAP = {
    # Contemporary R&B
    "r. kelly": "Contemporary R&B",
    "usher": "Contemporary R&B",
    "chris brown": "Contemporary R&B",
    "trey songz": "Contemporary R&B",
    "ne-yo": "Contemporary R&B",
    "mario": "Contemporary R&B",
    "omarion": "Contemporary R&B",
    "b2k": "Contemporary R&B",
    "ray j": "Contemporary R&B",
    "jagged edge": "Contemporary R&B",
    "joe": "Contemporary R&B",
    "tyrese": "Contemporary R&B",
    "ginuwine": "Contemporary R&B",
    "tank": "Contemporary R&B",
    "avant": "Contemporary R&B",
    "lloyd": "Contemporary R&B",
    "pretty ricky": "Contemporary R&B",
    "jeremih": "Contemporary R&B",
    "jason derulo": "Contemporary R&B",
    "august alsina": "Contemporary R&B",
    "jacquees": "Contemporary R&B",
    "ella mai": "Contemporary R&B",
    "h.e.r.": "Contemporary R&B",
    "summer walker": "Contemporary R&B",
    "sza": "Contemporary R&B",
    "jhené aiko": "Contemporary R&B",
    "jhene aiko": "Contemporary R&B",
    "kehlani": "Contemporary R&B",
    "normani": "Contemporary R&B",
    "chloe x halle": "Contemporary R&B",
    "tinashe": "Contemporary R&B",
    "ari lennox": "Contemporary R&B",
    "lucky daye": "Contemporary R&B",
    "giveon": "Contemporary R&B",
    "brent faiyaz": "Alternative R&B",
    "6lack": "Alternative R&B",
    "bryson tiller": "Contemporary R&B",
    "tory lanez": "Contemporary R&B",
    "ty dolla $ign": "Contemporary R&B",
    "ty dolla sign": "Contemporary R&B",

    # Queens of R&B
    "beyoncé": "Contemporary R&B",
    "beyonce": "Contemporary R&B",
    "mary j. blige": "Contemporary R&B",
    "alicia keys": "Contemporary R&B",
    "keyshia cole": "Contemporary R&B",
    "ciara": "Contemporary R&B",
    "ashanti": "Contemporary R&B",
    "aaliyah": "Contemporary R&B",
    "brandy": "Contemporary R&B",
    "monica": "Contemporary R&B",
    "kelly rowland": "Contemporary R&B",
    "destiny's child": "Contemporary R&B",
    "tlc": "Contemporary R&B",
    "en vogue": "Contemporary R&B",
    "total": "Contemporary R&B",
    "swv": "Contemporary R&B",
    "xscape": "Contemporary R&B",
    "702": "Contemporary R&B",
    "3lw": "Contemporary R&B",
    "mya": "Contemporary R&B",
    "tamia": "Contemporary R&B",
    "deborah cox": "Contemporary R&B",
    "faith evans": "Contemporary R&B",
    "toni braxton": "Contemporary R&B",
    "anita baker": "Contemporary R&B",
    "whitney houston": "Contemporary R&B",

    # Neo-Soul
    "erykah badu": "Neo-Soul",
    "d'angelo": "Neo-Soul",
    "lauryn hill": "Neo-Soul",
    "the fugees": "Neo-Soul",
    "musiq soulchild": "Neo-Soul",
    "musiq": "Neo-Soul",
    "jill scott": "Neo-Soul",
    "india.arie": "Neo-Soul",
    "india arie": "Neo-Soul",
    "floetry": "Neo-Soul",
    "bilal": "Neo-Soul",
    "dwele": "Neo-Soul",
    "raheem devaughn": "Neo-Soul",
    "anthony hamilton": "Neo-Soul",
    "amel larrieux": "Neo-Soul",
    "frank ocean": "Alternative R&B",
    "the weeknd": "Alternative R&B",
    "miguel": "Alternative R&B",
    "solange": "Alternative R&B",

    # New Jack Swing
    "bobby brown": "New Jack Swing",
    "bell biv devoe": "New Jack Swing",
    "new edition": "New Jack Swing",
    "guy": "New Jack Swing",
    "keith sweat": "New Jack Swing",
    "al b. sure!": "New Jack Swing",
    "al b. sure": "New Jack Swing",
    "johnny gill": "New Jack Swing",
    "color me badd": "New Jack Swing",
    "abc": "New Jack Swing",
    "today": "New Jack Swing",
    "jodeci": "New Jack Swing",
    "h-town": "New Jack Swing",
    "shai": "New Jack Swing",
    "silk": "New Jack Swing",
    "dru hill": "New Jack Swing",
    "sisqo": "New Jack Swing",
    "blackstreet": "New Jack Swing",
    "teddy riley": "New Jack Swing",
    "wreckx-n-effect": "New Jack Swing",
    "tevin campbell": "New Jack Swing",

    # Quiet Storm
    "brian mcknight": "Quiet Storm",
    "babyface": "Quiet Storm",
    "luther vandross": "Quiet Storm",
    "maxwell": "Quiet Storm",
    "gerald levert": "Quiet Storm",
    "levert": "Quiet Storm",
    "freddie jackson": "Quiet Storm",
    "james ingram": "Quiet Storm",
    "peabo bryson": "Quiet Storm",
    "jeffrey osborne": "Quiet Storm",
    "howard hewett": "Quiet Storm",
    "el debarge": "Quiet Storm",
    "debarge": "Quiet Storm",
    "alexander o'neal": "Quiet Storm",

    # PBR&B / Alternative R&B
    "the internet": "Alternative R&B",
    "syd": "Alternative R&B",
    "daniel caesar": "Alternative R&B",
    "khalid": "Alternative R&B",
    "jorja smith": "Alternative R&B",
    "snoh aalegra": "Alternative R&B",
    "ravyn lenae": "Alternative R&B",
    "blood orange": "Alternative R&B",
    "sampha": "Alternative R&B",
    "kelela": "Alternative R&B",
    "fka twigs": "Alternative R&B",
    "steve lacy": "Alternative R&B",
    "mac ayres": "Alternative R&B",
    "emotional oranges": "Alternative R&B",
    "pink sweat$": "Alternative R&B",

    # More Contemporary
    "112": "Contemporary R&B",
    "boyz ii men": "Contemporary R&B",
    "r&b": "Contemporary R&B",
    "john legend": "Contemporary R&B",
    "robin thicke": "Contemporary R&B",
    "eric benet": "Contemporary R&B",
    "eric benét": "Contemporary R&B",
    "carl thomas": "Contemporary R&B",
    "case": "Contemporary R&B",
    "donell jones": "Contemporary R&B",
    "next": "Contemporary R&B",
    "montell jordan": "Contemporary R&B",
    "k-ci & jojo": "Contemporary R&B",
    "k. michelle": "Contemporary R&B",
    "tamar braxton": "Contemporary R&B",
    "fantasia": "Contemporary R&B",
    "jennifer hudson": "Contemporary R&B",
    "rihanna": "Contemporary R&B",

    # Additional unmapped R&B artists
    "jaheim": "Contemporary R&B",
    "janet jackson": "Contemporary R&B",
    "akon": "Contemporary R&B",
    "stevie wonder": "Contemporary R&B",
    "marques houston": "Contemporary R&B",
    "the-dream": "Contemporary R&B",
    "the isley brothers": "Contemporary R&B",
    "isley brothers": "Contemporary R&B",
    "aretha franklin": "Contemporary R&B",
    "marvin gaye": "Contemporary R&B",
    "angie stone": "Neo-Soul",
    "prince": "Contemporary R&B",
    "the gap band": "Contemporary R&B",
    "gap band": "Contemporary R&B",
    "bow wow": "Contemporary R&B",
    "bobby v.": "Contemporary R&B",
    "bobby valentino": "Contemporary R&B",
    "bobby v": "Contemporary R&B",
    "leon bridges": "Neo-Soul",
    "keri hilson": "Contemporary R&B",
    "day26": "Contemporary R&B",
    "jamie foxx": "Contemporary R&B",
    "kelly price": "Contemporary R&B",
    "dave hollister": "Contemporary R&B",
    "nivea": "Contemporary R&B",
    "jermaine dupri": "Contemporary R&B",
    "letoya": "Contemporary R&B",
    "letoya luckett": "Contemporary R&B",
    "chrisette michele": "Neo-Soul",
    "pleasure p": "Contemporary R&B",
    "sammie": "Contemporary R&B",
    "teairra mari": "Contemporary R&B",
    "mya": "Contemporary R&B",
    "tamia": "Contemporary R&B",
    "amerie": "Contemporary R&B",
    "sunshine anderson": "Contemporary R&B",
    "musiq soulchild": "Neo-Soul",
    "tweet": "Neo-Soul",
    "vivian green": "Neo-Soul",
    "goapele": "Neo-Soul",
    "corinne bailey rae": "Neo-Soul",
    "amel larrieux": "Neo-Soul",
    "kindred the family soul": "Neo-Soul",
    "kenny lattimore": "Quiet Storm",
    "chanté moore": "Quiet Storm",
    "chante moore": "Quiet Storm",
    "glenn jones": "Quiet Storm",
    "silk": "New Jack Swing",
    "total": "Contemporary R&B",
    "toni braxton": "Contemporary R&B",
    "sza": "Alternative R&B",
    "summer walker": "Alternative R&B",
    "victoria monet": "Contemporary R&B",
    "coco jones": "Contemporary R&B",
    "dvsn": "Alternative R&B",
    "partynextdoor": "Alternative R&B",
    "majid jordan": "Alternative R&B",
}

AFROBEATS_ARTIST_MAP = {
    "burna boy": "Afrofusion",
    "wizkid": "Afropop",
    "davido": "Afropop",
    "mr eazi": "Afropop",
    "tekno": "Afropop",
    "olamide": "Afropop",
    "timaya": "Afropop",
    "flavour": "Highlife",
    "flavour n'abania": "Highlife",
    "yemi alade": "Afropop",
    "tiwa savage": "Afropop",
    "teni": "Afropop",
    "kizz daniel": "Afropop",
    "fireboy dml": "Afropop",
    "rema": "Afropop",
    "ckay": "Afropop",
    "omah lay": "Afrofusion",
    "asake": "Afropop",
    "ayra starr": "Afropop",
    "bnxn": "Afropop",
    "ruger": "Afropop",
    "joeboy": "Afropop",
    "p-square": "Afropop",
    "d'banj": "Afropop",
    "2baba": "Afropop",
    "2face idibia": "Afropop",
    "wande coal": "Afropop",
    "iyanya": "Afropop",
    "sarkodie": "Afropop",
    "stonebwoy": "Afropop",
    "shatta wale": "Afropop",
    "r2bees": "Afropop",
    "maleek berry": "Afropop",
    "juls": "Afropop",
    "nonso amadi": "Afropop",
    "patoranking": "Afropop",
    "simi": "Afropop",
    "adekunle gold": "Highlife",
    "dice ailes": "Afropop",
    "lojay": "Afrofusion",
    "tems": "Afrofusion",
    "amaarae": "Afrofusion",
    "victony": "Afrofusion",
    "fela kuti": "Afrobeat (Classic)",
    "femi kuti": "Afrobeat (Classic)",
    "seun kuti": "Afrobeat (Classic)",
    "made kuti": "Afrobeat (Classic)",
    "tony allen": "Afrobeat (Classic)",
    "antibalas": "Afrobeat (Classic)",
    # Amapiano-adjacent
    "uncle waffles": "Amapiano-Afrobeats",
    "major lazer": "Afrofusion",
    # Coupé-Décalé / Ndombolo
    "dj arafat": "Coupé-Décalé",
    "serge beynaud": "Coupé-Décalé",
    "fally ipupa": "Ndombolo",
    "koffi olomidé": "Ndombolo",
    "koffi olomide": "Ndombolo",
    "awilo longomba": "Ndombolo",
    # Afroswing
    "j hus": "Afroswing",
    "not3s": "Afroswing",
    "nsg": "Afroswing",
    "yxng bane": "Afroswing",
    "kojo funds": "Afroswing",
    "tion wayne": "Afroswing",
}

HOUSE_ARTIST_MAP = {
    # Deep House
    "larry heard": "Deep House",
    "mr. fingers": "Deep House",
    "kerri chandler": "Deep House",
    "ron trent": "Deep House",
    "chez damier": "Deep House",
    "lil louis": "Deep House",
    "moodymann": "Deep House",
    "theo parrish": "Deep House",
    "rick wade": "Deep House",
    "sascha dive": "Deep House",
    "chaos in the cbd": "Deep House",
    "hnny": "Deep House",
    "harvey sutherland": "Deep House",
    "ross from friends": "Deep House",
    "barry can't swim": "Deep House",
    "disclosure": "Deep House",
    "kaytranada": "Deep House",
    "channel tres": "Deep House",

    # Tech House
    "fisher": "Tech House",
    "chris lake": "Tech House",
    "green velvet": "Tech House",
    "patrick topping": "Tech House",
    "solardo": "Tech House",
    "camelphat": "Tech House",

    # Afro House
    "black coffee": "Afro House",
    "culoe de song": "Afro House",
    "caiiro": "Afro House",
    "enoo napa": "Afro House",
    "dele sosimi afrobeat orchestra": "Afro House",

    # Chicago House
    "frankie knuckles": "Chicago House",
    "marshall jefferson": "Chicago House",
    "ron hardy": "Chicago House",
    "jesse saunders": "Chicago House",
    "chip e.": "Chicago House",
    "farley jackmaster funk": "Chicago House",
    "phuture": "Chicago House",
    "dj pierre": "Chicago House",
    "adonis": "Chicago House",
    "jamie principle": "Chicago House",

    # Soulful House
    "louie vega": "Soulful House",
    "masters at work": "Soulful House",
    "kenny dope": "Soulful House",
    "blaze": "Soulful House",
    "joe claussell": "Soulful House",
    "danny krivit": "Soulful House",
    "tony humphries": "Soulful House",
    "larry levan": "Soulful House",

    # Progressive House
    "deadmau5": "Progressive House",
    "eric prydz": "Progressive House",
    "lane 8": "Progressive House",

    # Funky / Jackin House
    "azealia banks": "Funky House",
    "cakes da killa": "Funky House",
    "earth boys": "Funky House",

    # General
    "fred again..": "UK House",
    "fred again": "UK House",
    "justice": "French House",
    "daft punk": "French House",
    "zerb": "Deep House",
    "peggy gou": "Deep House",
    "teuteu": "Deep House",
    "kygo": "Tropical House",
}

POP_ARTIST_MAP = {
    "charli xcx": "Electropop",
    "britney spears": "Dance Pop",
    "rihanna": "Dance Pop",
    "mariah carey": "Pop R&B",
    "justin timberlake": "Dance Pop",
    "beyoncé": "Pop R&B",
    "beyonce": "Pop R&B",
    "lady gaga": "Dance Pop",
    "jennifer lopez": "Dance Pop",
    "destiny's child": "Pop R&B",
    "madonna": "Dance Pop",
    "michael jackson": "Dance Pop",
    "janet jackson": "Dance Pop",
    "danity kane": "Dance Pop",
    "bow wow": "Pop Rap",
    "chris brown": "Pop R&B",
    "the pussycat dolls": "Dance Pop",
    "fergie": "Dance Pop",
    "gwen stefani": "Dance Pop",
    "shakira": "Dance Pop",
    "christina aguilera": "Dance Pop",
    "pink": "Pop Rock",
    "p!nk": "Pop Rock",
    "avril lavigne": "Pop Rock",
    "kelly clarkson": "Pop Rock",
    "dua lipa": "Dance Pop",
    "ariana grande": "Dance Pop",
    "the weeknd": "Synth Pop",
    "billie eilish": "Art Pop",
    "lorde": "Art Pop",
    "lana del rey": "Art Pop",
    "taylor swift": "Synth Pop",
    "lizzo": "Dance Pop",
    "doja cat": "Dance Pop",
    "olivia rodrigo": "Pop Rock",
    "sabrina carpenter": "Dance Pop",
    "chappell roan": "Synth Pop",

    # Additional unmapped Pop artists
    "katy perry": "Dance Pop",
    "mary j. blige": "Pop R&B",
    "*nsync": "Dance Pop",
    "nsync": "Dance Pop",
    "brandy": "Pop R&B",
    "ashlee simpson": "Pop Rock",
    "the marías": "Indie Pop",
    "the marias": "Indie Pop",
    "the black eyed peas": "Dance Pop",
    "steve lacy": "Indie Pop",
    "miley cyrus": "Dance Pop",
    "jason derulo": "Dance Pop",
    "ke$ha": "Dance Pop",
    "kesha": "Dance Pop",
    "spice girls": "Dance Pop",
    "stevie wonder": "Pop R&B",
    "maroon 5": "Pop Rock",
    "sophie": "Art Pop",
    "usher": "Pop R&B",
    "craig david": "Pop R&B",
    "sean paul": "Dance Pop",
    "jonas brothers": "Pop Rock",
    "whitney houston": "Pop R&B",
    "backstreet boys": "Dance Pop",
    "b2k": "Pop R&B",
    "boyz ii men": "Pop R&B",
    "98 degrees": "Dance Pop",
    "o-town": "Dance Pop",
    "dream": "Dance Pop",
    "3lw": "Pop R&B",
    "b5": "Pop R&B",
    "lloyd": "Pop R&B",
    "nelly": "Pop Rap",
    "ciara": "Pop R&B",
    "ashanti": "Pop R&B",
    "akon": "Pop Rap",
    "ne-yo": "Pop R&B",
    "chris brown": "Pop R&B",
    "trey songz": "Pop R&B",
    "omarion": "Pop R&B",
    "mario": "Pop R&B",
    "alicia keys": "Pop R&B",
    "john legend": "Pop R&B",
    "selena gomez": "Dance Pop",
    "camila cabello": "Dance Pop",
    "cardi b": "Pop Rap",
    "megan thee stallion": "Pop Rap",
    "lizzo": "Dance Pop",
    "harry styles": "Synth Pop",
    "bad bunny": "Dance Pop",
    "the 1975": "Synth Pop",
    "tame impala": "Indie Pop",
    "mgmt": "Indie Pop",
    "vampire weekend": "Indie Pop",
    "clairo": "Indie Pop",
    "phoebe bridgers": "Indie Pop",
    "king princess": "Indie Pop",
    "troye sivan": "Synth Pop",
    "sam smith": "Dance Pop",
    "adele": "Pop Ballad",
    "ed sheeran": "Pop Ballad",
    "bruno mars": "Dance Pop",
    "silk sonic": "Pop R&B",
    "the weeknd": "Synth Pop",
    "sza": "Pop R&B",
    "three 6 mafia": "Pop Rap",
    "key!": "Pop Rap",
    "davido": "Pop R&B",
}

DANCE_ARTIST_MAP = {
    "david guetta": "EDM",
    "tiësto": "EDM",
    "tiesto": "EDM",
    "calvin harris": "EDM",
    "swedish house mafia": "EDM",
    "avicii": "EDM",
    "martin garrix": "EDM",
    "marshmello": "EDM",
    "the chainsmokers": "EDM",
    "skrillex": "EDM",
    "diplo": "EDM",
    "major lazer": "EDM",
    "daft punk": "Electronica",
    "the chemical brothers": "Electronica",
    "the prodigy": "Electronica",
    "fatboy slim": "Electronica",
    "kaytranada": "Electronica",
    "gesaffelstein": "Electronica",
    "justice": "Electronica",
    "charli xcx": "Electropop",
    "shygirl": "Electropop",
    "sophie": "Electropop",
    "ag cook": "Electropop",
    "peggy gou": "Electronica",
    "whitney houston": "Hi-NRG",
    "jennifer hudson": "Hi-NRG",
    "christina aguilera": "Hi-NRG",
    "destiny's child": "Hi-NRG",
    "vjuan allure": "Ballroom",
    "rihanna": "Dance Pop",
    "deadmau5": "EDM",
    "tove lo": "Electropop",
    "romy": "Electropop",
    "toro y moi": "Electronica",
    "fuse odg": "EDM",
    "moby": "Electronica",
    "axwell": "EDM",
    "kaskade": "EDM",
    "dj snake": "EDM",
    "mike posner": "EDM",
    "morgan page": "EDM",
    "machine girl": "Electronica",
    "confidence man": "Electronica",
    "sg lewis": "UK Dance",
    "jungle": "UK Dance",
    "bicep": "UK Dance",
    "nia archives": "UK Dance",
    "mv bill": "Electronica",
    "snow strippers": "Electropop",
    "fred again..": "UK Dance",
    "fred again": "UK Dance",
    "disclosure": "UK Dance",
    "mura masa": "UK Dance",
    "jamie xx": "UK Dance",
    "four tet": "Electronica",
    "caribou": "Electronica",
    "flume": "Electronica",
    "odesza": "Electronica",
    "rüfüs du sol": "Electronica",
    "bonobo": "Electronica",
}

SOUL_ARTIST_MAP = {
    "aretha franklin": "Classic Soul",
    "marvin gaye": "Classic Soul",
    "stevie wonder": "Classic Soul",
    "otis redding": "Classic Soul",
    "sam cooke": "Classic Soul",
    "ray charles": "Classic Soul",
    "james brown": "Classic Soul",
    "al green": "Classic Soul",
    "curtis mayfield": "Classic Soul",
    "the temptations": "Classic Soul",
    "the four tops": "Classic Soul",
    "four tops": "Classic Soul",
    "the supremes": "Classic Soul",
    "smokey robinson": "Classic Soul",
    "the isley brothers": "Classic Soul",
    "isley brothers": "Classic Soul",
    "earth, wind & fire": "Classic Soul",
    "earth wind & fire": "Classic Soul",
    "kool & the gang": "Classic Soul",
    "the commodores": "Classic Soul",
    "commodores": "Classic Soul",
    "the stylistics": "Philly Soul",
    "the o'jays": "Philly Soul",
    "harold melvin & the blue notes": "Philly Soul",
    "teddy pendergrass": "Philly Soul",
    "the delfonics": "Philly Soul",
    "the spinners": "Philly Soul",
    "billy paul": "Philly Soul",
    "d'angelo": "Neo-Soul",
    "erykah badu": "Neo-Soul",
    "angie stone": "Neo-Soul",
    "eric benet": "Neo-Soul",
    "eric benét": "Neo-Soul",
    "lucy pearl": "Neo-Soul",
    "prince": "Psychedelic Soul",
    "sly & the family stone": "Psychedelic Soul",
    "parliament": "Psychedelic Soul",
    "funkadelic": "Psychedelic Soul",
    "george clinton": "Psychedelic Soul",
    "bootsy collins": "Psychedelic Soul",
    "lakeside": "Funk",
    "fatback band": "Funk",
    "rick james": "Funk",
    "cameo": "Funk",
    "the gap band": "Funk",
    "gap band": "Funk",
    "zapp": "Funk",
    "roger": "Funk",
    "gabriel & dresden": "Deep House",
    "carl thomas": "Neo-Soul",
}

ROCK_ARTIST_MAP = {
    "fall out boy": "Pop Punk",
    "blink-182": "Pop Punk",
    "my chemical romance": "Emo",
    "coldplay": "Alternative",
    "tracy chapman": "Folk Rock",
    "fleetwood mac": "Classic Rock",
    "limp bizkit": "Nu Metal",
    "the fray": "Alternative",
    "billy ocean": "Pop Rock",
    "buddy holly": "Classic Rock",
    "belly": "Alternative",
    "bootsy collins": "Funk Rock",
    "mary j. blige": "Pop Rock",
    "brandy": "Pop Rock",
    "mustard": "Pop Rock",
    "red hot chili peppers": "Alternative",
    "nirvana": "Grunge",
    "pearl jam": "Grunge",
    "foo fighters": "Alternative",
    "radiohead": "Alternative",
    "u2": "Classic Rock",
    "the rolling stones": "Classic Rock",
    "led zeppelin": "Classic Rock",
    "the beatles": "Classic Rock",
    "queen": "Classic Rock",
    "pink floyd": "Psychedelic",
    "jimi hendrix": "Psychedelic",
    "green day": "Pop Punk",
    "paramore": "Pop Punk",
    "linkin park": "Nu Metal",
}

REGGAE_ARTIST_MAP = {
    "bob marley": "Roots Reggae",
    "bob marley & the wailers": "Roots Reggae",
    "peter tosh": "Roots Reggae",
    "bunny wailer": "Roots Reggae",
    "dennis brown": "Roots Reggae",
    "burning spear": "Roots Reggae",
    "gregory isaacs": "Lovers Rock",
    "beres hammond": "Lovers Rock",
    "sanchez": "Lovers Rock",
    "maxi priest": "Lovers Rock",
    "freddie mcgregor": "Lovers Rock",
    "barrington levy": "Roots Reggae",
    "lee scratch perry": "Dub",
    "lee 'scratch' perry": "Dub",
    "king tubby": "Dub",
    "augustus pablo": "Dub",
    "scientist": "Dub",
    "mad professor": "Dub",
    "sizzla": "Roots Reggae",
    "capleton": "Roots Reggae",
    "luciano": "Roots Reggae",
    "damian marley": "Roots Reggae",
    "stephen marley": "Roots Reggae",
    "chronixx": "Roots Reggae",
    "protoje": "Roots Reggae",
    "shaggy": "Ragga",
    "sean paul": "Ragga",
    "shabba ranks": "Ragga",
    "super cat": "Ragga",
    "buju banton": "Ragga",
    "mr. vegas": "Ragga",
    "wayne wonder": "Lovers Rock",
}

JAZZ_ARTIST_MAP = {
    "miles davis": "Cool Jazz",
    "john coltrane": "Bebop",
    "charlie parker": "Bebop",
    "thelonious monk": "Bebop",
    "duke ellington": "Classic Jazz",
    "louis armstrong": "Classic Jazz",
    "herbie hancock": "Jazz Fusion",
    "chick corea": "Jazz Fusion",
    "weather report": "Jazz Fusion",
    "pat metheny": "Jazz Fusion",
    "kenny g": "Smooth Jazz",
    "george benson": "Smooth Jazz",
    "grover washington jr.": "Smooth Jazz",
    "bob james": "Smooth Jazz",
    "david sanborn": "Smooth Jazz",
    "sade": "Smooth Jazz",
    "norah jones": "Smooth Jazz",
    "robert glasper": "Jazz Fusion",
    "kamasi washington": "Jazz Fusion",
    "thundercat": "Jazz Fusion",
    "roy ayers": "Acid Jazz",
    "brand new heavies": "Acid Jazz",
    "jamiroquai": "Acid Jazz",
    "incognito": "Acid Jazz",
    "us3": "Acid Jazz",
}

DISCO_ARTIST_MAP = {
    "donna summer": "Classic Disco",
    "bee gees": "Classic Disco",
    "chic": "Classic Disco",
    "nile rodgers": "Classic Disco",
    "gloria gaynor": "Classic Disco",
    "kool & the gang": "Classic Disco",
    "earth, wind & fire": "Classic Disco",
    "sister sledge": "Classic Disco",
    "the trammps": "Classic Disco",
    "village people": "Classic Disco",
    "diana ross": "Classic Disco",
    "michael jackson": "Classic Disco",
    "daft punk": "Nu-Disco",
    "todd terje": "Nu-Disco",
    "lindstrøm": "Nu-Disco",
    "horse meat disco": "Nu-Disco",
}

# Master lookup: genre → artist map
GENRE_ARTIST_MAPS = {
    "Hip-Hop:Rap": HIPHOP_ARTIST_MAP,
    "R&B": RNB_ARTIST_MAP,
    "Afrobeats": AFROBEATS_ARTIST_MAP,
    "House": HOUSE_ARTIST_MAP,
    "Pop": POP_ARTIST_MAP,
    "Dance": DANCE_ARTIST_MAP,
    "Soul": SOUL_ARTIST_MAP,
    "Rock": ROCK_ARTIST_MAP,
    "Reggae": REGGAE_ARTIST_MAP,
    "Jazz": JAZZ_ARTIST_MAP,
    "Disco": DISCO_ARTIST_MAP,
}

# Decade-based subgenre hints for Hip-Hop when artist isn't mapped
HIPHOP_DECADE_DEFAULTS = {
    "1970s": "Old School",
    "1980s": "Old School",
    "1990s": "Golden Age",
    "2000s": "Bling Era",
    "2010s": "Trap",
    "2020s": "Trap",
}

# Genre tag to subgenre mapping (when ID3 genre tag contains useful info)
GENRE_TAG_SUBGENRE_MAP = {
    # Hip-Hop subgenres from tags
    "trap": "Trap",
    "trap music": "Trap",
    "southern hip hop": "Southern",
    "gangsta rap": "Gangsta",
    "east coast hip hop": "East Coast",
    "west coast hip hop": "West Coast",
    "conscious hip hop": "Conscious",
    "underground hip hop": "Conscious",
    "boom bap": "Boom Bap",
    "drill": "Drill",
    "crunk": "Crunk",
    "g-funk": "G-Funk",
    "cloud rap": "Cloud Rap",
    "mumble rap": "Trap",
    # R&B subgenres
    "neo-soul": "Neo-Soul",
    "neo soul": "Neo-Soul",
    "new jack swing": "New Jack Swing",
    "quiet storm": "Quiet Storm",
    "contemporary r&b": "Contemporary R&B",
    "alternative r&b": "Alternative R&B",
    "pbr&b": "Alternative R&B",
    # House subgenres
    "deep house": "Deep House",
    "tech house": "Tech House",
    "progressive house": "Progressive House",
    "afro house": "Afro House",
    "soulful house": "Soulful House",
    "chicago house": "Chicago House",
    "acid house": "Acid House",
    "tropical house": "Tropical House",
    "funky house": "Funky House",
    "french house": "French House",
    # Other
    "edm": "EDM",
    "electronica": "Electronica",
    "synthwave": "Synthwave",
}


def normalize_artist(artist: str) -> str:
    """Normalize artist name for lookup."""
    if not artist:
        return ""
    # Take the first artist if multiple (before feat/ft/&/x/,)
    a = artist.lower().strip()
    # Remove leading track numbers like "004 - "
    a = re.sub(r"^\d+\s*[-–]\s*", "", a)
    # Split on common separators for featuring artists
    for sep in [" feat.", " feat ", " ft.", " ft ", " featuring ", " x ", " & ", ", "]:
        a = a.split(sep)[0]
    return a.strip()


def classify_track(track: dict) -> str:
    """Determine the subgenre for a track. Returns subgenre string."""
    genre = track["current_genre"]

    # 1. If already in a subgenre folder, keep it (but skip decade-like names)
    sfp = track.get("subgenre_from_path") or ""
    if sfp and not re.match(r"^\d{2}'s$", sfp):  # Skip "00's" etc.
        return sfp

    # 2. Check ID3 genre tag for subgenre hints
    genre_tag = (track.get("genre_tag") or "").lower().strip()
    for tag_key, subgenre in GENRE_TAG_SUBGENRE_MAP.items():
        if tag_key in genre_tag:
            return subgenre

    # 3. Artist-based classification
    artist_map = GENRE_ARTIST_MAPS.get(genre, {})
    if artist_map:
        # Try primary artist
        primary = normalize_artist(track.get("artist") or "")
        if primary in artist_map:
            return artist_map[primary]

        # Try album artist
        album_artist = normalize_artist(track.get("album_artist") or "")
        if album_artist in artist_map:
            return artist_map[album_artist]

        # Try from filename (format: "NNN - Artist - Title.mp3")
        fname = track.get("filename", "")
        m = re.match(r"^\d+\s*[-–]\s*(.+?)(?:\s*[-–]\s*.+)?\.mp3$", fname, re.IGNORECASE)
        if m:
            fname_artist = m.group(1).lower().strip()
            if fname_artist in artist_map:
                return artist_map[fname_artist]

    # 4. Decade-based default for Hip-Hop
    if genre == "Hip-Hop:Rap" and track.get("decade"):
        default = HIPHOP_DECADE_DEFAULTS.get(track["decade"])
        if default:
            return default

    # 5. Genre-specific defaults
    genre_defaults = {
        "Hip-Hop:Rap": "General Hip-Hop",
        "R&B": "General R&B",
        "Pop": "General Pop",
        "Rock": "General Rock",
        "House": "General House",
        "Dance": "General Dance",
        "Soul": "General Soul",
        "Jazz": "General Jazz",
        "Reggae": "General Reggae",
        "Afrobeats": "General Afrobeats",
        "Disco": "General Disco",
        "Dancehall": "General Dancehall",
        "Latin": "General Latin",
        "Techno": "General Techno",
        "Trance": "General Trance",
        "Country": "General Country",
        "Classical": "General Classical",
        "Gospel": "General Gospel",
        "Christian": "General Christian",
        "Christmas": "General Christmas",
        "Lo-Fi": "General Lo-Fi",
        "UK Music": "General UK Music",
        "UK Funky": "General UK Funky",
        "Baltimore Club": "General Baltimore Club",
        "Jersey Club": "General Jersey Club",
        "Soca": "General Soca",
        "Amapiano": "General Amapiano",
        "Jungle": "General Jungle",
        "Reggaeton": "General Reggaeton",
        "Breakbeat": "General Breakbeat",
        "Dubstep": "General Dubstep",
        "Bassline": "General Bassline",
        "Drum & Bass": "General Drum & Bass",
        "Motown": "General Motown",
        "Garage": "General Garage",
        "Baile Funk": "General Baile Funk",
        "No Genre": "Unclassified",
        "Unknown Genre": "Unclassified",
        "Alternative": "General Alternative",
        "Bhangra": "General Bhangra",
        "Bollywood": "General Bollywood",
        "Lounge": "General Lounge",
    }

    return genre_defaults.get(genre, "Unclassified")


def main():
    print("Loading manifest...")
    with open(MANIFEST) as f:
        tracks = json.load(f)

    print(f"Classifying {len(tracks)} tracks...")

    classified = []
    subgenre_counts = {}

    for track in tracks:
        subgenre = classify_track(track)
        track["proposed_subgenre"] = subgenre

        key = f"{track['current_genre']} → {subgenre}"
        subgenre_counts[key] = subgenre_counts.get(key, 0) + 1

        classified.append(track)

    # Save full classification JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump(classified, f, indent=2, ensure_ascii=False)

    # Save review CSV
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "current_path", "artist", "title", "current_genre",
            "year", "decade", "proposed_subgenre", "classification_source"
        ])
        for t in classified:
            # Determine classification source
            source = "default"
            if t.get("subgenre_from_path"):
                source = "existing_folder"
            elif any(k in (t.get("genre_tag") or "").lower() for k in GENRE_TAG_SUBGENRE_MAP):
                source = "id3_tag"
            elif normalize_artist(t.get("artist") or "") in GENRE_ARTIST_MAPS.get(t["current_genre"], {}):
                source = "artist_map"
            elif normalize_artist(t.get("album_artist") or "") in GENRE_ARTIST_MAPS.get(t["current_genre"], {}):
                source = "artist_map"
            elif t["current_genre"] == "Hip-Hop:Rap" and t.get("decade") in HIPHOP_DECADE_DEFAULTS:
                source = "decade_default"

            writer.writerow([
                t["file_path"],
                t.get("artist", ""),
                t.get("title", ""),
                t["current_genre"],
                t.get("year_from_path", ""),
                t.get("decade", ""),
                t["proposed_subgenre"],
                source,
            ])

    # Print summary
    print(f"\n--- Classification Summary ---")
    print(f"Total tracks classified: {len(classified)}")

    # Group by genre
    by_genre = {}
    for key, count in sorted(subgenre_counts.items()):
        genre = key.split(" → ")[0]
        subgenre = key.split(" → ")[1]
        if genre not in by_genre:
            by_genre[genre] = {}
        by_genre[genre][subgenre] = count

    for genre in sorted(by_genre.keys()):
        print(f"\n{genre}:")
        for sub, count in sorted(by_genre[genre].items(), key=lambda x: -x[1]):
            print(f"  {sub}: {count}")

    # Count by source
    source_counts = {"existing_folder": 0, "id3_tag": 0, "artist_map": 0, "decade_default": 0, "default": 0}
    for t in classified:
        if t.get("subgenre_from_path"):
            source_counts["existing_folder"] += 1
        elif any(k in (t.get("genre_tag") or "").lower() for k in GENRE_TAG_SUBGENRE_MAP):
            source_counts["id3_tag"] += 1
        elif normalize_artist(t.get("artist") or "") in GENRE_ARTIST_MAPS.get(t["current_genre"], {}):
            source_counts["artist_map"] += 1
        elif normalize_artist(t.get("album_artist") or "") in GENRE_ARTIST_MAPS.get(t["current_genre"], {}):
            source_counts["artist_map"] += 1
        elif t["current_genre"] == "Hip-Hop:Rap" and t.get("decade") in HIPHOP_DECADE_DEFAULTS:
            source_counts["decade_default"] += 1
        else:
            source_counts["default"] += 1

    print(f"\n--- Classification Sources ---")
    for src, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        pct = count / len(classified) * 100
        print(f"  {src}: {count} ({pct:.1f}%)")

    print(f"\nClassification saved to:")
    print(f"  JSON: {OUTPUT_JSON}")
    print(f"  CSV:  {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
