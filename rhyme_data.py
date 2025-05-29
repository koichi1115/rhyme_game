# 英語の韻データ
english_rhyme_pairs = [
    # 基本的な韻
    {"word": "cat", "rhymes": [
        {"word": "hat", "type": "perfect", "points": 100},
        {"word": "bat", "type": "perfect", "points": 100},
        {"word": "rat", "type": "perfect", "points": 100},
        {"word": "mat", "type": "perfect", "points": 100},
        {"word": "fat", "type": "perfect", "points": 100}
    ], "non_rhymes": ["dog", "fish", "bird", "mouse", "cow"]},
    
    {"word": "light", "rhymes": [
        {"word": "night", "type": "perfect", "points": 100},
        {"word": "sight", "type": "perfect", "points": 100},
        {"word": "fight", "type": "perfect", "points": 100},
        {"word": "bright", "type": "perfect", "points": 100},
        {"word": "might", "type": "perfect", "points": 100},
        {"word": "right", "type": "perfect", "points": 100}
    ], "non_rhymes": ["dark", "day", "sun", "lamp", "shadow"]},
    
    {"word": "game", "rhymes": [
        {"word": "fame", "type": "perfect", "points": 100},
        {"word": "name", "type": "perfect", "points": 100},
        {"word": "same", "type": "perfect", "points": 100},
        {"word": "flame", "type": "perfect", "points": 100},
        {"word": "blame", "type": "perfect", "points": 100},
        {"word": "tame", "type": "perfect", "points": 100}
    ], "non_rhymes": ["play", "fun", "joy", "sport", "match"]},
    
    {"word": "cool", "rhymes": [
        {"word": "pool", "type": "perfect", "points": 100},
        {"word": "rule", "type": "perfect", "points": 100},
        {"word": "fool", "type": "perfect", "points": 100},
        {"word": "school", "type": "perfect", "points": 100},
        {"word": "tool", "type": "perfect", "points": 100},
        {"word": "jewel", "type": "perfect", "points": 100}
    ], "non_rhymes": ["hot", "warm", "heat", "cold", "nice"]},
    
    {"word": "beat", "rhymes": [
        {"word": "feet", "type": "perfect", "points": 100},
        {"word": "heat", "type": "perfect", "points": 100},
        {"word": "seat", "type": "perfect", "points": 100},
        {"word": "street", "type": "perfect", "points": 100},
        {"word": "sweet", "type": "perfect", "points": 100},
        {"word": "fleet", "type": "perfect", "points": 100}
    ], "non_rhymes": ["rhythm", "sound", "noise", "drum", "bass"]},
    
    # ヒップホップで使われる韻
    {"word": "flow", "rhymes": [
        {"word": "go", "type": "perfect", "points": 100},
        {"word": "show", "type": "perfect", "points": 100},
        {"word": "know", "type": "perfect", "points": 100},
        {"word": "grow", "type": "perfect", "points": 100},
        {"word": "blow", "type": "perfect", "points": 100},
        {"word": "slow", "type": "perfect", "points": 100}
    ], "non_rhymes": ["stop", "halt", "end", "rap", "verse"]},
    
    {"word": "rhyme", "rhymes": [
        {"word": "time", "type": "perfect", "points": 100},
        {"word": "climb", "type": "perfect", "points": 100},
        {"word": "dime", "type": "perfect", "points": 100},
        {"word": "prime", "type": "perfect", "points": 100},
        {"word": "crime", "type": "perfect", "points": 100},
        {"word": "slime", "type": "perfect", "points": 100}
    ], "non_rhymes": ["verse", "word", "line", "poem", "song"]},
    
    {"word": "star", "rhymes": [
        {"word": "far", "type": "perfect", "points": 100},
        {"word": "car", "type": "perfect", "points": 100},
        {"word": "bar", "type": "perfect", "points": 100},
        {"word": "jar", "type": "perfect", "points": 100},
        {"word": "scar", "type": "perfect", "points": 100},
        {"word": "guitar", "type": "perfect", "points": 100}
    ], "non_rhymes": ["sky", "night", "space", "moon", "sun"]},
    
    {"word": "high", "rhymes": [
        {"word": "sky", "type": "perfect", "points": 100},
        {"word": "fly", "type": "perfect", "points": 100},
        {"word": "try", "type": "perfect", "points": 100},
        {"word": "why", "type": "perfect", "points": 100},
        {"word": "bye", "type": "perfect", "points": 100},
        {"word": "cry", "type": "perfect", "points": 100}
    ], "non_rhymes": ["low", "down", "bottom", "ground", "floor"]},
    
    {"word": "dream", "rhymes": [
        {"word": "team", "type": "perfect", "points": 100},
        {"word": "stream", "type": "perfect", "points": 100},
        {"word": "beam", "type": "perfect", "points": 100},
        {"word": "cream", "type": "perfect", "points": 100},
        {"word": "scheme", "type": "perfect", "points": 100},
        {"word": "theme", "type": "perfect", "points": 100}
    ], "non_rhymes": ["sleep", "night", "rest", "wish", "hope"]},
    
    # 新しい韻のセット
    {"word": "rain", "rhymes": [
        {"word": "pain", "type": "perfect", "points": 100},
        {"word": "train", "type": "perfect", "points": 100},
        {"word": "brain", "type": "perfect", "points": 100},
        {"word": "chain", "type": "perfect", "points": 100},
        {"word": "gain", "type": "perfect", "points": 100}
    ], "non_rhymes": ["water", "cloud", "storm", "wet", "umbrella"]},
    
    {"word": "fire", "rhymes": [
        {"word": "desire", "type": "perfect", "points": 100},
        {"word": "wire", "type": "perfect", "points": 100},
        {"word": "tire", "type": "perfect", "points": 100},
        {"word": "higher", "type": "perfect", "points": 100},
        {"word": "buyer", "type": "perfect", "points": 100}
    ], "non_rhymes": ["flame", "hot", "burn", "smoke", "heat"]},
    
    {"word": "mind", "rhymes": [
        {"word": "find", "type": "perfect", "points": 100},
        {"word": "kind", "type": "perfect", "points": 100},
        {"word": "blind", "type": "perfect", "points": 100},
        {"word": "behind", "type": "perfect", "points": 100},
        {"word": "signed", "type": "perfect", "points": 100}
    ], "non_rhymes": ["brain", "think", "thought", "idea", "smart"]},
    
    {"word": "street", "rhymes": [
        {"word": "beat", "type": "perfect", "points": 100},
        {"word": "meet", "type": "perfect", "points": 100},
        {"word": "feet", "type": "perfect", "points": 100},
        {"word": "sweet", "type": "perfect", "points": 100},
        {"word": "complete", "type": "perfect", "points": 100}
    ], "non_rhymes": ["road", "path", "avenue", "lane", "way"]},
    
    {"word": "gold", "rhymes": [
        {"word": "bold", "type": "perfect", "points": 100},
        {"word": "cold", "type": "perfect", "points": 100},
        {"word": "fold", "type": "perfect", "points": 100},
        {"word": "hold", "type": "perfect", "points": 100},
        {"word": "sold", "type": "perfect", "points": 100}
    ], "non_rhymes": ["silver", "metal", "money", "rich", "shine"]},
    
    # 頭韻（アリタレーション）の例
    {"word": "Peter", "rhymes": [
        {"word": "Piper", "type": "alliteration", "points": 150},
        {"word": "picked", "type": "alliteration", "points": 150},
        {"word": "peck", "type": "alliteration", "points": 150},
        {"word": "pepper", "type": "alliteration", "points": 150},
        {"word": "purple", "type": "alliteration", "points": 150}
    ], "non_rhymes": ["salt", "vinegar", "chips", "sugar", "spice"]},
    
    {"word": "She", "rhymes": [
        {"word": "sells", "type": "alliteration", "points": 150},
        {"word": "seashells", "type": "alliteration", "points": 150},
        {"word": "seashore", "type": "alliteration", "points": 150},
        {"word": "surely", "type": "alliteration", "points": 150},
        {"word": "shining", "type": "alliteration", "points": 150}
    ], "non_rhymes": ["buys", "collects", "finds", "takes", "gives"]},
    
    {"word": "Crazy", "rhymes": [
        {"word": "cool", "type": "alliteration", "points": 150},
        {"word": "cats", "type": "alliteration", "points": 150},
        {"word": "create", "type": "alliteration", "points": 150},
        {"word": "chaos", "type": "alliteration", "points": 150},
        {"word": "constantly", "type": "alliteration", "points": 150}
    ], "non_rhymes": ["wild", "strange", "weird", "odd", "unusual"]},
    
    {"word": "Busy", "rhymes": [
        {"word": "bees", "type": "alliteration", "points": 150},
        {"word": "buzz", "type": "alliteration", "points": 150},
        {"word": "building", "type": "alliteration", "points": 150},
        {"word": "beautiful", "type": "alliteration", "points": 150},
        {"word": "boxes", "type": "alliteration", "points": 150}
    ], "non_rhymes": ["idle", "lazy", "slow", "relaxed", "calm"]},
    
    # 母音の長さによる韻の例
    {"word": "sensation", "rhymes": [
        {"word": "nation", "type": "partial", "points": 80},
        {"word": "station", "type": "partial", "points": 80},
        {"word": "vacation", "type": "perfect", "points": 120},
        {"word": "creation", "type": "perfect", "points": 120},
        {"word": "relation", "type": "perfect", "points": 120}
    ], "non_rhymes": ["feeling", "emotion", "sense", "touch", "experience"]},
    
    {"word": "education", "rhymes": [
        {"word": "nation", "type": "partial", "points": 80},
        {"word": "station", "type": "partial", "points": 80},
        {"word": "vacation", "type": "partial", "points": 80},
        {"word": "relation", "type": "perfect", "points": 120},
        {"word": "foundation", "type": "perfect", "points": 120}
    ], "non_rhymes": ["school", "learning", "teaching", "study", "knowledge"]},
    
    {"word": "inspiration", "rhymes": [
        {"word": "nation", "type": "partial", "points": 80},
        {"word": "creation", "type": "partial", "points": 80},
        {"word": "motivation", "type": "perfect", "points": 120},
        {"word": "dedication", "type": "perfect", "points": 120},
        {"word": "celebration", "type": "perfect", "points": 120}
    ], "non_rhymes": ["idea", "thought", "creativity", "spark", "muse"]},
    
    # ヒップホップスラング
    {"word": "dope", "rhymes": [
        {"word": "hope", "type": "perfect", "points": 100},
        {"word": "cope", "type": "perfect", "points": 100},
        {"word": "rope", "type": "perfect", "points": 100},
        {"word": "slope", "type": "perfect", "points": 100},
        {"word": "nope", "type": "perfect", "points": 100}
    ], "non_rhymes": ["cool", "great", "awesome", "nice", "good"]},
    
    {"word": "sick", "rhymes": [
        {"word": "click", "type": "perfect", "points": 100},
        {"word": "trick", "type": "perfect", "points": 100},
        {"word": "quick", "type": "perfect", "points": 100},
        {"word": "brick", "type": "perfect", "points": 100},
        {"word": "stick", "type": "perfect", "points": 100}
    ], "non_rhymes": ["ill", "cool", "awesome", "amazing", "great"]},
    
    {"word": "fresh", "rhymes": [
        {"word": "mesh", "type": "perfect", "points": 100},
        {"word": "flesh", "type": "perfect", "points": 100},
        {"word": "thresh", "type": "perfect", "points": 100},
        {"word": "refresh", "type": "perfect", "points": 100},
        {"word": "yes", "type": "partial", "points": 80}
    ], "non_rhymes": ["new", "cool", "clean", "nice", "good"]}
]
# 著名なリリックのパンチライン
famous_lyrics = [
    {"line": "Mom's spaghetti", "artist": "Eminem", "song": "Lose Yourself"},
    {"line": "Started from the bottom now we're here", "artist": "Drake", "song": "Started From The Bottom"},
    {"line": "All I do is win win win no matter what", "artist": "DJ Khaled", "song": "All I Do Is Win"},
    {"line": "I got 99 problems but a beat ain't one", "artist": "Jay-Z", "song": "99 Problems"},
    {"line": "Straight outta Compton", "artist": "N.W.A", "song": "Straight Outta Compton"},
    {"line": "California love", "artist": "2Pac", "song": "California Love"},
    {"line": "Cash rules everything around me", "artist": "Wu-Tang Clan", "song": "C.R.E.A.M."},
    {"line": "The blacker the berry, the sweeter the juice", "artist": "Kendrick Lamar", "song": "The Blacker The Berry"},
    {"line": "I'm not a businessman, I'm a business, man", "artist": "Jay-Z", "song": "Diamonds From Sierra Leone (Remix)"},
    {"line": "Real Gs move in silence like lasagna", "artist": "Lil Wayne", "song": "6 Foot 7 Foot"}
]
