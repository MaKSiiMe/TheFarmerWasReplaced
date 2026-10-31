# Lanceur des courses de classement et des simulations d'essai.
# 1 = course Hay_Single avec "lb_hay"            -> succès "Ferme compétitive"
# 2 = course Fastest_Reset avec "reset"          -> succès "Automatisation complète"
# 3 = simulation d'essai de "reset" (mêmes conditions que la course, ne compte pas)
# 8 = coûts de tous les déblocages à tous les niveaux, lus dans le vrai jeu (rien n'est dépensé)
# 9 = sonde en simulation : ordre de tous les déblocages (résultat dans output.txt)
CHOIX = 1

if CHOIX == 8:
	import reset
	for u in reset.ALL:
		for lvl in range(0, 21):
			c = get_cost(u, lvl)
			if c != None:
				quick_print("COUT", u, lvl, c)
	quick_print("FIN DES COUTS")

if CHOIX == 1:
	leaderboard_run(Leaderboards.Hay_Single, "lb_hay", 256)
elif CHOIX == 2:
	leaderboard_run(Leaderboards.Fastest_Reset, "reset", 256)
elif CHOIX == 3:
	t = simulate("reset", {}, {}, {}, -1, 256)
	quick_print("Fastest Reset simule en", t, "secondes")
elif CHOIX == 9:
	# Ressources quasi infinies : "reset" le détecte et passe en mode sonde
	big = 1000000000000
	items = {}
	for it in [Items.Hay, Items.Wood, Items.Carrot, Items.Pumpkin, Items.Cactus, Items.Bone, Items.Gold, Items.Weird_Substance, Items.Power, Items.Water, Items.Fertilizer]:
		items[it] = big
	quick_print("Lancement de la sonde")
	t = simulate("reset", {}, items, {}, 1, 256)
	quick_print("Sonde terminee en", t, "secondes simulees")
