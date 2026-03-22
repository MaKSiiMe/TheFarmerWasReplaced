def farm():
	# Phase 1: plant the entire farm
	for _ in range(get_world_size()):
		for _ in range(get_world_size()):
			if can_harvest():
				harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Pumpkin)
			use_item(Items.Fertilizer)
			move(North)
		move(East)

	# Phase 2: replace dead pumpkins until the whole farm is alive
	# ~1 in 5 pumpkins dies — a dead pumpkin breaks the mega-pumpkin group
	pumpkin_num = 0
	while pumpkin_num < get_world_size()**2:
		pumpkin_num = 0
		for _ in range(get_world_size()):
			for _ in range(get_world_size()):
				if get_entity_type() == Entities.Dead_Pumpkin:
					harvest()
					plant(Entities.Pumpkin)
					use_item(Items.Fertilizer)
				else:
					pumpkin_num += 1
				move(North)
			move(East)

	# Harvest the entire farm as one mega-pumpkin (yield = n³)
	do_a_flip()
	harvest()
