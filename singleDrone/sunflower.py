from move_to import move_to

def farm():
	size = get_world_size()
	# buckets[petal] = list of (x, y) positions ready to harvest
	buckets = {}
	total_on_farm = 0

	# Phase 1: single scan — plant empty tiles + collect harvestable positions
	for _ in range(size):
		for _ in range(size):
			e = get_entity_type()
			if e != Entities.Sunflower:
				if e != None:
					harvest()
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Sunflower)
				use_item(Items.Water)
			if get_entity_type() == Entities.Sunflower:
				total_on_farm += 1
				if can_harvest():
					p = measure()
					if p not in buckets:
						buckets[p] = []
					buckets[p].append((get_pos_x(), get_pos_y()))
			move(North)
		move(East)

	# Phase 2: harvest 15 → 7, every harvest gets the 5x bonus
	# Always keep at least 9 sunflowers on the farm (required for the 5x bonus)
	for petal in range(15, 6, -1):
		if petal not in buckets:
			continue
		for pos in buckets[petal]:
			if total_on_farm <= 9:
				return
			x = pos[0]
			y = pos[1]
			move_to(x, y)
			if can_harvest():
				harvest()
				total_on_farm -= 1
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Sunflower)
				use_item(Items.Water)
				total_on_farm += 1
