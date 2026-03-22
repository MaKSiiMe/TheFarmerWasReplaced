from move_to import move_to

# Gradient Bubble Sort with backtracking
# Reads the entire grid into memory to avoid unnecessary measure() calls during sort
# Cascade condition: values increase going North and East
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
		# Sort columns: values increase going North (increasing y)
		for x in range(size):
			for y in range(size - 1):
				if grid[(x, y)] > grid[(x, y + 1)]:
					move_to(x, y)
					swap(North)
					grid[(x, y)], grid[(x, y + 1)] = grid[(x, y + 1)], grid[(x, y)]
					changed = True
					# Backtrack: push the small value as far South as possible
					yy = y - 1
					while yy >= 0 and grid[(x, yy)] > grid[(x, yy + 1)]:
						move_to(x, yy)
						swap(North)
						grid[(x, yy)], grid[(x, yy + 1)] = grid[(x, yy + 1)], grid[(x, yy)]
						yy -= 1
		# Sort rows: values increase going East (increasing x)
		for y in range(size):
			for x in range(size - 1):
				if grid[(x, y)] > grid[(x + 1, y)]:
					move_to(x, y)
					swap(East)
					grid[(x, y)], grid[(x + 1, y)] = grid[(x + 1, y)], grid[(x, y)]
					changed = True
					# Backtrack: push the small value as far West as possible
					xx = x - 1
					while xx >= 0 and grid[(xx, y)] > grid[(xx + 1, y)]:
						move_to(xx, y)
						swap(East)
						grid[(xx, y)], grid[(xx + 1, y)] = grid[(xx + 1, y)], grid[(xx, y)]
						xx -= 1

def farm():
	size = get_world_size()
	# Plant all cacti
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
	# Wait for all cacti to grow (1s)
	do_a_flip()
	# Sort then trigger cascade harvest (yield = n²)
	sort()
	move_to(0, 0)
	harvest()
