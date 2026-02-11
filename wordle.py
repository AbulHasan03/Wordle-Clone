from flask import Flask, render_template, jsonify, request
from datetime import datetime
import random

app = Flask(__name__)

# List of 5-letter words for daily answers (curated common words)
WORD_LIST = [
    "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult", "after", "again",
    "agent", "agree", "ahead", "alarm", "album", "alert", "align", "alive", "allow", "alone",
    "along", "alter", "among", "anger", "angle", "angry", "apart", "apple", "apply", "arena",
    "argue", "arise", "array", "aside", "asset", "audio", "avoid", "award", "aware", "badly",
    "baker", "bases", "basic", "basis", "beach", "began", "begin", "being", "below", "bench",
    "billy", "birth", "black", "blame", "blind", "block", "blood", "board", "boost", "booth",
    "bound", "brain", "brand", "bread", "break", "breed", "brief", "bring", "broad", "broke",
    "brown", "build", "built", "buyer", "cable", "calif", "carry", "catch", "cause", "chain",
    "chair", "chart", "chase", "cheap", "check", "chest", "chief", "child", "china", "chose",
    "civil", "claim", "class", "clean", "clear", "click", "clock", "close", "coach", "coast",
    "could", "count", "court", "cover", "crack", "craft", "crash", "crazy", "cream", "crime",
    "cross", "crowd", "crown", "crude", "cycle", "daily", "dance", "dated", "dealt", "death",
    "debut", "delay", "depth", "doing", "doubt", "dozen", "draft", "drama", "drank", "drawn",
    "dream", "dress", "drill", "drink", "drive", "drove", "dying", "eager", "early", "earth",
    "eight", "elite", "empty", "enemy", "enjoy", "enter", "entry", "equal", "error", "event",
    "every", "exact", "exist", "extra", "faith", "false", "fault", "fiber", "field", "fifth",
    "fifty", "fight", "final", "first", "fixed", "flash", "fleet", "floor", "fluid", "focus",
    "force", "forth", "forty", "forum", "found", "frame", "frank", "fraud", "fresh", "front",
    "fruit", "fully", "funny", "giant", "given", "glass", "globe", "going", "grace", "grade",
    "grand", "grant", "grass", "great", "green", "gross", "group", "grown", "guard", "guess",
    "guest", "guide", "happy", "harry", "heart", "heavy", "hence", "henry", "horse", "hotel",
    "house", "human", "ideal", "image", "index", "inner", "input", "issue", "japan", "jimmy",
    "joint", "jones", "judge", "known", "label", "large", "laser", "later", "laugh", "layer",
    "learn", "lease", "least", "leave", "legal", "lemon", "level", "lewis", "light", "limit",
    "links", "lives", "local", "logic", "loose", "lower", "lucky", "lunch", "lying", "magic",
    "major", "maker", "march", "maria", "match", "maybe", "mayor", "meant", "media", "metal",
    "might", "minor", "minus", "mixed", "model", "money", "month", "moral", "motor", "mount",
    "mouse", "mouth", "movie", "music", "needs", "never", "newly", "night", "noise", "north",
    "noted", "novel", "nurse", "occur", "ocean", "offer", "often", "order", "other", "ought",
    "paint", "panel", "paper", "party", "peace", "peter", "phase", "phone", "photo", "piece",
    "pilot", "pitch", "place", "plain", "plane", "plant", "plate", "point", "pound", "power",
    "press", "price", "pride", "prime", "print", "prior", "prize", "proof", "proud", "prove",
    "queen", "quick", "quiet", "quite", "radio", "raise", "range", "rapid", "ratio", "reach",
    "ready", "refer", "right", "rival", "river", "robin", "roger", "roman", "rough", "round",
    "route", "royal", "rural", "scale", "scene", "scope", "score", "sense", "serve", "seven",
    "shall", "shape", "share", "sharp", "sheet", "shelf", "shell", "shift", "shine", "shirt",
    "shock", "shoot", "short", "shown", "sight", "since", "sixth", "sixty", "sized", "skill",
    "sleep", "slide", "small", "smart", "smile", "smith", "smoke", "solid", "solve", "sorry",
    "sound", "south", "space", "spare", "speak", "speed", "spend", "spent", "split", "spoke",
    "sport", "staff", "stage", "stake", "stand", "start", "state", "steam", "steel", "stick",
    "still", "stock", "stone", "stood", "store", "storm", "story", "strip", "stuck", "study",
    "stuff", "style", "sugar", "suite", "super", "sweet", "table", "taken", "taste", "taxes",
    "teach", "teeth", "terry", "texas", "thank", "theft", "their", "theme", "there", "these",
    "thick", "thing", "think", "third", "those", "three", "threw", "throw", "tight", "times",
    "title", "today", "topic", "total", "touch", "tough", "tower", "track", "trade", "trail",
    "train", "trait", "treat", "trend", "trial", "tribe", "trick", "tried", "tries", "troop",
    "truck", "truly", "trust", "truth", "twice", "under", "undue", "union", "unity", "until",
    "upper", "upset", "urban", "usage", "usual", "valid", "value", "video", "virus", "visit",
    "vital", "vocal", "voice", "waste", "watch", "water", "wheel", "where", "which", "while",
    "white", "whole", "whose", "woman", "women", "world", "worry", "worse", "worst", "worth",
    "would", "wound", "write", "wrong", "wrote", "young", "youth"
]

