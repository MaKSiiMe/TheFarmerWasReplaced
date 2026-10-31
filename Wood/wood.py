import polyculture

# Bois : arbres en polyculture (voir polyculture.py)
def farm(target=None):
	if target == None:
		target = num_items(Items.Wood) + 10000000
	polyculture.farm(Entities.Tree, Items.Wood, target)


# Lancé directement : farme cette ressource sans fin (arrête le programme quand tu veux)
if __name__ == "__main__":
	farm(1000000000000000)
