from move_to import move_to

# Cactus : on plante tout, on trie chaque colonne puis chaque ligne, et une seule
# récolte ramasse toute la ferme (n² cactus récoltés -> n⁴ cactus gagnés).
# Trier les colonnes puis les lignes suffit : trier les lignes ne détruit pas
# l'ordre des colonnes, donc un seul passage de chaque (au lieu de 5 avant).
# Tri cocktail "double face" : sur chaque case, le drone remet en ordre la paire
# derrière lui, la paire devant, puis encore celle derrière (measure() ne coûte
# qu'un tick, seuls swap et move coûtent cher). Simulé sur 2000 colonnes :
# ~490 actions par colonne au lieu de ~650 avec un cocktail simple.
# La colonne est déjà dégrossie pendant la plantation, et le tri repart du haut.


def _fix(fwd, back, pos, lo, hi):
	# Renvoie True si au moins un échange a été fait
	moved = False
	if pos > lo and measure(back) > measure():
		swap(back)
		moved = True
	if pos < hi and measure() > measure(fwd):
		swap(fwd)
		moved = True
	if pos > lo and measure(back) > measure():
		swap(back)
		moved = True
	return moved


def _sort(fwd, back, n, pos):
	# Tri d'une ligne de n cases ; le drone est à l'indice pos (0 ou n-1)
	lo = 0
	hi = n - 1
	going_back = pos > 0
	while lo < hi:
		mark = -1
		if going_back:
			while True:
				if _fix(fwd, back, pos, lo, hi):
					mark = pos
				if pos <= lo + 1:
					break
				move(back)
				pos -= 1
			if mark < 0:
				return
			lo = max(lo, mark - 1)
		else:
			while True:
				if _fix(fwd, back, pos, lo, hi):
					mark = pos
				if pos >= hi - 1:
					break
				move(fwd)
				pos += 1
			if mark < 0:
				return
			hi = min(hi, mark + 1)
		going_back = not going_back


def _col():
	n = get_world_size()
	for y in range(n):
		if get_entity_type() != None:
			harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Cactus)
		if y > 0 and measure(South) > measure():
			swap(South)
		if y < n - 1:
			move(North)
	_sort(North, South, n, n - 1)


def _row():
	_sort(East, West, get_world_size(), 0)


def farm(target=None):
	if target == None:
		target = num_items(Items.Cactus) + 1
	clear()
	n = get_world_size()
	while num_items(Items.Cactus) < target:
		# Planter + trier les colonnes en parallèle
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

		# Trier les lignes en parallèle
		move_to(0, 0)
		handles = []
		for _ in range(n - 1):
			d = spawn_drone(_row)
			if d != None:
				handles.append(d)
			move(North)
		_row()
		for d in handles:
			wait_for(d)

		# Une récolte pour toute la ferme
		while not can_harvest():
			pass
		harvest()


# Lancé directement : farme cette ressource sans fin (arrête le programme quand tu veux)
if __name__ == "__main__":
	farm(1000000000000000)
