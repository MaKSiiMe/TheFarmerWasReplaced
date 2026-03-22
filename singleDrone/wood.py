def farm():
	for _ in range(get_world_size()):
		for _ in range(get_world_size()):
			if can_harvest():
				harvest()
			if (get_pos_x() + get_pos_y()) % 2 == 0:
				plant(Entities.Tree)
			else:
				plant(Entities.Bush)
			use_item(Items.Fertilizer)
			move(North)
		move(East)
