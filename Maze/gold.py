from move_to import move_to

# Or : 16 labyrinthes 8x8 (grille 4x4), 2 drones par labyrinthe.
#
# - Or par trésor = aire du labyrinthe x bonus Mazes, Weird_Substance par trésor = côté x bonus
#   -> un 8x8 donne 8 or par Weird_Substance.
# - Chaque labyrinthe est réutilisé jusqu'à 300 fois : on le cartographie une seule fois,
#   puis chaque trésor est atteint par le plus court chemin (BFS) sur la carte.
#   La carte s'enrichit en route, car des murs disparaissent à chaque déplacement du trésor.
# - Chaque drone s'occupe d'une moitié du labyrinthe et attend au centre de sa moitié
#   quand le trésor est chez l'autre.

DIRS = [North, East, South, West]
MAZE = 8


def _scan(op, c, lx, ly, m):
	# Note les passages ouverts autour de la case c (et le passage inverse chez le voisin)
	if ly < m - 1 and can_move(North):
		op[c * 4] = True
		op[(c + 1) * 4 + 2] = True
	if lx < m - 1 and can_move(East):
		op[c * 4 + 1] = True
		op[(c + m) * 4 + 3] = True
	if ly > 0 and can_move(South):
		op[c * 4 + 2] = True
		op[(c - 1) * 4] = True
	if lx > 0 and can_move(West):
		op[c * 4 + 3] = True
		op[(c - m) * 4 + 1] = True


def _explore(x0, y0, m):
	# Parcours en profondeur de tout le labyrinthe, renvoie la carte des passages
	op = []
	seen = []
	for _ in range(m * m):
		seen.append(False)
		for _ in range(4):
			op.append(False)
	delta = [1, m, -1, -m]
	lx = get_pos_x() - x0
	ly = get_pos_y() - y0
	c = lx * m + ly
	seen[c] = True
	_scan(op, c, lx, ly, m)
	back = []
	while True:
		moved = False
		for d in range(4):
			if op[c * 4 + d]:
				if not seen[c + delta[d]]:
					move(DIRS[d])
					c = c + delta[d]
					seen[c] = True
					_scan(op, c, c // m, c % m, m)
					back.append((d + 2) % 4)
					moved = True
					break
		if not moved:
			if len(back) == 0:
				return op
			d = back.pop()
			move(DIRS[d])
			c = c + delta[d]


def _goto(op, x0, y0, m, tx, ty):
	# Plus court chemin sur la carte connue (BFS lancé depuis la cible)
	delta = [1, m, -1, -m]
	src = (get_pos_x() - x0) * m + get_pos_y() - y0
	dst = (tx - x0) * m + ty - y0
	if src == dst:
		return True
	step = []
	for _ in range(m * m):
		step.append(-1)
	step[dst] = 4
	q = [dst]
	qi = 0
	found = False
	while qi < len(q) and not found:
		c = q[qi]
		qi += 1
		for d in range(4):
			if op[c * 4 + d]:
				nc = c + delta[d]
				if step[nc] < 0:
					step[nc] = (d + 2) % 4
					if nc == src:
						found = True
					q.append(nc)
	if not found:
		return False
	c = src
	while c != dst:
		d = step[c]
		if not move(DIRS[d]):
			return False
		c = c + delta[d]
		_scan(op, c, c // m, c % m, m)
	return True


def _worker(x0, y0, m, role, target, total):
	# Attendre que tous les drones soient placés : un labyrinthe créé trop tôt
	# bloquerait le drone principal qui doit encore aller placer les autres
	while num_drones() < total:
		pass
	sub = m * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
	half = m // 2
	cx = x0 + half
	cy = y0 + half
	# Case d'attente : centre de sa moitié du labyrinthe
	px = x0 + half // 2 + role * half
	py = cy
	op = None
	while num_items(Items.Gold) < target:
		t = measure()
		if t == None:
			# Pas de labyrinthe : le drone 0 le crée, le drone 1 attend
			if role == 0:
				if num_items(Items.Weird_Substance) < sub:
					return
				move_to(cx, cy)
				if get_entity_type() != None:
					harvest()
				plant(Entities.Bush)
				use_item(Items.Weird_Substance, sub)
			else:
				while measure() == None:
					if num_items(Items.Weird_Substance) < sub or num_items(Items.Gold) >= target:
						return
			op = _explore(x0, y0, m)
			continue
		if op == None:
			op = _explore(x0, y0, m)
		mine = (t[0] - x0 < half) == (role == 0)
		if mine:
			if not _goto(op, x0, y0, m, t[0], t[1]):
				# Carte périmée (labyrinthe recréé) : on recartographie
				op = None
				continue
			if get_entity_type() == Entities.Treasure:
				use_item(Items.Weird_Substance, sub)
				if get_entity_type() == Entities.Treasure:
					# Le trésor n'a pas bougé (300 déplacements atteints) : on le récolte
					# et le drone 0 recrée un labyrinthe. Ne jamais quitter ici, sinon
					# l'autre drone du labyrinthe reste bloqué à attendre.
					harvest()
		elif get_pos_x() != px or get_pos_y() != py:
			if not _goto(op, x0, y0, m, px, py):
				op = None
		else:
			while measure() == t and num_items(Items.Gold) < target:
				pass


def farm(target=None):
	if target == None:
		target = num_items(Items.Gold) + 1
	m = MAZE
	n = get_world_size()
	k = n // m
	sub = m * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
	if num_items(Items.Weird_Substance) < sub * k * k * 4:
		quick_print("Pas assez de Weird_Substance pour les labyrinthes")
		return False
	clear()
	jobs = []
	for i in range(k):
		for j in range(k):
			jobs.append((i * m, j * m, 0))
			jobs.append((i * m, j * m, 1))
	# Pas plus de jobs que de drones (les paires restent complètes : 0 puis 1)
	while len(jobs) > max_drones():
		jobs.pop()
	total = len(jobs)
	handles = []
	last = jobs.pop()
	for jb in jobs:
		move_to(jb[0] + m // 2, jb[1] + m // 2)
		d = spawn_drone(_worker, jb[0], jb[1], m, jb[2], target, total)
		if d != None:
			handles.append(d)
	move_to(last[0] + m // 2, last[1] + m // 2)
	_worker(last[0], last[1], m, last[2], target, total)
	for d in handles:
		wait_for(d)
	return True


# Lancé directement : farme cette ressource sans fin (arrête le programme quand tu veux)
if __name__ == "__main__":
	farm(1000000000000000)
