from settings import screen_height

level_0 = {
    'terrain': './levels/0/level_0_Tiles.csv',
    'fg palms': './levels/0/level_0_Palms.csv',
    'bg palms': './levels/0/level_0_Backround.csv',
    'crates': './levels/0/level_0_Crates.csv',
    'enemies': './levels/0/level_0_Enemies.csv',
    'constraints': './levels/0/level_0_Barriers.csv',
    'player': './levels/0/level_0_Player.csv',
    'grass': './levels/0/level_0_Grass.csv',
}

level_1 = {
    'terrain': './levels/1/level_1_Tiles.csv',
    'fg palms': './levels/1/level_1_Palms.csv',
    'bg palms': './levels/1/level_1_Backround.csv',
    'crates': './levels/1/level_1_Crates.csv',
    'enemies': './levels/1/level_1_Enemies.csv',
    'constraints': './levels/1/level_1_Barriers.csv',
    'player': './levels/1/level_1_Player.csv',
    'grass': './levels/1/level_1_Grass.csv',
}

level_2 = {
    'terrain': './levels/2/level_2_Tiles.csv',
    'fg palms': './levels/2/level_2_Palms.csv',
    'bg palms': './levels/2/level_2_Backround.csv',
    'crates': './levels/2/level_2_Crates.csv',
    'enemies': './levels/2/level_2_Enemies.csv',
    'constraints': './levels/2/level_2_Barriers.csv',
    'player': './levels/2/level_2_Player.csv',
    'grass': './levels/2/level_2_Grass.csv',
}

level_3 = {
    'terrain': './levels/3/level_3_Tiles.csv',
    'fg palms': './levels/3/level_3_Palms.csv',
    'bg palms': './levels/3/level_3_Backround.csv',
    'crates': './levels/3/level_3_Crates.csv',
    'enemies': './levels/3/level_3_Enemies.csv',
    'constraints': './levels/3/level_3_Barriers.csv',
    'player': './levels/3/level_3_Player.csv',
    'grass': './levels/3/level_3_Grass.csv',
}

level_4 = {
    'terrain': './levels/4/level_4_Tiles.csv',
    'fg palms': './levels/4/level_4_Palms.csv',
    'bg palms': './levels/4/level_4_Backround.csv',
    'crates': './levels/4/level_4_Crates.csv',
    'enemies': './levels/4/level_4_Enemies.csv',
    'constraints': './levels/4/level_4_Barriers.csv',
    'player': './levels/4/level_4_Player.csv',
    'grass': './levels/4/level_4_Grass.csv',
}


levels = {
    0: level_0,
    1: level_1,
    2: level_2,
    3: level_3,
    4: level_4,
}

level_0_data = {'node_pos':(150, screen_height//2 + 50), 'unlock':1}
level_1_data = {'node_pos':(350,250), 'unlock':2}
level_2_data = {'node_pos':(575,screen_height-250), 'unlock':3}
level_3_data = {'node_pos':(775,250), 'unlock':4}
level_4_data = {'node_pos':(1050, screen_height//2 + 50), 'unlock':5}

level_data = {
	0: level_0_data,
	1: level_1_data,
	2: level_2_data,
	3: level_3_data,
	4: level_4_data,
    }
