def farm():
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if can_harvest():
				harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Carrot)
			use_item(Items.Fertilizer)
			move(North)
		move(East)
