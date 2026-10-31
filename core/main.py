# Programme principal : farme automatiquement ce qui manque pour débloquer
# le Top Hat puis la dernière amélioration (The Farmer's Remains).
# À chaque tour, il choisit la ressource la plus en retard (en %) et la farme
# par tranches de 20 % de l'objectif, en produisant d'abord ses ingrédients si besoin.

import grass
import wood
import carrot
import pumpkin
import sunflower
import cactus
import gold
import bone

FARMS = {
	Items.Hay: grass.farm,
	Items.Wood: wood.farm,
	Items.Carrot: carrot.farm,
	Items.Pumpkin: pumpkin.farm,
	Items.Cactus: cactus.farm,
	Items.Power: sunflower.farm,
	Items.Gold: gold.farm,
	Items.Bone: bone.farm
}

# Ce qu'on plante pour obtenir chaque ressource (pour vérifier les ingrédients)
SEEDS = {
	Items.Wood: Entities.Tree,
	Items.Carrot: Entities.Carrot,
	Items.Pumpkin: Entities.Pumpkin,
	Items.Cactus: Entities.Cactus,
	Items.Power: Entities.Sunflower,
	Items.Bone: Entities.Apple
}

FINAL_UNLOCKS = [Unlocks.Top_Hat, Unlocks.The_Farmers_Remains]


def produce(item, target, depth):
	if item in SEEDS and depth < 4:
		cost = get_cost(SEEDS[item])
		if cost != None:
			n = get_world_size()
			k = 4 * n * n
			if item == Items.Bone:
				# une partie de snake = une pomme par case
				k = n * n
			for ing in cost:
				need = cost[ing] * k
				if num_items(ing) < need:
					quick_print("Ingredient:", ing, "pour", item)
					produce(ing, need * 2, depth + 1)
	before = num_items(item)
	FARMS[item](target)
	return num_items(item) > before


def goals():
	g = {}
	for u in FINAL_UNLOCKS:
		c = get_cost(u)
		if c != None:
			for it in c:
				if it in g:
					g[it] = g[it] + c[it]
				else:
					g[it] = c[it]
	return g


stuck = []
while True:
	for u in FINAL_UNLOCKS:
		if unlock(u):
			quick_print("Debloque:", u)
	g = goals()
	if len(g) == 0:
		break

	if num_items(Items.Power) < 1000:
		sunflower.farm(5000)

	worst = None
	ratio = 2
	for it in g:
		r = num_items(it) / g[it]
		if r < ratio and not (it in stuck):
			ratio = r
			worst = it
	if worst == None:
		quick_print("Plus rien a farmer automatiquement :", g)
		break

	target = min(g[worst], num_items(worst) + g[worst] / 5)
	quick_print("Farm", worst, ":", num_items(worst), "->", target, "/", g[worst])
	if not produce(worst, target, 0):
		quick_print("Aucun progres sur", worst)
		stuck.append(worst)

clear()
change_hat(Hats.Top_Hat)
do_a_flip()
