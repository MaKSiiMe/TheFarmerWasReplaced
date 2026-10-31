# Course Hay_Single : 1 drone, ferme 8x8, objectif 100M de foin, puis le programme s'arrête.
#
# Principe :
# - L'herbe repousse toute seule sur la prairie : jamais besoin de la replanter.
# - Le compagnon n'a pas besoin d'être mûr : un buisson tout juste planté suffit.
# - Chaque pousse d'herbe demande un type au hasard (buisson, arbre ou carotte) à une
#   position au hasard à 3 cases ou moins. Si TOUTES ces cases sont déjà des buissons,
#   la demande tombe juste 1 fois sur 3, sans aucun déplacement.
# - Sinon on récolte quand même (foin normal) : ça retire au sort pour 1 seule action.
# Donc : deux herbes côte à côte au centre, entourées de buissons sur 3 cases, et le
# drone fait l'aller-retour entre les deux (≈ 2 actions par récolte, 32 % avec bonus).
# En plus, quand la demande d'une des deux herbes vise une case voisine du drone avec le
# mauvais type, il y plante le bon (4 actions) : ~40 % de récoltes avec bonus.
#
# Mesuré dans la course : action ≈ 0,036 s, l'herbe est toujours prête (eau ≥ 0,95),
# donc le temps dépend du nombre d'actions et du calcul par tour (1 tick par opération).

TARGET = 100000000
HOMES = [(3, 4), (4, 4)]
OPP = {North: South, South: North, East: West, West: East}


def _goto(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)


def _setup():
	n = get_world_size()
	is_home = {}
	for h in HOMES:
		is_home[h] = True
	# Buissons sur toutes les cases à 3 cases ou moins d'une maison (parcours en serpentin)
	for x in range(n):
		ys = range(n)
		if x % 2 == 1:
			ys = range(n - 1, -1, -1)
		for y in ys:
			near = False
			for h in HOMES:
				if abs(h[0] - x) + abs(h[1] - y) <= 3:
					near = True
			if near and not ((x, y) in is_home):
				_goto(x, y)
				if get_entity_type() != Entities.Bush:
					if get_entity_type() != None:
						harvest()
					plant(Entities.Bush)


def _fix(dr, t, p, content):
	# Va sur la case voisine, y plante le type demandé, revient (4 actions)
	move(dr)
	harvest()
	if t == Entities.Carrot and get_ground_type() != Grounds.Soil:
		till()
	if not plant(t):
		plant(Entities.Bush)
		t = Entities.Bush
	content[p] = t
	move(OPP[dr])


def _check(nb, cur, other, content):
	# cur : demande (type, position) d'une des deux herbes. Corrigée seulement si elle vise
	# une case voisine du drone, n'a pas déjà le bon type, et ne casse pas la demande
	# (satisfaite) de l'autre herbe. Plus loin que voisin, ce n'est pas rentable.
	if cur == None:
		return
	p = cur[1]
	if not (p in nb):
		return
	t = cur[0]
	if content[p] == t:
		return
	if other != None and other[1] == p and content[p] == other[0]:
		return
	if t == Entities.Carrot:
		cost = get_cost(Entities.Carrot)
		for it in cost:
			if num_items(it) < cost[it]:
				return
	_fix(nb[p], t, p, content)


def _neighbors(h):
	return {(h[0] - 1, h[1]): West, (h[0] + 1, h[1]): East, (h[0], h[1] + 1): North, (h[0], h[1] - 1): South}


def _run():
	t_start = get_time()
	_setup()
	t_loop = get_time()
	a = HOMES[0]
	b = HOMES[1]
	# Ce qui est planté autour des maisons (tout est buisson après _setup)
	content = {}
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			if (x, y) != a and (x, y) != b:
				if abs(a[0] - x) + abs(a[1] - y) <= 3 or abs(b[0] - x) + abs(b[1] - y) <= 3:
					content[(x, y)] = Entities.Bush
	# Voisins de chaque maison (sans l'autre maison) -> direction pour y aller
	nba = _neighbors(a)
	nba.pop(b)
	nbb = _neighbors(b)
	nbb.pop(a)
	_goto(a[0], a[1])
	cura = None
	curb = None
	# Boucle déroulée (a est à l'Ouest de b) : le moins de calcul possible par tour
	while num_items(Items.Hay) < TARGET:
		if can_harvest():
			harvest()
			cura = get_companion()
			_check(nba, cura, curb, content)
			_check(nba, curb, cura, content)
		if get_water() < 0.95:
			use_item(Items.Water)
		move(East)
		if can_harvest():
			harvest()
			curb = get_companion()
			_check(nbb, curb, cura, content)
			_check(nbb, cura, curb, content)
		if get_water() < 0.95:
			use_item(Items.Water)
		move(West)
	quick_print("STATS preparation", t_loop - t_start, "s, boucle", get_time() - t_loop, "s")


# Exécuté directement par la course (pas quand "classement" l'importe pour les mesures)
if __name__ == "__main__":
	_run()
