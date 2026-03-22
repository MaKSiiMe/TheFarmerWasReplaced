def farm():
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if can_harvest():
				harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Pumpkin)
			use_item(Items.Fertilizer)
			move(North)
		move(East)

	pumpkin_num = 0
	while pumpkin_num < get_world_size()**2:
		pumpkin_num = 0
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				if get_entity_type() == Entities.Dead_Pumpkin:
					harvest()
					plant(Entities.Pumpkin)
					use_item(Items.Fertilizer)
				else:
					pumpkin_num += 1
				move(North)
			move(East)
	do_a_flip()
	harvest()
