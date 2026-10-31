# Succès restants.
# MODE = 1 : petits succès (cochon, saltos, chapeaux, cactus à l'envers,
#            import circulaire, puis débordement de pile qui arrête le programme)
# (Les courses de classement sont maintenant dans "classement".)

MODE = 1

# Importation circulaire : ce fichier s'importe lui-même
import succes
import cactus
from move_to import move_to

HATS = [Hats.Gray_Hat, Hats.Purple_Hat, Hats.Green_Hat, Hats.Brown_Hat, Hats.Gold_Hat]
FLIPS = 22


def _flipper(hat):
	# Défilé de mode + Maître acrobate : chaque drone met un chapeau et fait des saltos
	change_hat(hat)
	for _ in range(FLIPS):
		do_a_flip()


def _rev_col():
	n = get_world_size()
	for y in range(n):
		if get_entity_type() != None:
			harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Cactus)
		if y < n - 1:
			move(North)
	# Le drone est en haut : trier en décroissant vers le Nord (= croissant vers le Sud)
	cactus._sort(South, North, n, 0)


def _rev_row():
	cactus._sort(West, East, get_world_size(), 0)


def _wrong_order():
	# Ordre erroné : tout le champ trié dans le mauvais sens (plus grands au Sud-Ouest)
	clear()
	n = get_world_size()
	handles = []
	for _ in range(n - 1):
		d = spawn_drone(_rev_col)
		if d != None:
			handles.append(d)
		move(East)
	_rev_col()
	for d in handles:
		wait_for(d)
	move_to(n - 1, 0)
	handles = []
	for _ in range(n - 1):
		d = spawn_drone(_rev_row)
		if d != None:
			handles.append(d)
		move(North)
	_rev_row()
	for d in handles:
		wait_for(d)
	while not can_harvest():
		pass
	harvest()


def _overflow():
	_overflow()


if __name__ == "__main__":
	if MODE == 1:
		# Ça fait du bien
		pet_the_piggy()

		# Défilé de mode + Maître acrobate (32 drones x 22 saltos)
		clear()
		handles = []
		for i in range(max_drones() - 1):
			d = spawn_drone(_flipper, HATS[i % len(HATS)])
			if d != None:
				handles.append(d)
		_flipper(Hats.Wizard_Hat)
		for d in handles:
			wait_for(d)

		# Ordre erroné
		_wrong_order()

		# Débordement de pile (arrête le programme avec une erreur, c'est voulu)
		_overflow()
	else:
		print("Les courses de classement sont maintenant dans classement")
