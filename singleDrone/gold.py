# Returns unvisited directions sorted by distance to treasure
# Best directions are at the END of the list (for O(1) pop())
def get_dirs(visited):
	pos = measure()
	if pos == None:
		return []
	tx = pos[0]
	ty = pos[1]
	cx = get_pos_x()
	cy = get_pos_y()
	offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
	dirs_list = [North, East, South, West]
	valid_dirs = []
	valid_scores = []
	for i in range(4):
		nx = cx + offsets[i][0]
		ny = cy + offsets[i][1]
		if can_move(dirs_list[i]) and (nx, ny) not in visited:
			valid_dirs.append(dirs_list[i])
			valid_scores.append((tx - nx)**2 + (ty - ny)**2)
	# Sort descending by score → pop() returns the closest direction to treasure
	for i in range(len(valid_dirs)):
		for j in range(len(valid_dirs) - 1 - i):
			if valid_scores[j] < valid_scores[j + 1]:
				valid_scores[j], valid_scores[j + 1] = valid_scores[j + 1], valid_scores[j]
				valid_dirs[j], valid_dirs[j + 1] = valid_dirs[j + 1], valid_dirs[j]
	return valid_dirs

def farm():
	# Create the maze
	plant(Entities.Bush)
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)

	visited = {}
	visited[(get_pos_x(), get_pos_y())] = True
	stack = [get_dirs(visited)]
	back = []

	# DFS with measure() heuristic: always explore the direction closest to the treasure first
	while get_entity_type() != Entities.Treasure:
		if len(stack) == 0:
			stack.append(get_dirs(visited))
			continue
		dirs = stack[-1]
		if len(dirs) > 0:
			# Move in the best available direction
			d = dirs.pop()
			cx = get_pos_x()
			cy = get_pos_y()
			if d == North:
				nx, ny = cx, cy + 1
			elif d == East:
				nx, ny = cx + 1, cy
			elif d == South:
				nx, ny = cx, cy - 1
			else:
				nx, ny = cx - 1, cy
			visited[(nx, ny)] = True
			back.append(d)
			move(d)
			stack.append(get_dirs(visited))
		else:
			# Dead end: backtrack to previous tile
			stack.pop()
			if len(back) > 0:
				b = back.pop()
				if b == North:
					move(South)
				elif b == South:
					move(North)
				elif b == East:
					move(West)
				else:
					move(East)

	harvest()
