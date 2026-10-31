from move_to import move_to

# Citrouilles : toute la ferme devient une seule méga-citrouille (n*n*6 pour n >= 6).
# Chaque drone plante sa colonne puis ne revisite que les cases pas encore prêtes,
# en remplaçant les citrouilles mortes, jusqu'à ce que toute sa colonne soit mûre.


def _col():
	n = get_world_size()
	for _ in range(n):
		if get_entity_type() != None:
			harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Pumpkin)
		if get_water() < 0.75:
			use_item(Items.Water)
		move(North)
	pending = []
	for y in range(n):
		pending.append(y)
	y = 0
	while len(pending) > 0:
		left = []
		for t in pending:
			while y != t:
				move(North)
				y = (y + 1) % n
			e = get_entity_type()
			if e == Entities.Dead_Pumpkin or e == None:
				if plant(Entities.Pumpkin):
					if get_water() < 0.75:
						use_item(Items.Water)
					left.append(t)
			elif not can_harvest():
				left.append(t)
		pending = left


def farm(target=None):
	if target == None:
		target = num_items(Items.Pumpkin) + 1
	clear()
	n = get_world_size()
	while num_items(Items.Pumpkin) < target:
		move_to(0, 0)
		handles = []
		for _ in range(n - 1):
			d = spawn_drone(_col)
			if d != None:
				handles.append(d)
			move(East)
		_col()
		for d in handles:
			wait_for(d)
		while not can_harvest():
			pass
		harvest()


# Lancé directement : farme cette ressource sans fin (arrête le programme quand tu veux)
if __name__ == "__main__":
	farm(1000000000000000)