# Expanded list of valid 5-letter words for guessing
# This allows players to use common words to narrow down the answer
VALID_GUESSES = set(WORD_LIST + [
    "aback", "abase", "abate", "abbey", "abbot", "abhor", "abide", "abode", "abort", "abound",
    "abuse", "abyss", "acorn", "acres", "actor", "acute", "adept", "admin", "admire", "adobe",
    "adopt", "adore", "adorn", "adult", "after", "again", "agent", "agile", "aging", "agony",
    "agree", "ahead", "aisle", "alarm", "album", "alert", "algae", "alibi", "alien", "align",
    "alike", "alive", "alley", "alloy", "allow", "alloy", "alone", "along", "aloof", "aloud",
    "alpha", "altar", "alter", "amber", "amble", "amend", "amino", "amiss", "amaze", "among",
    "ample", "amply", "amuse", "angel", "anger", "angle", "angry", "angst", "ankle", "annex",
    "annoy", "antic", "anvil", "aorta", "apart", "aphid", "apnea", "apple", "apply", "apron",
    "arbor", "arcane", "arena", "argue", "arise", "armed", "armor", "aroma", "arose", "array",
    "arrow", "arson", "артек", "ascot", "ashen", "ashes", "aside", "askew", "aspen", "assay",
    "asset", "atlas", "atoll", "atone", "attic", "audio", "audit", "augur", "auntinch", "aura",
    "aural", "auto", "avail", "avert", "avian", "avoid", "awake", "award", "aware", "awash",
    "awful", "awoke", "axial", "axiom", "axion", "azure", "badge", "badly", "bagel", "baker",
    "balmy", "banal", "banjo", "barge", "baron", "basal", "baste", "batch", "baton", "bayou",
    "beach", "beads", "beady", "beard", "beast", "began", "begat", "begin", "begun", "being",
    "belch", "belie", "belle", "belly", "below", "bench", "beret", "berry", "berth", "beset",
    "bevel", "beware", "beyond", "bidding", "biker", "bilge", "binge", "bingo", "biome", "birch",
    "birth", "bison", "black", "blade", "blame", "bland", "blank", "blare", "blast", "blaze",
    "bleak", "bleat", "bleed", "blend", "bless", "blimp", "blind", "blink", "bliss", "blitz",
    "bloat", "block", "bloke", "blond", "blood", "bloom", "blown", "bluer", "blues", "bluff",
    "blunt", "blurb", "blurt", "blush", "board", "boast", "bobby", "boney", "bonus", "booby",
    "boost", "booth", "booty", "booze", "boozy", "borax", "botch", "bough", "bound", "bowel",
    "boxer", "brace", "braid", "brain", "brake", "brand", "brash", "brass", "brave", "bravo",
    "brawl", "brawn", "bread", "break", "breed", "briar", "bribe", "brick", "bride", "brief",
    "brine", "bring", "brink", "briny", "brisk", "broad", "broil", "broke", "brook", "broom",
    "broth", "brown", "brunt", "brush", "brute", "buddy", "budge", "buggy", "build", "built",
    "bulge", "bulky", "bully", "bumpy", "bunch", "bunny", "buoyburglary", "burly", "burnt", "burst",
    "bused", "bushy", "butch", "butte", "buxom", "buyer", "bylaw", "cabal", "cabin", "cable",
    "cacao", "cache", "cacti", "cadet", "cadre", "caféaker", "camel", "cameo", "campo", "canal",
    "candy", "canny", "canoe", "canon", "caper", "caput", "carat", "cargo", "carol", "carry",
    "carve", "caste", "catch", "cater", "catty", "caulk", "cause", "cavil", "cease", "cedar",
    "cello", "chafe", "chaff", "chain", "chair", "chalk", "champ", "chant", "chaos", "chard",
    "charm", "chart", "chase", "chasm", "cheap", "cheat", "check", "cheek", "cheer", "chess",
    "chest", "chick", "chief", "child", "chile", "chili", "chill", "chimp", "china", "chirp",
    "chive", "chock", "choir", "choke", "chomp", "chord", "chore", "chose", "chunk", "churn",
    "chute", "cider", "cigar", "cinch", "circa", "civic", "civil", "clack", "claim", "clamp",
    "clang", "clank", "clash", "clasp", "class", "clave", "clean", "clear", "cleat", "cleft",
    "clerk", "click", "cliff", "climb", "cling", "clink", "cloak", "clock", "clone", "close",
    "cloth", "cloud", "clout", "clove", "clown", "cluck", "clued", "clump", "clung", "clunk",
    "coach", "coast", "cobra", "cocoa", "colon", "color", "comet", "comic", "comma", "conch",
    "condo", "coral", "corny", "couch", "cough", "could", "count", "coupe", "court", "coven",
    "cover", "covet", "cower", "crack", "craft", "cramp", "crane", "crank", "crash", "crass",
    "crate", "crave", "crawl", "craze", "crazy", "creak", "cream", "crease", "create", "creed",
    "creek", "creep", "creme", "crepe", "crept", "cress", "crest", "crick", "cried", "crier",
    "crime", "crimp", "crisp", "croak", "crock", "crook", "croon", "cross", "croup", "crowd",
    "crown", "crude", "cruel", "cruet", "crumb", "crunk", "crush", "crust", "crypt", "cubic",
    "cumin", "cupid", "curb", "cured", "curly", "curry", "curse", "curve", "cushy", "cutie",
    "cycle", "cynic", "daddy", "daily", "dairy", "daisy", "dally", "dance", "dandy", "dated",
    "datum", "daunt", "dealt", "death", "debar", "debit", "debug", "debut", "decaf", "decay",
    "decor", "decoy", "decry", "deity", "delay", "delta", "delve", "demon", "demur", "denim",
    "dense", "depot", "depth", "derby", "deter", "detox", "deuce", "devil", "diary", "dicey",
    "diety", "digit", "dilly", "dimly", "diner", "dingo", "dingy", "diode", "dirge", "dirty",
    "disco", "ditch", "ditto", "ditty", "diver", "dizzy", "dodge", "dodgy", "dogma", "doing",
    "dolly", "dolor", "donor", "donut", "dopey", "doubt", "dough", "dowdy", "dowel", "down",
    "downy", "dowry", "dozen", "draft", "drain", "drake", "drama", "drank", "drape", "drawl",
    "drawn", "dread", "dream", "drear", "dregs", "dress", "dried", "drier", "drift", "drill",
    "drink", "drive", "droit", "droll", "drone", "drool", "droop", "dross", "drove", "drown",
    "druid", "drunk", "dryer", "dryly", "duchy", "ducky", "dummy", "dumpy", "dunce", "dusky",
    "dusty", "duvet", "dwarf", "dwell", "dwelt", "dying", "eager", "eagle", "early", "earth",
    "easel", "eaten", "eater", "ebony", "eclat", "edict", "edify", "eerie", "egret", "eight",
    "eject", "eking", "elate", "elbow", "elder", "elect", "elegy", "elfin", "elide", "elite",
    "elope", "elude", "elute", "elves", "email", "embed", "ember", "emcee", "emend", "emery",
    "emits", "empty", "enact", "endow", "enema", "enemy", "enjoy", "ennui", "ensue", "enter",
    "entry", "envoy", "epoch", "epoxy", "equal", "equip", "erase", "erect", "erode", "error",
    "erupt", "essay", "ester", "ether", "ethic", "ethos", "evade", "evens", "event", "every",
    "evict", "evoke", "exact", "exalt", "excel", "exert", "exile", "exist", "exorcexpat",
    "expel", "extol", "extra", "exude", "exult", "eying", "fable", "facet", "faint", "fairy",
    "faith", "faker", "falls", "false", "fancy", "fanny", "farce", "fatal", "fatty", "fault",
    "fauna", "favor", "feast", "fecal", "feign", "faint", "felon", "femme", "femur", "fence",
    "feral", "ferry", "fetal", "fetch", "fetid", "fetus", "fever", "fewer", "fiber", "ficus",
    "field", "fiend", "fiery", "fifth", "fifty", "fight", "filch", "filet", "filly", "filth",
    "filmy", "final", "finch", "finer", "finicky", "finite", "fiord", "fired", "first", "fishy",
    "fixer", "fizzy", "fjord", "flack", "flail", "flair", "flake", "flaky", "flame", "flank",
    "flare", "flash", "flask", "fleck", "fleet", "flesh", "flick", "flier", "fling", "flint",
    "flirt", "float", "flock", "flood", "floor", "flora", "floss", "flour", "flout", "flown",
    "fluff", "fluid", "fluke", "flung", "flunk", "flush", "flute", "foamy", "focal", "focus",
    "foggy", "foist", "folio", "folly", "fondu", "forceford", "forgo", "forte", "forth", "forty",
    "forum", "found", "foyer", "frail", "frame", "frank", "fraud", "freak", "freed", "freer",
    "fresh", "friar", "fried", "frill", "frisk", "fritz", "frock", "frond", "front", "frost",
    "froth", "frown", "froze", "fruit", "fudge", "fugue", "fully", "fumed", "fungi", "funky",
    "funny", "furry", "fussy", "fusty", "futon", "fuzzy", "gaily", "gamer", "gamma", "gamut",
    "gassy", "gaudy", "gauge", "gaunt", "gauze", "gavel", "gawk", "gazer", "gecko", "geese",
    "geeky", "genre", "ghost", "ghoul", "giant", "giddy", "given", "giver", "glade", "gland",
    "glare", "glass", "glaze", "gleam", "glean", "glide", "glint", "glitz", "gloat", "globe",
    "gloom", "glory", "gloss", "glove", "gnash", "gnome", "godly", "going", "golly", "gonad",
    "goner", "gonna", "goose", "gorge", "gouge", "gourd", "grace", "grade", "craft", "grain",
    "grand", "grant", "grape", "graph", "grasp", "grass", "grate", "grave", "gravy", "graze",
    "great", "greed", "greek", "green", "greet", "grief", "grill", "grime", "grimy", "grind",
    "gripe", "groan", "groin", "groom", "grope", "gross", "group", "grout", "grove", "growl",
    "grown", "gruel", "gruff", "grunt", "guano", "guard", "guava", "guess", "guest", "guide",
    "guild", "guilt", "guise", "gulch", "gully", "gumbo", "gummy", "guppy", "gusto", "gusty",
    "gutsy", "habit", "hairy", "halve", "handy", "happy", "hardy", "harem", "harpy", "harry",
    "harsh", "haste", "hasty", "hatch", "hater", "haunt", "haven", "havoc", "hazel", "heady",
    "heard", "heart", "heath", "heave", "heavy", "hedge", "hefty", "heigh", "heist", "helix",
    "hello", "helm", "hence", "heron", "hinge", "hippo", "hippy", "hitch", "hoard", "hoarse",
    "hobby", "hoist", "holly", "homer", "homme", "honey", "honor", "hooey", "horde", "horny",
    "horse", "hotdog", "hotel", "hotly", "hound", "house", "hovel", "hover", "howdy", "human",
    "humid", "humor", "humph", "humus", "hunch", "hunky", "hurry", "husky", "hussy", "hutch",
    "hydro", "hyena", "hyper", "icily", "icing", "ideal", "idiom", "idiot", "idler", "igloo",
    "image", "imbue", "impel", "imply", "inane", "inapt", "incur", "index", "inept", "inert",
    "infer", "ingot", "inked", "inkle", "inlet", "inner", "input", "inter", "intro", "inure",
    "irate", "irony", "islet", "issue", "itchy", "ivory", "jaunt", "jazzy", "jeans", "jelly",
    "jenny", "jerky", "jetty", "jewel", "jiffy", "joint", "joker", "jolly", "joust", "judge",
    "juice", "juicy", "julep", "jumbo", "jumpy", "junco", "junky", "juror", "kappa", "karma",
    "kayak", "kebab", "khaki", "kiosk", "kitty", "knack", "knave", "knead", "kneed", "kneel",
    "knelt", "knife", "knock", "knoll", "known", "koala", "krill", "label", "labor", "laden",
    "ladle", "lager", "lance", "lanky", "lapel", "lapse", "large", "larva", "lasso", "latch",
    "later", "lathe", "latte", "laugh", "laura", "lava", "lawn", "layer", "leach", "leafy",
    "leaky", "leant", "leapt", "learn", "lease", "leash", "least", "leave", "ledge", "leech",
    "leery", "lefty", "legal", "leger", "lemon", "lemur", "leper", "level", "lever", "libel",
    "licit", "liege", "lifer", "light", "liken", "lilac", "limbo", "limit", "linen", "liner",
    "lingo", "links", "lions", "lipid", "lithe", "liter", "litre", "litter", "little", "livid",
    "llama", "loamy", "loath", "lobby", "local", "locus", "lodge", "lofty", "logic", "login",
    "loopy", "loose", "lorry", "loser", "lotta", "lotto", "lotus", "louse", "lousy", "lovat",
    "loved", "lover", "lower", "lowly", "loyal", "lucid", "lucky", "lumen", "lumpy", "lunar",
    "lunch", "lunge", "lupin", "lurch", "lurid", "lusty", "lute", "lying", "lymph", "lynch",
    "lyric", "macaw", "macho", "macro", "madam", "madly", "mafia", "magic", "magma", "maize",
    "major", "maker", "mamma", "mammy", "mango", "mania", "manic", "manly", "manor", "maple",
    "march", "marry", "marsh", "mason", "masse", "match", "mated", "mater", "matey", "matte",
    "mauve", "maxim", "maybe", "mayor", "mealy", "meant", "meaty", "mecca", "medal", "media",
    "medic", "melee", "melon", "mercy", "merge", "merit", "merry", "messy", "metal", "meter",
    "metro", "micro", "midge", "midst", "might", "milky", "mimic", "mince", "miner", "minim",
    "minor", "minty", "minus", "mirth", "miser", "missy", "mixed", "mixer", "moan", "mocha",
    "model", "modem", "mogul", "moist", "molar", "moldy", "molly", "money", "month", "moody",
    "moose", "moral", "moray", "moron", "morph", "mossy", "motel", "motif", "motor", "motto",
    "moult", "mound", "mount", "mourn", "mouse", "mousy", "mouth", "mover", "movie", "mower",
    "mucky", "mucus", "muddy", "mulch", "multi", "mummy", "munch", "mural", "murky", "mushy",
    "music", "musky", "musty", "muted", "myrrh", "myths", "nacho", "nadir", "naive", "nanny",
    "nasal", "nasty", "natal", "naval", "navel", "needy", "neigh", "nerdy", "nerve", "never",
    "newer", "newly", "nicer", "niche", "niece", "nifty", "night", "ninja", "ninth", "noble",
    "nobly", "noise", "noisy", "nomad", "noose", "north", "nosey", "notch", "noted", "notre",
    "nought", "novel", "nudge", "nurse", "nutty", "nylon", "nymph", "oaken", "obese", "occur",
    "ocean", "octet", "odder", "oddly", "offal", "offer", "often", "ogler", "olive", "omega",
    "onion", "onset", "opal", "opera", "opine", "opium", "optic", "orbit", "order", "organ",
    "other", "otter", "ought", "ounce", "outdo", "outer", "outgo", "ovary", "ovate", "overt",
    "owing", "owner", "oxide", "ozone", "pagan", "pager", "paint", "paise", "palate", "paler",
    "pallet", "palmy", "panda", "panel", "panic", "pansy", "paper", "pappy", "parch", "pardon",
    "parer", "parka", "parry", "parse", "pasta", "paste", "pasty", "patch", "pate", "patio",
    "patsy", "patty", "pause", "payee", "payer", "peace", "peach", "pearl", "pecan", "pedal",
    "penal", "pence", "penis", "penny", "perch", "peril", "perky", "perry", "pesky", "pesto",
    "petal", "petty", "phase", "phlegm", "phone", "phony", "photo", "piano", "picky", "piece",
    "piety", "piggy", "pilot", "pinch", "piney", "pinky", "pinto", "pious", "piper", "pique",
    "pirate", "pitch", "pithy", "pivot", "pixel", "pixie", "pizza", "place", "plaid", "plain",
    "plait", "plane", "plank", "plant", "plate", "plaza", "plead", "pleat", "plied", "plier",
    "plonk", "pluck", "plumb", "plume", "plump", "plunk", "plush", "poach", "podgy", "poem",
    "point", "poise", "poker", "polar", "polka", "polyp", "pooch", "poppy", "porch", "poser",
    "posit", "posse", "pouch", "pound", "pouty", "power", "prank", "prawn", "preen", "press",
    "price", "prick", "pride", "pried", "prime", "primo", "print", "prior", "prism", "privy",
    "prize", "probe", "prone", "prong", "proof", "prose", "proud", "prove", "prowl", "proxy",
    "prude", "prune", "psalm", "pubic", "pudgy", "puff", "pulse", "punch", "puny", "pupil",
    "puppy", "puree", "purer", "purge", "purse", "pushy", "putty", "pygmy", "quack", "quaff",
    "quail", "quake", "qualm", "quark", "quart", "quash", "quasi", "quay", "queasy", "queen",
    "queer", "quell", "query", "quest", "queue", "quick", "quiet", "quilt", "quirk", "quite",
    "quota", "quote", "quoth", "rabbi", "rabbit", "rabid", "racer", "radar", "radii", "radio",
    "radon", "rainy", "raise", "rajah", "rally", "ralph", "ranch", "randy", "range", "rangy",
    "rapid", "rarer", "raspy", "rater", "ratio", "ratty", "raven", "rayon", "razor", "reach",
    "react", "ready", "realm", "reams", "reaper", "rearm", "rebel", "reboot", "rebound", "recap",
    "recur", "redan", "redid", "redo", "refer", "refit", "regal", "reign", "reins", "relax",
    "relay", "relic", "remit", "renew", "repay", "repel", "reply", "rerun", "reset", "resin",
    "retch", "retro", "retry", "reuse", "revel", "review", "revue", "rhino", "rhyme", "rider",
    "ridge", "rifle", "right", "rigid", "rigor", "rinse", "ripen", "riper", "risen", "riser",
    "risky", "rival", "riven", "river", "rivet", "roach", "roast", "robin", "robot", "rocky",
    "rodeo", "roger", "rogue", "roost", "roomy", "roost", "rooty", "roper", "rorty", "rosin",
    "rotor", "rouge", "rough", "round", "rouse", "route", "rover", "rowdy", "rower", "royal",
    "ruddy", "ruder", "rugby", "ruler", "rumba", "rummy", "rumor", "run up", "rupee", "rural",
    "rusty", "rutty", "saber", "sable", "sadly", "safer", "sahib", "saint", "salad", "sally",
    "salon", "salsa", "salty", "salve", "salvo", "samba", "sandy", "saner", "sappy", "sassy",
    "satin", "satire", "sauce", "saucy", "sauna", "saute", "savor", "savoy", "savvy", "scald",
    "scale", "scalp", "scamp", "scant", "scare", "scarf", "scary", "scene", "scent", "scold",
    "scone", "scoop", "scope", "scorch", "score", "scorn", "scour", "scout", "scowl", "scram",
    "scrap", "scree", "screw", "scrub", "scuba", "scuff", "seam", "seamy", "sedan", "sedate",
    "sedge", "seedy", "segue", "seize", "semen", "sense", "sepia", "serif", "serum", "serve",
    "servo", "setup", "seven", "sever", "sewer", "shack", "shade", "shady", "shaft", "shake",
    "shaky", "shale", "shall", "shalt", "shame", "shank", "shape", "shard", "share", "shark",
    "sharp", "shave", "shawl", "sheaf", "shear", "sheen", "sheep", "sheer", "sheet", "sheik",
    "shelf", "shell", "shied", "shier", "shift", "shine", "shiny", "shire", "shirk", "shirt",
    "shoal", "shock", "shone", "shook", "shoot", "shore", "shorn", "short", "shout", "shove",
    "shown", "showy", "shrank", "shred", "shrew", "shrub", "shrug", "shuck", "shunt", "shush",
    "shyly", "siege", "sieve", "sight", "sigma", "silky", "silly", "since", "sinew", "singe",
    "sinus", "siren", "sissy", "sitar", "sixth", "sixty", "sized", "skate", "skein", "skelp",
    "skier", "skiff", "skill", "skimp", "skirt", "skulk", "skull", "skunk", "slack", "slain",
    "slalom", "slang", "slant", "slash", "slate", "slave", "sleek", "sleep", "sleet", "slept",
    "slice", "slick", "slide", "slime", "slimy", "sling", "slink", "slither", "slope", "slosh",
    "sloth", "slump", "slung", "slunk", "slurp", "slush", "slyly", "smack", "small", "smart",
    "smash", "smear", "smell", "smelt", "smile", "smirk", "smite", "smoky", "snack", "snafu",
    "snail", "snake", "snaky", "snap", "snare", "snarl", "sneak", "sneer", "snide", "sniff",
    "snipe", "snitch", "snoop", "snore", "snort", "snout", "snowy", "snuck", "snuff", "soapy",
    "sober", "soggy", "solar", "solid", "solve", "sonar", "sonic", "soothe", "sorry", "sound",
    "south", "sower", "space", "spade", "spank", "spare", "spark", "spasm", "spawn", "speak",
    "spear", "speck", "speed", "spell", "spelt", "spend", "spent", "sperm", "spice", "spicy",
    "spider", "spied", "spiel", "spike", "spiky", "spill", "spilt", "spine", "spiny", "spiral",
    "spite", "splat", "split", "spoil", "spoke", "spoof", "spook", "spool", "spoon", "spore",
    "sport", "spout", "spray", "spree", "sprig", "spry", "spunk", "spurn", "spurt", "squad",
    "squat", "squid", "stack", "staff", "stage", "staid", "stain", "stair", "stake", "stale",
    "stalk", "stall", "stamp", "stand", "stank", "staph", "stare", "stark", "start", "stash",
    "state", "stave", "stead", "steak", "steal", "steam", "steed", "steel", "steep", "steer",
    "stein", "stern", "stick", "stiff", "still", "stilt", "sting", "stink", "stint", "stock",
    "stoic", "stoke", "stole", "stomp", "stone", "stony", "stood", "stool", "stoop", "store",
    "stork", "storm", "story", "stout", "stove", "strap", "straw", "stray", "strep", "strip",
    "strive", "strode", "stroke", "stroll", "strong", "strove", "struck", "strung", "strut", "stuck",
    "study", "stuff", "stump", "stung", "stunk", "stunt", "style", "suave", "suchn", "sully",
    "sumac", "sunny", "super", "surer", "surge", "surly", "sushi", "swain", "swamp", "swank",
    "swarm", "swash", "swath", "swear", "sweat", "sweep", "sweet", "swell", "swept", "swift",
    "swill", "swine", "swing", "swipe", "swirl", "swish", "swiss", "swoon", "swoop", "sword",
    "swore", "sworn", "swum", "swung", "sylph", "synod", "syrup", "tabby", "tabla", "table",
    "taboo", "tacit", "tacky", "taffy", "taint", "taken", "taker", "talc", "tally", "talon",
    "tamer", "tango", "tangy", "taper", "tapir", "tardy", "tarot", "tarry", "tartan", "taste",
    "tasty", "tatar", "tater", "tatty", "taunt", "tawny", "teach", "teary", "tease", "teddy",
    "teens", "teeny", "teeth", "tempo", "tempt", "tenet", "tenor", "tense", "tenth", "tepee",
    "tepid", "terra", "terse", "testy", "tethy", "thank", "theft", "their", "theme", "there",
    "these", "thick", "thief", "thigh", "thing", "think", "third", "thorn", "those", "three",
    "threw", "throb", "throw", "thrum", "thumb", "thump", "thunk", "tiara", "tibia", "tidal",
    "tiger", "tight", "tilde", "tiler", "tilth", "timer", "timid", "tinge", "tinny", "tipsy",
    "titan", "tithe", "title", "toast", "today", "toddy", "token", "tonal", "tonga", "tonic",
    "tooth", "topaz", "topic", "torch", "torso", "total", "totem", "touch", "tough", "towel",
    "tower", "toxic", "toxin", "trace", "track", "tract", "trade", "trail", "train", "trait",
    "tramp", "trash", "travail", "trawl", "tread", "treat", "treble", "trend", "trench", "tress",
    "triad", "trial", "tribe", "trice", "trick", "tried", "trier", "trike", "trill", "trine",
    "tripe", "trite", "troll", "tromp", "troop", "trope", "troth", "trout", "trove", "truce",
    "truck", "truer", "truly", "trump", "trunk", "truss", "trust", "truth", "tryst", "tubal",
    "tubby", "tuber", "tudor", "tulip", "tulle", "tumor", "tunic", "tunny", "turbo", "tureen",
    "turf", "turn", "tusks", "tutor", "tutti", "tutu", "twain", "twang", "tweak", "tweed",
    "tweet", "twerp", "twice", "twill", "twine", "twink", "twirl", "twist", "twixt", "tying",
    "udder", "ulcer", "ultra", "umbra", "unary", "uncle", "uncap", "uncut", "under", "undid",
    "undue", "unfed", "unfit", "unify", "union", "unite", "unity", "unlit", "unmet", "unpeg",
    "unpin", "unset", "unsex", "untie", "until", "unwed", "unwit", "unzip", "upper", "upset",
    "urban", "urine", "usage", "usher", "using", "usual", "usurp", "usury", "utter", "vague",
    "valet", "valid", "valor", "value", "valve", "vapid", "vapor", "vault", "vaunt", "vegan",
    "venom", "venue", "verb", "verge", "verse", "verso", "verve", "vetch", "vexed", "viand",
    "vibes", "vicar", "video", "vigil", "vigor", "villa", "vinyl", "viola", "viper", "viral",
    "vireo", "virus", "visit", "visor", "vista", "vital", "vivid", "vixen", "vocal", "vodka",
    "vogue", "voice", "voila", "vomit", "voter", "vouch", "vowed", "vowel", "vroom", "wacky",
    "wafer", "wager", "wagon", "waist", "waive", "waken", "waker", "waltz", "warbl", "waste",
    "watch", "water", "waver", "waxed", "waxen", "weary", "weave", "wedge", "weedy", "weigh",
    "weird", "welsh", "wench", "wetly", "whack", "whale", "wharf", "wheat", "wheel", "whelk",
    "whelp", "where", "which", "whiff", "while", "whim", "whine", "whiny", "whirl", "whisk",
    "white", "whole", "whoop", "whore", "whose", "widen", "wider", "widow", "width", "wield",
    "wight", "willy", "wimpy", "wince", "winch", "windy", "wiper", "wired", "wiser", "wispy",
    "witch", "witty", "woken", "woman", "women", "woody", "wooer", "wordy", "world", "worry",
    "worse", "worst", "worth", "would", "wound", "woven", "wrack", "wrath", "wreak", "wreck",
    "wrest", "wring", "wrist", "write", "wrong", "wrote", "wrought", "wrung", "wryly", "xerox",
    "yacht", "yahoo", "yearn", "yeast", "yield", "yokel", "young", "yours", "youth", "zebra",
    "zesty", "zonal"
])

