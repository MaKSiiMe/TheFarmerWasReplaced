# Lanceur des courses de classement.
# Mets le nom de la course dans CHOIX puis exécute ce fichier.
#   "Hay", "Wood", "Carrots", "Pumpkins", "Cactus", "Sunflowers", "Maze", "Dinosaur"
#   "Hay_Single"
#   "Fastest_Reset"  (course)  /  "Reset_Test" (simulation d'essai, ne compte pas)
#   "Couts"  : coûts de tous les déblocages à tous les niveaux (fenêtre Sortie, rien n'est dépensé)
CHOIX = "Mesure_Hay"

COURSES = {
	"Hay": [Leaderboards.Hay, "lb_hay"],
	"Wood": [Leaderboards.Wood, "lb_wood"],
	"Carrots": [Leaderboards.Carrots, "lb_carrot"],
	"Pumpkins": [Leaderboards.Pumpkins, "lb_pumpkins"],
	"Cactus": [Leaderboards.Cactus, "lb_cactus"],
	"Sunflowers": [Leaderboards.Sunflowers, "lb_sunflowers"],
	"Maze": [Leaderboards.Maze, "lb_maze"],
	"Dinosaur": [Leaderboards.Dinosaur, "lb_dinosaur"],
	"Hay_Single": [Leaderboards.Hay_Single, "lb_hay_single"],
	"Fastest_Reset": [Leaderboards.Fastest_Reset, "reset"]
}

if CHOIX in COURSES:
	c = COURSES[CHOIX]
	leaderboard_run(c[0], c[1], 256)
elif CHOIX == "Reset_Test":
	t = simulate("reset", {}, {}, {}, -1, 256)
	quick_print("Fastest Reset simule en", t, "secondes")
elif CHOIX == "Couts":
	import reset
	for u in reset.ALL:
		for lvl in range(0, 21):
			cost = get_cost(u, lvl)
			if cost != None:
				quick_print("COUT", u, lvl, cost)
	quick_print("FIN DES COUTS")
elif CHOIX == "Mesure_Hay":
	# Mesures dans le vrai jeu, ferme réduite à 8x8 le temps du programme
	set_world_size(8)
	import lb_hay_single
	lb_hay_single._setup()
	h = lb_hay_single.HOMES[0]
	lb_hay_single._goto(h[0], h[1])
	# 1. Durée d'une action
	t0 = get_time()
	for _ in range(10):
		move(East)
		move(West)
	quick_print("MESURE action (move) =", (get_time() - t0) / 20, "s")
	# 2. Repousse de l'herbe sans eau puis avec eau
	for watered in [False, True]:
		if watered:
			while get_water() < 0.95 and num_items(Items.Water) >= 1:
				use_item(Items.Water)
		total = 0
		for _ in range(10):
			while not can_harvest():
				pass
			harvest()
			t0 = get_time()
			while not can_harvest():
				pass
			total += get_time() - t0
		quick_print("MESURE repousse herbe, eau =", get_water(), ":", total / 10, "s")
	# 3. Foin par récolte : normal / avec bonus
	base = 0
	bonus = 0
	nb = 0
	nbb = 0
	for _ in range(200):
		while not can_harvest():
			pass
		before = num_items(Items.Hay)
		harvest()
		gain = num_items(Items.Hay) - before
		if base == 0 or gain < base:
			base = gain
		if gain > base * 2:
			bonus = gain
			nbb += 1
		nb += 1
	quick_print("MESURE foin normal =", base, "avec bonus =", bonus, "bonus sur", nbb, "/", nb, "recoltes")
	quick_print("MESURE eau en stock =", num_items(Items.Water), "power =", num_items(Items.Power))
else:
	print("Choix inconnu :", CHOIX)
