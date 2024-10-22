import pandas as pd
import requests as req
from io import StringIO

heroes = ['anti-mage', 'axe', 'bane', 'bloodseeker', 'crystal-maiden', 'drow-ranger', 'earthshaker', 'juggernaut', 'mirana', 'morphling', 'shadow-fiend', 'phantom-lancer', 'puck', 'pudge', 'razor', 'sand-king', 'storm-spirit', 'sven', 'tiny', 'vengeful-spirit', 'windranger', 'zeus', 'kunkka', 'lina', 'lion', 'shadow-shaman', 'slardar', 'tidehunter', 'witch-doctor', 'lich', 'riki', 'enigma', 'tinker', 'sniper', 'necrophos', 'warlock', 'beastmaster', 'queen-of-pain', 'venomancer', 'faceless-void', 'wraith-king', 'death-prophet', 'phantom-assassin', 'pugna', 'templar-assassin', 'viper', 'luna', 'dragon-knight', 'dazzle', 'clockwerk', 'leshrac', "nature's-prophet", 'lifestealer', 'dark-seer', 'clinkz', 'omniknight', 'enchantress', 'huskar', 'night-stalker', 'broodmother', 'bounty-hunter', 'weaver', 'jakiro', 'batrider', 'chen', 'spectre', 'ancient-apparition', 'doom', 'ursa', 'spirit-breaker', 'gyrocopter', 'alchemist', 'invoker', 'silencer', 'outworld-destroyer', 'lycan', 'brewmaster', 'shadow-demon', 'lone-druid', 'chaos-knight', 'meepo', 'treant-protector', 'ogre-magi', 'undying', 'rubick', 'disruptor', 'nyx-assassin', 'naga-siren', 'keeper-of-the-light', 'io', 'visage', 'slark', 'medusa', 'troll-warlord', 'centaur-warrunner', 'magnus', 'timbersaw', 'bristleback', 'tusk', 'skywrath-mage', 'abaddon', 'elder-titan', 'legion-commander', 'techies', 'ember-spirit', 'earth-spirit', 'underlord', 'terrorblade', 'phoenix', 'oracle', 'winter-wyvern', 'arc-warden', 'monkey-king', 'dark-willow', 'pangolier', 'grimstroke', 'hoodwink', 'void-spirit', 'snapfire', 'mars', 'dawnbreaker', 'marci', 'primal-beast', 'muerta']
hero_attributes = {}
request_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
    }    
for hero in heroes:
    
    DATA_URL = "https://pt.dotabuff.com/heroes/"+hero
    response = req.get(DATA_URL, headers=request_headers)   
    response_text = response.text
    start_index = response.text.find(" - DOTABUFF")
    next_dash_left = (response_text.rfind('- ', 0, start_index))+2
    substring = response.text[next_dash_left:start_index]
    individual_strings = [s.strip() for s in substring.split(',')]
    hero_attributes[hero] = individual_strings
    print(f"{hero}                ", end="\r")

df = pd.DataFrame.from_dict(hero_attributes, orient='index', columns=['Role1', 'Role2', 'Role3', 'Role4', 'Role5', 'Role6', 'Role7'])

print(df.head)
html_tables = pd.read_html(StringIO(response.text), index_col=0)     


            