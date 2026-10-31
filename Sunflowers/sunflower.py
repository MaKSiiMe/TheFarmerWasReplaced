from move_to import move_to

# Tournesols : bonus x8 quand on récolte un tournesol qui a le plus de pétales de la ferme
# (avec au moins 10 tournesols). Récolter un tournesol qui n'est PAS le maximum fait aussi
# perdre le bonus de la récolte suivante.
#
# Trois méthodes :
# 1 = "que des 15" : juste après la plantation on détruit tout ce qui n'a pas 15 pétales.
#     Risque : si le jeu compte ces destructions comme des récoltes, le bonus saute souvent.
# 2 = "sans pétales" : on récolte tout ce qui est mûr, sans chercher le bonus (classement du Lab).
# 3 = "vagues synchronisées" : chaque drone a un bloc de 4x8, tous plantent puis récoltent
#     les 15 pendant le même créneau de temps, puis les 14, ... jusqu'aux 7. Les drones se
#     calent sur get_time() (pas besoin de mémoire partagée), aucune destruction, presque
#     toutes les récoltes ont le bonus.
#
# MODE = 0 lance le banc d'essai : chaque méthode tourne 60 s de jeu et la puissance
# gagnée par seconde est écrite dans output.txt.

MODE = 0
BEST = 3
TEST_SECONDS = 60


# ---------- 1. que des 15 ----------
def _reroll():
	while True:
		if get_entity_type() == None:
			if not plant(Entities.Sunflower):
				return
		if measure() == 15:
			return
		harvest()


def _w15(target, end):
	n = get_world_size()
	while num_items(Items.Power) < target and get_time() < end:
		for _ in range(n):
			e = get_entity_type()
			if e != Entities.Sunflower or can_harvest():
				if e != None:
					harvest()
				if get_ground_type() != Grounds.Soil:
					till()
				_reroll()
				if get_water() < 0.75 and num_items(Items.Water) >= 1:
					use_item(Items.Water)
			move(North)


# ---------- 2. sans pétales ----------
def _wall(target, end):
	n = get_world_size()
	while num_items(Items.Power) < target and get_time() < end:
		for _ in range(n):
			if can_harvest():
				harvest()
			if get_entity_type() == None:
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Sunflower)
				if get_water() < 0.75 and num_items(Items.Water) >= 1:
					use_item(Items.Water)
			move(North)


def _columns(worker, target, end):
	clear()
	n = get_world_size()
	handles = []
	for _ in range(n - 1):
		d = spawn_drone(worker, target, end)
		if d != None:
			handles.append(d)
		move(East)
	worker(target, end)
	for d in handles:
		wait_for(d)


# ---------- 3. vagues synchronisées ----------
def _wave_worker(x0, y0, E, PLANT, SLOT, target, end):
	tiles = []
	for i in range(4):
		if i % 2 == 0:
			for y in range(y0, y0 + 8):
				tiles.append((x0 + i, y))
		else:
			for y in range(y0 + 7, y0 - 1, -1):
				tiles.append((x0 + i, y))
	for t in tiles:
		move_to(t[0], t[1])
		if get_entity_type() != None:
			harvest()
		if get_ground_type() != Grounds.Soil:
			till()
	C = PLANT + 9 * SLOT
	k = 0
	while num_items(Items.Power) < target and get_time() < end:
		S = E + k * C
		k += 1
		while get_time() < S:
			pass
		# Plantation de tout le bloc, en notant les pétales
		waves = {}
		for p in range(7, 16):
			waves[p] = []
		for t in tiles:
			move_to(t[0], t[1])
			if get_entity_type() != None:
				harvest()
			plant(Entities.Sunflower)
			if get_water() < 0.75 and num_items(Items.Water) >= 1:
				use_item(Items.Water)
			p = measure()
			if p in waves:
				waves[p].append(t)
		# Récolte par vagues : 15, 14, ..., 7, chacune dans son créneau commun
		for i in range(9):
			while get_time() < S + PLANT + i * SLOT:
				pass
			todo = waves[15 - i]
			while len(todo) > 0:
				# Case la plus proche d'abord
				cx = get_pos_x()
				cy = get_pos_y()
				best = 0
				bd = 99
				for j in range(len(todo)):
					d = abs(todo[j][0] - cx) + abs(todo[j][1] - cy)
					if d < bd:
						bd = d
						best = j
				t = todo.pop(best)
				move_to(t[0], t[1])
				if get_entity_type() == Entities.Sunflower:
					while not can_harvest():
						pass
					harvest()


def _waves(target, end):
	clear()
	n = get_world_size()
	# Durée d'une action, mesurée sur quelques déplacements (+20 % de marge pour le code)
	t0 = get_time()
	for _ in range(6):
		move(North)
	a = (get_time() - t0) / 6 * 1.2
	PLANT = a * 115 + 1.5
	SLOT = a * 28
	E = get_time() + a * 260 + 0.5
	blocks = []
	for j in range(n // 8):
		for i in range(n // 4):
			blocks.append((i * 4, j * 8))
	last = blocks.pop()
	handles = []
	for b in blocks:
		move_to(b[0], b[1])
		d = spawn_drone(_wave_worker, b[0], b[1], E, PLANT, SLOT, target, end)
		if d != None:
			handles.append(d)
	_wave_worker(last[0], last[1], E, PLANT, SLOT, target, end)
	for d in handles:
		wait_for(d)


def _run(mode, target, end):
	if mode == 1:
		_columns(_w15, target, end)
	elif mode == 2:
		_columns(_wall, target, end)
	else:
		_waves(target, end)


def farm(target=None):
	if target == None:
		target = num_items(Items.Power) + 1
	_run(BEST, target, get_time() + 1000000000)


def bench():
	for mode in [1, 2, 3]:
		p0 = num_items(Items.Power)
		t0 = get_time()
		_run(mode, 1000000000000000, t0 + TEST_SECONDS)
		dt = get_time() - t0
		quick_print("Tournesols methode", mode, ":", (num_items(Items.Power) - p0) / dt, "power/s sur", dt, "s")


# Lancé directement : banc d'essai (MODE = 0) ou une méthode sans fin
if __name__ == "__main__":
	if MODE == 0:
		bench()
	else:
		_run(MODE, 1000000000000000, get_time() + 1000000000)
