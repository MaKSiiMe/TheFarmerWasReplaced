# Course Wood : 32 drones, ferme 32x32, objectif 10 milliards de bois, puis le programme s'arrête.
#
# Ici c'est le temps de pousse des arbres qui limite (≈ 7 s sans eau, ≈ 1,4 s avec eau
# pleine, x2 par arbre voisin), pas le nombre d'actions. Donc :
# - damier : un arbre sur deux cases (aucun arbre n'a d'arbre voisin), compagnons ailleurs ;
# - chaque drone a un bloc de 4x8 qu'il parcourt en boucle (cycle de 32 cases) ;
# - il retient la demande de chaque arbre replanté et, en passant sur la case demandée
#   (si elle est dans son bloc), il y plante le bon type ;
# - un arbre mûr dont le compagnon va être planté attend au plus un tour avant d'être
#   récolté (un bonus x160 vaut bien ~2 s d'attente) ;
# - eau sur les arbres dès qu'il en reste assez pour tous les drones.

TARGET = 10000000000
BW = 4
BH = 8


def _path():
	# Cycle hamiltonien d'un bloc 4x8 (positions locales) et direction vers la case suivante
	cells = []
	for x in range(BW):
		cells.append((x, 0))
	for c in range(BW - 1):
		x = BW - 1 - c
		if c % 2 == 0:
			for y in range(1, BH):
				cells.append((x, y))
		else:
			for y in range(BH - 1, 0, -1):
				cells.append((x, y))
	for y in range(BH - 1, 0, -1):
		cells.append((0, y))
	dirs = []
	for i in range(len(cells)):
		a = cells[i]
		b = cells[(i + 1) % len(cells)]
		if b[0] > a[0]:
			dirs.append(East)
		elif b[0] < a[0]:
			dirs.append(West)
		elif b[1] > a[1]:
			dirs.append(North)
		else:
			dirs.append(South)
	return cells, dirs


def _add(want, p, t):
	if p in want:
		d = want[p]
		if t in d:
			d[t] += 1
		else:
			d[t] = 1
	else:
		want[p] = {t: 1}


def _remove(want, p, t):
	d = want[p]
	d[t] -= 1
	if d[t] == 0:
		d.pop(t)
		if len(d) == 0:
			want.pop(p)


def _worker(x0, y0, target, report):
	t_start = get_time()
	cells, dirs = _path()
	n = len(cells)
	pos = []
	tree = []
	for c in cells:
		pos.append((x0 + c[0], y0 + c[1]))
		tree.append((x0 + c[0] + y0 + c[1]) % 2 == 0)
	content = {}
	for i in range(n):
		if not tree[i]:
			content[pos[i]] = Entities.Bush
	req = {}
	want = {}
	waited = {}
	carrot_cost = get_cost(Entities.Carrot)

	# Mise en place : sol labouré, arbres en damier, buissons ailleurs
	for i in range(n):
		if get_entity_type() != None:
			harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		if tree[i]:
			plant(Entities.Tree)
			c = get_companion()
			req[pos[i]] = c
			if c != None and c[1] in content:
				_add(want, c[1], c[0])
		else:
			plant(Entities.Bush)
		move(dirs[i])

	t_loop = get_time()
	harvests = 0
	waits = 0
	fixes = 0
	not_grown = 0
	while num_items(Items.Wood) < target:
		for i in range(n):
			p = pos[i]
			if tree[i]:
				if can_harvest():
					r = req[p]
					if r != None and r[1] in content and content[r[1]] != r[0] and not (p in waited):
						# Son compagnon peut encore être planté : on attend un tour
						waited[p] = True
						waits += 1
					else:
						if p in waited:
							waited.pop(p)
						harvest()
						harvests += 1
						if r != None and r[1] in content:
							_remove(want, r[1], r[0])
						plant(Entities.Tree)
						if get_water() < 0.75 and num_items(Items.Water) >= 64:
							use_item(Items.Water)
						c = get_companion()
						req[p] = c
						if c != None and c[1] in content:
							_add(want, c[1], c[0])
				else:
					not_grown += 1
			elif p in want:
				# Planter le type le plus demandé par les arbres en attente
				d = want[p]
				cur = content[p]
				best = cur
				bc = 0
				if cur in d:
					bc = d[cur]
				for t in d:
					if d[t] > bc:
						best = t
						bc = d[t]
				if best == Entities.Carrot:
					for it in carrot_cost:
						if num_items(it) < carrot_cost[it]:
							best = cur
				if best != cur:
					harvest()
					if plant(best):
						content[p] = best
					else:
						plant(cur)
					fixes += 1
			move(dirs[i])
	if report:
		t_end = get_time()
		quick_print("STATS bloc", x0, y0, ": preparation", t_loop - t_start, "s, boucle", t_end - t_loop, "s")
		quick_print("STATS recoltes", harvests, "attentes compagnon", waits, "corrections", fixes, "arbre pas mur", not_grown)
		quick_print("STATS eau du sol", get_water(), "stock eau", num_items(Items.Water), "bois", num_items(Items.Wood))


def _go(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)


def _run():
	n = get_world_size()
	blocks = []
	for j in range(n // BH):
		for i in range(n // BW):
			blocks.append((i * BW, j * BH))
	last = blocks.pop()
	handles = []
	for b in blocks:
		_go(b[0], b[1])
		d = spawn_drone(_worker, b[0], b[1], TARGET, False)
		if d != None:
			handles.append(d)
	_go(last[0], last[1])
	_worker(last[0], last[1], TARGET, True)
	for d in handles:
		wait_for(d)


if __name__ == "__main__":
	_run()