def get_daily_word():
    """Get the word for today based on the date"""
    # Use the date as a seed to get consistent word for the day
    today = datetime.now().date()
    seed = int(today.strftime("%Y%m%d"))
    random.seed(seed)
    return random.choice(WORD_LIST).upper()

def check_guess(guess, target):
    """
    Check a guess against the target word and return feedback
    Returns a list of statuses: 'correct', 'present', or 'absent'
    """
    guess = guess.upper()
    target = target.upper()
    result = ['absent'] * 5
    target_letters = list(target)
    
    # First pass: mark correct letters
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = 'correct'
            target_letters[i] = None  # Mark as used
    
    # Second pass: mark present letters
    for i in range(5):
        if result[i] == 'absent' and guess[i] in target_letters:
            result[i] = 'present'
            target_letters[target_letters.index(guess[i])] = None  # Mark as used
    
    return result

@app.route('/')
def index():
    return render_template('wordle.html')

@app.route('/api/check', methods=['POST'])
def check():
    data = request.get_json()
    guess = data.get('guess', '').strip().upper()
    guess_number = data.get('guess_number', 1)  # Track which guess this is
    
    if len(guess) != 5:
        return jsonify({'error': 'Guess must be 5 letters'}), 400
    
    if guess.lower() not in VALID_GUESSES:
        return jsonify({'error': 'Not a valid word'}), 400
    
    target = get_daily_word()
    result = check_guess(guess, target)
    
    is_correct = guess == target
    is_last_guess = guess_number >= 6
    
    return jsonify({
        'result': result,
        'correct': is_correct,
        'word': target if (is_correct or is_last_guess) else None
    })

@app.route('/api/word')
def get_word():
    """Get today's word (only for debugging, remove in production)"""
    return jsonify({'word': get_daily_word()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)