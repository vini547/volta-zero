import pandas as pd
import requests as req
from io import StringIO
import streamlit as st

# Define heroes and items
heroes = ['anti-mage', 'axe', 'bane', 'bloodseeker', 'crystal-maiden', 'drow-ranger', 'earthshaker', 'juggernaut', 'mirana', 'morphling', 'shadow-fiend', 'phantom-lancer', 'puck', 'pudge', 'razor', 'sand-king', 'storm-spirit', 'sven', 'tiny', 'vengeful-spirit', 'windranger', 'zeus', 'kunkka', 'lina', 'lion', 'shadow-shaman', 'slardar', 'tidehunter', 'witch-doctor', 'lich', 'riki', 'enigma', 'tinker', 'sniper', 'necrophos', 'warlock', 'beastmaster', 'queen-of-pain', 'venomancer', 'faceless-void', 'wraith-king', 'death-prophet', 'phantom-assassin', 'pugna', 'templar-assassin', 'viper', 'luna', 'dragon-knight', 'dazzle', 'clockwerk', 'leshrac', "nature's-prophet", 'lifestealer', 'dark-seer', 'clinkz', 'omniknight', 'enchantress', 'huskar', 'night-stalker', 'broodmother', 'bounty-hunter', 'weaver', 'jakiro', 'batrider', 'chen', 'spectre', 'ancient-apparition', 'doom', 'ursa', 'spirit-breaker', 'gyrocopter', 'alchemist', 'invoker', 'silencer', 'outworld-destroyer', 'lycan', 'brewmaster', 'shadow-demon', 'lone-druid', 'chaos-knight', 'meepo', 'treant-protector', 'ogre-magi', 'undying', 'rubick', 'disruptor', 'nyx-assassin', 'naga-siren', 'keeper-of-the-light', 'io', 'visage', 'slark', 'medusa', 'troll-warlord', 'centaur-warrunner', 'magnus', 'timbersaw', 'bristleback', 'tusk', 'skywrath-mage', 'abaddon', 'elder-titan', 'legion-commander', 'techies', 'ember-spirit', 'earth-spirit', 'underlord', 'terrorblade', 'phoenix', 'oracle', 'winter-wyvern', 'arc-warden', 'monkey-king', 'dark-willow', 'pangolier', 'grimstroke', 'hoodwink', 'void-spirit', 'snapfire', 'mars', 'dawnbreaker', 'marci', 'primal-beast', 'muerta']
request_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
    }
# Streamlit app
st.markdown("# DOTA 2 Team Builder®")

# Asking the user to enter 5 heroes
st.markdown("### Select 5 heroes:")
selected_heroes = [st.text_input(f"Hero {i}", value="", key=f"hero_{i}") for i in range(1, 6)]
st.markdown(selected_heroes)

# Function to predict matching heroes based on user input
def predict_hero(input_text, hero_list):
    return [hero for hero in hero_list if hero.lower().startswith(input_text.lower())]

# Function to get hero counters
@st.cache_data
def all_counters(heroes_list):    
    counters = []    
    for hero in heroes_list:
        DATA_URL = f"https://pt.dotabuff.com/heroes/{hero}/counters"
        response = req.get(DATA_URL, headers=request_headers)
        html_tables = pd.read_html(StringIO(response.text), index_col=0)
        counters.append(html_tables[1].iloc[0:5, 0].tolist())  # Top 5 counters
    return counters

@st.cache_data
def all_weakers(heroes_list):   
    weakers = []    
    for hero in heroes_list:
        DATA_URL2 = f"https://pt.dotabuff.com/heroes/{hero}/counters"
        response2= req.get(DATA_URL2, headers=request_headers)
        html_tables2= pd.read_html(StringIO(response2.text), index_col=0)
        weakers.append(html_tables2[2].iloc[0:5, 0].tolist())  # Top 5 counters
    return weakers

@st.cache_data
def get_hero_roles(heroes_list):
    hero_attributes = {}
    request_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'}
    
    for hero in heroes_list:
        DATA_URL = f"https://pt.dotabuff.com/heroes/{hero}"
        response = req.get(DATA_URL, headers=request_headers)
        response_text = response.text
        start_index = response.text.find(" - DOTABUFF")
        next_dash_left = (response_text.rfind('- ', 0, start_index)) + 2
        substring = response.text[next_dash_left:start_index]
        roles = [s.strip() for s in substring.split(',')]
        hero_attributes[hero] = roles
        
    return pd.DataFrame.from_dict(hero_attributes, orient='index', columns=['Role1', 'Role2', 'Role3', 'Role4', 'Role5', 'Role6'])

# Fetch hero counters and roles
if all(hero in heroes for hero in selected_heroes):
    counters = all_counters(selected_heroes)
    st.markdown("### Hero Counters")
    st.write(pd.DataFrame(counters, index=selected_heroes, columns=[f"Counter {i+1}" for i in range(5)]))
    
    roles_df = get_hero_roles(selected_heroes)
    st.markdown("### Hero Roles")
    st.write(roles_df)

    weakers1 = all_weakers(selected_heroes)
    st.markdown("### Hero Weakers")
    st.write(pd.DataFrame(weakers1, index=selected_heroes, columns=[f"Weaker {i+1}" for i in range(5)]))
else:
    st.write("Please enter valid hero names from the list.")