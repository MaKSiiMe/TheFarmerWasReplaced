# Fastest Reset (en construction).
# Pour l'instant : mode sonde, lancé par "classement" avec CHOIX = 9.
# Avec des ressources quasi infinies, on débloque tour par tour tout ce qui est possible
# et on note chaque déblocage avec son coût : ça donne l'arbre et les coûts exacts.

ALL = [
	Unlocks.Speed, Unlocks.Plant, Unlocks.Expand, Unlocks.Carrots, Unlocks.Grass,
	Unlocks.Trees, Unlocks.Watering, Unlocks.Fertilizer, Unlocks.Sunflowers,
	Unlocks.Pumpkins, Unlocks.Polyculture, Unlocks.Cactus, Unlocks.Dinosaurs,
	Unlocks.Mazes, Unlocks.Megafarm, Unlocks.Hats, Unlocks.Top_Hat,
	Unlocks.The_Farmers_Remains, Unlocks.Auto_Unlock, Unlocks.Costs, Unlocks.Debug,
	Unlocks.Debug_2, Unlocks.Dictionaries, Unlocks.Functions, Unlocks.Import,
	Unlocks.Lists, Unlocks.Loops, Unlocks.Operators, Unlocks.Senses,
	Unlocks.Simulation, Unlocks.Timing, Unlocks.Utilities, Unlocks.Variables,
	Unlocks.Leaderboard
]

quick_print("reset demarre, or =", num_items(Items.Gold))

if num_items(Items.Gold) > 1000000000:
	quick_print("SONDE debut, monde", get_world_size(), "drones", max_drones())
	for u in ALL:
		quick_print("INIT", u, num_unlocked(u), get_cost(u))
	rnd = 0
	while True:
		got = 0
		for u in ALL:
			c = get_cost(u)
			if c != None and unlock(u):
				got += 1
				quick_print("R", rnd, u, "niveau", num_unlocked(u), "cout", c)
		if got == 0:
			break
		rnd += 1
	quick_print("SONDE fin, monde", get_world_size(), "drones", max_drones())
