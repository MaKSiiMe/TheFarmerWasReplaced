# --- Choisir UNE des deux lignes ci-dessous ---
leaderboard_run(Leaderboards.Pumpkins, "leaderboard_pumpkins", 256)
# simulate("leaderboard_pumpkins", Unlocks, {}, {}, 1, 256)


def plant_col():
	for _ in range(get_world_size()):
		if get_entity_type() != None:
			harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		if get_water() < 0.75:
			use_item(Items.Water)
		plant(Entities.Pumpkin)
		use_item(Items.Fertilizer)
		move(North)


def maintain_col():
	"""Remplace les pumpkins morts et boucle jusqu'à ce que toute la colonne soit prête."""
	while True:
		ready = True
		for _ in range(get_world_size()):
			e = get_entity_type()
			if e == Entities.Dead_Pumpkin:
				harvest()
				if get_water() < 0.75:
					use_item(Items.Water)
				plant(Entities.Pumpkin)
				use_item(Items.Fertilizer)
				ready = False
			elif e != None and not can_harvest():
				ready = False
			move(North)
		if ready:
			return


size = get_world_size()

# Phase 1: planter toutes les colonnes en parallèle
handles = []
for _ in range(size - 1):
	handles.append(spawn_drone(plant_col))
	move(East)
plant_col()
for h in handles:
	wait_for(h)

# Phase 2: chaque drone gère sa colonne en boucle interne jusqu'à ce que tout soit prêt
handles = []
for _ in range(size - 1):
	handles.append(spawn_drone(maintain_col))
	move(East)
maintain_col()
for h in handles:
	wait_for(h)

# Phase 3: récolter le mega-pumpkin
do_a_flip()
harvest()
