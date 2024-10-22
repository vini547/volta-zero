import pandas as pd
import requests as req
from io import StringIO
import time as time 
import streamlit as st
import altair as alt
from urllib.error import URLError
import numpy as np


st.markdown("# DOTA 2 Team Builder®")
# Asking the user to enter 5 heroes through text inputs
# Function to predict matching heroes based on user input
def predict_hero(input_text, hero_list):
    suggestions = [hero for hero in hero_list if hero.lower().startswith(input_text.lower())]
    return suggestions

st.markdown("### Select 5 heroes:")

selected_heroes = []
for i in range(1, 6):
    hero = st.text_input(f"Hero {i}", value="", key=f"hero_{i}")
    selected_heroes.append(hero)

st.markdown(selected_heroes)

heroes1=[]
heroes2=[]
counters = []
weakers = []
heroes = ['anti-mage', 'axe', 'bane', 'bloodseeker', 'crystal-maiden', 'drow-ranger', 'earthshaker', 'juggernaut', 'mirana', 'morphling', 'shadow-fiend', 'phantom-lancer', 'puck', 'pudge', 'razor', 'sand-king', 'storm-spirit', 'sven', 'tiny', 'vengeful-spirit', 'windranger', 'zeus', 'kunkka', 'lina', 'lion', 'shadow-shaman', 'slardar', 'tidehunter', 'witch-doctor', 'lich', 'riki', 'enigma', 'tinker', 'sniper', 'necrophos', 'warlock', 'beastmaster', 'queen-of-pain', 'venomancer', 'faceless-void', 'wraith-king', 'death-prophet', 'phantom-assassin', 'pugna', 'templar-assassin', 'viper', 'luna', 'dragon-knight', 'dazzle', 'clockwerk', 'leshrac', "nature's-prophet", 'lifestealer', 'dark-seer', 'clinkz', 'omniknight', 'enchantress', 'huskar', 'night-stalker', 'broodmother', 'bounty-hunter', 'weaver', 'jakiro', 'batrider', 'chen', 'spectre', 'ancient-apparition', 'doom', 'ursa', 'spirit-breaker', 'gyrocopter', 'alchemist', 'invoker', 'silencer', 'outworld-destroyer', 'lycan', 'brewmaster', 'shadow-demon', 'lone-druid', 'chaos-knight', 'meepo', 'treant-protector', 'ogre-magi', 'undying', 'rubick', 'disruptor', 'nyx-assassin', 'naga-siren', 'keeper-of-the-light', 'io', 'visage', 'slark', 'medusa', 'troll-warlord', 'centaur-warrunner', 'magnus', 'timbersaw', 'bristleback', 'tusk', 'skywrath-mage', 'abaddon', 'elder-titan', 'legion-commander', 'techies', 'ember-spirit', 'earth-spirit', 'underlord', 'terrorblade', 'phoenix', 'oracle', 'winter-wyvern', 'arc-warden', 'monkey-king', 'dark-willow', 'pangolier', 'grimstroke', 'hoodwink', 'void-spirit', 'snapfire', 'mars', 'dawnbreaker', 'marci', 'primal-beast', 'muerta']
itens = ["aghanim's-shard", "aghanim's-scepter", 'power-treads', 'magic-wand', 'blink-dagger', 'arcane-boots', 'black-king-bar', 'phase-boots', 'wraith-band', 'bracer', 'manta-style', 'dust-of-appearance', 'aether-lens', 'quelling-blade', 'blade-mail', 'observer-and-sentry-wards', 'boots-of-travel', 'tranquil-boots', 'force-staff', 'hurricane-pike', 'glimmer-cape', 'hand-of-midas', "shiva's-guard", 'iron-branch', 'bottle', 'desolator', 'mind-breaker', 'boots-of-speed', 'null-talisman', 'smoke-of-deceit', 'daedalus', 'sentry-ward', "eul's-scepter-of-divinity", 'mjollnir', 'magic-stick', 'butterfly', "linken's-sphere", 'maelstrom', 'heart-of-tarrasque', 'elven-tunic', 'ogre-axe', 'paladin-sword', 'psychic-headband', 'healing-lotus', 'gleipnir', 'silver-edge', 'eye-of-skadi', 'monkey-king-bar', 'battle-fury', 'timeless-relic', 'diffusal-blade', 'observer-ward', 'octarine-core', "philosopher's-stone", 'dragon-lance', 'trickster-cloak', 'spirit-vessel', 'harpoon', 'shadow-blade', 'ghost-scepter', 'scythe-of-vyse', 'bloodthorn', 'mask-of-madness', 'wind-lace', 'ethereal-blade', 'ninja-gear', 'mage-slayer', 'orchid-malevolence', "vindicator's-axe", 'grove-bow', 'assault-cuirass', 'skull-basher', 'guardian-greaves', "aviana's-feather", 'eternal-shroud', 'radiance', 'khanda', 'solar-crest', 'satanic', 'echo-sabre', 'vambrace', 'kaya-and-sange', 'cloak-of-flames', 'abyssal-blade', 'clarity', 'lotus-orb', 'aeon-disk', 'dandelion-amulet', 'ogre-seal-totem', 'orb-of-corrosion', 'disperser', 'staff-of-wizardry', 'witch-blade', 'vanguard', 'crystalys', 'enchanted-quiver', 'refresher-orb', 'defiant-shell', 'parasma', 'soul-ring', 'ancient-guardian', 'circlet', "ascetic's-cap", 'vampire-fangs', 'point-booster', 'nemesis-curse', 'phylactery', 'dragon-scale', 'enchanted-mango', 'rattlecage', 'morbid-mask', 'rod-of-atos', "specialist's-array", 'sange-and-yasha', 'tango', 'great-healing-lotus', 'pipe-of-insight', "vladmir's-offering", 'havoc-hammer', 'telescope', "heaven's-halberd", 'blight-stone', 'ceremonial-robe', 'armlet-of-mordiggian', 'mithril-hammer', 'veil-of-discord', "pupil's-gift", 'falcon-blade', 'orb-of-destruction', 'bullwhip', 'gossamer-cape', "fairy's-trinket", 'wind-waker', 'overwhelming-blink', 'blade-of-alacrity', 'urn-of-shadows', 'eye-of-the-vizier', 'safety-bubble', 'moon-shard', 'kaya', 'stormcrafter', 'gem-of-true-sight', 'craggy-coat', 'crimson-guard', 'nullifier', 'healing-salve', 'yasha', 'faded-broach', 'bloodstone', 'swift-blink', 'arcane-ring', 'dagon-level-5', "martyr's-plate", 'boots-of-bearing', 'greater-healing-lotus', 'orb-of-venom', 'whisper-of-the-dread', 'gauntlets-of-strength', 'aegis-of-the-immortal', 'mekansm', 'javelin', 'platemail', 'perseverance', 'boots-of-travel-2', 'cloak', 'royal-jelly', 'ring-of-protection', 'divine-rapier', 'hyperstone', 'yasha-and-kaya', 'void-stone', 'reaver', 'meteor-hammer', 'blitz-knuckles', 'blood-grenade', 'claymore', 'occult-bracelet', 'broom-handle', 'duelist-gloves', 'buckler', 'tiara-of-selemene', 'trusty-shovel', 'shadow-amulet', 'ring-of-tarrasque', 'fluffy-hat', 'infused-raindrops', 'doubloon', 'ring-of-basilius', 'diadem', 'holy-locket', 'ultimate-orb', 'sange', 'vitality-booster', 'demon-edge', 'pig-pole', 'slippers-of-agility', 'headdress', 'tier-4-token', 'tier-3-token', 'lance-of-pursuit', 'energy-booster', 'cheese', 'eaglesong', 'drum-of-endurance', "sage's-mask", 'faerie-fire', 'ring-of-health', 'mystic-staff', 'spark-of-courage', 'cornucopia', 'light-collector', 'voodoo-mask', 'broadsword', "giant's-ring", 'belt-of-strength', 'mirror-shield', 'oblivion-staff', 'seeds-of-serenity', 'stygian-desolator', 'arcane-blink', 'gloves-of-haste', 'mantle-of-intelligence', 'apex', 'pirate-hat', 'talisman-of-evasion', 'helm-of-iron-will', 'pavise', 'chainmail', 'tier-2-token', 'crown', 'tier-1-token', 'soul-booster', 'seer-stone', 'force-boots', 'dagon', 'ring-of-regen', "revenant's-brooch", "roshan's-banner", 'book-of-the-dead', 'robe-of-the-magi', 'dagon-level-3', 'dagon-level-4', 'sacred-relic', 'dagon-level-2', 'blades-of-attack', 'band-of-elvenskin', 'magic-lamp', "arcanist's-armor", 'book-of-shadows', 'refresher-shard', 'unwavering-condition', 'helm-of-the-overlord', 'helm-of-the-dominator', 'tier-5-token', "aghanim's-blessing---roshan", 'tango-shared', 'town-portal-scroll', "aghanim's-blessing", 'block-of-cheese']
@st.cache_data
def all_counters(heroes_list: list):    
    try:
        if all(hero in heroes for hero in heroes_list):
            heroes1 = heroes_list  # Save the input list as heroes1
            request_headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
            }
            counters = []  # Initialize counters list
            
            for hero in heroes_list:
                DATA_URL = "https://pt.dotabuff.com/heroes/"+hero+"/counters"      
                response = req.get(DATA_URL, headers=request_headers)         
                html_tables = pd.read_html(StringIO(response.text), index_col=0)     
                counters.append(html_tables[1].iloc[0:5, 0].tolist())  # Add top 5 counters to the list
            
            return counters, heroes1   
        
    except ValueError:
        st.write("Hero names must be completely lower case and separated by '-'.")
        st.write("Try: 'Anti Mage' into 'anti-mage'.")
    
    return counters
