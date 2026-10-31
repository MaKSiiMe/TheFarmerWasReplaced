# Snake (chapeau dinosaure) : cycle hamiltonien + raccourcis ("perturbed Hamiltonian cycle").
#
# Le serpent suit un cycle qui passe par toutes les cases de la ferme. Tant qu'il
# avance dans l'ordre du cycle, tout son corps reste "derrière" lui et il ne peut
# jamais se bloquer. Tant qu'il est court, il saute vers une case voisine plus loin
# dans le cycle, sans jamais sauter la pomme ni rattraper le bout de sa queue.
#
# Passé 30 % de la ferme, on arrête les raccourcis : ils laisseraient des trous dans
# le corps où les pommes tomberaient, ce qui obligerait à refaire des tours complets.
# Simulé (32x32) : ~155 000 moves et ~8,4M ticks contre ~244 000 moves et ~18M ticks
# avec des raccourcis jusqu'à la fin, 0 défaite sur 260 parties.
#
# Cycle : rangée y=0 vers l'Est, serpentin vertical de x=n-1 à x=1, retour par x=0.
# Les raccourcis possibles sont donc les voisins Est/Ouest dans le serpentin,
# le voisin Nord sur la rangée 0 et le voisin Est sur la colonne 0.
#
# Os gagnés = longueur² : on remplit toute la ferme avant de récolter.

SHORTCUT_UNTIL = 0.3


def _tables(n):
	# cx, cy : coordonnées de chaque position du cycle ; idx : position dans le cycle de (x, y)
	cx = []
	cy = []
	for x in range(n):
		cx.append(x)
		cy.append(0)
	for c in range(n - 1):
		x = n - 1 - c
		if c % 2 == 0:
			for y in range(1, n):
				cx.append(x)
				cy.append(y)
		else:
			for y in range(n - 1, 0, -1):
				cx.append(x)
				cy.append(y)
	for y in range(n - 1, 0, -1):
		cx.append(0)
		cy.append(y)
	N = n * n
	idx = []
	for _ in range(N):
		idx.append(0)
	nd = []
	for k in range(N):
		idx[cx[k] * n + cy[k]] = k
	for k in range(N - 1):
		if cx[k + 1] > cx[k]:
			nd.append(East)
		elif cx[k + 1] < cx[k]:
			nd.append(West)
		elif cy[k + 1] > cy[k]:
			nd.append(North)
		else:
			nd.append(South)
	nd.append(South)
	return cx, cy, idx, nd


def _run(n, cx, cy, idx, nd):
	N = n * n
	m = n - 1
	stop = N * SHORTCUT_UNTIL
	body = []
	for _ in range(N):
		body.append(0)

	clear()
	change_hat(Hats.Dinosaur_Hat)
	h = 0
	s = 0
	L = 0
	# On démarre sur la première pomme : measure() donne la position de la suivante
	grow = True
	last = False
	a = -1
	p = measure()
	if p == None:
		last = True
	else:
		a = idx[p[0] * n + p[1]]

	# Phase 1 : serpent court, raccourcis vers la pomme
	while L < stop and a >= 0:
		dt = (body[(s - L) % N] - h) % N
		if dt == 0:
			dt = N
		da = (a - h) % N
		lim = dt - 3
		if da < lim:
			lim = da
		if da < dt:
			# Marge pour la croissance (et les pommes suivantes si la place se réduit)
			lim -= 1
			if (dt - da) * 4 > N - L - 1:
				lim -= 10
		nh = h + 1
		dr = nd[h]
		if lim > 1:
			best = 1
			x = cx[h]
			y = cy[h]
			if y == 0:
				j = idx[x * n + 1]
				d = (j - h) % N
				if d <= lim and d > best:
					nh = j
					dr = North
			else:
				if x > 0:
					j = idx[(x - 1) * n + y]
					d = (j - h) % N
					if d <= lim and d > best:
						best = d
						nh = j
						dr = West
				if x < m:
					j = idx[(x + 1) * n + y]
					d = (j - h) % N
					if d <= lim and d > best:
						nh = j
						dr = East
		if not move(dr):
			if dr == nd[h] or not move(nd[h]):
				break
			nh = h + 1
		if nh == N:
			nh = 0
		if grow:
			L += 1
			grow = False
		h = nh
		s += 1
		if s == N:
			s = 0
		body[s] = h
		if h == a:
			grow = True
			p = measure()
			if p == None:
				last = True
				a = -1
			else:
				a = idx[p[0] * n + p[1]]

	# Phase 2 : on suit le cycle sans calcul jusqu'à remplir la ferme
	# (sauf si plus aucune pomme n'apparaît : on mange la dernière et on s'arrête)
	while move(nd[h]):
		if last:
			break
		h += 1
		if h == N:
			h = 0
		if h == a:
			L += 1
			p = measure()
			if p == None:
				last = True
			else:
				a = idx[p[0] * n + p[1]]

	# Enlever le chapeau récolte la queue
	change_hat(Hats.Straw_Hat)
	quick_print("Snake termine, longueur environ", L)


def farm(target=None):
	if target == None:
		target = num_items(Items.Bone) + 1
	n = get_world_size()
	quick_print("Snake : preparation du cycle")
	cx, cy, idx, nd = _tables(n)
	while num_items(Items.Bone) < target:
		cost = get_cost(Entities.Apple)
		for it in cost:
			if num_items(it) < cost[it] * n * n:
				print("Pas assez de", it)
				quick_print("Pas assez de", it, ": il faut", cost[it] * n * n, "pour remplir la ferme")
				return False
		_run(n, cx, cy, idx, nd)
	return True


# Lancé directement : farme cette ressource sans fin (arrête le programme quand tu veux)
if __name__ == "__main__":
	farm(1000000000000000)
