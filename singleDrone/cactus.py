def move_to(tx, ty):
	size = get_world_size()
	while get_pos_x() != tx:
		dx = (tx - get_pos_x()) % size
		if dx <= size / 2:
			move(East)
		else:
			move(West)
	while get_pos_y() != ty:
		dy = (ty - get_pos_y()) % size
		if dy <= size / 2:
			move(North)
		else:
			move(South)

# Gradient Bubble Sort avec backtracking
# Lit toute la grille en mémoire → évite les measure() inutiles pendant le tri
# Valeurs croissantes vers le Nord et vers l'Est (condition cascade)
def sort():
	size = get_world_size()
	grid = {}
	for x in range(size):
		for y in range(size):
			move_to(x, y)
			grid[(x, y)] = measure()

	changed = True
	while changed:
		changed = False
		# Tri colonnes : valeurs croissantes vers le Nord (y croissant)
		for x in range(size):
			for y in range(size - 1):
				if grid[(x, y)] > grid[(x, y + 1)]:
					move_to(x, y)
					swap(North)
					grid[(x, y)], grid[(x, y + 1)] = grid[(x, y + 1)], grid[(x, y)]
					changed = True
					# Backtracking : pousse la petite valeur aussi loin au Sud que possible
					yy = y - 1
					while yy >= 0 and grid[(x, yy)] > grid[(x, yy + 1)]:
						move_to(x, yy)
						swap(North)
						grid[(x, yy)], grid[(x, yy + 1)] = grid[(x, yy + 1)], grid[(x, yy)]
						yy -= 1
		# Tri lignes : valeurs croissantes vers l'Est (x croissant)
		for y in range(size):
			for x in range(size - 1):
				if grid[(x, y)] > grid[(x + 1, y)]:
					move_to(x, y)
					swap(East)
					grid[(x, y)], grid[(x + 1, y)] = grid[(x + 1, y)], grid[(x, y)]
					changed = True
					# Backtracking : pousse la petite valeur aussi loin à l'Ouest que possible
					xx = x - 1
					while xx >= 0 and grid[(xx, y)] > grid[(xx + 1, y)]:
						move_to(xx, y)
						swap(East)
						grid[(xx, y)], grid[(xx + 1, y)] = grid[(xx + 1, y)], grid[(xx, y)]
						xx -= 1

def farm():
	size = get_world_size()
	# Planter tous les cactus
	for _ in range(size):
		for _ in range(size):
			if can_harvest():
				harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Cactus)
			use_item(Items.Fertilizer)
			move(North)
		move(East)
	# Attendre que tous soient prêts (1s)
	do_a_flip()
	# Trier puis récolter en cascade (rendement n²)
	sort()
	move_to(0, 0)
	harvest()
