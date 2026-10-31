from move_to import move_to

# Moteur de polyculture utilisé par grass.py, wood.py et carrot.py.
#
# La ferme est découpée en blocs de 4x8 (32 blocs = 32 drones sur une ferme 32x32).
# Dans chaque bloc, quelques cases "maison" portent la culture principale ; toutes les
# autres cases servent à planter le compagnon demandé par chaque maison.
# Une récolte avec son compagnon rapporte x5, doublé à chaque amélioration de Polyculture.
#
# Pour chaque maison : récolter -> replanter -> lire get_companion().
# Si le compagnon tombe hors du bloc, sur une maison, ou sur une case déjà réservée
# pour un autre type, on détruit la jeune pousse et on replante pour retirer au sort
# (2 actions, bien moins cher que de perdre le multiplicateur).
# Le drone retient ce qu'il a planté, donc un compagnon déjà en place ne coûte aucun trajet.

BLOCK_W = 4
BLOCK_H = 8


def _homes(main):
	# Maisons non adjacentes (les arbres poussent 2x moins vite par arbre voisin)
	if main == Entities.Grass:
		return [(1, 2), (2, 5)]
	if main == Entities.Bush:
		return [(1, 1), (2, 4), (1, 6)]
	return [(1, 1), (2, 3), (1, 5), (2, 6)]


def _prepare(entity):
	# Plante `entity` sous le drone en remplaçant ce qui s'y trouve ; renvoie True si elle y est
	e = get_entity_type()
	if e == entity:
		return True
	if e != None:
		harvest()
	if entity == Entities.Grass:
		if get_ground_type() == Grounds.Soil:
			till()
		if get_entity_type() == Entities.Grass:
			return True
	elif entity == Entities.Carrot:
		if get_ground_type() != Grounds.Soil:
			till()
	return plant(entity)


def _affordable(entity):
	cost = get_cost(entity)
	for it in cost:
		if num_items(it) < cost[it]:
			return False
	return True


def _companion(p, main, x0, y0, w, h, is_home, content, claims, home_slot):
	for _ in range(6):
		c = get_companion()
		if c == None:
			return
		typ = c[0]
		s = c[1]
		lx = s[0] - x0
		ly = s[1] - y0
		ok = lx >= 0 and lx < w and ly >= 0 and ly < h and not (s in is_home)
		if ok and s in claims and claims[s] > 0 and content[s] != typ:
			ok = False
		if ok and main == Entities.Tree and typ == Entities.Tree:
			if abs(s[0] - p[0]) + abs(s[1] - p[1]) == 1:
				ok = False
		present = s in content and content[s] == typ
		if ok and not present and not _affordable(typ):
			# Pas les ressources pour ce compagnon (ex. carottes en début de course)
			ok = False
		if ok:
			if not present:
				move_to(s[0], s[1])
				if not _prepare(typ):
					if s in content:
						content.pop(s)
					return
				content[s] = typ
			if s in claims:
				claims[s] = claims[s] + 1
			else:
				claims[s] = 1
			home_slot[p] = s
			return
		# Compagnon impossible : on retire au sort
		harvest()
		_prepare(main)


def _worker(x0, y0, w, h, main, item, target, homes):
	is_home = {}
	for p in homes:
		is_home[p] = True
	content = {}
	claims = {}
	home_slot = {}
	while num_items(item) < target:
		for p in homes:
			move_to(p[0], p[1])
			if get_entity_type() == main and not can_harvest():
				continue
			if can_harvest():
				harvest()
			if p in home_slot:
				s = home_slot.pop(p)
				claims[s] = claims[s] - 1
			_prepare(main)
			# Assez d'eau pour tous les drones, sinon ils se la disputent au même instant
			if get_water() < 0.75 and num_items(Items.Water) >= 32:
				use_item(Items.Water)
			_companion(p, main, x0, y0, w, h, is_home, content, claims, home_slot)


def farm(main, item, target):
	clear()
	n = get_world_size()
	rel = _homes(main)
	bx = n // BLOCK_W
	by = n // BLOCK_H
	if max_drones() < bx * by:
		# Pas assez de drones pour un bloc chacun (ex. course à un seul drone) :
		# un seul drone gère toute la ferme, avec les maisons de tous les blocs
		homes = []
		for j in range(by):
			for i in range(bx):
				for hm in rel:
					homes.append((i * BLOCK_W + hm[0], j * BLOCK_H + hm[1]))
		_worker(0, 0, n, n, main, item, target, homes)
		return
	handles = []
	for j in range(by):
		for i in range(bx):
			x0 = i * BLOCK_W
			y0 = j * BLOCK_H
			homes = []
			for hm in rel:
				homes.append((x0 + hm[0], y0 + hm[1]))
			if i == bx - 1 and j == by - 1:
				_worker(x0, y0, BLOCK_W, BLOCK_H, main, item, target, homes)
			else:
				move_to(x0, y0)
				d = spawn_drone(_worker, x0, y0, BLOCK_W, BLOCK_H, main, item, target, homes)
				if d != None:
					handles.append(d)
	for d in handles:
		wait_for(d)
