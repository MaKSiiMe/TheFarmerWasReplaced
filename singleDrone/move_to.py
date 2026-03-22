# Moves the drone to (tx, ty) using the shortest path.
# Uses modular arithmetic to handle farm wrapping (going West can be faster than East).
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
