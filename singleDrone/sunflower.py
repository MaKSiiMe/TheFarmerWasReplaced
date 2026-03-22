def farm():
	petal_counter = 15
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if can_harvest():
				harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Sunflower)
			use_item(Items.Fertilizer)
			move(North)
		move(East)
	
	while petal_counter >= 7:
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				if can_harvest():
					if measure() == petal_counter:
						harvest()
				move(North)
			move(East)
		petal_counter -= 1