def all_weakers(heroes_list: list):
    try:
        # Ensure all heroes in the list are valid
        if all(hero in heroes for hero in heroes_list):
            heroes1 = heroes_list  # Save the input list as heroes1
            request_headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
            }
            counters = []  # Initialize counters list
            
            for hero in heroes_list:
                DATA_URL = "https://pt.dotabuff.com/heroes/"+hero+"/counters"      
                response = req.get(DATA_URL, headers=request_headers)         
                html_tables = pd.read_html(StringIO(response.text), index_col=0)     
                counters.append(html_tables[2].iloc[0:5, 0].tolist())  # Add top 5 counters to the list
            
            return counters, heroes1   
        
    except ValueError:
        st.write("Hero names must be completely lower case and separated by '-'.")
        st.write("Try: 'Anti Mage' into 'anti-mage'.")

def get_heroes_list():     
    request_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
     }     
    DATA_URL = "https://pt.dotabuff.com/heroes/meta"      
    response = req.get(DATA_URL, headers=request_headers)         
    html_tables = pd.read_html(StringIO(response.text),index_col=0)
    heroes_raw = html_tables[0].iloc[0:len(html_tables[0]),0].tolist()
    heroes = list(map(lambda hero: (hero.lower().replace(' ','-')), heroes_raw))
    return heroes

def get_itens_list():    
    request_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
     }     
    DATA_URL = "https://pt.dotabuff.com/items"      
    response = req.get(DATA_URL, headers=request_headers)         
    html_tables = pd.read_html(StringIO(response.text),index_col=0)
    heroes_raw = html_tables[0].iloc[0:len(html_tables[0]),0].tolist()
    itens = list(map(lambda hero: (hero.lower().replace(' ','-').replace('(','').replace(')','')), heroes_raw))
    return itens
     
a = all_counters(selected_heroes)   
b = all_weakers(selected_heroes) 
        
lista1 = get_heroes_list()
lista2 = get_itens_list()

a_df=pd.DataFrame(a[0])
b_df=pd.DataFrame(b[0])

a_df = a_df.transpose()
b_df = b_df.transpose()

a_df.columns=a[1]
b_df.columns=b[1]

a_df.index=a_df.index+1
b_df.index=b_df.index+1

st.markdown("## DOTA 2 Team Builder®")
st.write(a_df)
st.write(b_df)
st.write(lista1)
st.write(lista2)
